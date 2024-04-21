from django.contrib import admin
from .models import FileName, FolderId, SheetName, CredentialsModel

# Register your models here.

admin.site.register(FileName)
admin.site.register(FolderId)
admin.site.register(SheetName)
admin.site.register(CredentialsModel)
