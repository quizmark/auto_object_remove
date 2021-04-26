from django.contrib import admin
from blog.models import Post
class PostAdmin(admin.ModelAdmin):
    list_display=['title','body','date']
    list_filter=['date']
    search_fields=['title']
admin.site.register(Post,PostAdmin)
# Register your models here.
