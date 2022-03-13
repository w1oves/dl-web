from django.db import models
from django.db.models.base import Model

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=20)
    interpreter = models.CharField(max_length=200)
    config_dir = models.CharField(max_length=200)
    work_dir = models.CharField(max_length=200)
    train_script = models.CharField(max_length=200)
    test_script = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"""
        name:{self.name}
        interpreter:{self.interpreter}
        config_dir:{self.config_dir}
        work_dir:{self.work_dir}
        train_script:{self.train_script}
        test_script:{self.test_script}
        """
