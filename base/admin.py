from django.contrib import admin
from buddyStudy.utils import set_app_models_to_admin
from .models import *

# Register your models here.
set_app_models_to_admin('base')
