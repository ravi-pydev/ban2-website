from rest_framework import serializers

from .content import SERVICES

EVENT_TYPES = [s['title'] for s in SERVICES] + ['Other']


class EnquirySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    company = serializers.CharField(max_length=120, required=False, allow_blank=True)
    event_type = serializers.ChoiceField(choices=EVENT_TYPES)
    guests = serializers.IntegerField(min_value=1, max_value=100000, required=False, allow_null=True)
    date = serializers.DateField(required=False, allow_null=True)
    message = serializers.CharField(max_length=3000, required=False, allow_blank=True)
    # Honeypot: hidden from people, bots tend to fill it in.
    website = serializers.CharField(required=False, allow_blank=True)

    def to_internal_value(self, data):
        # HTML forms send empty strings for blank optional number/date fields.
        if hasattr(data, 'dict'):
            data = data.dict()
        data = {k: (None if k in ('guests', 'date') and v == '' else v) for k, v in data.items()}
        return super().to_internal_value(data)

    @property
    def is_spam(self):
        return bool(self.validated_data.get('website'))
