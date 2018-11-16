from django.shortcuts import render
from django.http import HttpResponse
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_confirmation_token
from django.core.mail import EmailMessage
from django.core.mail import send_mail
# Create your views here.
def signup(request):
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
            return render(request, 'registration/register.html', {"signup_form": new_user_form})
    else:
        new_form = RegisterForm()
        return render(request, 'registration/register.html', {"signup_form": new_form})

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
