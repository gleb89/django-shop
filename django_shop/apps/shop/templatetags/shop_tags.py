from django import template

register = template.Library()

@register.simple_tag
def product_in_cart(request, product_sku):
    in_cart = False
    if request.session.get('cart'):
        if any(d['sku'] == product_sku for d in request.session['cart']):
            in_cart = True
    return in_cart