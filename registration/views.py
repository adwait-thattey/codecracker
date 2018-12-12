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
from questions.utils import run_in_background

@run_in_background
def send_account_activation_email(request, user_instance):
    current_site = get_current_site(request)
    email_subject = "Activate Your CodeCracker Account "
    email_message = render_to_string('registration/email_sent.html',
                                     {'user_fullname': user_instance.get_full_name(),
                                      'domain': current_site.domain,
                                      'uid': urlsafe_base64_encode(
                                          force_bytes(
                                              user_instance.pk)).decode(),
                                      'token': account_confirmation_token.make_token(
                                          user_instance),
                                      })

    user_instance.email_user(email_subject, email_message)
    connection.close()
    return

    # return redirect('registration:account_activation_email_sent')

def email_confirmation_required(func):
    """
    A decorator which allows to access url only if email for current user has been confirmed.
    THE DECORATOR login_required MUST ALWAYS PRECEDE THIS
    """

    def checker(request, *args, **kwargs):
        if request.user.emailconfirmation.email_confirmed is True:
            return func(request, *args, **kwargs)

        else:
            return render(request, "registration/email_not_confirmed.html")

    return checker

@login_required
def generate_new_activation_link(request):
    send_account_activation_email(request, request.user)
    return render(request, "registration/email_confirmation.html")


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

            send_account_activation_email(request,new_user)
            return render(request, "registration/email_confirmation.html")
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
        return render(request, "registration/email_confirmed.html")
    else:
        return render(request, "registration/email_activation_link_invalid.html")

def logout_view(request):
    logout(request)
    return redirect('landing')

@login_required
@email_confirmation_required
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
        return render(request, 'registration/profile.html', {'form':form})
    context = {
        'form': form,
        'questions':questions,
        'contests':contests,
        'submissions':submissions,
        "recent_submissions":recent_submissions,
    }
    return render(request, 'registration/profile.html', context)
