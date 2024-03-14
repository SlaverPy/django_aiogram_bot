from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import m2m_changed
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.functional import cached_property
from django.utils.html import format_html
from environs import Env

from core.core.utils import user_directory_path

env = Env()
env.read_env()


class BaseModel(models.Model):
    created_at = models.DateTimeField(verbose_name="Создано", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Обновлено", auto_now=True)

    class Meta:
        abstract = True


class PromoCodes(BaseModel):
    code = models.CharField(verbose_name="Название группы", max_length=128, blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="Активный промокод")
    awards_list = models.CharField(verbose_name="Награды:", max_length=512, blank=True, null=True)
    is_one_time_use = models.BooleanField(default=False, verbose_name="Одноразовый")
    user = models.ForeignKey("UserBot", verbose_name="Пользователь", on_delete=models.SET_NULL,
                             null=True, blank=True, related_name="promocodes")

    def __str__(self):
        return self.code


class UserBot(BaseModel):
    telegram_id = models.BigIntegerField(verbose_name="ID Пользователя Телеграм", blank=True, null=True)
    telegram_username = models.CharField(verbose_name="Username Телеграм", max_length=32, blank=True, null=True)
    telegram_first_name = models.CharField(verbose_name="Имя пользователя", max_length=64, blank=True, null=True)
    telegram_last_name = models.CharField(verbose_name="Фамилия пользователя", max_length=64, blank=True, null=True)
    used_promo_codes = models.ManyToManyField(PromoCodes, through='PromoCodeUsage',
                                              verbose_name="Использованные промокоды", related_name='user')

    class Meta:
        verbose_name = "Пользователь бота"
        verbose_name_plural = "Пользователи бота"

    def __str__(self):
        return f"{self.telegram_username}: {self.telegram_id}"


class Group(BaseModel):
    name = models.CharField(verbose_name="Название группы", max_length=128, blank=True, null=True)
    weight = models.FloatField(verbose_name="Вес группы", blank=True, null=True)

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self):
        return f"{self.name}"
