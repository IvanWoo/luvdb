import os
import uuid
from io import BytesIO

from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.files.base import ContentFile
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from PIL import Image

from activity_feed.models import Activity
from entity.models import Entity, Person, Role
from read.models import LanguageField
from write.models import create_mentions_notifications, handle_tags


# helpers
def rename_movie_poster(instance, filename):
    _, extension = os.path.splitext(filename)
    unique_id = uuid.uuid4()
    directory_name = (
        f"{slugify(instance.title, allow_unicode=True)}-{instance.release_date}"
    )
    new_name = f"{unique_id}{extension}"
    return os.path.join("posters", directory_name, new_name)


class Studio(Entity):
    history = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    death_date = models.DateField(blank=True, null=True)

    def __str__(self):
        if self.location:
            return f"{self.location}: {self.name}"
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100, blank=True, null=True)
    romanized_title = models.CharField(max_length=100, blank=True, null=True)
    studio = models.ManyToManyField(Studio, related_name="movies")
    persons = models.ManyToManyField(Person, through="MovieRole", related_name="movies")
    release_date = models.CharField(
        max_length=10, blank=True, null=True
    )  # YYYY or YYYY-MM or YYYY-MM-DD
    description = models.TextField(blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    poster = models.ImageField(upload_to=rename_movie_poster, null=True, blank=True)
    poster_sens = models.BooleanField(default=False, null=True, blank=True)
    box_office = models.CharField(max_length=20, blank=True, null=True)
    duration = models.CharField(max_length=10, blank=True, null=True)
    languages = LanguageField(blank=True, null=True)
    genres = models.ManyToManyField("Genre", related_name="movies", blank=True)

    # entry meta data
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="movies_created",
        on_delete=models.SET_NULL,
        null=True,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="movies_updated",
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # If the instance already exists in the database
        if self.pk:
            # Get the existing instance from the database
            old_instance = Movie.objects.get(pk=self.pk)
            # If the poster has been updated
            if old_instance.poster != self.poster:
                # Delete the old poster
                old_instance.poster.delete(save=False)

        super().save(*args, **kwargs)

        if self.poster:
            img = Image.open(self.poster.open(mode="rb"))

            if img.height > 500 or img.width > 500:
                output_size = (500, 500)
                img.thumbnail(output_size)

                # Save the image to a BytesIO object
                temp_file = BytesIO()
                img.save(temp_file, format=img.format)
                temp_file.seek(0)

                # Save the BytesIO object to the FileField
                self.poster.save(
                    self.poster.name, ContentFile(temp_file.read()), save=False
                )

            img.close()
            self.poster.close()

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("watch:movie_detail", args=[str(self.id)])


class MovieRole(models.Model):
    """
    A Role of a Person in a Movie
    """

    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="movieroles"
    )
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    alt_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.movie} - {self.person} - {self.role}"
