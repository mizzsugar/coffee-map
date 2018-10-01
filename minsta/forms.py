from django import forms
import re
import minsta

# formの役割は与えられたデータをきれいにして（全部小文字にするとか、全角半角ぐっちゃの奴を可能な限り半角にするとか、名前が半角スペースに始まるわけがないものをtrim（stripする）とか）
# それをした後に与えられた値が妥当かどうか検査する
# 妥当かどうか判断して、妥当だと判断した後に妥当だと判断したデータをどう扱うかはformには関係ない
# formはis_validでtrueかfalseを返すだけ


#https://docs.djangoproject.com/en/2.0/topics/http/file-uploads/


class SendMailForm(forms.Form):
    email = forms.EmailField(
        label='メールアドレス',
        widget=forms.TextInput(attrs={'class':'form-control'})
    )


choices =  [(int(cafe.id), str(cafe.cafe_name)) for cafe in minsta.models.Cafe.list()]

class NewPostForm(forms.Form):
    file = forms.FileField(label='写真', widget=forms.FileInput(attrs={'class':'form-control-file'}))
    comment = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control-file'}), label='コメント')
    cafe = forms.ChoiceField(
        label='お店',
        choices=choices, 
        required=True
    )
    


def has_digit(text):
    return re.search("\d", text)

def has_alphabet(text):
    return re.search("[a-zA-Z]", text)


class RegistrationForm(forms.Form):
    username = forms.CharField(label='ユーザー名', widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    # email = forms.EmailField(label='メールアドレス', widget=forms.TextInput(attrs={'class':'form-control'}))

    def is_valid(self):
        valid = super().is_valid()
        password = self.cleaned_data['password']
        if len(password) < 8:
            self.add_error('password', "文字数が8文字未満です。")
        if not has_digit(password):
            self.add_error('password',"数字が含まれていません")
        if not has_alphabet(password):
            self.add_error('password',"アルファベットが含まれていません")

        has_password_error = self.has_error('password')
        
        # if self.has_error('password'):
        #     raise minsta.exceptions.RegistrationError(registration_form)
        return valid and not has_password_error
        




class LoginForm(forms.Form):
    username = forms.CharField(label='ユーザー名', widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput(attrs={'class':'form-control'}))

    


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(label='現在のパスワード', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password = forms.CharField(label='新しいパスワード', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    check_password = forms.CharField(label='確認用パスワード', widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def is_valid(self):
        valid = super().is_valid()
        new_password = self.cleaned_data['new_password']
        check_password = self.cleaned_data['check_password']
        if new_password != check_password:
            self.add_error('new_password', "確認用のパスワードと一致していません。")

        has_not_same_error = self.has_error('new_password')
        
        # if self.has_error('password'):
        #     raise minsta.exceptions.RegistrationError(registration_form)
        return valid and not has_not_same_error


class ForgetPasswordForm(forms.Form):
    new_password = forms.CharField(label='新しいパスワード', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    check_password = forms.CharField(label='確認用パスワード', widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def is_valid(self):
        valid = super().is_valid()
        new_password = self.cleaned_data['new_password']
        check_password = self.cleaned_data['check_password']
        if len(new_password) < 8:
            self.add_error('new_password', "文字数が8文字未満です。")
        if not has_digit(new_password):
            self.add_error('new_password',"数字が含まれていません")
        if not has_alphabet(new_password):
            self.add_error('new_password',"アルファベットが含まれていません")
        if new_password != check_password:
            self.add_error('new_password', "確認用のパスワードと一致していません。")

        has_not_same_error = self.has_error('new_password')
        
        # if self.has_error('password'):
        #     raise minsta.exceptions.RegistrationError(registration_form)
        return valid and not has_not_same_error