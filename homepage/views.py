import logging
from email.utils import formataddr, parseaddr

from django.conf import settings
from django.core.mail import EmailMessage
from django.db.models import Count, F
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import APIException, Throttled
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from . import models
from . import serializers as s

logger = logging.getLogger(__name__)


def frontend(request):
    """Serve the React app's index.html for page URLs (/, /about/, …); React Router takes over."""
    index = settings.FRONTEND_DIST / 'index.html'
    if not index.is_file():
        return HttpResponse(
            'Frontend not built. Run `npm run build` in frontend/ and restart the server, '
            'or use the dev server: `npm run dev` (http://127.0.0.1:5173).',
            status=503, content_type='text/plain; charset=utf-8')
    return HttpResponse(index.read_text(encoding='utf-8'))


class ContentNotLoaded(APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = 'Site content is not loaded. Run: python manage.py load_seed'
    default_code = 'content_not_loaded'


def get_site_settings():
    site = models.SiteSettings.objects.first()
    if site is None:
        raise ContentNotLoaded()
    return site


def get_profile():
    profile = models.Profile.objects.first()
    if profile is None:
        raise ContentNotLoaded()
    return profile


def many(serializer_class, queryset, request):
    return serializer_class(queryset, many=True, context={'request': request}).data


def reviews_data(request):
    """Published reviews sorted by rating (high to low), plus the average and breakdown."""
    reviews = (models.Testimonial.objects.filter(is_published=True)
               .select_related('event_session')
               .order_by('-rating', F('received_on').desc(nulls_last=True), '-created_at'))
    counts = dict(reviews.order_by().values_list('rating').annotate(n=Count('id')))
    total = sum(counts.values())
    average = sum(r * n for r, n in counts.items()) / total if total else 0
    return {
        'summary': {
            'count': total,
            'average': round(average, 1),
            'breakdown': [{'stars': stars, 'count': counts.get(stars, 0)} for stars in range(5, 0, -1)],
        },
        'reviews': many(s.ReviewSerializer, reviews, request),
    }


def notify_owner(subject, template, context):
    """Email the site owner. Returns True if sent; failures are logged, not raised."""
    site = models.SiteSettings.objects.first()
    recipient = site.enquiry_email if site else settings.ENQUIRY_EMAIL_TO
    default_name, sender = parseaddr(settings.DEFAULT_FROM_EMAIL)
    site_name = site.site_name if site else default_name
    body = render_to_string(template, dict(context, site_name=site_name,
                                           received=timezone.localtime()))
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=formataddr((f'{site_name} Website', sender)),
        to=[recipient],
        reply_to=[context['reply_to']] if context.get('reply_to') else None,
    )
    try:
        email.send()
    except Exception:
        logger.exception('Failed to send email: %s', subject)
        return False
    return True


def page_sections(page, request):
    """Active sections of a page as {key: data}, e.g. {'hero': {...}, 'intro': {...}}."""
    sections = models.PageSection.objects.filter(page=page, is_active=True)
    return {section.key: s.PageSectionSerializer(section, context={'request': request}).data
            for section in sections}


class ApiRootView(APIView):
    """Event & Experience by Ban2 API. Lists the available endpoints."""

    def get(self, request):
        return Response({
            'site': reverse('api:site', request=request),
            'home': reverse('api:home', request=request),
            'about': reverse('api:about', request=request),
            'enquiries': reverse('api:enquiries', request=request),
            'reviews': reverse('api:reviews', request=request),
            'feedback': reverse('api:feedback', request=request),
        })


class SiteView(APIView):
    """Site-wide details used by every page: name, WhatsApp number and profile."""

    def get(self, request):
        site = get_site_settings()
        profile = s.ProfileSerializer(get_profile(), context={'request': request}).data
        profile.update(tagline=site.tagline, service_area=site.service_area)
        return Response({
            'site_name': site.site_name,
            'whatsapp_number': site.whatsapp_number,
            'profile': profile,
        })


class HomeView(APIView):
    """Content for the home (business) page."""

    def get(self, request):
        sections = page_sections('home', request)
        if 'hero' not in sections:
            raise ContentNotLoaded()
        return Response({
            'hero': sections['hero'],
            'intro': sections.get('intro'),
            'cta': sections.get('cta'),
            'stats': many(s.StatSerializer, models.Stat.objects.filter(is_active=True), request),
            'services': many(s.ServiceSerializer,
                             models.Service.objects.filter(is_active=True), request),
            'sessions': many(s.EventSessionSerializer,
                             models.EventSession.objects.filter(is_published=True), request),
            'why_me': many(s.SellingPointSerializer,
                           models.SellingPoint.objects.filter(is_active=True), request),
            'process': many(s.ProcessStepSerializer, models.ProcessStep.objects.all(), request),
            'client_types': list(models.ClientType.objects.values_list('name', flat=True)),
            'testimonials': many(s.TestimonialSerializer,
                                 models.Testimonial.objects.filter(is_published=True), request),
            'faqs': many(s.FaqSerializer, models.Faq.objects.filter(is_active=True), request),
            'reviews': reviews_data(request),
        })


