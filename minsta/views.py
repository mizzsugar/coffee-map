import django.http
import minsta.models
import minsta.forms
from django.shortcuts import render
import uuid
from django.contrib.auth.models import User
import re
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
import minsta.exceptions
import minsta.domain
from django.core.mail import send_mail
from django.views import View
import django.core.exceptions
from django.template.loader import get_template
import json


def send_mail(request):
    if request.method == 'POST':
        minsta.domain.send_registration_request(request.POST)
        return render(request, 'succeed_sending.html')
    else:
        send_mail_form = minsta.forms.SendMailForm()
        return render(request, 'send_mail.html', {'send_mail_form': send_mail_form})


def forget_password_request(request):
    if request.method == 'POST':
        send_mail_form = minsta.forms.SendMailForm(request.POST)
        send_mail_form.is_valid()
        email = send_mail_form.cleaned_data['email']
        users = User.objects.all()

        for user in users: # TODO: for文だとユーザー多いと処理遅くなりそう
            if email == user.email:
                register_uuid = uuid.uuid4().hex
                minsta.models.ForgetPasswordUser.create(
                    register_uuid, email, user
                )
                minsta.domain.send_forget_password_request(user)
                return render(request, 'succeed_sending.html')
            else:
                pass
        send_mail_form.add_error('email', 'このメールアドレスは登録されていません')  
        return render(request, 'forget_password_request.html', {'send_mail_form': send_mail_form, 'user':user})
    else:
        send_mail_form = minsta.forms.SendMailForm()
        return render(request, 'forget_password_request.html', {'send_mail_form': send_mail_form})


class ForgetPasswordUser(View):
    def get(self, request, register_uuid):
        forget_password_form = minsta.forms.ForgetPasswordForm()
        try:
            minsta.models.ForgetPasswordUser.get_by_uuid(register_uuid)
        except django.core.exceptions.ObjectDoesNotExist:
            return render(request, 'url_does_not_exit.html')
        return render(request, 'change_password_forgotten.html', {'forget_password_form': forget_password_form, 'register_uuid':register_uuid})


    def post(self, request, register_uuid): # ここ変更する
        forget_password_form = minsta.forms.ForgetPasswordForm(request.POST)
        if not forget_password_form.is_valid():
            return render(request, 'change_password_forgotten.html', {'forget_password_form': forget_password_form,  'register_uuid':register_uuid})
        user = minsta.models.ForgetPasswordUser.get_by_uuid(register_uuid).user_id
        user.set_password(request.POST['new_password']) 
        user.save()
        minsta.models.ForgetPasswordUser.get_by_uuid(register_uuid).delete()
        # パスワードを変えると、自動的にログアウトされる動きをする
        return django.http.HttpResponseRedirect('/changed_password')


def get_post_new_post(request):
    try:
        minsta.domain.check_authenticated(request.user)
    except minsta.exceptions.LoginRequiredError:
        return django.http.HttpResponseRedirect('/login')
    form = minsta.forms.NewPostForm()
    return render(request, 'new_post.html', {'form': form, 'user':request.user}) #'cafes': cafes


def post_post_new_post(request):
    try:
        minsta.domain.post_new_post(request.user, request.POST, request.FILES)
    except minsta.exceptions.LoginRequiredError:
        return django.http.HttpResponseRedirect('/login')
    except minsta.exceptions.ValidationError as e:
        return render(request, 'new_post.html', {'form': e.form, 'user':request.user}) #'cafes': cafes 
    return django.http.HttpResponseRedirect('/list')


def post_new_post(request): 
    if request.method == 'POST':
        return post_post_new_post(request)
    return get_post_new_post(request)


def list(request):
    posts = minsta.models.Post.list()
    return render(request, 'list.html', {'posts': posts})


