
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    foto_perfil = models.ImageField(upload_to='perfis/', blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Perfil de {self.user.username}'


class Post(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    conteudo = models.TextField()
    imagem = models.ImageField(upload_to='posts/', blank=True, null=True)
    criado_em = models.DateTimeField(default=timezone.now)
    curtidas = models.ManyToManyField(User, related_name='posts_curtidos', blank=True)
    
    class Meta:
        ordering = ['-criado_em']
    
    def __str__(self):
        return f'Post de {self.autor.username} - {self.criado_em}'
    
    def total_curtidas(self):
        return self.curtidas.count()

class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    conteudo = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['criado_em']
    
    def __str__(self):
        return f'Comentário de {self.autor.username}'

class Seguidor(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seguindo')
    seguindo = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seguidores')
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('usuario', 'seguindo')
    
    def __str__(self):
        return f'{self.usuario} segue {self.seguindo}'