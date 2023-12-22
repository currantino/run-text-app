from django import forms


class MessageForVideoForm(forms.Form):
    message = forms.CharField(label='Message', initial='Hello, World!', required=True, max_length=30)
