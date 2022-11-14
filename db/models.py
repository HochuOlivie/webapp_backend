import json
from django.db import models


class User(models.Model):
    tg_id = models.IntegerField()
    tg_username = models.TextField()
    phone = models.TextField()


class PartnerReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.PositiveSmallIntegerField()


class CustomerReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.PositiveSmallIntegerField()


class Order(models.Model):
    feature_from = models.JSONField()
    user = models.ForeignKey(User, default=None, blank=True, null=True, on_delete=models.CASCADE)


class Offer(models.Model):
    feature_from = models.JSONField()
    user = models.ForeignKey(User, default=None, blank=True, null=True, on_delete=models.CASCADE)


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feature = models.JSONField()
