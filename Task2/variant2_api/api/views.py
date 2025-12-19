from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import Organization
from .serializers import OrganizationManyEmployeesSerializer, OrganizationSerializer, UserSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all().order_by("organization_name")
    serializer_class = OrganizationSerializer

    @action(detail=False, methods=["get"], url_path="many-employees")
    def many_employees(self, request):
        qs = (
            self.get_queryset()
            .annotate(employee_count=Count("memberships__user",filter=Q(memberships__dismissal_date__isnull=True),distinct=True))
            .order_by("-employee_count", "organization_name")[:10]
        )
        serializer = OrganizationManyEmployeesSerializer(qs, many=True, context=self.get_serializer_context())
        return Response(serializer.data)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        get_user_model()
        .objects.all()
        .prefetch_related("memberships__organization")
        .order_by("username")
    )
    serializer_class = UserSerializer