from django.contrib.auth.models import User   #inbuild user model
from django import forms
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm,AuthenticationForm   #usercreation->registration,passwordchng->reset password, authentication->login form

class SignUpForm(UserCreationForm):
    password2=forms.CharField(label="Confirm password(again)", widget=forms.PasswordInput)  #changing label of password confirm
    class Meta:
        model=User
        fields=['username','first_name','last_name','email']
        labels={'email':'Email'}      #changing label of email confirm

class ChngPass(PasswordChangeForm):
    username=forms.CharField(label="Username", max_length=50, required=True,widget=forms.TextInput(attrs={'autofocus':'autofocus'}))  #add newefeild user and shoft autofocus to it
    new_password2=forms.CharField(label="confirm Password",widget=forms.PasswordInput)   #changing label of password confirm
    field_order=['username','old_password','new_password1','new_password2']   #setting order of feilds to be displayed
    def __init__(self, *args, **kwargs):   #removing autofocus from old password
        super().__init__( *args, **kwargs)

        self.fields['old_password'].widget.attrs.pop('autofocus',None)  #---------------------------------

class UsrLogin(AuthenticationForm):
    error_messages={
        'invalid_login':'Invalid Username and Password'       #updating in build error message in time of login
    }        