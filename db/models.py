from django.db import models


class User(models.Model):
    tg_id = models.IntegerField()
    tg_username = models.TextField()
    name = models.TextField()
    phone = models.TextField()
    address = models.TextField()
    status = models.CharField(max_length=2, choices=[('co', 'courier'), ('cu', 'customer')])


class Courier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reviews_count = models.IntegerField()
    reviews_score = models.FloatField()


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reviews_count = models.IntegerField()
    reviews_score = models.FloatField(default=None, blank=True, null=True)


class Review(models.Model):
    courier = models.ForeignKey(Courier, default=None, blank=True, null=True, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, default=None, blank=True, null=True, on_delete=models.CASCADE)
    points = models.PositiveSmallIntegerField()
