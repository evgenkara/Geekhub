from django import forms
from shop.models import Product


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        quant = kwargs.pop('quant', None)
        super(CartAddProductForm, self).__init__(*args, **kwargs)
        if quant:
            quant_choices = [(i, str(i)) for i in range(1, quant['quant'] + 1)]
            self.fields['quantity'].choices = quant_choices




# class CartAddProductForm(forms.Form):
#     quantity = forms.TypedChoiceField(choices=[], coerce=int)
#     update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
#
#     def __init__(self, product, product_id, *args, **kwargs):
#         super(CartAddProductForm, self).__init__(*args, **kwargs)
#
#         obj = Product.objects.get(pk=product_id)
#         stock = obj.stock
#         quant_choices = [(i, str(i)) for i in range(1, stock+1)]
#         self.fields['quantity'].choices = quant_choices
