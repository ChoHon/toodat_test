from django.db import models
from rest_framework import status
from rest_framework.exceptions import ValidationError

from work.models import Work
from account.models import User

class Coupon(models.Model):
    name = models.CharField(max_length=100)
    discount_amount = models.PositiveIntegerField(default=0)
    discount_rate = models.PositiveIntegerField(default=0)
    count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "coupon"

class CouponUser(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    work = models.ForeignKey(Work, on_delete=models.CASCADE)

    code = models.CharField(max_length=8, unique=True, default=None)
    is_used = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "coupon_user"
        constraints = [
            models.UniqueConstraint(
                fields=["coupon", "user", "work"],
                name="unique coupon"
            )
        ]