from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('edit/', views.edit, name='edit'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/wanted', views.wanted, name='wanted'),
    path('<int:pk>/wanting', views.wanting, name='wanting'),
    path('posts/<int:pk>', views.post_detail, name='post_detail'),
    path('notation/', views.notation, name='notation'),
]
