from django.templatetags.static import static
from rest_framework import serializers

from . import models

OTHER_EVENT_TYPE = 'Other'


def image_url(request, name):
    """Turn an image file name into a full URL. Values that are already URLs pass through."""
    if not name:
        return ''
    if name.startswith(('http://', 'https://', '/')):
        return name
    url = static(f'homepage/img/{name}')
    return request.build_absolute_uri(url) if request else url


def month_year(value):
    return value.strftime('%b %Y') if value else ''


class ImageField(serializers.Field):
    def to_representation(self, value):
        return image_url(self.context.get('request'), value)


# ---------------------------------------------------------------------------
# Read-only content. Field names match what the frontend already expects.
# ---------------------------------------------------------------------------

class PageSectionSerializer(serializers.ModelSerializer):
    image = ImageField()
    text = serializers.CharField(source='body')
    paragraphs = serializers.ListField(child=serializers.CharField(), read_only=True)
    items = serializers.ListField(source='item_list', child=serializers.CharField(), read_only=True)
    button = serializers.CharField(source='button_label')

    class Meta:
        model = models.PageSection
        fields = ['kicker', 'heading', 'text', 'paragraphs', 'items', 'image', 'button']


class StatSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Stat
        fields = ['value', 'label']


class ServiceSerializer(serializers.ModelSerializer):
    image = ImageField()
    text = serializers.CharField(source='description')

    class Meta:
        model = models.Service
        fields = ['icon', 'title', 'image', 'text']


class EventSessionSerializer(serializers.ModelSerializer):
    image = ImageField()
    text = serializers.CharField(source='description')

    class Meta:
        model = models.EventSession
        fields = ['title', 'image', 'text']


class SellingPointSerializer(serializers.ModelSerializer):
    text = serializers.CharField(source='description')

    class Meta:
        model = models.SellingPoint
        fields = ['icon', 'title', 'text']


class ProcessStepSerializer(serializers.ModelSerializer):
    text = serializers.CharField(source='description')

    class Meta:
        model = models.ProcessStep
        fields = ['title', 'text']


class TestimonialSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='client_name')
    role = serializers.SerializerMethodField()
    sample = serializers.SerializerMethodField()

    class Meta:
        model = models.Testimonial
        fields = ['quote', 'name', 'role', 'rating', 'sample']

    def get_role(self, obj):
        return ', '.join(part for part in (obj.client_role, obj.company) if part)

    def get_sample(self, obj):
        # Without the client's consent the quote is treated as a placeholder.
        return not obj.consent_given


class FaqSerializer(serializers.ModelSerializer):
    q = serializers.CharField(source='question')
    a = serializers.CharField(source='answer')

    class Meta:
        model = models.Faq
        fields = ['q', 'a']


class ExperienceSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='job_title')
    period = serializers.SerializerMethodField()
    points = serializers.SlugRelatedField(many=True, read_only=True, slug_field='point')

    class Meta:
        model = models.Experience
        fields = ['role', 'company', 'location', 'period', 'points']

    def get_period(self, obj):
        return f"{month_year(obj.start_date)} – {month_year(obj.end_date) or 'Present'}"


class HighlightSerializer(serializers.ModelSerializer):
    text = serializers.CharField(source='description')

    class Meta:
        model = models.Highlight
        fields = ['icon', 'title', 'text']


class EducationSerializer(serializers.ModelSerializer):
    degree = serializers.CharField(source='qualification')
    school = serializers.CharField(source='institution')
    date = serializers.SerializerMethodField()

    class Meta:
        model = models.Education
        fields = ['degree', 'school', 'note', 'date']

    def get_date(self, obj):
        return month_year(obj.completed_on)


class LanguageSerializer(serializers.ModelSerializer):
    level = serializers.CharField(source='proficiency')
    percent = serializers.IntegerField(source='level_percent')

    class Meta:
        model = models.Language
        fields = ['name', 'level', 'percent']


class ProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='full_name')
    title = serializers.CharField(source='job_title')
    image = ImageField(source='photo')
    dob = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()

    class Meta:
        model = models.Profile
        fields = ['name', 'title', 'summary', 'email', 'phone', 'location', 'dob', 'image']

    def get_dob(self, obj):
        return obj.date_of_birth.strftime('%d %b %Y') if obj.show_dob and obj.date_of_birth else ''

    def get_phone(self, obj):
        return obj.phone if obj.show_phone else ''


# ---------------------------------------------------------------------------
# Enquiry form input
# ---------------------------------------------------------------------------

def event_type_choices():
    titles = list(models.Service.objects.filter(is_active=True).values_list('title', flat=True))
    return titles + [OTHER_EVENT_TYPE]


class EnquirySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    company = serializers.CharField(max_length=120, required=False, allow_blank=True)
    event_type = serializers.ChoiceField(choices=[])
    guests = serializers.IntegerField(min_value=1, max_value=100000, required=False, allow_null=True)
    date = serializers.DateField(required=False, allow_null=True)
    message = serializers.CharField(max_length=3000, required=False, allow_blank=True)
    # Honeypot: hidden from people, bots tend to fill it in.
    website = serializers.CharField(required=False, allow_blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Event types come from the services table, so they follow edits in admin.
        self.fields['event_type'].choices = event_type_choices()

    def to_internal_value(self, data):
        # HTML forms send empty strings for blank optional number/date fields.
        if hasattr(data, 'dict'):
            data = data.dict()
        data = {k: (None if k in ('guests', 'date') and v == '' else v) for k, v in data.items()}
        return super().to_internal_value(data)

    @property
    def is_spam(self):
        return bool(self.validated_data.get('website'))
