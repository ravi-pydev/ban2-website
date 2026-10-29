import copy
import logging

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import Throttled
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from . import content
from .serializers import EnquirySerializer

logger = logging.getLogger(__name__)


def with_image_urls(request, data):
    """Return a copy of data with every 'image' file name turned into a full URL."""
    data = copy.deepcopy(data)

    def walk(node):
        if isinstance(node, dict):
            for key, value in node.items():
                if key == 'image' and isinstance(value, str):
                    node[key] = request.build_absolute_uri(static(f'homepage/img/{value}'))
                else:
                    walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(data)
    return data


class ApiRootView(APIView):
    """Ban2Plans API. Lists the available endpoints."""

    def get(self, request):
        return Response({
            'site': reverse('api:site', request=request),
            'home': reverse('api:home', request=request),
            'about': reverse('api:about', request=request),
            'enquiries': reverse('api:enquiries', request=request),
        })


class SiteView(APIView):
    """Site-wide details used by every page: name, profile and contact info."""

    def get(self, request):
        profile = dict(content.PROFILE, image='profile.jpg')
        return Response(with_image_urls(request, {
            'site_name': content.SITE_NAME,
            'whatsapp_number': content.WHATSAPP_NUMBER,
            'profile': profile,
        }))


class HomeView(APIView):
    """Content for the home (business) page."""

    def get(self, request):
        return Response(with_image_urls(request, {
            'hero': content.HERO,
            'stats': content.STATS,
            'intro': content.INTRO,
            'services': content.SERVICES,
            'sessions': content.SESSIONS,
            'why_me': content.WHY_ME,
            'process': content.PROCESS,
            'client_types': content.CLIENT_TYPES,
            'testimonials': content.TESTIMONIALS,
            'faqs': content.FAQS,
        }))


class AboutView(APIView):
    """Content for the About Me (resume) page."""

    def get(self, request):
        return Response({
            'stats': content.STATS,
            'experience': content.EXPERIENCE,
            'highlights': content.HIGHLIGHTS,
            'education': content.EDUCATION,
            'skills': content.SKILLS,
            'languages': content.LANGUAGES,
            'interests': content.INTERESTS,
        })


class EnquiryView(APIView):
    """Submit an event enquiry. It is emailed to the site owner."""

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'enquiries'

    def get(self, request):
        # Lets the browsable API show the form and the allowed event types.
        return Response({'event_types': list(EnquirySerializer().fields['event_type'].choices)})

    def post(self, request):
        serializer = EnquirySerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'ok': False, 'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        # Pretend success to bots so they don't retry.
        if serializer.is_spam:
            return Response({'ok': True}, status=status.HTTP_201_CREATED)

        data = serializer.validated_data
        subject = f"New enquiry: {data['event_type']} – {data['name']}"
        if data.get('company'):
            subject += f", {data['company']}"
        body = render_to_string(
            'homepage/email/enquiry.txt', {'e': data, 'received': timezone.localtime()}
        )
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.ENQUIRY_EMAIL_TO],
            reply_to=[data['email']],
        )
        try:
            email.send()
        except Exception:
            logger.exception('Failed to send enquiry email')
            return Response(
                {'ok': False,
                 'error': 'Email could not be sent. Please try WhatsApp or email directly.'},
                status=status.HTTP_502_BAD_GATEWAY,
            )
        return Response({'ok': True}, status=status.HTTP_201_CREATED)

    def throttled(self, request, wait):
        raise Throttled(wait, detail='Too many enquiries. Please try again later.')
