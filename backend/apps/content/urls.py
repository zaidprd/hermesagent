from django.urls import path

from . import views

app_name = "content"

urlpatterns = [
    path("projects/<int:project_pk>/keywords/", views.keyword_create, name="keyword_create"),
    path("keywords/<int:pk>/card/", views.keyword_card, name="keyword_card"),
    path("titles/<int:pk>/approve/", views.title_approve, name="title_approve"),
    path("titles/<int:pk>/reject/", views.title_reject, name="title_reject"),
    path("titles/<int:title_pk>/article/generate/", views.article_generate, name="article_generate"),
    path("articles/<int:pk>/card/", views.article_card, name="article_card"),
    path("articles/<int:pk>/publish/", views.article_publish, name="article_publish"),
    path("articles/<int:pk>/", views.article_detail, name="article_detail"),
]
