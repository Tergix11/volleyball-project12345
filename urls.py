from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from main import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('logout/', views.user_logout, name='logout'),
]

# Раздаём медиафайлы (загруженные фото и т.д.) всегда, а не только при
# DEBUG=True — для маленького проекта без S3/CDN это самый простой вариант,
# чтобы фотографии открывались и на Railway.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
