from django.urls import path, include

from apps.shop.views import (
    products_list,
    product_detail,
    category_products,
    search_results_view,
    cart_page,
    checkout_page,
    checkout_success_page,
    add_to_cart,
    update_cart,
    clear_cart,

    cart_api,
)


# app_name = 'products'

urlpatterns = [
    path('products/', include(([
        path('', products_list, name='list'),
        path('<int:id>/', product_detail, name='detail'),
    ], 'products'), namespace='products')),


    path('category/', include(([
        path('<slug:slug>/', category_products, name='slug'),
    ], 'category'), namespace='category')),


    path('search-results/', include(([
        path('', search_results_view, name='results'),
    ], 'search'), namespace='search')),


    # Cart
    path('cart/', include(([
        path('', cart_page, name='page'),
        path('checkout/', checkout_page, name='checkout'),
        path('checkout-success/', checkout_success_page, name='checkout-success'),
        path('add/', add_to_cart, name='add'),
        path('update/', update_cart, name='update'),
        path('clear-cart/', clear_cart, name='clear'),

        path('api/', cart_api, name='api'),
    ], 'cart'), namespace='cart')),
]