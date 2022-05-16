from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Competition(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    pub_date = models.DateTimeField("published at", auto_now_add=True)

    def get_absolute_url(self):
        return reverse("leaderboard", args=(self.id,))


def data_file_path(instance: "Phase", filename):
    return f"datasets/{instance.competition_id}/{instance.id}/data"


def labels_file_path(instance: "Phase", filename):
    return f"datasets/{instance.competition_id}/{instance.id}/labels"


class Phase(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    competition = models.ForeignKey(
        Competition, on_delete=models.CASCADE, related_name="phases"
    )
    data_file = models.FileField(
        null=True,
        blank=True,
        upload_to=data_file_path,
        storage=settings.COMPETITIONS_UPLOADS_STORAGE,
        help_text="file containing the features",
    )
    data_file_name = models.CharField(max_length=256, null=True, blank=True)
    labels_file = models.FileField(
        null=True,
        blank=True,
        upload_to=labels_file_path,
        storage=settings.COMPETITIONS_UPLOADS_STORAGE,
        help_text="file containing the labels",
    )
    labels_file_name = models.CharField(max_length=256, null=True, blank=True)


class Submission(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=32, decimal_places=16, null=True)


class Run(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    status = models.CharField(
        max_length=32,
        help_text='status of the run, e.g., "PENDING", "SUCCESS", "FAILED".',
    )
    score = models.DecimalField(max_digits=32, decimal_places=16, null=True)


# class Score(models.Model):
#     run = models.ForeignKey(Run, on_delete=models.CASCADE)
#     name = models.CharField(max_length=128)
#     value = models.DecimalField(max_digits=32, decimal_places=16)
