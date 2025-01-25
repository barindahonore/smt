from django.contrib import admin

from core.models import *
from .models import *

# Register your models here.

admin.site.register(Isibo)
admin.site.register(Citizens)
admin.site.register(Messages)
admin.site.register(Family)
admin.site.register(Events)
admin.site.register(Files)
admin.site.register(Post)
admin.site.register(Abakandida)