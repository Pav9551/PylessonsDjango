from django import forms
MARKETS = [
    ('lenta-super', 'Лента супермаркет'),
    ('5ka', 'Пятерочка'),
    ('perekrestok', 'Перекресток'),
]
class ContactForm(forms.Form):
    name = forms.CharField(label='Название')
    message = forms.CharField(label='Сообщение')
    email = forms.EmailField(label='email')
class RequestForm(forms.Form):
    name = forms.CharField(label='Название')
    message = forms.CharField(label='Сообщение')
    email = forms.EmailField(label='email')
    favorite_markets = forms.MultipleChoiceField(
        label='Магазин',
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={"checked": ""}),
        choices=MARKETS,
    )


