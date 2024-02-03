from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.db import models

from api.conf.models import BaseModel


class User(AbstractUser, PermissionsMixin, BaseModel):
    """
    Profile information of user. Additional stuff
    """
    is_banned = models.BooleanField(default=False)

    @property
    def full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()
