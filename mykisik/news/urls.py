from django.urls import path

# from django.views.decorators.cache import cache_page
from .views import HomeNews, NewsByCategry, AddNews, add_comment, news_detail

urlpatterns = [
    path("", HomeNews.as_view(), name="home"),
    path(
        "category/<int:category_id>/", NewsByCategry.as_view(), name="category"
    ),
    path("news/<int:news_id>/", news_detail, name="detail_news"),
    path("news/add_news/", AddNews.as_view(), name="add_news"),
    path("news/<int:news_id>/comment/", add_comment, name="add_comment"),
]
