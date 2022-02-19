from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import classonlymethod
from django.views.generic.edit import UpdateView, DeleteView
from functools import update_wrapper
from .forms import LoginForm
from .models import Category, Product
from cart.forms import CartAddProductForm
from .serializers import CategorySerializer, ProductSerializer
from rest_framework import permissions
from rest_framework import viewsets


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            user = authenticate(username=form_data['username'], password=form_data['password'])
            if user:
                if user.is_active:
                    login(request, user)
                    return product_list(request)
            else:
                messages.error(request, 'username or password not correct')
                render(request, 'shop/product/login.html')
    else:
        form = LoginForm()
    return render(request, 'shop/product/login.html', {'form': form})


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm(quant={'quant': product.stock})
    return render(request, 'shop/product/detail.html',
                  {'product': product, 'cart_product_form': cart_product_form})


def check_admin(user):
    return user.is_authenticated and user.is_superuser


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return check_admin(request.user)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class ProductUpdate(UpdateView):
    model = Product
    template_name = 'shop/product/product_edit.html'
    fields = ['name', 'description', 'price', 'stock']

    @classonlymethod
    def as_view(cls, **initkwargs):
        """Main entry point for a request-response process."""
        for key in initkwargs:
            if key in cls.http_method_names:
                raise TypeError("You tried to pass in the %s method name as a "
                                "keyword argument to %s(). Don't do that."
                                % (key, cls.__name__))
            if not hasattr(cls, key):
                raise TypeError("%s() received an invalid keyword %r. as_view "
                                "only accepts arguments that are already "
                                "attributes of the class." % (cls.__name__, key))

        def view(request, *args, **kwargs):
            if check_admin(request.user):
                self = cls(**initkwargs)
                if hasattr(self, 'get') and not hasattr(self, 'head'):
                    self.head = self.get
                self.request = request
                self.args = args
                self.kwargs = kwargs
                return self.dispatch(request, *args, **kwargs)
            else:
                messages.error(request, "Can't access the page. Only for admin")
                return product_list(request)

        view.view_class = cls
        view.view_initkwargs = initkwargs
        # take name and docstring from class
        update_wrapper(view, cls, updated=())
        # and possible attributes set by decorators
        # like csrf_exempt from dispatch
        update_wrapper(view, cls.dispatch, assigned=())
        return view


class ProductDelete(DeleteView):
    model = Product
    template_name = 'shop/product/product_delete.html'
    success_url = reverse_lazy("shop:product_list")

    @classonlymethod
    def as_view(cls, **initkwargs):
        """Main entry point for a request-response process."""
        for key in initkwargs:
            if key in cls.http_method_names:
                raise TypeError("You tried to pass in the %s method name as a "
                                "keyword argument to %s(). Don't do that."
                                % (key, cls.__name__))
            if not hasattr(cls, key):
                raise TypeError("%s() received an invalid keyword %r. as_view "
                                "only accepts arguments that are already "
                                "attributes of the class." % (cls.__name__, key))

        def view(request, *args, **kwargs):
            if check_admin(request.user):
                self = cls(**initkwargs)
                if hasattr(self, 'get') and not hasattr(self, 'head'):
                    self.head = self.get
                self.setup(request, *args, **kwargs)
                if not hasattr(self, 'request'):
                    raise AttributeError(
                        "%s instance has no 'request' attribute. Did you override "
                        "setup() and forget to call super()?" % cls.__name__
                    )
                return self.dispatch(request, *args, **kwargs)
            else:
                messages.error(request, "Can't access the page. Only for admin")
                return product_list(request)

        view.view_class = cls
        view.view_initkwargs = initkwargs
        # take name and docstring from class
        update_wrapper(view, cls, updated=())
        # and possible attributes set by decorators
        # like csrf_exempt from dispatch
        update_wrapper(view, cls.dispatch, assigned=())
        return view
