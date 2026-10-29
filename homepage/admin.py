from django.contrib import admin

from . import models


@admin.register(models.SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'whatsapp_number', 'enquiry_email']


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'job_title', 'email', 'location']


@admin.register(models.PageSection)
class PageSectionAdmin(admin.ModelAdmin):
    list_display = ['page', 'key', 'heading', 'is_active']
    list_filter = ['page', 'is_active']


@admin.register(models.Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'sort_order', 'is_active']
    list_editable = ['sort_order', 'is_active']
    prepopulated_fields = {'slug': ['title']}


@admin.register(models.EventSession)
class EventSessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'service', 'event_date', 'guest_count', 'is_featured', 'is_published']
    list_filter = ['service', 'is_published', 'is_featured']


@admin.register(models.Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'company', 'rating', 'consent_given', 'is_published']
    list_filter = ['is_published', 'consent_given']


@admin.register(models.Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ['question', 'sort_order', 'is_active']
    list_editable = ['sort_order', 'is_active']


@admin.register(models.Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ['value', 'label', 'sort_order', 'is_active']


@admin.register(models.SellingPoint)
class SellingPointAdmin(admin.ModelAdmin):
    list_display = ['title', 'sort_order', 'is_active']


@admin.register(models.ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    list_display = ['step_number', 'title']


@admin.register(models.ClientType)
class ClientTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'sort_order']


class ExperiencePointInline(admin.TabularInline):
    model = models.ExperiencePoint
    extra = 1


@admin.register(models.Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['job_title', 'company', 'start_date', 'end_date']
    inlines = [ExperiencePointInline]


@admin.register(models.Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['qualification', 'institution', 'completed_on']


admin.site.register([models.Highlight, models.Skill, models.Language, models.Interest])


class EnquiryFollowupInline(admin.StackedInline):
    model = models.EnquiryFollowup
    extra = 1


@admin.register(models.Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'event_type', 'guests', 'preferred_date', 'status', 'created_at']
    list_filter = ['status', 'event_type']
    search_fields = ['name', 'email', 'company', 'message']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at', 'ip_address', 'user_agent', 'email_sent']
    inlines = [EnquiryFollowupInline]
