from django.contrib import admin

# Register your models here.
from contests.models import Contest, ContestQuestion

admin.site.register(Contest)

admin.site.register(ContestQuestion)