def login(request):
    if request.method == 'POST':
        login_form = minsta.forms.LoginForm(request.POST)
        if not login_form.is_valid():
            login_form.add_error('password', "validation_errorです")
            return render(request, 'login.html', {'login_form': login_form})
        username = login_form.cleaned_data['username']
        password = login_form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            django_login(request, user)
            return django.http.HttpResponseRedirect('/post_new_post')
        login_form.add_error('password', "ユーザー名またはパスワードが異なります。")
        return render(request, 'login.html', {'login_form': login_form})
    else:
        login_form = minsta.forms.LoginForm()
    return render(request, 'login.html', {'login_form': login_form})
    # アカウントとパスワードが合致したら、その人専用の投稿画面に遷移する
    # アカウントとパスワードが合致しなかったら、エラーメッセージ付きのログイン画面に遷移する


def logout(request):
    django_logout(request)
    return render(request, 'logout.html')
    

class RegistrationUser(View):
    def get(self, request, register_uuid):
        registration_form = minsta.forms.RegistrationForm()
        try:
            minsta.models.ProvisionalUser.get_by_uuid(register_uuid)
        except django.core.exceptions.ObjectDoesNotExist:
            return render(request, 'url_does_not_exit.html')
        return render(request, 'registration.html', {'registration_form': registration_form, 'register_uuid':register_uuid})


    def post(self, request, register_uuid):
        try:
            user = minsta.domain.register(request.POST, register_uuid) 
        except minsta.exceptions.RegistrationError as e:
            return render(request, 'registration.html', {'registration_form': e.form, 'user':request.user})
        # provisionaluserからdeleteする
        django_login(request, user)
        return django.http.HttpResponseRedirect('/post_new_post')


def change_password(request):
    if not request.user.is_authenticated:
        return django.http.HttpResponseRedirect('/login')
    if request.method == 'POST':
        change_password_form = minsta.forms.ChangePasswordForm(request.POST)
        if not change_password_form.is_valid():
            if not request.user.check_password(change_password_form.cleaned_data['current_password']): # check_password(password)で現在ログインしているユーザーのパスワードと一致するか確かめられる
                change_password_form.add_error('current_password', "現在使用しているパスワードと異なります。")
            return render(request, 'change_password.html', {'change_password_form': change_password_form})
        user = request.user
        user.set_password(request.POST['new_password'])
        user.save()
        # パスワードを変えると、自動的にログアウトされる動きをするのはDjangoの仕様
        return django.http.HttpResponseRedirect('/changed_password')
    else:
        change_password_form = minsta.forms.ChangePasswordForm()
    return render(request, 'change_password.html', {'change_password_form': change_password_form})


def changed_password(request):
    return render(request, 'changed_password.html')


def test_layout(request):
    return render(request, 'test.html')


def introdoce_cafe(request,id):
    cafe = minsta.models.Cafe.get_by_id(id)
    cafe_photos = minsta.models.Post.get_latest3_photos(id)
    return render(request, 'introdoce_cafe.html', {'cafe': cafe, 'cafe_photos':cafe_photos})


def cafe_info(request ,id):
    cafe = minsta.models.Cafe.get_by_id(id)
    cafe_json = json.dumps({"id":cafe.id, "latitude":cafe.latitude, "longitude":cafe.longitude})
    print(cafe_json)
    return django.http.HttpResponse(cafe_json, content_type='application/json')


def cafe_list(request):
    cafes = minsta.domain.get_cafe_photos() # View用のphotoも加えたクラスにする
    print(cafes[2].photo_list)
    # cafe_photos = minsta.models.Post.get_latest3_photos(id)
    # print(minsta.models.Cafe.get_cafe_id().values('id'))
    return render(request, 'cafe_list.html',  {'cafes': cafes})


def user_page(request, username):
    post_user = User.objects.get(username=username)
    views_user_posts = minsta.domain.get_user_post(username)
    return render(request, 'user_page.html', {'posts': views_user_posts, 'user':post_user})
    # TODO: ここで編集と削除も行いたい。 投稿をクリック→モーダルでフォーム→編集→update。削除ボタン→削除

