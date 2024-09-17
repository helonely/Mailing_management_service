from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView
from config import settings

app_name = BlogConfig.name

urlpatterns = [
    path('news/', BlogListView.as_view(), name='blog_list'),
    path('news/<int:pk>', cache_page(300)(BlogDetailView.as_view()), name='blog_detail'),
    path('create/', BlogCreateView.as_view(), name='blog_create'),
    path('edit/<int:pk>', BlogUpdateView.as_view(), name='blog_update'),
    path('delete/<int:pk>', BlogDeleteView.as_view(), name='blog_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

