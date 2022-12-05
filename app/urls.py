from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('pricing/', views.pricing, name='pricing'),
    path('getWebsites/', views.getWebsites, name='getWebsites'),
    path('identify_login/', views.identify_login, name='identify_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/video_stream/', views.video_stream, name='video_stream'),
    path('dashboard/add_photos/', views.add_photos, name='add_photos'),
    path('dashboard/add_photos/<slug:user_id>/', views.click_photos, name='click_photos'),
    path('dashboard/train_model/', views.train_model, name='train_model'),
    path('dashboard/detected/', views.detected, name='detected'),
    path('dashboard/identify/', views.identify, name='identify'),
    path('dashboard/add_user/', views.add_user, name='add_user'),
    path('dashboard/add_website/', views.add_website, name='add_website'),
    path('dashboard/admin_website/', views.admin_website, name='admin_website'),
    path('dashboard/admin_website/<slug:website_id>/', views.delete_website, name='delete_website')
]