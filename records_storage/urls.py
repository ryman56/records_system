from django.contrib import admin
from django.urls import path
from records import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('accounts/login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('records/', views.records_view, name='records'),
    path('profile/', views.profile_view, name='profile'),
    path('departments/', views.departments_view, name='departments'),
    path('departments/<int:department_id>/', views.department_records, name='department_records'),
    path('upload/', views.upload_document_view, name='upload_document'),
    path('document/view/<int:record_id>/', views.view_document, name='view_document'),
    path('document/download/<int:record_id>/', views.download_document, name='download_document'),
] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)