# cars/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q
from .models import *
from .forms import *
from django import forms

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=False, help_text='Opcional. Usado para recuperação de senha.')
    
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customizar mensagens de ajuda
        self.fields['username'].help_text = '150 caracteres ou menos. Apenas letras, números e @/./+/-/_'
        self.fields['password1'].help_text = 'Mínimo 8 caracteres. Não pode ser muito similar ao nome de usuário.'
        self.fields['password2'].help_text = 'Digite a mesma senha novamente para confirmação.'

def registro(request):
    if request.user.is_authenticated:
        return redirect('feed')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            
            # Salvar email se fornecido
            if form.cleaned_data.get('email'):
                user.email = form.cleaned_data.get('email')
            
            user.save()
            
            # Criar perfil do usuário
            Profile.objects.create(user=user)
            
            # Fazer login automático
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            
            # Mensagem de sucesso
            messages.success(request, f'Bem-vindo ao CarSocial, {username}! 🚗')
            
            return redirect('feed') 
    else:
        form = CustomUserCreationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'cars/registro.html', context)

# View opcional para completar perfil após registro
from django.contrib.auth.decorators import login_required

# Forms.py - Formulário ainda mais customizado (opcional)
class RegistroForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Escolha um nome de usuário',
            'autofocus': True,
        })
    )
    
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'seu@email.com (opcional)',
        })
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite uma senha forte',
        })
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme sua senha',
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise forms.ValidationError('O nome de usuário deve ter pelo menos 3 caracteres.')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este email já está em uso.')
        return email

@login_required
def feed(request):
    # Pegar posts dos usuários que o usuário atual segue + seus próprios posts
    seguindo_ids = request.user.seguindo.values_list('seguindo_id', flat=True)
    posts = Post.objects.all()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.save()
            return redirect('feed')
    else:
        form = PostForm()
    
    context = {
        'posts': posts,
        'form': form,
    }
    return render(request, 'cars/feed.html', context)

@login_required
def perfil(request, username):
    usuario = get_object_or_404(User, username=username)
    posts = usuario.posts.all()
    esta_seguindo = request.user.seguindo.filter(seguindo=usuario).exists()
    
    context = {
        'usuario': usuario,
        'posts': posts,
        'esta_seguindo': esta_seguindo,
    }
    return render(request, 'cars/perfil.html', context)

@login_required
def curtir_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.curtidas.all():
        post.curtidas.remove(request.user)
    else:
        post.curtidas.add(request.user)
    return redirect('feed')

@login_required
def seguir_usuario(request, username):
    usuario_a_seguir = get_object_or_404(User, username=username)
    if usuario_a_seguir != request.user:
        Seguidor.objects.get_or_create(
            usuario=request.user,
            seguindo=usuario_a_seguir
        )
    return redirect('perfil', username=username)

@login_required
def deixar_de_seguir(request, username):
    usuario_a_deixar = get_object_or_404(User, username=username)
    Seguidor.objects.filter(
        usuario=request.user,
        seguindo=usuario_a_deixar
    ).delete()
    return redirect('perfil', username=username)
