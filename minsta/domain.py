import minsta.exceptions
import uuid
import re
from django.contrib.auth.models import User
import django.db
from typing import(
    Any,
    Dict
) 
from django.utils.datastructures import MultiValueDict
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.template.loader import get_template
import minsta.models


def send_registration_request(request_user) -> None:
    send_mail_form = minsta.forms.SendMailForm(request_user)
    send_mail_form.is_valid()
    email = send_mail_form.cleaned_data['email']
    register_uuid = uuid.uuid4().hex
    minsta.models.ProvisionalUser.create(
        email=email,
        register_uuid = register_uuid
    )
    mail_template = get_template('provisional_user.txt')
    context = {
    "register_uuid": register_uuid,
    }
    message = mail_template.render(context)
    send_mail('CoffeeMap仮登録',
    message, 
    'coffeemap@coffee.sugar-code.space',
    [email])


def send_forget_password_request(user_id: int) -> None:
    forget_password_user = minsta.models.ForgetPasswordUser.get_by_user_id(user_id)
    mail_template = get_template('forget_password_user.txt') # TODO: メール文章内のURLを本番環境のものに直す
    context = {
    "register_uuid": forget_password_user.register_uuid,
    "user": forget_password_user.user_id.username # TODO: ユーザー名も入れる？
    }
    message = mail_template.render(context)
    send_mail('CoffeeMappパスワード再発行',
    message, 
    'coffeemap@coffee.sugar-code.space', 
    [forget_password_user.email])


def post_new_post(author: User, post: Dict[str, Any], file: MultiValueDict) -> None:
    if not author.is_authenticated:
        raise minsta.exceptions.LoginRequiredError()
    form = minsta.forms.NewPostForm(post, file) # キーワード引数は位置引数よりも後ろに書く
    if not form.is_valid():
        raise minsta.exceptions.ValidationError(form)
    
    file_path = handle_uploaded_file(form.cleaned_data['file'])
    minsta.models.Post.create(author, file_path, form.cleaned_data['comment'], form.cleaned_data['cafe'])


def check_authenticated(user) -> None:
    if not user.is_authenticated:
        raise minsta.exceptions.LoginRequiredError()


def handle_uploaded_file(f) -> str: # TODO: returns str??
    file_path = "uploads/{}.jpeg".format(uuid.uuid4().hex)
    with open('minsta/static/{}'.format(file_path), 'wb') as destination:
        # 'minsta/static/uploads/{}.jpeg'.format(uuid.uuid4().hex) .format()で{}の中を()の中に置き換えてくれる
        # uuidとは、ランダムでユニークなIDの規格である。uuid.uuid4().hexの.hexで文字列にする。
        # hexで、ランダムな文字列を16進数で返す
        for chunk in f.chunks():
            destination.write(chunk)
    return file_path


def expire_frogetpassworduser() -> None:
    expired_users=minsta.models.ForgetPasswordUser.get_older_than(datetime.now()+timedelta(days=1))
    for expired_user in expired_users:
        expired_user.delete()


def register(user_profile: RegistrationForm, register_uuid: str) -> User:
    """ユーザ登録をする

    :raises FormError: 与えられた情報が不正なとき、もしくはDBにすでに同じユーザー名が登録されているとき
    :return: 登録されたユーザ
    """
    registration_form = minsta.forms.RegistrationForm(user_profile)
    if not registration_form.is_valid():
        raise minsta.exceptions.FormError(registration_form)
    provisional_user = minsta.models.ProvisionalUser.get_by_uuid(register_uuid)
    try:
        user = User.objects.create_user(
            username=registration_form.cleaned_data['username'],
            password=registration_form.cleaned_data['password'],
            email=provisional_user.email 
        )
    except django.db.IntegrityError:
        registration_form.add_error('username', 'このユーザー名はすでに登録されているため無効です')
        raise minsta.exceptions.FormError(registration_form)
    provisional_user.delete()
    return user


def change_forgotten_password(user_profile: ForgetPasswordForm, register_uuid: str) -> User:
    change_forgotten_password_form = minsta.forms.ForgetPasswordForm(user_profile)
    if not change_forgotten_password_form.is_valid():
        raise minsta.exceptions.FormError(change_forgotten_password_form)
    forget_password_user = minsta.models.ForgetPasswordUser.get_by_uuid(register_uuid)
    try: # ここを変更する。パスワード変更
        user = User.objects.create_user(
            username=registration_form.cleaned_data['username'],
            password=registration_form.cleaned_data['password'],
            email=provisional_user.email 
        )
    except django.db.IntegrityError:
        registration_form.add_error('username', 'このユーザー名はすでに登録されているため無効です')
        raise minsta.exceptions.FormError(registration_form)
    provisional_user.delete()
    return user


class CafePhotos:
    def __init__(self, cafe_id, location, latitude, longitude, cafe_name, comment, hp, facebook, instagram, twitter, work_time, area, photo_list):
        self.cafe_id = cafe_id
        self.location = location
        self.latitude = latitude
        self.longitude = longitude
        self.cafe_name = cafe_name
        self.comment = comment
        self.hp = hp
        self.facebook = facebook
        self.instagram = instagram
        self.twitter = twitter
        self.work_time = work_time
        self.area = area
        self.photo_list = photo_list


def get_cafe_photos() -> :List[CafePhotos]:
    cafes = minsta.models.Cafe.list()
    cafe_photos = []  # List[CafePhotos]
    for cafe in cafes:
        photos = []
        for photo in minsta.models.Post.get_latest3_photos(cafe):
            photos.append(photo)

        cafe_photos.append(CafePhotos(cafe.id, cafe.location, cafe.latitude, cafe.longitude, cafe.cafe_name, cafe.comment, 
            cafe.hp, cafe.facebook, cafe.instagram, cafe.twitter, cafe.work_time, cafe.area, photos))
    return cafe_photos


class UserPost:
    def __init__(self, file_path: str, comment: str, cafe: Cafe, posted_at: datetime):
        self.file_path = file_path # TODO: is this str?
        self.comment = comment
        self.cafe = cafe
        self.posted_at = posted_at # TODO: what is this attribute?


def get_user_post(username: str) -> List[UserPost]:
    user = User.objects.get(username=username)
    user_posts = minsta.models.Post.get_by_user(user=user)
    posts = []
    for user_post in user_posts:
        posts.append(UserPost(user_post.file_path, user_post.comment, user_post.cafe, user_post.posted_at))
    return posts
