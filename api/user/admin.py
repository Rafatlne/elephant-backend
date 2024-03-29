# Register your models here.
from api.conf.admin import AbstractAdmin
from django.contrib import admin
from api.user.models import User

from django import forms
from django.contrib.auth.admin import GroupAdmin as origGroupAdmin
from django.contrib.auth.models import Group


class GroupAdminForm(forms.ModelForm):
    """
    ModelForm that adds an additional multiple select field for managing
    the users in the group.
    """

    users = forms.ModelMultipleChoiceField(
        User.objects.all(),
        widget=admin.widgets.FilteredSelectMultiple("Users", False),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            initial_users = self.instance.user_set.values_list("pk", flat=True)
            self.initial["users"] = initial_users

    def save(self, *args, **kwargs):
        kwargs["commit"] = True
        return super(GroupAdminForm, self).save(*args, **kwargs)

    def save_m2m(self):
        self.instance.user_set.clear()
        self.instance.user_set.add(*self.cleaned_data["users"])


class GroupAdmin(origGroupAdmin):
    """
    Customized GroupAdmin class that uses the customized form to allow
    management of users within a group.
    """

    form = GroupAdminForm


class UserAdmin(AbstractAdmin):
    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )


admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
admin.site.register(User, UserAdmin)
