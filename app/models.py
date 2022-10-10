from django.db import models
from django.urls import reverse

from django.contrib.auth.models import User


class User(User):
    isAdmin = models.BooleanField("Admin", default=False)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


class Product(models.Model):
    name = models.CharField("Name", max_length=255)
    category = models.CharField("Category", max_length=50)
    price = models.IntegerField("Price")
    desc = models.TextField("Description")
    image = models.ImageField("Image Field", upload_to='images/', height_field=None, width_field=None, max_length=None)
    event_dt = models.DateTimeField("Auction Ends at", null=True)
    created_at = models.DateTimeField("Created At", auto_now=True, auto_now_add=False)
    owned_by = models.ForeignKey(User, on_delete=models.CASCADE)
    approved = models.BooleanField("Approval Status", default=False)
    banned = models.BooleanField("Banned", default=False)


class Bid(models.Model):
    bid_by = models.ForeignKey(User, verbose_name="Bid By", on_delete=models.CASCADE)
    bid_price = models.IntegerField("Bid Price")
    bid_at = models.DateTimeField("Bid Created At", auto_now=True, auto_now_add=False)
    bid_product = models.ForeignKey(Product, verbose_name="Bid for", on_delete=models.CASCADE)


class RequestAndIP(models.Model):
    ip = models.TextField("IP Address")
    last_request_time = models.DateTimeField("Created At", auto_now=True, auto_now_add=False)
    req_counter = models.IntegerField("Requests left")
    # isBanned = models.BooleanField("Is Banned")