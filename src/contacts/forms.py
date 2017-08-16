from django import forms


class ContactListParamsForm(forms.Form):
    """
    Validates HTTP parameters of contact list endpoint
    """
    image_width = forms.IntegerField(label='image width', min_value=0, required=False)
    image_height = forms.IntegerField(label='image width', min_value=0, required=False)
