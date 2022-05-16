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
    score = tables.Column()
    timestamp = tables.Column()


class UserSubmissionsTable(tables.Table):
    timestamp = tables.Column()
    competition = tables.Column()
    score = tables.Column()

    def render_competition(self, value, record):
        url = reverse("leaderboard", args=(value.pk,))
        return format_html('<a href="{}">{}</b>', url, value.name)
