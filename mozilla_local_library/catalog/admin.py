from django.contrib import admin
from .models import Author, Book, BookInstance, Genre

# Register your models here.
# admin.site.register(Author)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_of_birth', 'date_of_death')
    fields = ('name', ('date_of_birth', 'date_of_death'))


admin.site.register(Author, AuthorAdmin)
# admin.site.register(Book)
# admin.site.register(Genre)


class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra: 0


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')

    inlines = [BookInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')

    list_display = ('id', 'book', 'status', 'due_back')

    fieldsets = (
        (None, {'fields': ('book', 'imprint', 'id')}),
        ('Availability', {'fields': [('status', 'due_back')]})
    )
