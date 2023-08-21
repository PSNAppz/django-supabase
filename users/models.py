import uuid

from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from django.utils import timezone
from django.utils.crypto import get_random_string
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.reverse import reverse

from users.managers import UserManager


def revenuecat_id_gen():
    uid = uuid.uuid4()
    revenuecat_id = 'CAT' + str(uid.hex)
    return revenuecat_id

def player_id_short():
    return get_random_string(length=2, allowed_chars='abcdefghjkmnpqrstuvwxy').upper() + get_random_string(length=4, allowed_chars='23456789').upper()


class User(AbstractBaseUser, PermissionsMixin):

    uid = models.CharField(unique=True, default=uuid.uuid1, max_length=50)
    revenuecat_id = models.CharField(max_length=50, null=True, blank=True)
    display_name = models.CharField(
        'display name',
        max_length=30,
        null=True,
        blank=True,
    )
    phone_number = PhoneNumberField(
        'phone number',
        unique=True,
        null=True,
        blank=True,
        error_messages={
            'unique': "A user with the same mobile number already exists. Please enter a new mobile number.",
        },
    )
    email = models.EmailField(
        'email address',
        unique=True,
        null=True,
        blank=True,
        error_messages={
            'unique': "This email address already exists. Please enter a new email address.",
        },
    )

    notification_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text='Designates whether this user should be treated as active. '
        'Unselect this instead of deleting accounts.',
    )
    date_joined = models.DateTimeField('date joined', default=timezone.now)
    is_deleted = models.BooleanField(default=False)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'uid'
    REQUIRED_FIELDS = ['phone_number']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return f'{self.identifer}'

    def clean(self):
        pass

    @property
    def identifer(self):
        return self.display_name or self.phone_number or self.email or self.uid
    def get_absolute_url(self):
        return reverse('users-detail', kwargs={'pk': self.pk})

    def get_username(self):
        """Return the username for this User."""
        return self.identifer
    @property
    def identifer(self):
        return self.display_name or self.phone_number or self.email or self.uid

    @property
    def first_name(self):
        if not self.display_name:
            return None
        return self.display_name.split(maxsplit=1)[0]

    @property
    def last_name(self):
        if not self.display_name:
            return None

        name: list = self.display_name.split(maxsplit=1)

        if len(name) <= 1:
            return None

        return name[1]

    @first_name.setter
    def first_name(self, value):
        if not self.display_name:
            self.display_name = value
            return

        name = self.display_name.split(maxsplit=1)
        name[0] = value
        self.display_name = ' '.join(name)

    @last_name.setter
    def last_name(self, value):
        if not self.display_name:
            self.display_name = value
            return None

        name = self.display_name.split(maxsplit=1)

        if len(name) <= 1:
            self.display_name += ' ' + value
            return None

        name[1] = value
        self.display_name = ' '.join(name)

    def revenuecat_user(self):
        if self.revenuecat_id is not None:
            return self.revenuecat_id
        self.revenuecat_id = revenuecat_id_gen()
        self.save()    
        return self.phone_number    

    def save(self, *args, **kwargs):
        if self.id is None:  # this means it being created, not updated
            self.revenuecat_id = revenuecat_id_gen()
        super().save(*args, **kwargs)        


# Model to store the list of logged in users
class UserAuthTime(models.Model):
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="login_times"
    )
    auth_key = models.TextField(null=True, blank=True)
    auth_agent = models.TextField(null=True, blank=True)
    created_at = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user} - {self.auth_key}"
