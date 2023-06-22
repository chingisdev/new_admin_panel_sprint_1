from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
import uuid


# Create your models here.


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Этот параметр указывает Django, что этот класс не является представлением таблицы
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(TimeStampedMixin, UUIDMixin):
    # Первым аргументом обычно идёт человекочитаемое название поля
    name = models.CharField(_('name'), max_length=255)
    # blank=True делает поле необязательным для заполнения.
    description = models.TextField(_('description'), blank=True)

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = "content\".\"genre"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    def __str__(self):
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.TextField(_('full name'), blank=False)

    def __str__(self):
        return self.full_name

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = "content\".\"person"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')


class Filmwork(TimeStampedMixin, UUIDMixin):
    class FilmType(models.TextChoices):
        MOVIE = 'movie', _('movie')
        TV_SHOW = 'tv-show', _('tv-show')

    title = models.TextField(_('title'), blank=False)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateTimeField()
    file_path = models.FileField(_('file'), blank=True, null=True, upload_to='movies/')
    rating = models.FloatField(_('rating'), blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    type = models.TextField(_('type'), choices=FilmType.choices, default=FilmType.MOVIE)
    # Параметр upload_to указывает, в какой подпапке будут храниться загружемые файлы.
    # Базовая папка указана в файле настроек как MEDIA_ROOT
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField(Person, through='PersonFilmwork')

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = "content\".\"film_work"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = _('film')
        verbose_name_plural = _('films')

    def __str__(self):
        return self.title


class PersonFilmwork(UUIDMixin):
    film_work_id = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person_id = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.TextField(_('role'), null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"


class GenreFilmwork(UUIDMixin):
    film_work_id = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre_id = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
