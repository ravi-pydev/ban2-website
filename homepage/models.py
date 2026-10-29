"""Database tables for Ban2Plans. Mirrors the MySQL schema in docs/sqls/*.sql."""

from django.db import models
from django.db.models import Q


class TimeStamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# ---------------------------------------------------------------------------
# Site and profile (01, 02)
# ---------------------------------------------------------------------------

class SiteSettings(TimeStamped):
    id = models.PositiveSmallIntegerField(primary_key=True, default=1)
    site_name = models.CharField(max_length=100)
    tagline = models.CharField(max_length=200, blank=True)
    whatsapp_number = models.CharField(
        max_length=20, db_comment='Country code + number, digits only, e.g. 919412833444')
    enquiry_email = models.EmailField(
        max_length=254, db_comment='Inbox that receives enquiry emails')
    service_area = models.CharField(max_length=150, blank=True)

    class Meta:
        db_table = 'site_settings'
        verbose_name_plural = 'site settings'
        constraints = [
            models.CheckConstraint(condition=Q(id=1), name='chk_site_settings_single_row'),
        ]

    def __str__(self):
        return self.site_name


class Profile(TimeStamped):
    full_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    current_company = models.CharField(max_length=150, blank=True)
    summary = models.TextField(blank=True)
    email = models.EmailField(max_length=254, unique=True)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    photo = models.CharField(max_length=255, blank=True, db_comment='Image file name or URL')
    show_dob = models.BooleanField(default=True)
    show_phone = models.BooleanField(default=False)

    class Meta:
        db_table = 'profile'

    def __str__(self):
        return self.full_name


# ---------------------------------------------------------------------------
# Page copy (13)
# ---------------------------------------------------------------------------

class PageSection(TimeStamped):
    """A block of page wording, e.g. the home page hero, intro or call-to-action band."""

    page = models.CharField(max_length=30, default='home')
    key = models.CharField(max_length=30, db_comment='Which block: hero, intro, cta')
    kicker = models.CharField(max_length=100, blank=True, db_comment='Small label above the heading')
    heading = models.CharField(max_length=200)
    body = models.TextField(blank=True, db_comment='Paragraphs separated by a blank line')
    items = models.TextField(blank=True, db_comment='List items, one per line')
    image = models.CharField(max_length=255, blank=True)
    button_label = models.CharField(max_length=60, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'page_sections'
        ordering = ['page', 'key']
        constraints = [
            models.UniqueConstraint(fields=['page', 'key'], name='uq_page_sections_page_key'),
        ]

    def __str__(self):
        return f'{self.page} / {self.key}'

    @property
    def paragraphs(self):
        return [p.strip() for p in self.body.replace('\r\n', '\n').split('\n\n') if p.strip()]

    @property
    def item_list(self):
        return [line.strip() for line in self.items.splitlines() if line.strip()]


# ---------------------------------------------------------------------------
# Business content (03 - 07)
# ---------------------------------------------------------------------------

class Service(TimeStamped):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField()
    icon = models.CharField(
        max_length=30, blank=True, db_comment='Icon name used by the frontend, e.g. mic, globe')
    image = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'services'
        ordering = ['sort_order', 'id']
        indexes = [models.Index(fields=['is_active', 'sort_order'], name='ix_services_active_order')]

    def __str__(self):
        return self.title


class EventSession(TimeStamped):
    service = models.ForeignKey(
        Service, null=True, blank=True, on_delete=models.SET_NULL, related_name='event_sessions')
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    image = models.CharField(max_length=255, blank=True)
    client_name = models.CharField(
        max_length=150, blank=True, db_comment='Shown only if the client agreed')
    venue = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=100, blank=True)
    event_date = models.DateField(null=True, blank=True)
    guest_count = models.PositiveIntegerField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'event_sessions'
        ordering = ['sort_order', 'id']
        indexes = [
            models.Index(fields=['is_published', 'sort_order'], name='ix_evsess_published_order'),
            models.Index(fields=['event_date'], name='ix_event_sessions_event_date'),
        ]

    def __str__(self):
        return self.title


