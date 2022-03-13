from django.contrib import admin
from .models import User
from filelist.models import Machine
from tdb.models import TDB
from runner.models import TestRunner, TrainRunner

admin.site.register(User)
admin.site.register(Machine)
admin.site.register(TDB)
admin.site.register(TrainRunner)
admin.site.register(TestRunner)
