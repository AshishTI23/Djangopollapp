from django.contrib import admin
from .models import MakePoll, Vote
# Register your models here.
admin.site.register(MakePoll)
admin.site.register(Vote)
