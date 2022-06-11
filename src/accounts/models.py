from django.contrib.auth.hashers import make_password, identify_hasher
from django.db.models import EmailField, BooleanField
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, is_active=True, is_staff=None, is_admin=None):

        if not email:
            raise ValueError("The given email nust be set")

        if not password:
            raise ValueError("The given password nust be set")

        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.is_active = is_active
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password=password, is_staff=True, is_admin=True)

        return user

    def create_staffuser(self, email, password=None):
        user = self.create_user(email, password=password, is_staff=True, is_admin=False)

        return user


class User(AbstractBaseUser):
    email = EmailField(unique=True, max_length=255)
    staff = BooleanField(default=False)
    is_active = BooleanField(default=True)
    admin = BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    object = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.admin:
            return True

        return self.staff

    @property
    def is_admin(self):
        return self.admin

    def save(self, *args, **kwargs):
        try:
            _alg = identify_hasher(self.password)
        except ValueError:
            self.password = make_password(self.password)

        super().save(*args, **kwargs)