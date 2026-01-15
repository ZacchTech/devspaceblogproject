from django.shortcuts import render, redirect 
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
#class inherintance
#UPDATE FORM
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

#step 2

# Create your views here.
#step 1
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username =form.cleaned_data.get('username')
            messages.success(request, f'Your account as being created! You are now able to login page')
            return redirect('login')
    else:   
    #step 1
         form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form,  'hide_sidebar': True})


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {
            'username': '',  # Remove username help text
        }
    
   # def __init__(self, *args, **kwargs):
    #    super(UserRegisterForm, self).__init__(*args, **kwargs)
     #   # Remove help text from password fields
      #  self.fields['password1'].help_text = ''
       # self.fields['password2'].help_text = ''

@login_required
def profile(request):
   if request.method == 'POST':
      u_form = UserUpdateForm(request.POST, instance=request.user)
      p_form = ProfileUpdateForm(request.POST, 
                                 request.FILES,
                                 instance = request.user.profile)
      if u_form.is_valid() and p_form.is_valid():
          u_form.save()
          p_form.save()
          messages.success(request,f'Your Account has beeng Update!')
          return redirect('profile')
      
   else:
      u_form = UserUpdateForm(instance = request.user)
      p_form = ProfileUpdateForm(instance = request.user.profile)  
       
   context = {
        'u_form': u_form,
        'p_form': p_form
    }
   return render(request, 'users/profile.html', {**context, 'hide_sidebar': True})

def login_view(request):
    return render(request, 'users/login.html', {
        'hide_sidebar': True
    })