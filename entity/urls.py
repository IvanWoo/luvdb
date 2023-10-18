from django.urls import path

from .views import (
    CompanyAutocomplete,
    CompanyCreateView,
    CompanyDetailView,
    CompanyUpdateView,
    CreatorAutoComplete,
    CreatorCreateView,
    CreatorDetailView,
    CreatorUpdateView,
    RoleAutocomplete,
    RoleCreateView,
    RoleDetailView,
    RoleUpdateView,
)

app_name = "entity"

urlpatterns = [
    # creator
    path("creator/create/", CreatorCreateView.as_view(), name="creator_create"),
    path("creator/<int:pk>/", CreatorDetailView.as_view(), name="creator_detail"),
    path(
        "creator/<int:pk>/update/", CreatorUpdateView.as_view(), name="creator_update"
    ),
    path(
        "creator-autocomplete/",
        CreatorAutoComplete.as_view(),
        name="creator-autocomplete",
    ),
    # role
    path("role/create/", RoleCreateView.as_view(), name="role_create"),
    path("role/<int:pk>/", RoleDetailView.as_view(), name="role_detail"),
    path("role/<int:pk>/update/", RoleUpdateView.as_view(), name="role_update"),
    path("role-autocomplete/", RoleAutocomplete.as_view(), name="role-autocomplete"),
    # company
    path("company/create/", CompanyCreateView.as_view(), name="company_create"),
    path("company/<int:pk>/", CompanyDetailView.as_view(), name="company_detail"),
    path(
        "company/<int:pk>/update/", CompanyUpdateView.as_view(), name="company_update"
    ),
    path(
        "company-autocomplete/",
        CompanyAutocomplete.as_view(),
        name="company-autocomplete",
    ),
]
