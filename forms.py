from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UserCreationEmailForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ('username', 'email')

	def __init__(self, *args, **kwargs):
		self.user_cache = None
		super(UserCreationEmailForm, self).__init__(*args,**kwargs)

	def clean(self):
		email = self.cleaned_data.get('email')
		try:
			self.user_cache = User.objects.get(email=email)
			raise forms.ValidationError('Email ya registrado')
			return None
		except User.DoesNotExist:
			return self.cleaned_data

	def get_user(self):
		return self.user_cache

class EmailAuthenticationForm(forms.Form):
	email = forms.EmailField(required=True)
	password = forms.CharField(required=True, widget=forms.PasswordInput)

	def __init__(self, *args, **kwargs):
		self.user_cache = None
		super(EmailAuthenticationForm, self).__init__(*args,**kwargs)

	def clean(self):
		email = self.cleaned_data.get('email')
		password = self.cleaned_data.get('password')

		self.user_cache = authenticate(email=email, password=password)

		if self.user_cache is None:
			raise forms.ValidationError('Usuario Incorrecto')
		elif not self.user_cache.is_active:
			raise forms.ValidationError('Usuario Inactivo')
		return self.cleaned_data

	def get_user(self):
		return self.user_cache