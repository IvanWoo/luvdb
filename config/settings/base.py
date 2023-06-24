"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path

from environs import Env

from write.spoiler_extension import SpoilerExtension

from ..s3_storage_backends import MediaStorage

env = Env()
env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "accounts",
    "dal",
    "dal_select2",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",  # 3rd party
    "django.contrib.staticfiles",
    # third-party apps
    "crispy_forms",
    "crispy_bootstrap5",
    "markdownify",
    "mathfilters",
    "reversion",
    "storages",
    # local apps
    "notify",
    "activity_feed",
    "entity",
    "write",
    "read",
    "listen",
    "play",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "notify.context_processors.notifications",
            ],
            "libraries": {
                "account_tags": "accounts.templatetags.account_tags",
                "url_filters": "activity_feed.templatetags.url_filters",
                "linkify": "write.templatetags.linkify",
                "parse_activity_type": "activity_feed.templatetags.parse_activity_type",
            },
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": env.dj_db_url("DATABASE_URL", default="sqlite:///db.sqlite3"),
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Berlin"

USE_I18N = True

USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "accounts.CustomUser"

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_CLASS_CONVERTERS = {
    "form-select": "",
}


LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "activity_feed:activity_feed"
LOGOUT_REDIRECT_URL = "login"


# Markdownify settings
MARKDOWNIFY = {
    "default": {
        "WHITELIST_TAGS": [
            "abbr",
            "acronym",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "blockquote",
            "cite",
            "code",
            "dfn",
            "em",
            "i",
            "kbd",
            "strong",
            "samp",
            "var",
            "b",
            "i",
            "ul",
            "ol",
            "li",
            "dl",
            "dt",
            "dd",
            "img",
            "pre",
            "div",
            "span",
            "table",
            "thead",
            "tbody",
            "tfoot",
            "tr",
            "th",
            "td",
            "p",
            "br",
            "details",
            "summary",
            "caption",
            "col",
            "colgroup",
            "fieldset",
            "legend",
            "section",
            "article",
            "figure",
            "header",
            "footer",
            "aside",
            "center",
            "main",
            "nav",
            "output",
            "progress",
            "meter",
            "audio",
            "video",
            "canvas",
            "ruby",
            "rt",
            "rp",
            "s",
            "strike",
            "del",
            "ins",
            "a",
            "small",
            "sup",
            "sub",
            "u",
            "mark",
            "time",
        ],
        "WHITELIST_ATTRS": ["src", "alt", "href", "title", "class", "id", "target"],
        "WHITELIST_STYLES": [
            "color",
            "font-weight",
        ],
        "MARKDOWN_EXTENSIONS": [
            "fenced_code",
            "extra",
            "nl2br",
            "codehilite",
            "admonition",
        ],
    }
}
