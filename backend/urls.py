from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_image, name='upload_image'),
    path('api/upload/', views.ImageUploadAPIView.as_view(), name='api_upload_image'),
]
