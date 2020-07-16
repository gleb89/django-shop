from django import forms


class CheckoutForm(forms.Form):
    fio      = forms.CharField(max_length=255, help_text='Укажите вашу Фамилию, Имя и Отчество')
    zip_code = forms.CharField(max_length=50, help_text="<a href=\"https://pochta.ru/post-index\" target=\"_blank\">Найти свой индекс</a>")
    address  = forms.CharField(max_length=255, help_text='Город, улица, дом, квартира')
    phone    = forms.CharField(max_length=100, help_text='Укажите в формате: +7 999 000-00-00')
    email    = forms.EmailField(max_length=200, help_text='Укажите ваш действующий email')
    message  = forms.CharField(widget=forms.Textarea,
                                max_length=1000,
                                required=False,
                                help_text='Укажите комментарий или примечание к вашему заказу')

