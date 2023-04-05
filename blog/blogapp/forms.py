from django import forms
from .models import Good, Post_for_Coincidence, Coincidence
MARKETS = [
    ('lenta-super', 'Лента супермаркет'),
    ('5ka', 'Пятерочка'),
    ('perekrestok', 'Перекресток'),
]
CITIES = [
    ('moskva', 'Москва'),
    #('novosibirsk', 'Новосибирск'),
    ('sankt-peterburg', 'Санкт-Петербург'),
    ('samara', 'Самара'),
    ('ekaterinburg', 'Екатеринбург'),
]

class ContactForm(forms.Form):
    name = forms.CharField(label='Название')
    message = forms.CharField(label='Сообщение')
    email = forms.EmailField(label='email')
class RequestForm(forms.Form):

    favorite_markets = forms.MultipleChoiceField(
        label='Магазин:',
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={"checked": ""}),
        choices=MARKETS,
    )
    favorite_cities = forms.ChoiceField(
        label='Город:',
        required=False,
        widget=forms.RadioSelect(),
        choices=CITIES,
        initial='moskva'
    )

class CreateForm(forms.Form):
    class Meta:
        model = Good
        #fields = '__all__'
        # fields = ('name', 'category')
        exclude = ('user',)
class PostForm(forms.ModelForm):
    #сoincid = forms.ModelMultipleChoiceField(queryset=Coincidence.objects.all(),
                                         #widget=forms.CheckboxSelectMultiple())
    class Meta:
        model = Post_for_Coincidence
        #fields= '__all__'
        exclude = ('user',)

'''class PostForm(forms.ModelForm):
    name = forms.CharField(label='Название',
                           widget=forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control'}))

    # Чекбоксы
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(),
                                          widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Post
        fields = '__all__'
        # fields = ('name', 'category')
        #exclude = ('user',)'''


