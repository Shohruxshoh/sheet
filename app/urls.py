from django.urls import path
from .views import FileWritingView, AAA, LoginViewApi
from .f import index, login_oauth, get_file_name

urlpatterns = [
    path('', FileWritingView.as_view(), name="aaaa"),
    path('index', index, name='index'),
    path('login', login_oauth, name='login'),
    path('get-file', get_file_name),
    path('aaa', AAA.as_view(), name='api-index'),
    path('login-api', LoginViewApi.as_view(), name='login-api'),
]
