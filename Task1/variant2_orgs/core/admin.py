from django.contrib import admin
from .models import Membership, Organization, Position

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display=("name",)
    search_fields=("name",)

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display=("organization_name","founding_date","director_name")
    search_fields=("organization_name","director_name","address")
    list_filter=("founding_date",)

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display=("user","organization","position","hire_date","dismissal_date")
    list_filter=("position","organization")
    search_fields=("user__username","user__first_name","user__last_name","organization__organization_name","position__name")
