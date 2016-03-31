from django import forms
from django.utils.translation import ugettext_lazy as _
from registration.models import Account
from django.contrib.auth.models import User


class RegistrationForm(forms.Form):
 
    first_name = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)),
                                  label=_("First Name"),
                                  error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    middle_name = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=False, max_length=30)),
                                  label=_("Middle Name"),
                                  error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    last_name = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)),
                                  label=_("Last Name"),
                                  error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    user_name = forms.RegexField(regex=r'^[\d\w]+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)),
                                  label=_("User Name"),
                                  error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
    phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$', 
                                    error_messages={ 'invalid': _("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.") })
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password (again)"))
 
    def __init__(self, *args, **kw):
        self.user_obj = kw.pop('user', None)
        super(RegistrationForm, self).__init__(*args, **kw)
        if not self.user_obj.is_anonymous():
            self.fields["first_name"].initial = self.user_obj.account.first_name
            self.fields["middle_name"].initial = self.user_obj.account.middle_name
            self.fields["last_name"].initial = self.user_obj.account.last_name
            self.fields["user_name"].initial = self.user_obj.username
            self.fields["email"].initial = self.user_obj.account.email
            self.fields["phone_number"].initial = self.user_obj.account.mobile_no
            
            #import ipdb; ipdb.set_trace()
            # It is not mandatory to update password
            self.fields['password1'].required = False
            self.fields['password2'].required = False
            
            del self.fields['password1']
            del self.fields['password2']
 
    def clean_user_name(self):
        try:
            user_obj = User.objects.get(username__iexact=self.cleaned_data['user_name'])
            if self.user_obj == user_obj:
                return self.cleaned_data['user_name']
        except User.DoesNotExist:
            return self.cleaned_data['user_name']
    
        raise forms.ValidationError(_("The user name already exists. Please try another one."))
 
    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data
