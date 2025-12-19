from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from .forms import MembershipForm, OrganizationForm, PositionForm
from .models import Membership, Organization, Position


class HomeView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        User = get_user_model()
        ctx.update(
            {
                "org_count": Organization.objects.count(),
                "pos_count": Position.objects.count(),
                "mem_count": Membership.objects.count(),
                "user_count": User.objects.count(),
            }
        )
        return ctx


class TitleCancelMixin:
    title = ""
    cancel_url = None

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({"title": self.title, "cancel_url": self.cancel_url})
        return ctx


class PaginatedListView(ListView):
    paginate_by = 20


class FormTemplateMixin(TitleCancelMixin):
    template_name = "core/form.html"


class DeleteTemplateMixin(TitleCancelMixin):
    template_name = "core/confirm_delete.html"


class OrganizationList(PaginatedListView):
    model = Organization
    template_name = "core/organization_list.html"


class OrganizationDetail(DetailView):
    model = Organization
    template_name = "core/organization_detail.html"
    queryset = Organization.objects.prefetch_related("memberships__user", "memberships__position")


class OrganizationCreate(FormTemplateMixin, CreateView):
    model = Organization
    form_class = OrganizationForm
    title = "Добавить организацию"
    cancel_url = reverse_lazy("core:organization-list")
    success_url = reverse_lazy("core:organization-list")


class OrganizationUpdate(FormTemplateMixin, UpdateView):
    model = Organization
    form_class = OrganizationForm
    title = "Изменить организацию"
    cancel_url = reverse_lazy("core:organization-list")
    success_url = reverse_lazy("core:organization-list")


class OrganizationDelete(DeleteTemplateMixin, DeleteView):
    model = Organization
    title = "Удаление организации"
    cancel_url = reverse_lazy("core:organization-list")
    success_url = reverse_lazy("core:organization-list")


class PositionList(PaginatedListView):
    model = Position
    template_name = "core/position_list.html"


class PositionDetail(DetailView):
    model = Position
    template_name = "core/position_detail.html"
    queryset = Position.objects.prefetch_related("memberships__user", "memberships__organization")


class PositionCreate(FormTemplateMixin, CreateView):
    model = Position
    form_class = PositionForm
    title = "Добавить должность"
    cancel_url = reverse_lazy("core:position-list")
    success_url = reverse_lazy("core:position-list")


class PositionUpdate(FormTemplateMixin, UpdateView):
    model = Position
    form_class = PositionForm
    title = "Изменить должность"
    cancel_url = reverse_lazy("core:position-list")
    success_url = reverse_lazy("core:position-list")


class PositionDelete(DeleteTemplateMixin, DeleteView):
    model = Position
    title = "Удаление должности"
    cancel_url = reverse_lazy("core:position-list")
    success_url = reverse_lazy("core:position-list")


class MembershipList(PaginatedListView):
    model = Membership
    template_name = "core/membership_list.html"
    queryset = Membership.objects.select_related("user", "organization", "position")


class MembershipDetail(DetailView):
    model = Membership
    template_name = "core/membership_detail.html"
    queryset = Membership.objects.select_related("user", "organization", "position")


class MembershipCreate(FormTemplateMixin, CreateView):
    model = Membership
    form_class = MembershipForm
    title = "Добавить запись состава"
    cancel_url = reverse_lazy("core:membership-list")
    success_url = reverse_lazy("core:membership-list")

    def get_initial(self):
        initial = super().get_initial()
        q = self.request.GET
        for key in ("user", "organization", "position"):
            if q.get(key):
                initial[key] = q.get(key)
        return initial


class MembershipUpdate(FormTemplateMixin, UpdateView):
    model = Membership
    form_class = MembershipForm
    title = "Изменить запись состава"
    cancel_url = reverse_lazy("core:membership-list")
    success_url = reverse_lazy("core:membership-list")


class MembershipDelete(DeleteTemplateMixin, DeleteView):
    model = Membership
    title = "Удаление записи состава"
    cancel_url = reverse_lazy("core:membership-list")
    success_url = reverse_lazy("core:membership-list")
