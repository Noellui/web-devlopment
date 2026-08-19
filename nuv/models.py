from django.db import models
class Product(models.Model):
    p_id = models.AutoField(primary_key=True)
    p_title = models.CharField(max_length=200)
    p_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    p_description = models.TextField(
        max_length=1000
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    modified_at = models.DateTimeField(
        auto_now=True
    )
    is_active = models.BooleanField(
        default=True
    )
    qty = models.PositiveIntegerField(
        default=0
    )
    p_img_url = models.URLField(
        max_length=500,
        blank=True
    )

    def __str__(self):
        return self.p_title