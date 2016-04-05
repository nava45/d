from django import forms
from django.utils.translation import ugettext_lazy as _
from registration.models import Account
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from nocaptcha_recaptcha.fields import NoReCaptchaField


class RegistrationForm(forms.Form):
 
    first_name = forms.RegexField(regex=r'^[a-zA-Z\-]+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)),
                                  label=_("First Name"),
                                  error_messages={ 'invalid': _("This value must contain only letters.") })
    middle_name = forms.RegexField(regex=r'^[a-zA-Z\-]+$', widget=forms.TextInput(attrs=dict(required=False, max_length=30)),
                                  label=_("Middle Name"),
                                  error_messages={ 'invalid': _("This value must contain only letters.") })
    last_name = forms.RegexField(regex=r'^[a-zA-Z\-]+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)),
                                  label=_("Last Name"),
                                  error_messages={ 'invalid': _("This value must contain only letters.") })
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
    phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$', 
                                    error_messages={ 'invalid': _("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.") })
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True,
                                                                      min_length=6,
                                                                      max_length=30,
                                                                      render_value=False)),
                                label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True,
                                                                      min_length=6,
                                                                      max_length=30,
                                                                      render_value=False)),
                                label=_("Password (again)"))
    captcha = NoReCaptchaField()
    
    def __init__(self, *args, **kw):
        self.user_obj = kw.pop('user', None)
        super(RegistrationForm, self).__init__(*args, **kw)
        if self.user_obj and not self.user_obj.is_anonymous():
            self.fields["first_name"].initial = self.user_obj.account.first_name
            self.fields["middle_name"].initial = self.user_obj.account.middle_name
            self.fields["last_name"].initial = self.user_obj.account.last_name
            self.fields["email"].initial = self.user_obj.account.email
            self.fields["phone_number"].initial = self.user_obj.account.mobile_no
            
            #import ipdb; ipdb.set_trace()
            # It is not mandatory to update password
            self.fields['password1'].required = False
            self.fields['password2'].required = False
            
            del self.fields['password1']
            del self.fields['password2']
 
    def clean_email(self):
        try:
            user_obj = User.objects.get(email__iexact=self.cleaned_data['email'])
        except User.DoesNotExist:
            return self.cleaned_data['email']
    
        raise forms.ValidationError(_("The email already exists. Please try another one."))
 
    def clean_password1(self):
        if 'password1' in self.cleaned_data and len(self.cleaned_data['password1']) < 6:
            raise forms.ValidationError(_("The Password must be more than 6 chars."))
        return self.cleaned_data['password1']
 
    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data


class LoginForm(forms.Form):
    error_messages = {
        'invalid_login': _("Please enter a correct email and password. "
                           "Note that both fields may be case-sensitive."),
        'inactive': _("This account is inactive."),
    }


    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
    password = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True,
                                                                    max_length=30,
                                                                    render_value=False)),
                                label=_("Password"))
    
    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    
                )

        if user_obj:
            self.user_cache = authenticate(username=user_obj.username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    
                )
            else:
                #self.confirm_login_allowed(self.user_cache)
                pass

        return self.cleaned_data
        
    def get_user(self):
        return self.user_cache
