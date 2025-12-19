from django import forms
from django.contrib.auth import get_user_model
from .models import Membership, Organization, Position


class StyledModelForm(forms.ModelForm):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        for f in self.fields.values():
            w = f.widget
            cls = "input"
            if isinstance(w, (forms.Select, forms.SelectMultiple)):
                cls = "select"
            if isinstance(w, forms.Textarea):
                cls = "textarea"
            if isinstance(w, forms.CheckboxInput):
                cls = "check"
            w.attrs = {**w.attrs, "class": (" ".join([w.attrs.get("class", "").strip(), cls])).strip()}
            if isinstance(w, forms.DateInput):
                w.attrs = {**w.attrs, "type": "date"}


class PositionForm(StyledModelForm):
    class Meta:
        model = Position
        fields = ("name",)


class OrganizationForm(StyledModelForm):
    class Meta:
        model = Organization
        fields = ("organization_name", "founding_date", "address", "director_name")
        widgets = {"founding_date": forms.DateInput()}


class MembershipForm(StyledModelForm):
    class Meta:
        model = Membership
        fields = ("user", "organization", "position", "hire_date", "dismissal_date")
        widgets = {"hire_date": forms.DateInput(), "dismissal_date": forms.DateInput()}

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        U = get_user_model()
        self.fields["user"].queryset = U.objects.order_by("username")
        self.fields["organization"].queryset = Organization.objects.order_by("organization_name")
        self.fields["position"].queryset = Position.objects.order_by("name")
