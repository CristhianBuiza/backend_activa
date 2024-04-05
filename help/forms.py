from dal import autocomplete
from django import forms
from django.contrib.auth.models import User
from help.models import RequestAttention

class RequestAttentionForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url='user-autocomplete')  # Usa la URL definida antes
    )

    class Meta:
        model = RequestAttention
        fields = ('__all__')