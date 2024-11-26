from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, login, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(login=login, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(login, email, password, **extra_fields)

class Users(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    email = models.EmailField(unique=True)
    login = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=200)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['email', 'full_name']

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.full_name

class Services(models.Model):
    name = models.CharField(
        verbose_name="Название услуги",
        blank=False,
        max_length = 100,
    )

    service_type = models.CharField(
        verbose_name = "Тип услуги",
        blank=False,
        max_length = 100,
    )

    price = models.IntegerField(
        verbose_name = "Цена в рублях",
        blank=False,
    )

    class Meta:
        verbose_name = "Услугa"
        verbose_name_plural = "Услуги"
    
    def __str__(self):
        return self.name
    
class Order(models.Model):
    STATUS_CHOICES = [ 
        ('new', 'Новая заявка'),
        ('completed', 'Услуга оказана'),
        ('cancelled', 'Услуга отменена')
    ]

    TYPE_OF_PAYMENT = {
        ('cash', 'Наличными'),
        ('cards', 'Картой'),
    }

    address = models.CharField(
        verbose_name = "Адрес",
        blank = False,
        max_length = 100,
    )

    contact_data = models.CharField(
        verbose_name = "Контактная информация",
        blank = False,
        max_length = 12,
    )

    service_id = models.ForeignKey(
        Services,
        on_delete=models.CASCADE,
        blank = False,
        verbose_name="Услуги"
    )

    user_id = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        blank = False,
    )

    payment_type = models.CharField(
        verbose_name = "Тип оплаты",
        blank = False,
        choices=TYPE_OF_PAYMENT,
        default='cash',
        max_length = 40,
    )

    status = models.CharField(
        verbose_name="Статус заявки",
        max_length=10,
        choices=STATUS_CHOICES,
        default='new',
        blank=False,
    )

    date_time = models.DateTimeField(
        verbose_name="Дата и время",
        blank=False
    )

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
    
    def __str__(self):
        return self.contact_data
    


