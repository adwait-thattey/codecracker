from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from .forms import RegisterForm, ProfileEditForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_confirmation_token
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from .forms import GoogleRegisterFrom, ProfileEditForm
from django.core.mail import send_mail
from .models import UserProfile
from questions.models import Question, Submission
from contests.models import Contest
# Create your views here.
def signup(request):
    google_form = GoogleRegisterFrom()
    if request.method == "POST":
        new_user_form = RegisterForm(request.POST)
        if new_user_form.is_valid():
            new_user = User.objects.create_user(
                    username=new_user_form.cleaned_data["username"],
                    password=new_user_form.cleaned_data["password"],
                    email=new_user_form.cleaned_data["email"]
                )

            new_user.first_name = new_user_form.cleaned_data["first_name"]
            new_user.last_name = new_user_form.cleaned_data["last_name"]
            new_user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('registration/email.html', {
                'user': new_user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(new_user.pk)).decode(),
                'token':account_confirmation_token.make_token(new_user),
            })
            to_email = new_user_form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
        else:
            return render(request, 'registration/register.html', {"signup_form": new_user_form, "google_form":google_form})
    else:
        new_form = RegisterForm()
        return render(request, 'registration/register.html', {"signup_form": new_form, "google_form":google_form})

def google_sign_in(request):
    if request.method == "GET":
        raise Http404

    else:
        google_form = GoogleRegisterFrom(request.POST)

        if google_form.is_valid():
            u = User.objects.filter(email=google_form.cleaned_data["gog_email"])
            if u.exists():
                login(request, u[0])
                return redirect('home')
            else:
                user = User.objects.create(email=google_form.cleaned_data["gog_email"],
                                    username=google_form.cleaned_data["gog_email"].split('@')[0],
                                    first_name=google_form.cleaned_data["gog_full_name"].split(' ')[0],
                                    last_name=google_form.cleaned_data["gog_full_name"].split(' ')[1]
                                    )

                login(request,user)
                return redirect('home')

        else:
            return HttpResponse("There was some error. Please try again later")

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        new_user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        new_user = None
    if new_user is not None and account_confirmation_token.check_token(new_user, token):
        new_user.emailconfirmation.email_confirmed = True
        new_user.emailconfirmation.save()
        login(request, new_user, backend = "django.contrib.auth.backends.ModelBackend")
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def logout_view(request):
    logout(request)
    return redirect('landing')

@login_required
def profile(request):
    instance = get_object_or_404(UserProfile, user= request.user)
    questions= Question.objects.filter(author= request.user)
    contests= Contest.objects.filter(author= request.user)
    submissions= Submission.objects.filter(user= request.user).order_by('-submitted_on')
    recent_submissions= submissions[:4]
    form = ProfileEditForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponse("edited successfully!!!")
    context = {
        'form': form,
        'questions':questions,
        'contests':contests,
        'submissions':submissions,
        "recent_submissions":recent_submissions,
    }
    return render(request, 'registration/profile.html', context)
