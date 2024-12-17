from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Student)
admin.site.register(Staff)
admin.site.register(Librarian)
admin.site.register(LibraryHistory)
admin.site.register(FeeRecords)