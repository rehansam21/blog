from django.contrib import admin

# Register your models here.
from .models import Posts
from .models import Demo


class PostAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'updated', 'create_date')
    search_fields = ['title', 'content']


admin.site.register(Posts, PostAdmin)


class DemoAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)
    search_fields = ['title', 'content']


admin.site.register(Demo, DemoAdmin)
