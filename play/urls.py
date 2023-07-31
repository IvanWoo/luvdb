from django.urls import path

from .views import (
    DeveloperAutocomplete,
    DeveloperCreateView,
    DeveloperDetailView,
    DeveloperUpdateView,
    GameCastDetailView,
    GameCheckInAllListView,
    GameCheckInDeleteView,
    GameCheckInDetailView,
    GameCheckInListView,
    GameCheckInUpdateView,
    GameCheckInUserListView,
    GameCreateView,
    GameDetailView,
    GamePublisherAutocomplete,
    GamePublisherCreateView,
    GamePublisherDetailView,
    GamePublisherUpdateView,
    GameSeriesCreateView,
    GameSeriesDetailView,
    GameSeriesUpdateView,
    GameUpdateView,
    GenreAutocomplete,
    GenreDetailView,
    PlatformAutocomplete,
    PlatformCreateView,
    PlatformDetailView,
    PlayListView,
    WorkAutocomplete,
    WorkCreateView,
    WorkDetailView,
    WorkUpdateView,
)

app_name = "play"
urlpatterns = [
    # play
    path("recent/", PlayListView.as_view(), name="play_list"),
    # work
    path("work/create/", WorkCreateView.as_view(), name="work_create"),
    path("work/<int:pk>/", WorkDetailView.as_view(), name="work_detail"),
    path("work/<int:pk>/update/", WorkUpdateView.as_view(), name="work_update"),
    # game
    path("game/create/", GameCreateView.as_view(), name="game_create"),
    path("game/<int:pk>/", GameDetailView.as_view(), name="game_detail"),
    path("game/<int:pk>/update/", GameUpdateView.as_view(), name="game_update"),
    # developer
    path("developer/create/", DeveloperCreateView.as_view(), name="developer_create"),
    path("developer/<int:pk>/", DeveloperDetailView.as_view(), name="developer_detail"),
    path(
        "developer/<int:pk>/update/",
        DeveloperUpdateView.as_view(),
        name="developer_update",
    ),
    # publisher
    path(
        "publisher/create/", GamePublisherCreateView.as_view(), name="publisher_create"
    ),
    path(
        "publisher/<int:pk>/",
        GamePublisherDetailView.as_view(),
        name="publisher_detail",
    ),
    path(
        "publisher/<int:pk>/update/",
        GamePublisherUpdateView.as_view(),
        name="publisher_update",
    ),
    # platform
    path("platform/create/", PlatformCreateView.as_view(), name="platform_create"),
    path("platform/<int:pk>/", PlatformDetailView.as_view(), name="platform_detail"),
    # autocomplete
    path(
        "developer-autocomplete/",
        DeveloperAutocomplete.as_view(),
        name="developer-autocomplete",
    ),
    path(
        "platform-autocomplete/",
        PlatformAutocomplete.as_view(),
        name="platform-autocomplete",
    ),
    path(
        "publisher-autocomplete/",
        GamePublisherAutocomplete.as_view(),
        name="publisher-autocomplete",
    ),
    path("work-autocomplete/", WorkAutocomplete.as_view(), name="work-autocomplete"),
    path("genre-autocomplete/", GenreAutocomplete.as_view(), name="genre-autocomplete"),
    # checkin
    path(
        "game/<int:game_id>/checkins/",
        view=GameCheckInAllListView.as_view(),
        name="game_checkin_all_list",
    ),
    path(
        "game/<int:game_id>/<str:username>/checkins/",
        view=GameCheckInListView.as_view(),
        name="game_checkin_list",
    ),
    # cast
    path("game/<int:pk>/cast/", GameCastDetailView.as_view(), name="game_cast_detail"),
    # checkin
    path(
        "checkin/<int:pk>/", GameCheckInDetailView.as_view(), name="game_checkin_detail"
    ),
    path(
        "checkin/<int:pk>/update/",
        GameCheckInUpdateView.as_view(),
        name="game_checkin_update",
    ),
    path(
        "checkin/<int:pk>/delete/",
        GameCheckInDeleteView.as_view(),
        name="game_checkin_delete",
    ),
    path(
        "<str:username>/checkins/",
        GameCheckInUserListView.as_view(),
        name="game_checkin_user_list",
    ),
    # series
    path("series/create/", GameSeriesCreateView.as_view(), name="series_create"),
    path("series/<int:pk>/", GameSeriesDetailView.as_view(), name="series_detail"),
    path(
        "series/<int:pk>/update/", GameSeriesUpdateView.as_view(), name="series_update"
    ),
    # genre
    path("genre/<slug:slug>/", GenreDetailView.as_view(), name="genre_detail"),
]
