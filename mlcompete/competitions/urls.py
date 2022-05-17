from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path("", views.CompetitionIndexView.as_view(), name="competitions"),
    path("", views.CompetitionIndexView.as_view(), name="home"),
    path(
        "competitions/<int:competition>",
        views.LeaderBoardView.as_view(),
        name="competition",
    ),
    path(
        "competitions/<int:competition>/<int:phase>",
        views.LeaderBoardView.as_view(),
        name="leaderboard",
    ),
    path(
        "competitions/<int:competition>/",
        views.LeaderBoardView.as_view(),
        name="leaderboard",
    ),
    path(
        "competitions/<int:competition>/submit",
        views.SubmissionCreate.as_view(),
        name="submission_create",
    ),
    path(
        "users/<int:pk>/",
        views.UserProfile.as_view(),
        name="user_profile",
    ),
    path(
        "competitions/add", views.CompetitionCreate.as_view(), name="competition_create"
    ),
    path(
        "competitions/<int:pk>/edit",
        views.CompetitionUpdate.as_view(),
        name="competition_update",
    ),
    path(
        "competitions/<int:pk>/manage",
        views.CompetitionManage.as_view(),
        name="competition_manage",
    ),
    path(
        "competitions/<int:competition>/phases/add",
        views.PhaseCreate.as_view(),
        name="phase_create",
    ),
    path(
        "competitions/<int:competition>/phases/<int:pk>/edit",
        views.PhaseUpdate.as_view(),
        name="phase_update",
    ),
    path(
        "phases/<int:pk>/upload_data",
        views.PhaseUploadData.as_view(),
        name="phase_upload_data",
    ),
    path(
        "datasets/<int:competition>/<int:phase>/<str:filename>",
        views.phase_download_data,
        name="phase_download_data",
    ),
    path(
        "submissions/<int:pk>/script",
        views.SubmissionScriptDetails.as_view(),
        name="submission_script",
    ),
]
