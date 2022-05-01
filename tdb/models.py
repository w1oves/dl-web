from typing import List
from django.db import models
from dl2.models import User
import sh
import os
import os.path as osp
from configs import cache_root, ip_address
from configs.models import Port
import socket
import shutil
from runner.models import TrainRunner, TestRunner

# Create your models here.
class TDB(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    TrainRunner = models.ForeignKey(TrainRunner, on_delete=models.CASCADE, null=True)
    TestRunner = models.ForeignKey(TestRunner, on_delete=models.CASCADE, null=True)
    port = models.IntegerField()
    pid = models.IntegerField()
    name = models.CharField(max_length=200)
    link = models.URLField()
    cache_dir = models.CharField(max_length=200)

    def delete(self, using=False, keep_parents=False):
        print('Delete tensorboard',self.port)
        os.system(f"kill -9 {self.pid}")
        shutil.rmtree(self.cache_dir)
        Port.port_push(self.port)
        return super().delete(using=using, keep_parents=keep_parents)

    # def __str__(self) -> str:
    #     return f"{self.User.name,self.TrainRunner,self.TestRunner}:{self.port}"


def create_tdb(parent: models.Model, paths: List[str]) -> TDB:
    if not osp.isdir(cache_root):
        os.mkdir(cache_root)
    port = Port.port_pop()
    cache_dir = osp.join(cache_root, str(port))
    if not osp.isdir(cache_dir):
        os.mkdir(cache_dir)
    else:
        raise RuntimeError("重复的tensorboard端口")
    name = "<br>".join(osp.basename(p) for p in paths)
    link = f"{ip_address}:{port}"
    for path in paths:
        sh.ln("-s", path, osp.join(cache_dir, osp.basename(path)))
    p = sh.tensorboard(
        f"--logdir={cache_dir}",
        "--bind_all",
        "--samples_per_plugin=images=1000",
        f"--port={port}",
        _bg=True,
    )
    tdb = parent.tdb_set.create(
        port=port, pid=p.pid, name=name, link=link, cache_dir=cache_dir
    )
    tdb.save()
    return tdb


def close_tdb(user, port):
    t = user.tdb_set.get(port=port)
    t.delete()


def close_all_tdb(user):
    for t in user.tdb_set.all():
        t.delete()
