from django.db import models
from dl2.models import User
import os
import os.path as osp
from collections import OrderedDict

# Create your models here.
class Machine(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20)
    root_path = models.CharField(max_length=200)
    cur_file = models.CharField(max_length=200)
    cur_dir = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"""
        User:{self.User}
        root_path:{self.root_path}
        cur_path:{self.cur_file}
        cur_dir:{self.cur_dir}
        """

    def get_choices(self):
        choices = dict(default=OrderedDict(), dir=OrderedDict(), file=OrderedDict())
        choices["default"]["root"] = self.root_path
        choices["default"][".."] = osp.abspath(osp.join(self.cur_dir, ".."))
        for path in sorted(os.listdir(self.cur_dir)):
            p = osp.join(self.cur_dir, path)
            if osp.isfile(p):
                choices["file"][path] = p
            else:
                choices["dir"][path] = p
        return choices

    def enter_path(self, path):
        path = osp.join(self.cur_dir, path)
        if osp.isdir(path):
            self.cur_dir = path
        else:
            self.cur_file = path
