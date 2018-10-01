"""minsta URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import minsta.views


urlpatterns = [
    path("list", minsta.views.list),
    path("post_new_post", minsta.views.post_new_post),
    path('admin/', admin.site.urls),
    path("login", minsta.views.login),
    path("registration_user/<str:register_uuid>", minsta.views.RegistrationUser.as_view()), 
    path("logout", minsta.views.logout),
    path("change_password", minsta.views.change_password),
    path("changed_password", minsta.views.changed_password),
    path("send_mail", minsta.views.send_mail),
    path("forget_password_request", minsta.views.forget_password_request), # パスワード忘れ用メールフォーム
    path("change_password_forgotten/<str:register_uuid>", minsta.views.ForgetPasswordUser.as_view()), # パスワード忘れのパスワード変更画面
    path("introdoce_cafe/<int:id>", minsta.views.introdoce_cafe),
    path("cafe_info/<int:id>",minsta.views.cafe_info),
    path("cafe_list",minsta.views.cafe_list),
    path("user_page/<str:username>", minsta.views.user_page),
    path("testlayout", minsta.views.test_layout),
]
