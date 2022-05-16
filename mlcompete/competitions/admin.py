from django.contrib import admin

from mlcompete.competitions.models import Competition, Run, Submission

admin.site.register(Competition)
admin.site.register(Submission)
admin.site.register(Run)
