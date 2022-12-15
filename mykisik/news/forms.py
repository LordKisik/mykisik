from django import forms
from django.core.exceptions import ValidationError
import re
from captcha.fields import CaptchaField

from .models import Comment, News


class NewsForm(forms.ModelForm):
    """При создании или редактировании поста в поле группы, при отсутствии
    выбора, содержит сообщение -- Группа не выбрана --"""

    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].empty_label = "-- Категория не выбрана --"

    class Meta:
        model = News
        fields = ["title", "content", "is_published", "photo", "category"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(
                attrs={"class": "form-control", "rows": 5}
            ),
            "photo": forms.FileInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
        }

    def clean_title(self):
        title = self.cleaned_data["title"]
        if re.match(r"\d", title):
            raise ValidationError("Название не должно начинаться с цифры")
        elif len(title) > 100:
            raise ValidationError("Длина превышает 100 символов")
        return title


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        labels = {"text": "Текст комментария"}
        help_texts = {"text": "Введите текст комментария"}
