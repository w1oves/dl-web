from django.forms import ModelForm
from dl2.models import User
import os.path as osp


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = "__all__"

    def is_valid(self) -> bool:
        result = super().is_valid()
        if not result:
            return False
        obj = self.cleaned_data
        possible_files = [
            obj["interpreter"],
            obj["train_script"],
            obj["test_script"],
        ]
        possible_dirs = [obj["work_dir"], obj["config_dir"]]
        for file in possible_files:
            if not osp.isfile(file):
                return False
        for dir in possible_dirs:
            if not osp.isdir(dir):
                return False
        return True
