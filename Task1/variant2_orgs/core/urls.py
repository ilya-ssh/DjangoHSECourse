from django.urls import path
from . import views
app_name="core"
urlpatterns=[
    path("",views.HomeView.as_view(),name="home"),
    path("organizations/",views.OrganizationList.as_view(),name="organization-list"),
    path("organizations/add/",views.OrganizationCreate.as_view(),name="organization-create"),
    path("organizations/<int:pk>/",views.OrganizationDetail.as_view(),name="organization-detail"),
    path("organizations/<int:pk>/edit/",views.OrganizationUpdate.as_view(),name="organization-update"),
    path("organizations/<int:pk>/delete/",views.OrganizationDelete.as_view(),name="organization-delete"),
    path("positions/",views.PositionList.as_view(),name="position-list"),
    path("positions/add/",views.PositionCreate.as_view(),name="position-create"),
    path("positions/<int:pk>/",views.PositionDetail.as_view(),name="position-detail"),
    path("positions/<int:pk>/edit/",views.PositionUpdate.as_view(),name="position-update"),
    path("positions/<int:pk>/delete/",views.PositionDelete.as_view(),name="position-delete"),
    path("memberships/",views.MembershipList.as_view(),name="membership-list"),
    path("memberships/add/",views.MembershipCreate.as_view(),name="membership-create"),
    path("memberships/<int:pk>/",views.MembershipDetail.as_view(),name="membership-detail"),
    path("memberships/<int:pk>/edit/",views.MembershipUpdate.as_view(),name="membership-update"),
    path("memberships/<int:pk>/delete/",views.MembershipDelete.as_view(),name="membership-delete"),
]
