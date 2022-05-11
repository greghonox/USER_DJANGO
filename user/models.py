import random
import string

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))

# Create your models here.
def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))


class CustomAccountManager(BaseUserManager):
    def create_user(self, nome, last_name, password, **other_fields):

        user = self.model(nome=nome,
                          last_name=last_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, nome, last_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(nome, last_name, password, **other_fields)


class Funcionario(AbstractBaseUser, PermissionsMixin):
    nome = models.CharField(max_length=100, unique=True)
    last_name = models.CharField(max_length=100)
    profile_pic = models.ImageField(
        upload_to='users/', default='users/default.png')
    bio = models.TextField(_(
        'Bio'), max_length=500, blank=True)
    followers = models.ManyToManyField(
        "self",
        related_name='following',
        symmetrical=False,
        blank=True)
    slug = models.SlugField(max_length=255, unique=True)

    register_date = models.DateTimeField(default=timezone.now)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'nome'
    REQUIRED_FIELDS = ['last_name']

    def __str__(self):
        return f'{self.nome} {self.last_name}'

    def get_absolute_url(self):
        return reverse('users:user_detail', args=[self.slug])

    def count_following(self):
        users_following = Funcionario.objects.filter(followers=self)
        return users_following.count()

    def count_posts(self):
        return Post.objects.filter(author=self).count()

    def is_follower(self, other_user):
        if other_user in self.followers.all():
            return True
        return False

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(rand_slug() + "-")
        super(Funcionario, self).save(*args, **kwargs)

class Holerite(models.Model):
    ...

class Ponto(models.Model):
    ...    

class Folha(models.Model):
    ...
