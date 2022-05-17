import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html


class CompetitionsTable(tables.Table):
    name = tables.Column()
    description = tables.Column()
    pub_date = tables.Column()

    def render_name(self, value, record):
        url = reverse("leaderboard", args=(record.pk,))

        return format_html('<a href="{}">{}</b>', url, value)


class LeaderboardTable(tables.Table):
    user = tables.Column()
    label = tables.Column()
    score = tables.Column()
    timestamp = tables.Column()
    script_file = tables.Column()

    def render_user(self, value, record):
        url = reverse("user_profile", args=(value.id,))
        return format_html(
            '<a href="{url:s}">{username:s}</a>', url=url, username=value.username
        )

    def render_script_file(self, value, record):
        url = reverse("submission_script", args=(record.pk,))

        return format_html(
            '<a href="{url:s}">{filename:s}</a>',
            url=url,
            filename=record.script_file_name,
        )


class UserSubmissionsTable(tables.Table):
    timestamp = tables.Column()
    competition = tables.Column()
    score = tables.Column()

    def render_competition(self, value, record):
        url = reverse("leaderboard", args=(value.pk,))
        return format_html('<a href="{}">{}</b>', url, value.name)
