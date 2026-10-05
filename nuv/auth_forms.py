from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()


class BootstrapErrorMixin:
    """Adds Bootstrap's `is-invalid` class to every widget whose field has errors."""

    def full_clean(self):
        super().full_clean()
        for name in self.errors:
            if name in self.fields:
                w = self.fields[name].widget
                w.attrs['class'] = (w.attrs.get('class', '') + ' is-invalid').strip()


class SellerRegistrationForm(BootstrapErrorMixin, forms.ModelForm):
    password1 = forms.CharField(
        label='Password', strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'autocomplete': 'new-password',
            'placeholder': 'Create a password'}),
        error_messages={'required': 'Please enter a password.'},
        help_text='At least 8 characters, not entirely numeric, not too common.',
    )
    password2 = forms.CharField(
        label='Confirm password', strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'autocomplete': 'new-password',
            'placeholder': 'Repeat the password'}),
        error_messages={'required': 'Please confirm your password.'},
    )

    class Meta:
        model = User
        fields = ['first_name', 'username', 'email']
        labels = {'first_name': 'Full name / Store name'}
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. NAV Store'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'username', 'placeholder': 'Choose a username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'you@example.com'}),
        }
        error_messages = {
            'first_name': {'required': 'Please enter your name.'},
            'username': {'required': 'Please choose a username.'},
            'email': {'required': 'Please enter your email address.'},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in ('first_name', 'email'):
            self.fields[f].required = True

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        if len(username) < 4:
            raise ValidationError('Username must be at least 4 characters long.')
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError('This username is already taken.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('An account with this email already exists.')
        return email

    def clean_first_name(self):
        name = self.cleaned_data['first_name'].strip()
        if len(name) < 2:
            raise ValidationError('Name must be at least 2 characters long.')
        return name

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get('password1'), cleaned.get('password2')
        if p1 and p2:
            if p1 != p2:
                self.add_error('password2', 'The two passwords do not match.')
            else:
                # Temporary user so similarity validators can compare attributes
                temp = User(username=cleaned.get('username', ''), email=cleaned.get('email', ''),
                            first_name=cleaned.get('first_name', ''))
                try:
                    validate_password(p1, temp)
                except ValidationError as e:
                    self.add_error('password1', e)
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_staff = False
        user.is_superuser = False
        if commit:
            user.save()
            group, _ = Group.objects.get_or_create(name='Sellers')
            user.groups.add(group)
        return user


class SellerLoginForm(BootstrapErrorMixin, forms.ModelForm):
    """ModelForm on User used only for its fields; credentials are checked in clean()."""

    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'username',
                                               'placeholder': 'Enter your username', 'autofocus': True}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'current-password',
                                                   'placeholder': 'Enter your password'}),
        }
        error_messages = {
            'username': {'required': 'Please enter your username.'},
            'password': {'required': 'Please enter your password.'},
        }

    def __init__(self, *args, request=None, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def validate_unique(self):
        # Login must not run the "username already exists" check.
        pass

    def clean(self):
        cleaned = super().clean()
        username, password = cleaned.get('username'), cleaned.get('password')
        if username and password:
            user = authenticate(self.request, username=username.strip(), password=password)
            if user is None:
                raise ValidationError('Invalid username or password. Please try again.')
            self.user = user
        return cleaned

    def get_user(self):
        return self.user