from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.http import JsonResponse

# from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Categories, Products, ProductsImages
from .forms import CheckoutForm


def products_list(request):
    products = Products.objects.filter(active=True).order_by('-updated')

    # Filters
    filter_price = request.GET.get('price')
    filter_category = request.GET.get('category')

    if filter_price and filter_price == 'asc':
        products = products.order_by('price')

    if filter_price and filter_price == 'desc':
        products = products.order_by('-price')

    if filter_category and filter_category != '':
        products = products.filter(categories__slug=filter_category)
    # END Filters

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 6)
    # paginator = Paginator(products, 1)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    # END Pagination

    context = {
        'page_title': 'Каталог товаров',
        # 'page_description': 'Описание каталога',
        'products': products,
        'categories': Categories.objects.all(),
    }
    return render(request, 'shop/products_list.html', context=context)


def product_detail(request, id):
    product = Products.objects.filter(active=True).get(id=id)
    context = {
        'page_title': product.name,
        'product': product,
        'product_images': ProductsImages.objects.filter(product=product.pk),
        'other_products': Products.objects.filter(active=True).exclude(id=product.pk).order_by('?')[:6],
    }
    return render(request, 'shop/product_detail.html', context=context)


def category_products(request, slug):
    products = Products.objects.filter(active=True, categories__slug=slug).order_by('-updated')

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 6)
    # paginator = Paginator(products, 1)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    # END Pagination

    context = {
        'page_title': Categories.objects.get(slug=slug).name,
        'products': products,
    }
    return render(request, 'shop/category_products.html', context=context)


def search_results_view(request):
    search_query = request.GET.get('q')

    if search_query:
        products = Products.objects.filter(active=True, name__icontains=search_query)
        products_count = str(products.count())

        # Pagination
        page = request.GET.get('page', 1)
        paginator = Paginator(products, 6)

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        # END Pagination

        context = {
            'page_title': 'Результаты поиска: ' + search_query,
            'page_description': 'найдено ' + products_count + ' результатов',
            'products': products,
        }
        return render(request, 'shop/serch_results.html', context=context)

    if not search_query:
        return redirect('/products/')


def cart_page(request):
    context = {
        'page_title': 'Корзина',
    }
    return render(request, 'shop/cart_page.html', context=context)


def checkout_page(request):
    form = CheckoutForm()

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data['fio'])
            # print(form.cleaned_data['zip_code'])
            # print(form.cleaned_data['address'])
            # print(form.cleaned_data['phone'])
            # print(form.cleaned_data['email'])
            # print(form.cleaned_data['message'])

            # Send Order email from template
            total_qty = total_price = 0

            # Calculate totals
            for item in request.session.get('cart'):
                total_qty += item['qty']
                total_price += item['price']

            context_data = {
                'fio': form.cleaned_data['fio'],
                'zip_code': form.cleaned_data['zip_code'],
                'address': form.cleaned_data['address'],
                'phone': form.cleaned_data['phone'],
                'email': form.cleaned_data['email'],
                'message': form.cleaned_data['message'],
                'cart_items': request.session.get('cart'),
                'total_qty': total_qty,
                'total_price': total_price,
            }

            html_body = render_to_string("email_templates/order.html", context_data)
            msg = EmailMultiAlternatives(subject='Ваш заказ', from_email='beautyroom37@mail.ru', to=['beautyroom37@mail.ru',])
            msg.attach_alternative(html_body, "text/html")
            msg.send()

            if request.session.get('cart'):
                del request.session['cart']
                request.session.modified = True
                return redirect('/cart/checkout-success/')

            return redirect('/cart/checkout/')

    context = {
        'page_title': 'Оформление заказа',
        'form': form,
    }
    return render(request, 'shop/checkout_page.html', context=context)


def checkout_success_page(request):
    context = {
        'page_title': 'Ваш заказ успешно оформлен!',
    }
    return render(request, 'shop/checkout_success_page.html', context=context)


def add_to_cart(request):
    if request.method == 'POST':
        # check if session cart not exist
        if not request.session.get('cart'):
            request.session['cart'] = list()

        data = {
            'sku': request.POST.get('product_sku'),
            'name': request.POST.get('product_name'),
            'price': float(request.POST.get('product_price').replace(',', '.')),
            'qty': int(request.POST.get('product_qty')),
        }

        product_in_cart = False

        # check if product alredy in cart
        if not any(d['sku'] == request.POST.get('product_sku') for d in request.session['cart']):
            product_in_cart = True
            request.session['cart'].append(data)
            request.session.modified = True

    # If is AJAX
    if request.is_ajax():
        return JsonResponse({'product_in_cart': product_in_cart})

    return redirect(request.POST.get('url_from'))


def cart_api(request):
    cart_session = request.session.get('cart')
    if cart_session:
        return JsonResponse(cart_session, safe=False)
    else:
        return JsonResponse({'cart_session': 'is not exist'})


def delete_empty_cart(request):
    if len(request.session['cart']) == 0:
        del request.session['cart']
        request.session.modified = True


# remove empty {} from cart list
def remove_empty_dicts_from_cart(request):
    while {} in request.session['cart']:
        request.session['cart'].remove({})
        request.session.modified = True


def update_cart(request):
    if request.method == 'POST':
        # Remove product from cart
        if request.POST.get('remove-item'):
            for item in request.session['cart']:
                if item['sku'] == request.POST.get('remove-item'):
                    item.clear()
                    request.session.modified = True

                    remove_empty_dicts_from_cart(request)
                    delete_empty_cart(request)

            # if cart has any products, redirect to /cart/ route
            if request.session.get('cart'):
                return redirect('/cart/')

            # if cart session is not exist, redirect to /products/
            if not request.session.get('cart'):
                return redirect('/products/')
        # Go to checkout page
        if request.POST.get('checkout'):
            return redirect('/cart/checkout/')


def clear_cart(request):
    if request.method == 'POST':
        if request.session.get('cart'):
            del request.session['cart']
            request.session.modified = True
    return redirect('/products/')