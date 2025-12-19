from django.contrib.auth import get_user_model
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from .forms import MembershipForm, OrganizationForm, PositionForm
from .models import Membership, Organization, Position


class HomeView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        User = get_user_model()
        context["org_count"] = Organization.objects.count()
        context["pos_count"] = Position.objects.count()
        context["mem_count"] = Membership.objects.count()
        context["user_count"] = User.objects.count()
        return context


class BasePageMixin:
    title = ""
    cancel_url = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        context["cancel_url"] = self.cancel_url
        return context


class OrganizationList(ListView):
    model = Organization
    template_name = "core/organization_list.html"
    paginate_by = 20


class OrganizationDetail(DetailView):
    model = Organization
    template_name = "core/organization_detail.html"
    queryset = Organization.objects.prefetch_related("memberships__user", "memberships__position")


class OrganizationCreate(BasePageMixin, CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = "core/form.html"
    title = "Добавить организацию"
    cancel_url = reverse_lazy("core:organization-list")
    success_url = reverse_lazy("core:organization-list")


class OrganizationUpdate(BasePageMixin, UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = "core/form.html"
    title = "Изменить организацию"
    cancel_url = reverse_lazy("core:organization-list")
    success_url = reverse_lazy("core:organization-list")


class OrganizationDelete(BasePageMixin, DeleteView):
    model = Organization
    template_name = "core/confirm_delete.html"
    title = "Удаление организации"
    cancel_url = reverse_lazy("core:organization-list")
    success_url = reverse_lazy("core:organization-list")


class PositionList(ListView):
    model = Position
    template_name = "core/position_list.html"
    paginate_by = 20


class PositionDetail(DetailView):
    model = Position
    template_name = "core/position_detail.html"
    queryset = Position.objects.prefetch_related("memberships__user", "memberships__organization")


class PositionCreate(BasePageMixin, CreateView):
    model = Position
    form_class = PositionForm
    template_name = "core/form.html"
    title = "Добавить должность"
    cancel_url = reverse_lazy("core:position-list")
    success_url = reverse_lazy("core:position-list")


class PositionUpdate(BasePageMixin, UpdateView):
    model = Position
    form_class = PositionForm
    template_name = "core/form.html"
    title = "Изменить должность"
    cancel_url = reverse_lazy("core:position-list")
    success_url = reverse_lazy("core:position-list")


class PositionDelete(BasePageMixin, DeleteView):
    model = Position
    template_name = "core/confirm_delete.html"
    title = "Удаление должности"
    cancel_url = reverse_lazy("core:position-list")
    success_url = reverse_lazy("core:position-list")


class MembershipList(ListView):
    model = Membership
    template_name = "core/membership_list.html"
    paginate_by = 20

    def get_queryset(self):
        qs = Membership.objects.select_related("user", "organization", "position")

        q = (self.request.GET.get("q") or "").strip()
        org = (self.request.GET.get("org") or "").strip()
        pos = (self.request.GET.get("pos") or "").strip()
        status = (self.request.GET.get("status") or "").strip()
        sort = (self.request.GET.get("sort") or "").strip()

        if q:
            qs = qs.filter(Q(user__username__icontains=q) | Q(user__first_name__icontains=q) | Q(user__last_name__icontains=q) | Q(organization__organization_name__icontains=q) | Q(position__name__icontains=q))

        if org.isdigit():
            qs = qs.filter(organization_id=int(org))

        if pos.isdigit():
            qs = qs.filter(position_id=int(pos))

        if status == "active":
            qs = qs.filter(dismissal_date__isnull=True)
        elif status == "fired":
            qs = qs.filter(dismissal_date__isnull=False)

        sort_map = {
            "-hire_date": "-hire_date",
            "hire_date": "hire_date",
            "user": "user__username",
            "org": "organization__organization_name",
            "pos": "position__name"}
        order_by = sort_map.get(sort, "-hire_date")
        return qs.order_by(order_by, "id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        params = self.request.GET.copy()
        params.pop("page", None)
        context["qs"] = params.urlencode()

        context["orgs"] = Organization.objects.order_by("organization_name")
        context["positions"] = Position.objects.order_by("name")

        context["q"] = (self.request.GET.get("q") or "").strip()
        context["org"] = (self.request.GET.get("org") or "").strip()
        context["pos"] = (self.request.GET.get("pos") or "").strip()
        context["status"] = (self.request.GET.get("status") or "").strip()
        context["sort"] = (self.request.GET.get("sort") or "").strip() or "-hire_date"

        context["sort_options"] = [("-hire_date", "Сначала новые (по дате приема)"),
            ("hire_date", "Сначала старые (по дате приема)"),
            ("user", "По пользователю"),
            ("org", "По организации"),
            ("pos", "По должности")]
        context["status_options"] = [("", "Все"), ("active", "Только работающие"), ("fired", "Только уволенные")]
        return context


class MembershipDetail(DetailView):
    model = Membership
    template_name = "core/membership_detail.html"
    queryset = Membership.objects.select_related("user", "organization", "position")


class MembershipCreate(BasePageMixin, CreateView):
    model = Membership
    form_class = MembershipForm
    template_name = "core/form.html"
    title = "Добавить запись состава"
    cancel_url = reverse_lazy("core:membership-list")
    success_url = reverse_lazy("core:membership-list")

    def get_initial(self):
        initial = super().get_initial()
        q = self.request.GET
        if q.get("user"):
            initial["user"] = q.get("user")
        if q.get("organization"):
            initial["organization"] = q.get("organization")
        if q.get("position"):
            initial["position"] = q.get("position")
        return initial


class MembershipUpdate(BasePageMixin, UpdateView):
    model = Membership
    form_class = MembershipForm
    template_name = "core/form.html"
    title = "Изменить запись состава"
    cancel_url = reverse_lazy("core:membership-list")
    success_url = reverse_lazy("core:membership-list")


class MembershipDelete(BasePageMixin, DeleteView):
    model = Membership
    template_name = "core/confirm_delete.html"
    title = "Удаление записи состава"
    cancel_url = reverse_lazy("core:membership-list")
    success_url = reverse_lazy("core:membership-list")