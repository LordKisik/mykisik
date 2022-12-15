from django.db import models
from django.urls import reverse


class News(models.Model):
    title = models.CharField(max_length=150, verbose_name="Наименование")
    content = models.TextField(blank=True, verbose_name="Информация")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата публикации"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновленно")
    photo = models.ImageField(
        upload_to="photos/%Y/%m/%d/", verbose_name="Фото", blank=True
    )
    is_published = models.BooleanField(
        default=True, verbose_name="Опубликованно"
    )
    category = models.ForeignKey(
        "Category", on_delete=models.PROTECT, verbose_name="Категория"
    )

    def get_absolute_url(self):
        return reverse("detail_news", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "новость"
        verbose_name_plural = "новости"
        ordering = ["-created_at"]


class Category(models.Model):
    title = models.CharField(
        max_length=150, db_index=True, verbose_name="Наименование категории"
    )
    slug = models.SlugField(
        max_length=50, unique=True, db_index=True, verbose_name="URL"
    )

    def get_absolute_url(self):
        return reverse("category", kwargs={"category_id": self.pk})

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "категорию"
        verbose_name_plural = "категории"
        ordering = ["title"]


class Comment(models.Model):
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    text = models.TextField()
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата публикации"
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "Комментарии"
