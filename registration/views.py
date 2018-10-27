from django.shortcuts import render
from django.http import HttpResponse
from .forms import RegisterForm
from django.contrib.auth.models import User

# Create your views here.
def signup(request):
    if request.method == "POST":
        new_user_form = forms.RegisterForm(request.POST)
        
        if new_user_form.is_valid():
            new_user = User.objects.create_user(
                    username=new_user_form.cleaned_data["username"],
                    password=new_user_form.cleaned_data["password"],
                    email=new_user_form.cleaned_data["email"]
                )

            new_user.first_name = new_user_form.cleaned_data["first_name"]
            new_user.last_name = new_user_form.cleaned_data["last_name"]
            new_user.save()


            # Need to do email confirmation 
            return HttpResponse("You have been registered.")

        else:
            return render(request, 'registration/register.html', {"signup_form": new_user_form})

    else:
        new_form = forms.RegisterForm()
        return render(request, 'registration/register.html', {"signup_form": new_form})

