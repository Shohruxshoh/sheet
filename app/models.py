from django.db import models


# Create your models here.
class FileName(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    key = models.CharField(max_length=200, null=True, blank=True)
    word = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.name}-{self.pk}'


class FolderId(models.Model):
    folder = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.folder}-{self.pk}'


class SheetName(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    sheetId = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.name}-{self.pk}'


class CredentialsModel(models.Model):
    token = models.CharField(max_length=200, null=True, blank=True)
    refresh_token = models.CharField(max_length=200, null=True, blank=True)
    token_uri = models.CharField(max_length=200, null=True, blank=True)
    client_id = models.CharField(max_length=200, null=True, blank=True)
    client_secret = models.CharField(max_length=200, null=True, blank=True)
    scopes = models.CharField(max_length=250, null=True, blank=True)

# class File(models.Model):
#     file = models.FileField()
#
#     def __str__(self):
#         return f'{self.pk}'
