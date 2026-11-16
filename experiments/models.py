from django.db import models
from django.contrib.auth.models import User


class Experiment(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('planned', 'Запланирован'),
        ('completed', 'Завершён'),
    ]

    name = models.CharField(max_length=200, verbose_name='Название эксперимента')
    description = models.TextField(blank=True, verbose_name='Описание')
    baseline_conversion = models.FloatField(verbose_name='Базовая конверсия (%)')
    mde = models.FloatField(verbose_name='Минимально обнаруживаемый эффект (MDE)')
    alpha = models.FloatField(default=0.05, verbose_name='Уровень значимости (alpha)')
    power = models.FloatField(default=0.8, verbose_name='Статистическая мощность')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Эксперимент'
        verbose_name_plural = 'Эксперименты'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Variant(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=50, verbose_name='Название варианта')
    visitors = models.PositiveIntegerField(default=0, verbose_name='Количество посетителей')
    conversions = models.PositiveIntegerField(default=0, verbose_name='Количество конверсий')
    is_control = models.BooleanField(default=False, verbose_name='Контрольный вариант')

    class Meta:
        verbose_name = 'Вариант'
        verbose_name_plural = 'Варианты'

    def __str__(self):
        return f"{self.experiment.name} — {self.name}"

    @property
    def conversion_rate(self):
        if self.visitors == 0:
            return 0
        return round((self.conversions / self.visitors) * 100, 2)


class StatisticalResult(models.Model):
    experiment = models.OneToOneField(Experiment, on_delete=models.CASCADE, related_name='result')
    sample_size_per_variant = models.PositiveIntegerField(null=True, blank=True,
                                                          verbose_name='Размер выборки на вариант')
    p_value = models.FloatField(null=True, blank=True)
    relative_uplift = models.FloatField(null=True, blank=True, verbose_name='Относительный uplift (%)')
    confidence_interval_lower = models.FloatField(null=True, blank=True)
    confidence_interval_upper = models.FloatField(null=True, blank=True)
    is_significant = models.BooleanField(default=False, verbose_name='Статистически значимо')
    calculated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Статистический результат'
        verbose_name_plural = 'Статистические результаты'

    def __str__(self):
        return f"Результат: {self.experiment.name}"


from django.db import models

# Create your models here.
