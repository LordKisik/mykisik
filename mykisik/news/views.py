from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from django.shortcuts import render, redirect, get_object_or_404

from .models import Comment, News, Category
from .forms import CommentForm, NewsForm


class HomeNews(ListView):
    paginate_by = 3
    model = News
    template_name = "news/home_news_list.html"
    context_object_name = "news"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Главная страница"
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related(
            "category"
        )


class NewsByCategry(ListView):
    paginate_by = 3
    model = News
    template_name = "news/home_news_list.html"
    context_object_name = "news"
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Категория: " + str(
            Category.objects.get(pk=self.kwargs["category_id"])
        )
        return context

    def get_queryset(self):
        return News.objects.filter(
            category_id=self.kwargs["category_id"], is_published=True
        ).select_related("category")


def news_detail(request, news_id):
    news = get_object_or_404(News, id=news_id)
    title = news.content[:30]
    form = CommentForm()
    comments = Comment.objects.filter(news_id=news_id)
    template = "news/detail_news.html"
    context = {
        "news": news,
        "title": title,
        "form": form,
        "comments": comments,
    }
    return render(request, template, context)


class AddNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = "news/add_news.html"
    success_url = reverse_lazy("home")

    # success_url = reverse_lazy('detail_news', kwargs={'pk': news.pk})
    # Пока не работает


def add_comment(request, news_id):
    news = News.objects.get(pk=news_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.news = news
        comment.save()
    return redirect("detail_news", news_id=news_id)
