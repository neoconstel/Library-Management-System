from django.contrib import admin
from . import models

# trying to implement object permissions
from rules.contrib.admin import ObjectPermissionsModelAdmin

class BookAdmin(ObjectPermissionsModelAdmin):
    pass

# Register your models here.
admin.site.register(models.Book, BookAdmin)
admin.site.register(models.Student)
admin.site.register(models.Order)
admin.site.register(models.User)
