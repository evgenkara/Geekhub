import random

from .forms import ContactForm, CommentForm
from .models import Category, Movie
from .serializers import MovieSerializer, CategorySerializer

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from rest_framework import permissions
from rest_framework import viewsets
from .recommendations import user_recommendations


def movie_list(request):
    """Get required objects and render main page"""

    recommendations = soon = rand_soon = None
    categories = Category.objects.all()
    movies_all = Movie.objects.all()
    movies = movies_all.order_by('-id')[:20]
    soon_category = get_object_or_404(Category, slug='coming-soon')
    category_ua = get_object_or_404(Category, slug='filmi-ukrayinskogo-virobnictva')
    movies_ua = None
    # random coming soon film for banner
    if soon_category:
        soon = movies_all.filter(category=soon_category).order_by('?')[:20]
        rand_soon = random.choice(soon)
    # show ukrainian films
    if category_ua:
        movies_ua = movies_all.filter(category=category_ua).order_by('-id')[:20]
    # user recommendations
    if request.user.is_authenticated:
        recommendations = user_recommendations(request.user)
    return render(request,
                  'movies/movie/list.html',
                  {'categories': categories,
                   'movies': movies,
                   'soon': soon,
                   'rand_soon': rand_soon,
                   'movies_ua': movies_ua,
                   'recommendations': recommendations})


def movie_category(request, category_slug=None):
    """Movies by requested category."""

    category = None
    categories = Category.objects.all()
    movies_all = Movie.objects.all()
    if category_slug:
        if category_slug != 'all':
            category = get_object_or_404(Category, slug=category_slug)
            movies_all = movies_all.filter(category=category)

    paginator = Paginator(movies_all, 12)
    page_number = request.GET.get('page')
    movies = paginator.get_page(page_number)

    return render(request,
                  'movies/movie/category.html',
                  {'categories': categories,
                   'category': category,
                   'movies': movies})


def movie_detail(request, id, slug):
    """Movie page."""

    movie = get_object_or_404(Movie,
                              id=id,
                              slug=slug)
    comments = movie.comments.filter(active=True).order_by('-created_on')
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            new_comment.name = request.user.username
            new_comment.movie = movie
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'movies/movie/detail.html',
                  {'movie': movie,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form})


def contact(request):
    """Contact form in footer."""

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = request.POST.get('user_name', '')
            message = request.POST.get('question', '')
            from_email = request.POST.get('user_email', '')
            # send contact message(user question etc) to company email
            if name and message and from_email:
                try:
                    send_mail(f'Contact message from {from_email}', f'User name: {name}\nMessage:\n{message}',
                              from_email, [settings.EMAIL_HOST_USER])
                    messages.success(request, 'Дякуємо за повідомлення')
                # prevent header injection
                except BadHeaderError:
                    messages.error(request, 'Знайдено недійсний заголовок.')
            else:
                messages.error(request, 'Переконайтеся, що всі поля введені правильно.')
        else:
            messages.error(request, 'Переконайтеся, що всі поля введені правильно.')
            render(request, 'movies/footer/contact.html')
    else:
        form = ContactForm()
    return render(request, 'movies/footer/contact.html', {'form': form})


@login_required()
def watchlist_add(request, movie_id):
    """Add selected movie to watchlist."""

    movie = get_object_or_404(Movie, pk=movie_id)
    watchlist = request.user.profile.watchlist.all()
    if movie in watchlist:
        messages.add_message(request, messages.ERROR, "Фільм вже у вотчлісті.")
    else:
        request.user.profile.watchlist.add(movie)
        messages.add_message(request, messages.SUCCESS, "Фільм додано у вотчліст")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required()
def watchlist_remove(request, movie_id):
    """Remove item from user watchlist."""

    movie = get_object_or_404(Movie, pk=movie_id)
    watchlist = request.user.profile.watchlist.all()
    if movie in watchlist:
        request.user.profile.watchlist.remove(movie)
        messages.add_message(request, messages.SUCCESS, f"Успішно видалено з вотчліста")
    else:
        messages.add_message(request, messages.ERROR, f"Фільм відсутній у вашому вотчлісті")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def about(request):
    return render(request, 'movies/footer/about.html')


def privacy(request):
    return render(request, 'movies/footer/privacy.html')


class SearchResultsView(ListView):
    """Movie search."""

    paginate_by = 8
    model = Movie
    template_name = 'movies/movie/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = []
        if query:
            object_list = Movie.objects.filter(Q(name__icontains=query))
        return object_list


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('-id')
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all().order_by('-id')
    serializer_class = MovieSerializer
    permission_classes = [IsAdminOrReadOnly]
