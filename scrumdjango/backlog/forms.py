from django.forms import ModelForm, TextInput, NumberInput
from backlog.models import Item


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['text', 'points']
        help_texts = {
            'text': 'What needs to be done?',
            'points': '1, 2, 3, 5, 8, 13, 21, 34...',
        }

        widgets = {
            'text': TextInput(attrs={'class': 'form-control'}),
            'points': NumberInput(attrs={'class': 'form-control'}),
        }
