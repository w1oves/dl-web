from collections import OrderedDict
from django import forms
from django.forms.fields import DurationField, FileField, NullBooleanField
import os
import os.path as osp


class FileListForm(forms.Form):
    reset=forms.BooleanField(required=False,label='reset')
    def __init__(self,choices, **kwargs) -> None:
        self.reset=forms.BooleanField(required=False,label='reset')
        self.parent=forms.BooleanField(required=False,label='..')
        choices.pop('reset')
        choices.pop('..')
        for choice,label in choices.items():
            setattr(self,choice,forms.BooleanField(required=False,label=label))
        super().__init__(**kwargs)
