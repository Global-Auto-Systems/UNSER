from django.contrib import admin
from .models import *
from django.db import models
admin.site.register( Service )
admin.site.register( ServiceProvider )
admin.site.register( Status )
admin.site.register( Classe )
admin.site.register( Subject )
admin.site.register( LockdownPackage )
admin.site.register( DownloadResource )
admin.site.register( Communication )