import uuid
from django.db import models
from django.utils import timezone

from apps.common.managers import IsDeletedManager, GetOrNoneManager


class BaseModel(models.Model):
    """
    A base model class that includes common fields and methods for all models.

    Attributes:
        id (UUIDField): Unique identifier for the model instance.
        created_at (DateTimeField): Timestamp when the instance was created.
        updated_at (DateTimeField): Timestamp when the instance was last updated.
    """

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = GetOrNoneManager()

    class Meta:
        abstract = True


class IsDeletedModel(BaseModel):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-id']
        abstract = True

    objects = IsDeletedManager()

    def delete(self, *args, **kwargs):
        # Мягкое удаление is_deleted=True
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at"])

    def hard_delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)


from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Content(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=False, verbose_name='URL-идентификатор')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    metadata = models.JSONField(default=dict, blank=True, null=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:250]
            original_slug = self.slug
            counter = 1
            while Article.objects.filter(slug=self.slug).exists():
                self.slug = f'{original_slug}={counter}'
                counter += 1

        if self.text:
            self.word_count = len(self.text.strip().split())
        else:
            self.word_count = 0

        super().save(*args, **kwargs)


class Article(Content):
    text = models.TextField(blank=False)
    word_count = models.IntegerField(blank=True)


class Video(Content):
    video_url = models.URLField()
    duration = models.DurationField()

class Image(Content):
    image = models.ImageField(upload_to='images/')
    dimensions = models.CharField(max_length=20, blank=True)







