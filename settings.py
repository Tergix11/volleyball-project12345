from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------
# SECURITY
# -----------------------------
# В Railway добавь переменную окружения SECRET_KEY со своим значением.
# Если её нет — используется старое значение (для локальной разработки).
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-%dv2ii!aelr3t*u88t60c1mlf8s9(pv3%8o^5+n)*w68#1p*%2'
)

# DEBUG=False на проде. На Railway переменную DEBUG не задаём (или ставим "False").

DEBUG = os.environ.get('DEBUG', 'True') == 'True'
# Railway даёт домен вида xxx.up.railway.app — добавляем его автоматически.
ALLOWED_HOSTS = []
railway_domain = os.environ.get('RAILWAY_PUBLIC_DOMAIN')
if railway_domain:
    ALLOWED_HOSTS.append(railway_domain)
extra_hosts = os.environ.get('ALLOWED_HOSTS')
if extra_hosts:
    ALLOWED_HOSTS += [h.strip() for h in extra_hosts.split(',') if h.strip()]
if DEBUG:
    ALLOWED_HOSTS += ['localhost', '127.0.0.1']

CSRF_TRUSTED_ORIGINS = []
if railway_domain:
    CSRF_TRUSTED_ORIGINS.append(f'https://{railway_domain}')
extra_csrf = os.environ.get('CSRF_TRUSTED_ORIGINS')
if extra_csrf:
    CSRF_TRUSTED_ORIGINS += [h.strip() for h in extra_csrf.split(',') if h.strip()]

LOGIN_URL = '/login/'

# -----------------------------
# APPLICATIONS
# -----------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'main.apps.MainConfig',  # ← вот это правильно
]

AUTH_USER_MODEL = 'main.Users'
AUTHENTICATION_BACKENDS = [
    'main.auth_backend.UsersBackend',
]
# -----------------------------
# MIDDLEWARE
# -----------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# -----------------------------
# URL CONFIG
# -----------------------------
ROOT_URLCONF = 'volleyball_site.urls'


# -----------------------------
# TEMPLATES
# -----------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
      'DIRS': [BASE_DIR / "templates"],

        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'main.context_processors.unread_notifications',
                'main.context_processors.cart_count',
            ],
        },
    },
]


WSGI_APPLICATION = 'volleyball_site.wsgi.application'


# -----------------------------
# DATABASE
# -----------------------------
# Если Railway даёт переменную DATABASE_URL или MYSQL_URL (после добавления
# плагина MySQL в проект) — используем её. Иначе остаёмся на локальной
# конфигурации MySQL для разработки на своём компьютере.
db_url = os.environ.get('DATABASE_URL') or os.environ.get('MYSQL_URL')

if db_url:
    DATABASES = {
        'default': dj_database_url.parse(db_url, conn_max_age=600)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'volleyball_hub',
            'USER': 'root',
            'PASSWORD': '123456789',
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }


# -----------------------------
# PASSWORD VALIDATION
# -----------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# -----------------------------
# INTERNATIONALIZATION
# -----------------------------
LANGUAGE_CODE = 'ru'
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = False


# -----------------------------
# STATIC FILES
# -----------------------------
STATIC_URL = '/static/'
# Папки BASE_DIR/static в проекте нет — статика приложения main лежит
# в main/static/main и подхватывается автоматически через APP_DIRS,
# поэтому отдельный STATICFILES_DIRS не нужен (а ссылка на несуществующую
# папку ломает collectstatic на Railway).

# Сюда collectstatic будет складывать все статические файлы для продакшена.
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# -----------------------------
# DEFAULT PRIMARY KEY
# -----------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGOUT_REDIRECT_URL = '/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
