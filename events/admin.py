from django.contrib import admin
from .models import Event, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'city', 'category', 'is_active', 'is_featured']
    list_filter = ['city', 'category', 'is_active', 'is_featured']
    search_fields = ['name', 'venue']
    list_editable = ['is_active', 'is_featured']
    readonly_fields = ['created_at']
