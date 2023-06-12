from django.urls import path

from .views import (
    AccountDetailView,
    AccountUpdateView,
    GenerateInvitationCodeView,
    SignUpView,
    redirect_to_profile,
    search_view,
)

app_name = "accounts"
urlpatterns = [
    path("login/", view=redirect_to_profile, name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("update/", view=AccountUpdateView.as_view(), name="update"),
    path(
        "generate_invitation_code/",
        GenerateInvitationCodeView.as_view(),
        name="generate_invitation_code",
    ),
    path("search/", search_view, name="search"),
    path("people/<str:username>/", view=AccountDetailView.as_view(), name="detail"),
    path("profile", view=redirect_to_profile, name="profile"),
]