class ReviewsView(APIView):
    """All published client reviews, highest rating first, with the average and breakdown."""

    def get(self, request):
        return Response(reviews_data(request))


class FeedbackView(APIView):
    """Feedback from an existing client. Saved unpublished until the owner approves it in admin."""

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'feedback'

    def get_throttles(self):
        # Only limit submissions; loading the event list is free.
        return super().get_throttles() if self.request.method == 'POST' else []

    def get(self, request):
        # The events a client can pick from in the feedback form.
        events = models.EventSession.objects.filter(is_published=True).values('id', 'title')
        return Response({'events': list(events)})

    def post(self, request):
        serializer = s.FeedbackSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'ok': False, 'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_spam:
            return Response({'ok': True}, status=status.HTTP_201_CREATED)

        data = serializer.validated_data
        review = models.Testimonial.objects.create(
            event_session=data.get('event_session'),
            client_name=data['name'],
            client_email=data['email'],
            client_role=data.get('role', ''),
            company=data.get('company', ''),
            quote=data['feedback'],
            rating=data['rating'],
            consent_given=data['consent'],
            is_published=False,
            source=models.Testimonial.Source.WEBSITE,
            received_on=timezone.localdate(),
        )
        notify_owner(
            f"New {data['rating']}★ feedback from {data['name']} (awaiting approval)",
            'homepage/email/feedback.txt',
            {'f': data, 'review': review, 'reply_to': data['email'],
             'admin_url': request.build_absolute_uri(
                 reverse('admin:homepage_testimonial_change', args=[review.pk]))},
        )
        return Response({'ok': True, 'id': review.pk}, status=status.HTTP_201_CREATED)

    def throttled(self, request, wait):
        raise Throttled(wait, detail='Too many submissions. Please try again later.')


class AboutView(APIView):
    """Content for the About Me (resume) page."""

    def get(self, request):
        profile = get_profile()
        return Response({
            'stats': many(s.StatSerializer, models.Stat.objects.filter(is_active=True), request),
            'experience': many(
                s.ExperienceSerializer,
                profile.experience.order_by('sort_order').prefetch_related('points'), request),
            'highlights': many(s.HighlightSerializer, profile.highlights.all(), request),
            'education': many(s.EducationSerializer, profile.education.all(), request),
            'skills': list(profile.skills.values_list('name', flat=True)),
            'languages': many(s.LanguageSerializer, profile.languages.all(), request),
            'interests': list(profile.interests.values_list('name', flat=True)),
        })


class EnquiryView(APIView):
    """Submit an event enquiry. It is saved to the database and emailed to the site owner."""

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'enquiries'

    def get(self, request):
        # Lets the browsable API show the allowed event types.
        return Response({'event_types': s.event_type_choices()})

    def post(self, request):
        serializer = s.EnquirySerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'ok': False, 'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        # Pretend success to bots so they don't retry.
        if serializer.is_spam:
            return Response({'ok': True}, status=status.HTTP_201_CREATED)

        data = serializer.validated_data
        enquiry = models.Enquiry.objects.create(
            name=data['name'],
            email=data['email'],
            phone=data.get('phone', ''),
            company=data.get('company', ''),
            service=models.Service.objects.filter(title=data['event_type']).first(),
            event_type=data['event_type'],
            guests=data.get('guests'),
            preferred_date=data.get('date'),
            event_location=data.get('event_location', ''),
            message=data.get('message', ''),
            ip_address=request.META.get('REMOTE_ADDR') or None,
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:255],
        )

        subject = f"New enquiry: {data['event_type']} – {data['name']}"
        if data.get('company'):
            subject += f", {data['company']}"
        # The enquiry is already saved, so the visitor gets a success reply even if email fails.
        if notify_owner(subject, 'homepage/email/enquiry.txt',
                        {'e': data, 'reply_to': data['email']}):
            enquiry.email_sent = True
            enquiry.save(update_fields=['email_sent', 'updated_at'])
        return Response({'ok': True, 'id': enquiry.pk, 'email_sent': enquiry.email_sent},
                        status=status.HTTP_201_CREATED)

    def throttled(self, request, wait):
        raise Throttled(wait, detail='Too many enquiries. Please try again later.')
