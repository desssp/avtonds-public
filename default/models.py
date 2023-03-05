from django.core.exceptions import ValidationError

from .sources import enums
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from smart_selects.db_fields import ChainedForeignKey, GroupedForeignKey
from django.utils import timezone


class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self,
                     email: str,
                     password,
                     full_name: str = None,
                     short_name: str = None,
                     user_type: int = None,
                     **extra_fields):
        """
        Создает и сохраняет пользователя с введенным им email и паролем.
        """

        if not email:
            raise ValidationError('Необходимо заполнить e-mail')
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, short_name=short_name, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        # return user

    def create_user(self, email, password=None, full_name=None, short_name=None, user_type=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', True)
        if not user_type:
            raise ValidationError('Необходимо выбрать тип пользователя')
        if not full_name:
            raise ValidationError('Необходимо заполнить полное наименование')
        return self._create_user(email, password, full_name, short_name, user_type, **extra_fields)

    def create_superuser(self, email, password, user_type=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValidationError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValidationError('Superuser must have is_staff=True.')
        if user_type:
            raise ValidationError('Superuser wont have a user_type.')

        return self._create_user(email, password, user_type, **extra_fields)


class User(AbstractUser):
    """Custom User Model"""
    username = None
    email = models.EmailField('email_address', unique=True)
    user_type = models.IntegerField('Тип пользователя', choices=enums.USER_TYPES, blank=True, null=True)
    full_name = models.CharField('Полное наименование', max_length=150, blank=True, null=True)
    short_name = models.CharField('Краткое наименование', max_length=50, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email_address']

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.full_name or self.email


class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField('Статус', default=0)
    message = models.TextField('Ошибка или результат', null=True)
    timestamp = models.DateTimeField('Дата создания', auto_now_add=True)
    last_update = models.DateTimeField('Дата обновления', auto_now=True)

    def __str__(self):
        return '{}\t{}'.format(self.user.email, self.status)

    class Meta:
        verbose_name = 'Сессия'
        verbose_name_plural = 'Сессии'


class CarMark(models.Model):
    # ['id', 'name', 'cyrillic-name', 'popular', 'country', 'models']
    mark_char_id = models.CharField('Текстовый идентификатор', max_length=150)
    name = models.CharField('Наименование', max_length=150)
    name_cyrillic = models.CharField('Наименование на русском', max_length=150)
    rating = models.IntegerField('Уровень популярности', default=0)
    country = models.CharField('Страна производства', max_length=150)

    class Meta:
        verbose_name = 'Марка'
        verbose_name_plural = 'Марки'

    def __str__(self):
        return self.name


class CarModel(models.Model):
    # ['id', 'name', 'cyrillic-name', 'class', 'year-from', 'year-to']
    car_mark = models.ForeignKey(CarMark, on_delete=models.CASCADE)
    model_char_id = models.CharField('Текстовый идентификатор', max_length=150)
    name = models.CharField('Наименование', max_length=150)
    name_cyrillic = models.CharField('Наименование на русском', max_length=150)
    model_class = models.CharField('Класс авто', max_length=20, null=True)
    year_from = models.IntegerField('Год начала производства', null=True)
    year_to = models.IntegerField('Год окончания производства', null=True)

    class Meta:
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'

    def __str__(self):
        return self.name


class RequestStatus(models.Model):
    name = models.CharField('Наименование', max_length=50)

    class Meta:
        verbose_name = 'Статус запроса'
        verbose_name_plural = 'Статусы запроса'

    def __str__(self):
        return self.name


class OfferStatus(models.Model):
    name = models.CharField('Наименование', max_length=50)

    class Meta:
        verbose_name = 'Статус предложения'
        verbose_name_plural = 'Статусы предложения'

    def __str__(self):
        return self.name


class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    car_mark = models.ForeignKey(CarMark, on_delete=models.DO_NOTHING, verbose_name='Марка')
    car_model = ChainedForeignKey(CarModel,
                                  chained_field='car_mark',
                                  chained_model_field='car_mark',
                                  show_all=False,
                                  auto_choose=True,
                                  sort=True,
                                  on_delete=models.DO_NOTHING,
                                  verbose_name='Модель')
    color = models.CharField('Цвет', max_length=150, blank=True, null=True)
    body_type = models.IntegerField('Тип кузова', choices=enums.BODY_TYPES, blank=True, null=True)
    max_age = models.IntegerField('Год выпуска от', blank=True, null=True, validators=[
        MinValueValidator(1900),
        MaxValueValidator(timezone.now().year)])
    fuel = models.IntegerField('Топливо', choices=enums.FUEL_TYPES, blank=True, null=True)
    engine_capacity = models.DecimalField('Объем двигателя', max_digits=2, decimal_places=1, blank=True, null=True)
    engine_power = models.IntegerField('Мощность двигателя (л.с.)', blank=True, null=True)
    max_mileage = models.IntegerField('Пробег до (км)', blank=True, null=True)
    min_price = models.DecimalField('Бюджет от (RUB)', max_digits=11, decimal_places=0, blank=True, null=True)
    max_price = models.DecimalField('Бюджет до (RUB)', max_digits=11,  decimal_places=0, blank=True, null=True)
    additional_requirements = models.TextField('Дополнительные требования', blank=True, null=True)
    status = models.ForeignKey(RequestStatus, default=1, on_delete=models.DO_NOTHING, verbose_name='Статус')
    created = models.DateTimeField('Дата создания', default=timezone.now)
    last_update = AutoDateTimeField('Дата обновления', default=timezone.now)

    class Meta:
        verbose_name = 'Запрос'
        verbose_name_plural = 'Запросы'

    def __str__(self):
        return f'{self.user.full_name}\t{self.car_mark.name}/{self.car_model.name}\t{self.status.name}'


class Offer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    car_mark = models.ForeignKey(CarMark, on_delete=models.DO_NOTHING, verbose_name='Марка')
    # car_model = models.ForeignKey(CarModel, on_delete=models.DO_NOTHING)
    car_model = ChainedForeignKey(CarModel,
                                  chained_field='car_mark',
                                  chained_model_field='car_mark',
                                  show_all=False,
                                  auto_choose=True,
                                  sort=True,
                                  on_delete=models.DO_NOTHING,
                                  verbose_name='Модель')
    color = models.CharField('Цвет', max_length=150)
    year_of_issue = models.IntegerField('Год выпуска', validators=[
        MinValueValidator(1900),
        MaxValueValidator(timezone.now().year)])
    body_type = models.IntegerField('Тип кузова', choices=enums.BODY_TYPES, blank=True, null=True)
    fuel = models.IntegerField('Топливо', choices=enums.FUEL_TYPES, blank=True, null=True)
    engine_capacity = models.DecimalField('Объем двигателя', max_digits=2, decimal_places=1)
    engine_power = models.IntegerField('Мощность двигателя (л.с.)', blank=True, null=True)
    mileage = models.IntegerField('Пробег')
    price = models.DecimalField('Цена (RUB)', max_digits=11, decimal_places=2)
    location = models.TextField('Адрес местонахождения авто')
    additional_properties = models.TextField('Дополнительные данные', blank=True, null=True)
    status = models.ForeignKey(OfferStatus, default=1, on_delete=models.DO_NOTHING, verbose_name='Статус')
    created = models.DateTimeField('Дата создания', default=timezone.now)
    last_update = AutoDateTimeField('Дата обновления', default=timezone.now)

    class Meta:
        verbose_name = 'Предложение'
        verbose_name_plural = 'Предложения'

    def __str__(self):
        return f'{self.user.full_name}\t{self.car_mark.name}/{self.car_model.name}\t{self.status.name}'
