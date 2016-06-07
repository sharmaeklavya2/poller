from django.db import models

from six import text_type
from typing import Any, Optional

class UserManager(models.Manager):
    def create_user(username, email=None, password=None, **extra_fields):
        # type: (text_type, Optional[text_type], Optional[text_type], **Any) -> 'User'
        ...

class User(models.Model):
    username = ... # type: text_type
    password = ... # type: text_type
    is_active = ... # type: bool
    is_staff = ... # type: bool
    is_superuser = ... # type: bool
    id = ... # type: int
    objects = ... # type: UserManager

    def is_authenticated(self) -> bool: ...

