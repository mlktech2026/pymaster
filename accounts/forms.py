from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfile

COMMON_INPUT_CLASSES = (
    'form-input w-full px-3.5 py-2.5 rounded-xl border border-slate-300 '
    'bg-white text-slate-900 placeholder-slate-400 text-sm '
    'focus:outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 transition'
)

AUTH_INPUT_LEFT_ICON = (
    'form-input form-input-with-icon-left w-full pl-10 pr-3.5 py-2.5 rounded-xl '
    'border border-slate-300 bg-white text-slate-900 placeholder-slate-400 text-sm '
    'focus:outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 transition'
)

AUTH_INPUT_BOTH_ICONS = (
    'form-input form-input-with-icon-left form-input-with-icon-right w-full pl-10 pr-10 py-2.5 rounded-xl '
    'border border-slate-300 bg-white text-slate-900 placeholder-slate-400 text-sm '
    'focus:outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 transition'
)

class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'name@example.com',
            'class': AUTH_INPUT_LEFT_ICON,
            'autocomplete': 'email',
            'required': 'required'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Create a password (min. 6 characters)',
            'class': AUTH_INPUT_BOTH_ICONS,
            'autocomplete': 'new-password',
            'required': 'required'
        }),
        min_length=6
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Re-enter your password',
            'class': AUTH_INPUT_BOTH_ICONS,
            'autocomplete': 'new-password',
            'required': 'required'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Choose a username',
                'class': AUTH_INPUT_LEFT_ICON,
                'autocomplete': 'username',
                'required': 'required'
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError("Email is required.")
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'preferred_theme']
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Tell us about your Python learning journey...',
                'class': COMMON_INPUT_CLASSES
            }),
            'preferred_theme': forms.Select(attrs={
                'class': COMMON_INPUT_CLASSES
            }),
        }

class UserInfoUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': COMMON_INPUT_CLASSES, 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': COMMON_INPUT_CLASSES, 'placeholder': 'Last name'}),
            'email': forms.EmailInput(attrs={'class': COMMON_INPUT_CLASSES, 'placeholder': 'Email address'}),
        }
