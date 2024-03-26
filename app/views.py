from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .utils import is_ajax, classify_face
import base64
from logs.models import Log
from django.core.files.base import ContentFile 
from django.contrib.auth.models import User
from profiles.models import Profile
from dal import autocomplete
from django.contrib.auth.models import User

def login_view(request):
    return render(request, 'login.html', {})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    return render(request, 'main.html', {})

def find_user_view(request):
    if not is_ajax(request):
        return JsonResponse({'success': False, 'message': 'Invalid request'})
    if is_ajax(request) and request.method == 'POST':
        img = request.POST.get('photo')  # Get the photo data correctly
        if img:  # Check if img is not None
            _, str_img = img.split(';base64,')
            decoded_file = base64.b64decode(str_img)
            x = Log()
            x.photo = ContentFile(decoded_file, name='upload.jpg')
            x.save()
            res = classify_face(x.photo.path)
            user_exists = User.objects.filter(username=res).exists()
            if user_exists:
                user = User.objects.get(username=res)
                profile = Profile.objects.get(user=user)
                x.profile = profile
                x.save()
                login(request, user)
                return JsonResponse({'success': True, 'message': 'User found!'})
        else:
            return JsonResponse({'success': False, 'message': 'No photo provided'})
    return JsonResponse({'success': False, 'message': 'User not found!'})



class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # No olvides manejar tus permisos y seguridades aquí.
        qs = User.objects.all()

        if self.q:
            qs = qs.filter(username__istartswith=self.q)

        return qs
    
    def get_result_label(self, item):
        # Cambiar la representación del resultado para mostrar el nombre y apellido.
        return f"{item.first_name} {item.last_name} ({item.username})"