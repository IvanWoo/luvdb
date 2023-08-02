from django.contrib import admin

from .models import (
    Genre,
    Label,
    ListenCheckIn,
    Release,
    ReleaseRole,
    ReleaseTrack,
    Track,
    TrackRole,
    Work,
    WorkRole,
)


class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class WorkRoleInline(admin.TabularInline):
    model = WorkRole
    extra = 1


class WorkAdmin(admin.ModelAdmin):
    list_display = ["title", "release_date"]
    inlines = [WorkRoleInline]


class TrackRoleInline(admin.TabularInline):
    model = TrackRole
    extra = 1


class TrackAdmin(admin.ModelAdmin):
    list_display = ["title", "release_date", "length"]
    inlines = [TrackRoleInline]


class ReleaseRoleInline(admin.TabularInline):
    model = ReleaseRole
    extra = 1


class ReleaseTrackInline(admin.TabularInline):
    model = ReleaseTrack
    extra = 1


class ReleaseAdmin(admin.ModelAdmin):
    list_display = ["title", "release_date", "release_type", "release_format"]
    inlines = [ReleaseRoleInline, ReleaseTrackInline]


admin.site.register(Label)
admin.site.register(Work, WorkAdmin)
admin.site.register(Track, TrackAdmin)
admin.site.register(Release, ReleaseAdmin)
admin.site.register(ListenCheckIn)
admin.site.register(Genre, GenreAdmin)
