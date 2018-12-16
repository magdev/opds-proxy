# -*- coding: utf-8 -*-
from django.contrib import admin
from catalog.models import Book, Author, Category, Link, FeedUuid


class LinkInline(admin.TabularInline):
    model = Link
    extra = 1

class FeedUuidAdmin(admin.ModelAdmin):
    list_display = ('feed', 'uuid')
    list_per_page = 30
    readonly_fields = ('uuid',)

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'count_books')
    search_fields = ['name']
    list_per_page = 30
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'count_books')
    search_fields = ['name']
    list_per_page = 30

class LinkAdmin(admin.ModelAdmin):
    list_display = ('url', 'format')
    search_fields = ['url']
    list_filter = ('format',)
    list_per_page = 30
    readonly_fields = ('book',)
    
class BookAdmin(admin.ModelAdmin):
    inlines = [LinkInline]
    date_hierarchy = 'updated_at'
    exclude = ('created_at',)
    filter_horizontal = ('authors', 'categories')
    list_display = ('title', 'year', 'isbn', 'updated_at', 'origin', 'google_search')
    list_editable = ('year',)
    list_filter = ('year',)
    list_per_page = 30
    readonly_fields = ('uuid', 'created_at', 'updated_at')
    search_fields = ['title', 'summary', 'description', 'isbn']
    fieldsets = (
        (None, {
            'fields': ('title', 'summary', 'description', 'authors')
        }),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': (('isbn', 'year'), ('language', 'pages'), 'categories'),
        }),
        ('Origin', {
            'classes': ('collapse',),
            'fields': ('url', 'image'),
        }),
        ('Internal Data', {
            'classes': ('collapse',),
            'fields': ('uuid', ('created_at', 'updated_at')),
        }),
    )


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(FeedUuid, FeedUuidAdmin)

