from django.urls import include, path
from rest_framework import routers
from . import views


app_name = 'movies'

router = routers.DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'movies', views.MovieViewSet)

urlpatterns = [
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
    path('', views.movie_list, name='movie_list'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('privacy/', views.privacy, name='privacy'),
    path('watchlist-add/<int:movie_id>', views.watchlist_add, name='watchlist_add'),
    path('watchlist-remove/<int:movie_id>', views.watchlist_remove, name='watchlist_remove'),
    path('<category_slug>/',
         views.movie_category,
         name='movie_list_by_category'),
    path('<int:id>/<slug>/', views.movie_detail,
         name='movie_detail'),
    path('api/', include(router.urls), name='api'),
]
