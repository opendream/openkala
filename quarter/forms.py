from django.forms import ModelForm, Form
from django.forms.fields import ChoiceField, MultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple

from quarter.models import *


class ProjectCreateForm(ModelForm):
    class Meta:
        model = Project
