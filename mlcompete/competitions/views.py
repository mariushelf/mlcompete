from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView
from django_tables2 import SingleTableMixin, SingleTableView

from mlcompete.competitions.models import Competition, Phase, Submission
from mlcompete.competitions.tables import (
    CompetitionsTable,
    LeaderboardTable,
    UserSubmissionsTable,
)
from mlcompete.competitions.validators import SubmissionValidator


def index(request):
    return HttpResponse("Hello Competitor!")


class CompetitionIndexView(SingleTableView):
    template_name = "competitions/competition_list.html"
    table_class = CompetitionsTable

    def get_queryset(self):
        return Competition.objects.order_by("-pub_date").all()


class LeaderBoardView(SingleTableView):
    template_name = "competitions/leaderboard.html"
    table_class = LeaderboardTable

    def get_queryset(self):
        phase_id = self.kwargs.get("phase")
        if phase_id is None:
            try:
                phase_id = (
                    Competition.objects.get(pk=self.kwargs["competition"])
                    .phases.all()[0]
                    .id
                )
            except IndexError:
                phase_id = None

        if phase_id:
            return (
                Submission.objects.filter(
                    competition_id=self.kwargs["competition"], runs__phase_id=phase_id
                )
                .annotate(score=Max("runs__score"))  # TODO filter by phase
                .order_by("-score")
                .all()
            )
        else:
            return []

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        competition_id = self.kwargs["competition"]
        competition = get_object_or_404(Competition, pk=competition_id)
        context["competition"] = competition

        phase_id = self.kwargs.get("phase")
        if phase_id is None:
            try:
                phase = competition.phases.all()[0]
            except IndexError:
                phase = None
        else:
            phase = get_object_or_404(Phase, pk=phase_id)
        context["phase"] = phase

        return context


# @login_required
# def make_submission(request, competition: int):
#     print(request.user)
#     c = Competition.objects.get(pk=competition)
#     return render(
#         request, "competitions/submission_form.html", context={"competition": c}
#     )


class UserProfile(
    SingleTableMixin,
    DetailView,
):
    template_name = "competitions/user_detail.html"
    model = get_user_model()
    table_class = UserSubmissionsTable
    context_table_name = "submissions"

    def get_table_data(self, **kwargs):
        submissions = (
            Submission.objects.filter(user=self.request.user)
            .order_by("-timestamp")
            .all()
        )
        return submissions


class CompetitionCreate(LoginRequiredMixin, CreateView):
    model = Competition
    fields = ["name", "description"]


class CompetitionUpdate(UpdateView):
    fields = ["name", "description"]
    model = Competition


class CompetitionManage(DetailView):
    model = Competition
    template_name = "competitions/competition_manage.html"


class PhaseEditMixin:
    model = Phase
    fields = ["name", "description"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["competition"] = Competition.objects.get(pk=self.kwargs["competition"])
        return context

    def get_success_url(self):
        return reverse("competition_manage", kwargs={"pk": self.kwargs["competition"]})

    def form_valid(self, form):
        competition = get_object_or_404(Competition, pk=self.kwargs["competition"])
        form.instance.competition = competition
        return super().form_valid(form)


class PhaseCreate(LoginRequiredMixin, PhaseEditMixin, CreateView):
    pass


class PhaseUpdate(LoginRequiredMixin, PhaseEditMixin, UpdateView):
    pass


class SubmissionCreate(LoginRequiredMixin, CreateView):
    model = Submission
    fields = ["label", "script_file"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["competition"] = Competition.objects.get(pk=self.kwargs["competition"])
        return context

    def form_valid(self, form):
        f = form.files["script_file"]
        form.instance.script_file_name = f.name
        form.instance.user = self.request.user
        form.instance.competition_id = self.kwargs["competition"]
        competition = get_object_or_404(Competition, pk=form.instance.competition_id)
        form.instance.save()
        for phase in competition.phases.all():
            validator = SubmissionValidator(form.instance, phase)
            validator.validate()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "competition", kwargs={"competition": self.object.competition_id}
        )


class PhaseUploadData(LoginRequiredMixin, UpdateView):
    model = Phase
    fields = ["data_file", "labels_file"]
    template_name_suffix = "_upload_data_form"

    def form_valid(self, form):
        if f := form.files.get("data_file"):
            self.object.data_file_name = f.name
        if f := form.files.get("labels_file"):
            self.object.labels_file_name = f.name
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("competition_manage", kwargs={"pk": self.object.competition_id})


@login_required
def phase_download_data(request, competition: int, phase: int, filename: str):
    phase_obj = get_object_or_404(Phase, pk=phase)

    if "data" in filename:
        file = phase_obj.data_file
        orig_filename = phase_obj.data_file_name
    elif "labels" in filename:
        file = phase_obj.labels_file
        orig_filename = phase_obj.labels_file_name
    else:
        return HttpResponseNotFound()
    if file:
        response = HttpResponse(file)
        response["Content-Disposition"] = "attachment; filename=%s" % orig_filename
        return response
    else:
        return HttpResponseNotFound()


class SubmissionScriptDetails(LoginRequiredMixin, DetailView):
    model = Submission

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        with self.object.script_file.open("r") as f:
            sourcecode = f.read()
        context["sourcecode"] = sourcecode
        context["competition"] = self.object.competition
        return context