class Testimonial(TimeStamped):
    event_session = models.ForeignKey(
        EventSession, null=True, blank=True, on_delete=models.SET_NULL, related_name='testimonials')
    client_name = models.CharField(max_length=100)
    client_role = models.CharField(max_length=100, blank=True, db_comment='Designation')
    company = models.CharField(max_length=150, blank=True)
    quote = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    photo = models.CharField(max_length=255, blank=True)
    consent_given = models.BooleanField(
        default=False, db_comment='Client agreed to be quoted publicly')
    is_published = models.BooleanField(default=False)
    sort_order = models.PositiveSmallIntegerField(default=0)
    received_on = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'testimonials'
        ordering = ['sort_order', 'id']
        indexes = [
            models.Index(fields=['is_published', 'sort_order'], name='ix_testimonials_pub_order'),
        ]
        constraints = [
            models.CheckConstraint(condition=Q(rating__gte=1, rating__lte=5),
                                   name='chk_testimonials_rating'),
        ]

    def __str__(self):
        return f'{self.client_name} ({self.company})' if self.company else self.client_name


class Faq(TimeStamped):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'faqs'
        ordering = ['sort_order', 'id']
        verbose_name = 'FAQ'
        indexes = [models.Index(fields=['is_active', 'sort_order'], name='ix_faqs_active_order')]

    def __str__(self):
        return self.question


class Stat(models.Model):
    value = models.CharField(max_length=20, db_comment='Display text, e.g. 50+')
    label = models.CharField(max_length=100)
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'stats'
        ordering = ['sort_order', 'id']

    def __str__(self):
        return f'{self.value} {self.label}'


class SellingPoint(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    icon = models.CharField(max_length=30, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'selling_points'
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.title


class ProcessStep(models.Model):
    step_number = models.PositiveSmallIntegerField(unique=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    class Meta:
        db_table = 'process_steps'
        ordering = ['step_number']

    def __str__(self):
        return f'{self.step_number}. {self.title}'


class ClientType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'client_types'
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------
# Resume (08 - 10)
# ---------------------------------------------------------------------------

class Experience(TimeStamped):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='experience')
    job_title = models.CharField(max_length=100)
    company = models.CharField(max_length=150)
    location = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True, db_comment='NULL = current role')
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'experience'
        ordering = ['-start_date']
        verbose_name_plural = 'experience'
        indexes = [
            models.Index(fields=['profile', 'start_date'], name='ix_experience_profile_start'),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(end_date__isnull=True) | Q(end_date__gte=models.F('start_date')),
                name='chk_experience_dates'),
        ]

    def __str__(self):
        return f'{self.job_title}, {self.company}'


class ExperiencePoint(models.Model):
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='points')
    point = models.CharField(max_length=500)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'experience_points'
        ordering = ['sort_order', 'id']
        indexes = [
            models.Index(fields=['experience', 'sort_order'], name='ix_exp_points_experience'),
        ]

    def __str__(self):
        return self.point


class Education(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='education')
    qualification = models.CharField(
        max_length=150, db_comment='e.g. Masters of Hotel Management, 12th')
    institution = models.CharField(max_length=200, blank=True)
    note = models.CharField(max_length=200, blank=True, db_comment='e.g. Merit certificate')
    completed_on = models.DateField(
        null=True, blank=True, db_comment='Day is not significant; month and year are shown')
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'education'
        ordering = ['sort_order', '-completed_on']
        verbose_name_plural = 'education'
        indexes = [models.Index(fields=['profile', 'completed_on'], name='ix_education_profile')]

    def __str__(self):
        return self.qualification


