from django import forms


class ContactListParamsForm(forms.Form):
    image_width = forms.IntegerField(label='image width', min_value=0, required=False)
    image_height = forms.IntegerField(label='image width', min_value=0, required=False)
