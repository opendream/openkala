from django.forms import ModelForm
from openkala.quarter.models import *

class ProjectCreateForm(ModelForm):
    class Meta:
        model = Project
    
