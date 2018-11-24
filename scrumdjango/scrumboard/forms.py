from django.forms import (
    ModelForm,
    TextInput,
    NumberInput,
    DateInput,
    RadioSelect,
    SelectDateWidget,
    Select,
    ValidationError,
)
from scrumboard.models import Sprint, Task


class SprintForm(ModelForm):
    class Meta:
        model = Sprint
        fields = '__all__'
        widgets = {
            'number': NumberInput(attrs={'class': 'form-control'}),
            'date_from': DateInput(
                attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}
            ),
            'date_to': DateInput(
                attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''

    def clean(self):
        cleaned_data = super().clean()

        # Exclude selected sprint when calculating date overlap
        date_overlap_start = (
            Sprint.objects.filter(
                date_from__gte=cleaned_data.get('date_from'),
                date_from__lte=cleaned_data.get('date_to'),
            )
            .exclude(pk=self.instance.id)
            .count()
        )

        date_overlap_end = (
            Sprint.objects.filter(
                date_to__gte=cleaned_data.get('date_from'),
                date_to__lte=cleaned_data.get('date_to'),
            )
            .exclude(pk=self.instance.id)
            .count()
        )

        dates_overlap = date_overlap_start > 0 or date_overlap_end > 0

        if dates_overlap:
            self.add_error(
                'date_to', 'The selected dates overlap with an existing sprint.'
            )

        return cleaned_data


class TaskForm(ModelForm):
    class Meta:
        model = Task
        exclude = ['sprint']
        widgets = {
            'user': Select(attrs={'class': 'form-control'}),
            'text': TextInput(attrs={'class': 'form-control'}),
            'color': Select(attrs={'class': 'form-control'}),
            'points': NumberInput(attrs={'class': 'form-control numeric'}),
            'progress': Select(attrs={'class': 'form-control'}),
        }
        help_texts = {'text': 'What needs to be done?', 'points': '1, 2, 3, 5, 8, 13'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
