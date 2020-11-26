def cart_qty(request):
    qty = 0
    if request.session.get('cart'):
        for item in request.session['cart']:
            qty += item['qty']
    return {'cart_qty': qty}


def cart_total(request):
    cart_total_qty = 0
    cart_total_price = 0

    if request.session.get('cart'):
        for item in request.session['cart']:
            cart_total_qty += item['qty']
            cart_total_price += item['price']

    return {
        'cart_total_qty': cart_total_qty,
        'cart_total_price': cart_total_price,
    }