from django.forms import ModelForm
from quarter.models import *

class ProjectCreateForm(ModelForm):
    class Meta:
        model = Project
