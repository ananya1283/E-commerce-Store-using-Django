from django import forms

from .models import ShippingAddress


class ShippingForm(forms.ModelForm):

    class Meta:

        model=ShippingAddress

        fieds=['full_name','email','address1','address2','city','state','pincode']

        exclude=['user',]
        







