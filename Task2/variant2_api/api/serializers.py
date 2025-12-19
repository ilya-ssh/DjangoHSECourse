from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.models import Organization

class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organization
        fields = ("url", "id", "organization_name", "founding_date", "address", "director_name")

class OrganizationInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ("id", "organization_name")

class UserSerializer(serializers.ModelSerializer):
    organization = serializers.SerializerMethodField()
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "first_name", "last_name", "email", "organization")
    def get_organization(self, obj):
        mems = list(obj.memberships.all())
        if not mems:
            return None
        active = next((m for m in mems if m.dismissal_date is None), None)
        m = active or mems[0]
        return OrganizationInlineSerializer(m.organization, context=self.context).data

class OrganizationManyEmployeesSerializer(serializers.ModelSerializer):
    employee_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Organization
        fields = ("id", "organization_name", "employee_count")
