from django.db import models

# Create your models here.

import socket
import os
import os.path as osp
import sh
from . import ip_address


class Port(models.Model):
    port = models.IntegerField()
    available = models.BooleanField()

    @staticmethod
    def port_pop() -> int:
        """
        从数据库获取一个可用端口
        """
        Port._collect_port()
        port = Port.objects.filter(available=True).first()
        port.available = False
        port.save()
        if Port._net_is_used(port):
            return Port.port_pop()
        else:
            return port.port

    @staticmethod
    def port_push(port: int):
        """
        将使用过的端口添加进数据库
        """
        try:
            pid = sh.lsof(f"-i:{port}", "-t")
            os.system(f"kill -9 {pid}")
        except:
            pass
        port = Port.objects.get(port=port)
        port.available = True
        port.save()

    @staticmethod
    def _net_is_used(port: int) -> bool:
        """
        判断端口port是否在使用中
        """
        try:
            str(sh.lsof(f"-i:{port}"))
            return True
        except:
            return False
        # 错误的判断方式
        # ip = ip_address
        # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # try:
        #     s.connect((ip, port))
        #     s.shutdown(2)
        #     return True
        # except:
        #     return False

    @staticmethod
    def _collect_port():
        """
        从[9000,10000)的范围内获取可用端口
        """
        if Port.objects.all().count() < 100:
            for p in range(9000, 10000):
                port = Port(port=p, available=not Port._net_is_used(p))
                port.save()