class Highlight(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='highlights')
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=500, blank=True)
    icon = models.CharField(max_length=30, blank=True)
    achieved_on = models.DateField(null=True, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'highlights'
        ordering = ['sort_order', 'id']
        indexes = [models.Index(fields=['profile', 'sort_order'], name='ix_highlights_profile')]

    def __str__(self):
        return self.title


class Skill(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=60)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'skills'
        ordering = ['sort_order', 'id']
        constraints = [
            models.UniqueConstraint(fields=['profile', 'name'], name='uq_skills_profile_name'),
        ]

    def __str__(self):
        return self.name


class Language(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='languages')
    name = models.CharField(max_length=50)
    proficiency = models.CharField(
        max_length=60, db_comment='e.g. Full professional proficiency')
    level_percent = models.PositiveSmallIntegerField(
        default=100, db_comment='Width of the level bar')
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'languages'
        ordering = ['sort_order', 'id']
        constraints = [
            models.UniqueConstraint(fields=['profile', 'name'], name='uq_languages_profile_name'),
            models.CheckConstraint(condition=Q(level_percent__lte=100), name='chk_languages_level'),
        ]

    def __str__(self):
        return self.name


class Interest(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='interests')
    name = models.CharField(max_length=60)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'interests'
        ordering = ['sort_order', 'id']
        constraints = [
            models.UniqueConstraint(fields=['profile', 'name'], name='uq_interests_profile_name'),
        ]

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------
# Enquiries (11)
# ---------------------------------------------------------------------------

class Enquiry(TimeStamped):
    class Status(models.TextChoices):
        NEW = 'new', 'New'
        CONTACTED = 'contacted', 'Contacted'
        PROPOSAL_SENT = 'proposal_sent', 'Proposal sent'
        WON = 'won', 'Won'
        LOST = 'lost', 'Lost'
        SPAM = 'spam', 'Spam'

    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=120, blank=True)
    service = models.ForeignKey(
        Service, null=True, blank=True, on_delete=models.SET_NULL, related_name='enquiries',
        db_comment='Matching service, if event_type is one')
    event_type = models.CharField(
        max_length=120, db_comment='As chosen on the form, kept even if the service is renamed')
    guests = models.PositiveIntegerField(null=True, blank=True)
    preferred_date = models.DateField(null=True, blank=True)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    source = models.CharField(max_length=30, default='website')
    email_sent = models.BooleanField(default=False, db_comment='Notification email delivered')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'enquiries'
        ordering = ['-created_at']
        verbose_name_plural = 'enquiries'
        indexes = [
            models.Index(fields=['status', 'created_at'], name='ix_enquiries_status_created'),
            models.Index(fields=['email'], name='ix_enquiries_email'),
            models.Index(fields=['preferred_date'], name='ix_enquiries_preferred_date'),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(guests__isnull=True) | Q(guests__gte=1, guests__lte=100000),
                name='chk_enquiries_guests'),
        ]

    def __str__(self):
        return f'{self.name} – {self.event_type}'


class EnquiryFollowup(models.Model):
    class ContactMethod(models.TextChoices):
        CALL = 'call', 'Call'
        EMAIL = 'email', 'Email'
        WHATSAPP = 'whatsapp', 'WhatsApp'
        MEETING = 'meeting', 'Meeting'
        OTHER = 'other', 'Other'

    enquiry = models.ForeignKey(Enquiry, on_delete=models.CASCADE, related_name='followups')
    contact_method = models.CharField(max_length=20, choices=ContactMethod.choices)
    note = models.TextField()
    quoted_amount = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True, db_comment='In INR')
    next_action_on = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'enquiry_followups'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['enquiry', 'created_at'], name='ix_enquiry_followups_enquiry'),
            models.Index(fields=['next_action_on'], name='ix_followups_next_action'),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(quoted_amount__isnull=True) | Q(quoted_amount__gte=0),
                name='chk_enquiry_followups_amount'),
        ]

    def __str__(self):
        return f'{self.get_contact_method_display()} on {self.created_at:%d %b %Y}'
