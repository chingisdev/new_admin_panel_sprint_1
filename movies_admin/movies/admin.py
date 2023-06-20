from django.contrib import admin
from .models import Genre, Filmwork, GenreFilmwork, PersonFilmwork, Person
# Register your models here.


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ('name', 'description',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ('full_name',)


@admin.register(Filmwork)
class FilmWorkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline,)

    # Отображение полей в списке
    list_display = ('title', 'type', 'creation_date', 'rating',)

    # Фильтрация в списке
    list_filter = ('type', 'genres', )

    search_fields = ('title', 'description',)
