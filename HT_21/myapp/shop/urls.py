from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'categories', views.CategoryViewSet)

app_name = 'shop'
urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('api/', include(router.urls)),
    path('', views.product_list, name='product_list'),
    path('<category_slug>/',
         views.product_list,
         name='product_list_by_category'),
    path('<int:id>/<slug>/', views.product_detail,
         name='product_detail'),
    path('product/<int:pk>/edit/', views.ProductUpdate.as_view(), name='product_edit'),
    path('product/<int:pk>/delete/', views.ProductDelete.as_view(), name='product_delete'),
]
