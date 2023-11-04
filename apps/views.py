
from django.contrib.auth.tokens import PasswordResetTokenGenerator
account_activation_token = PasswordResetTokenGenerator()

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.contrib import messages
from authentification import settings

def home(request):
    return render(request, 'apps/index.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Vérification de l'existence du nom d'utilisateur
        if User.objects.filter(username=username).exists():
            return render(request, 'apps/register.html', {'error': 'Ce nom d\'utilisateur existe déjà. Veuillez en choisir un autre.'})

        # Vérification de l'existence de l'e-mail
        if User.objects.filter(email=email).exists():
            return render(request, 'apps/register.html', {'error': 'Cet e-mail existe déjà. Veuillez en choisir un autre.'})

        # Vérification de la validité de l'e-mail
        if '@' not in email:
            return render(request, 'apps/register.html', {'error': 'L\'e-mail n\'est pas valide.'})

        # Vérification de la validité du mot de passe
        if len(password) < 8:
            return render(request, 'apps/register.html', {'error': 'Le mot de passe doit contenir au moins 8 caractères.'})

        # Vérification de la correspondance entre le mot de passe et la confirmation
        if password != confirm_password:
            return render(request, 'apps/register.html', {'error': 'Les mots de passe ne sont pas identiques.'})

        # Créer un nouvel utilisateur
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False  # Désactiver le compte pour l'instant
        user.save()

        # Envoyer l'e-mail d'activation
        current_site = get_current_site(request)
        send_activation_email(user, current_site)

        messages.success(request, "Votre compte est bien créé et est en attente de validation. Veuillez consulter votre e-mail pour activer votre compte.")

        return redirect('login')

    return render(request, 'apps/register.html')

def send_activation_email(user, current_site):
    email_subject_confirmation = 'Activation de votre compte'
    activation_link = reverse('activate', kwargs={'uidb64': urlsafe_base64_encode(force_bytes(user.pk)), 'token': account_activation_token.make_token(user)})
    
    context = {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'activation_link': activation_link
    }

    messageConfirmation = render_to_string('confirm_email.html', context)
    
    email_confirmation = EmailMessage(
        email_subject_confirmation,
        messageConfirmation,
        settings.EMAIL_HOST_USER,
        [user.email],
    )
    
    email_confirmation.content_subtype = "html"
    email_confirmation.send()






from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

def activate(request, uidb64, token):
    
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
    
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Votre compte est activé avec succès.')
            return redirect('login')  # Rediriger vers la page de connexion
        
        else:
            messages.error(request, 'Le lien d\'activation est invalide ou a expiré.')
            return redirect('home')
        
from  django.contrib.auth  import authenticate, login       
        
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Vous avez bien connecté.')
            return redirect('home')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
            return redirect('login')

    return render(request, 'apps/login.html')

        
from django.contrib.auth import logout
def logOut(request):
    logout(request)
    messages.success(request, 'Vous avez été deconnecté.')
    
    return render(request,'apps/index.html')