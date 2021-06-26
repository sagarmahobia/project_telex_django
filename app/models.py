from django.db import models


class Icon(models.Model):
    id = models.IntegerField(primary_key=True)
    alias = models.CharField(max_length=15, default=True)


class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True, default=None)
    friendly_name = models.CharField(max_length=50, default=None)
    app_icon_id = models.CharField(max_length=35, default=0)


class Entity(models.Model):
    id = models.IntegerField(primary_key=True)
    entity_id = models.CharField(max_length=50, unique=True)
    entity_type = models.CharField(max_length=10)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    # FETCHED BY JOB
    fetched = models.BooleanField(default=False)
    last_updated = models.DateTimeField(null=True)
    title = models.CharField(max_length=30, null=True)
    image = models.CharField(max_length=500, null=True)
    description = models.CharField(max_length=300, null=True)
    subscribers = models.IntegerField(default=0)

    def __str__(self):
        return self.entity_id + " __ " + self.title
