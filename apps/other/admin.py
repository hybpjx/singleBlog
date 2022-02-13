from django.contrib import admin

# Register your models here.
from apps.other.models import *


admin.site.register(HelpSubmit)


admin.site.register(BugSubmit)