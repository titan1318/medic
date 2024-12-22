from django import forms

from promo.models import Promo
from users.forms import StyleFormMixin


class PromoForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Promo
        fields = ('title', 'sub_title', 'description', 'image')
        