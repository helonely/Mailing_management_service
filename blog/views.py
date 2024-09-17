from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.forms import BlogForm, BlogUpdateForm
from blog.models import Blog
from mailing.services import get_blog_from_cache


class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    extra_context = {
        'title': 'Новости',
    }

    def get_queryset(self):
        return get_blog_from_cache()


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data()

        item = Blog.objects.get(pk=self.kwargs.get('pk'))
        context_data['title'] = f"{item.title}"

        return context_data

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogCreateView(CreateView):
    model = Blog
    template_name = 'blog/blog_form.html'
    fields = ('title', 'content', 'picture', 'slug')
    success_url = reverse_lazy('blog:list')


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ['title', 'slug', 'content', 'picture', ]
    success_url = reverse_lazy('blog:list')

    def get_success_url(self):
        return reverse('blog:blog_detail', args=[self.kwargs.get('pk')])


class BlogDeleteView(DeleteView):
    model = Blog
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog:list')
