from django.db import models

from work.models import Work
from account.models import User

class Coupon(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    code = models.CharField(max_length=8, unique=True)
    is_used = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "coupon"
        constraints = [
            models.UniqueConstraint(
                fields=["work", "user"],
                name="unique coupon"
            )
        ]