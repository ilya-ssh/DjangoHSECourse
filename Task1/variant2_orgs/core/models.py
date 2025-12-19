from django.apps import apps
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

def default_position_id():
    Position = apps.get_model("core", "Position")
    obj, _ = Position.objects.get_or_create(name="Без должности")
    return obj.pk

class Position(models.Model):
    name = models.CharField(max_length=50, unique=True)
    class Meta:
        ordering = ["name"]
        verbose_name = "Должность"
        verbose_name_plural = "Должности"
    def __str__(self):
        return self.name

class Organization(models.Model):
    organization_name = models.CharField(max_length=50)
    founding_date = models.DateField(default=timezone.localdate)
    address = models.CharField(max_length=200)
    director_name = models.CharField(max_length=50)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL,through="Membership",related_name="organizations",blank=True)
    class Meta:
        ordering = ["organization_name"]
        verbose_name = "Организация"
        verbose_name_plural = "Организации"
    def __str__(self):
        return self.organization_name

class Membership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="memberships")
    organization = models.ForeignKey(Organization,on_delete=models.CASCADE,related_name="memberships")
    position = models.ForeignKey(Position,on_delete=models.SET_DEFAULT,default=default_position_id,related_name="memberships")
    hire_date = models.DateField(default=timezone.localdate)
    dismissal_date = models.DateField(null=True, blank=True)
    class Meta:
        unique_together = (("user", "organization"))
        ordering = ["-hire_date", "organization__organization_name", "user__username"]
        verbose_name = "Сотрудник в организации"
        verbose_name_plural = "Сотрудники в организациях"
    def clean(self):
        if self.dismissal_date and self.dismissal_date < self.hire_date:
            raise ValidationError({"dismissal_date": "Дата увольнения не может быть раньше даты приема"})
    def __str__(self):
        username = getattr(self.user, "get_username", None)
        if callable(username):
            username = self.user.get_username()
        else:
            username = str(self.user)
        return f"{username} — {self.organization} ({self.position})"