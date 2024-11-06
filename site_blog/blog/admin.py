from django.contrib import admin
from .models import Category, HeroImage, FAQ, Post, PostGallery, Like, Dislike



class PostGalleryInline(admin.StackedInline):
    model = PostGallery
    extra = 1


class PostAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'get_photos_for_admin']
    inlines = [PostGalleryInline]


admin.site.register(Category)
admin.site.register(HeroImage)
admin.site.register(FAQ)
admin.site.register(Post, PostAdmin)
admin.site.register(Like)
admin.site.register(Dislike)
# admin.site.register(PostGallery)
