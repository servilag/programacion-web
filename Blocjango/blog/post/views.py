from django.shortcuts import render,redirect
from .forms import PostForm, CommentForm, Registro
from django.contrib.auth.models import User  # Importa el modelo User
from django.contrib.auth.forms import UserCreationForm #user creation de django forms
from django.contrib import messages
from .models import Post, Category  # Importar modelo post, y Category
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404


# Create your views here.

def index(request):
    publicaciones_recientes = Post.objects.all().order_by('-created_at')[:6]  # Últimas 6 publicaciones
    return render(request, 'post/index.html',{'publicaciones_recientes': publicaciones_recientes})


def categorias(request):
    # Lista de IDs seleccionados
    categorias_ids = request.GET.getlist('categoria') 

    publicaciones = Post.objects.all().prefetch_related('category').order_by('-created_at')

    # filtrar
    if categorias_ids:
        # Usamos __in para buscar publicaciones que tengan CUALQUIERA de esos IDs
        publicaciones = publicaciones.filter(category__id__in=categorias_ids).distinct()

    todas_las_categorias = Category.objects.all()

    return render(request, 'post/categorias.html', {
        'categorias': todas_las_categorias,
        'publicaciones': publicaciones,
    })

@login_required
def publicaciones(request):
    if request.user.is_superuser or request.user.is_staff:
        posts = Post.objects.all().order_by('-created_at')  # Muestra todos los posts
    else:
        posts = Post.objects.filter(author=request.user).order_by('-created_at')  # Muestra solo los del usuario actual
    
    todas_las_categorias = Category.objects.all()
    return render(request, 'post/publicaciones.html', {'posts': posts})

@login_required
def perfil(request):
    # Obtener solo los posts que pertenecen al usuario logueado
    mis_publicaciones = Post.objects.filter(author=request.user)
    
    # Contar la cantidad total
    total_posts = mis_publicaciones.count()
    
    return render(request, 'post/perfil_usuario.html', {
        'total_posts': total_posts,
        'publicaciones': mis_publicaciones 
    })

@login_required
def nueva_publicacion(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES) #para las imagenes
        if form.is_valid():
            #Guardar el post 
            post = form.save(commit=False)
            post.author = request.user # asignar el autor manualmente
            post.save() 
            
            # Guarda las relaciones ManyToMany (las categorías)
            form.save_m2m() 
            
            return redirect('publicaciones')
    else:
        form = PostForm()
    return render(request, 'post/nueva_publicacion.html', {'form': form})

@login_required
def editar_publicacion(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('publicaciones')
    else:
        form = PostForm(instance=post)
    return render(request, 'post/editar_publicacion.html', {'form': form})

@login_required
def eliminar_publicacion(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('publicaciones')
    return render(request, 'post/borrar_publicacion.html', {'post': post})


def detalle_publicacion(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comentarios = post.comments.all().order_by('-created_at')  # Trae todos los comentarios ordenados por fecha
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.post = post
            comentario.author = request.user  # Se asigna el usuario autenticado
            comentario.save()
            return redirect('detalle_publicacion', post_id=post.id)

    return render(request, 'post/detalle_publicacion.html', {
        'post': post,
        'comentarios': comentarios,
        'form': form
    })

def registrar(request):
    if request.method == 'POST':
        form = Registro(request.POST)
        if form.is_valid():
            form.save()
            username= form.cleaned_data.get('username')
            messages.success(request, f'cuenta creada {username}')
            return redirect('index')
    else:
        form = Registro()
    return render(request,'post/registro.html', {'form':form})
