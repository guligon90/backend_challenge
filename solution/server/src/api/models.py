# Django imports
from django.conf import settings
from django.db import models
from django.db.exceptions import ValidationError

# Project imports
from api.utils import (
    BoundedNumber,
)


class Car(models.Model):
    gas_capacity = models.FloatField(min=0)
    current_gas_fraction = models.FloatField(min=0, max=1.0)

    @property
    def current_liters(self) -> float:
        return self.current_gas_fraction * self.gas_capacity

    def evaluate_gas_fraction(self, km_traveled: float) -> float:
        new_liters = self.current_liters - settings.GAS_CONSUMPTION_PER_KM*km_traveled

        return BoundedNumber(
            new_liters,
            self.gas_capacity.min,
            self.gas_capacity
        ).value

    def __str__(self) -> str:
        return f'{self.id}'


def restrict_tyre_amount(car_instance: Car) -> None:
    if Tyre.objects.filter(car_id=car_instance.id).count() >= 4:
        raise ValidationError(
            f'Team already has maximal amount of rounds {settings.MAX_NUM_OF_TYRES})'
        )


class Tyre(models.Model):
    degradation = models.FloatField(min=0, max=1.0)
    car = models.ForeignKey(
        Car,
        on_delete=models.Cascade,
        validators=[restrict_tyre_amount, ]
    )

    def evaluate_degradation(self, km_traveled: float) -> float:
        new_degradation = self.degradation + settings.TYRE_DEGRADATION_PER_KM*km_traveled

        return BoundedNumber(
            new_degradation,
            self.degradation.min,
            self.degradation.max
        ).value

    def __str__(self) -> str:
        return f'{self.id} - {self.degradation}'
