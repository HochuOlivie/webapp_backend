import json
from django.db import models


class User(models.Model):
    tg_id = models.IntegerField()
    tg_username = models.TextField()
    name = models.TextField()
    phone = models.TextField()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reviews_count = models.IntegerField(default=0)
    reviews_score = models.FloatField(default=None, blank=True, null=True)


class Courier(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)


class Customer(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)


class Review(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    is_for = models.CharField(max_length=2, choices=[('co', 'courier'), ('cu', 'customer')])
    points = models.PositiveSmallIntegerField()


class Order(models.Model):
    feature_from = models.JSONField()
    user = models.ForeignKey(User, default=None, blank=True, null=True, on_delete=models.CASCADE)


class Offer(models.Model):
    feature_from = models.JSONField()
    user = models.ForeignKey(User, default=None, blank=True, null=True, on_delete=models.CASCADE)
