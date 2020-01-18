from django.urls import path
from custom_user import views
from rest_framework.authtoken import views as drf_views
from account import views as account_views

urlpatterns = [
    path('', views.ProfileAPIView.as_view(), name=''),
    path('register/', views.register, name='register'),
    path('auth/', drf_views.obtain_auth_token),
    path('page_ranking/', views.page_ranking, name='ranking'),
    # account
    path('account/', account_views.my_accounts_view, name='my_accounts_view'),
    path('record/', account_views.my_records_view, name='my_records_view'),
]