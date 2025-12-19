from django import forms
from django.contrib.auth import get_user_model
from .models import Membership, Organization, Position

class StyledModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            css_class = "input"
            if isinstance(widget, (forms.Select, forms.SelectMultiple)):
                css_class = "select"
            elif isinstance(widget, forms.Textarea):
                css_class = "textarea"
            elif isinstance(widget, forms.CheckboxInput):
                css_class = "check"
            existing_classes = widget.attrs.get("class", "")
            widget.attrs["class"] = f"{existing_classes} {css_class}".strip()
            if isinstance(widget, forms.DateInput):
                widget.attrs["type"] = "date"


class PositionForm(StyledModelForm):
    class Meta:
        model = Position
        fields = ("name",)

class OrganizationForm(StyledModelForm):
    class Meta:
        model = Organization
        fields = ("organization_name", "founding_date", "address", "director_name")
        widgets = {"founding_date": forms.DateInput(),}

class MembershipForm(StyledModelForm):
    class Meta:
        model = Membership
        fields = ("user", "organization", "position", "hire_date", "dismissal_date")
        widgets = {"hire_date": forms.DateInput(),"dismissal_date": forms.DateInput(),}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user"].queryset = get_user_model().objects.order_by("username")
        self.fields["organization"].queryset = Organization.objects.order_by("organization_name")
        self.fields["position"].queryset = Position.objects.order_by("name")