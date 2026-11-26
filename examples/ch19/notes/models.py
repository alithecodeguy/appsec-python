from django.db import models


class Workspace(models.Model):
    name = models.CharField(max_length=80, unique=True)


class Note(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=4000)
