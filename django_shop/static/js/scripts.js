function csrf() {
    // Django AJAX https://medium.com/@a01701414/how-to-apply-ajax-with-django-2-1-8e9a4943f73
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader('X-CSRFToken', $('input[name="csrfmiddlewaretoken"]').val());
            }
        }
    })
}


function cartLinkMainNav() {
    $.getJSON('/cart/api/', (data) => {
        let i = 0

        if (data['cart_session'] != "is not exist") {
            $.each(data, (index, val) => {
                i += val['qty']
            })

            $('#cart-link_main-nav, #cart-link_xs').attr('href', '/cart/').removeAttr('style')
            $('#cart-link_main-nav .badge, #cart-link_xs .badge').removeClass('badge-secondary').addClass('badge-warning').empty().html(i)
        } else {
            $('#cart-link_main-nav, #cart-link_xs').attr('href', '').css('cursor', 'default')
            $('#cart-link_main-nav .badge, #cart-link_xs .badge').removeClass('badge-warning').addClass('badge-secondary').empty().html(i)
        }
    })
}


function addToCart() {
    $('form.add-to-cart-form').each((index, el) => {
        $(el).on('submit', (e) => {
            e.preventDefault()

            const form_action_url = $(el).attr('action')

            const product_sku   = $(el).find('input[name="product_sku"]').val()
            const product_name  = $(el).find('input[name="product_name"]').val()
            const product_price = $(el).find('input[name="product_price"]').val()
            const product_qty   = $(el).find('input[name="product_qty"]').val()

            $.ajax({
                url: form_action_url,
                type: "POST",
                dataType: "json",
                data: {
                    product_sku: product_sku,
                    product_name: product_name,
                    product_price: product_price,
                    product_qty: product_qty
                },
                success: (data) => {
                    // console.log(data)

                    if (data['product_in_cart'] == true) {
                        $(el).find('.in-cart-wrap').empty()
                        $(el).find('.in-cart-wrap').html(
                            '<button class="alredy-in-cart btn btn-secondary" disabled style="cursor: default;">' +
                                '<i class="fas fa-check"></i> Товар в корзине' +
                            '</button>')

                        cartLinkMainNav()
                    }
                }
            })
        })
    })
}


function cartAPI() {
    $('form.add-to-cart-form').each((index, el) => {
        const product_sku = $(el).find('input[name="product_sku"]').val()
        // console.log(product_sku)

        $(el).find('.in-cart-wrap').html(
            '<button type="submit" class="yet-not-in-cart btn btn-success">' +
                '<i class="fas fa-cart-plus"></i> В корзину' +
            '</button>')

        $.getJSON('/cart/api/', (data) => {
            // console.log(data)

            if (data['cart_session'] != "is not exist") {
                $.each(data, (index, val) => {
                    // console.log(index + ' ' + val['sku'])

                    if (product_sku == val['sku']) {
                        $(el).find('.in-cart-wrap').empty()
                        $(el).find('.in-cart-wrap').html(
                            '<button class="alredy-in-cart btn btn-secondary" disabled style="cursor: default;">' +
                                '<i class="fas fa-check"></i> Товар в корзине' +
                            '</button>')
                    }
                })
            }
        })
    })
}


$(document).ready(() => {
    cartLinkMainNav()
    cartAPI()

    csrf()
    addToCart()
})