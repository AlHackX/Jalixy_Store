from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, authenticate
from django.http import HttpResponse
from storeApp.models import Product, Review
from storeApp.forms import ReviewForm, CustomUserCreationForm, CustomAuthenticationForm

# Create your views here.
def index(request):

    products = Product.objects.all()
    return render(request, 'storeApp/index.html', {'products' : products})

def create_list_products():
    if Product.objects.exists():
        return

    list_products = [
        {
            'name' : 'Audifonos Gamer',
            'description' : 'Los mejores audifonos gamer',
            'full_cost' : 1200.00,
            'offer_cost' : 1000.00,
            'imagen' : 'audifonos_gamer.jpg'
        },
        {
            'name' : 'Mouse Gamer',
            'description' : 'El mouse mas versatil del mundo gamer',
            'full_cost' : 700.00,
            'offer_cost' : None,
            'imagen' : 'mouse_gamer.jpg'
        },
        {
            'name' : 'Teclado Gamer',
            'description' : 'El teclado mas bonito',
            'full_cost' : 800.00,
            'offer_cost' : None,
            'imagen' : 'teclado_gamer.jpg'
        },
        {
            'name' : 'Teclado Gamer 25%',
            'description' : 'Chiquito pero bonito',
            'full_cost' : 500.00,
            'offer_cost' : None,
            'imagen' : 'teclado_gamer_25.jpg'
        },
        {
            'name' : 'Mouse Pad',
            'description' : 'Visualmente hermoso y comodamente bueno',
            'full_cost' : 300.00,
            'offer_cost' : None,
            'imagen' : 'mousepad.jpg'
        },
        {
            'name' : 'Microfono',
            'description' : 'Tu voz aun mas hermosa',
            'full_cost' : 1200.00,
            'offer_cost' : 600.00,
            'imagen' : 'microfono.jpg'
        },
        {
            'name' : 'Monitor Vertical',
            'description' : 'Ahora podras ver los comentarios de YouTube con mejor vistazo',
            'full_cost' : 1500.00,
            'offer_cost' : 1000.00,
            'imagen' : 'monitor_vertical.jpg'
        },
        {
            'name' : 'Monitor Horizontal',
            'description' : 'Un mejor vistazo a tus tareas pendientes',
            'full_cost' : 1500.00,
            'offer_cost' : 1000.00,
            'imagen' : 'monitor_horizontal.jpg'
        },
        {
            'name' : 'LEDs RGB',
            'description' : 'Para que tu cuarto se vea mas bonito',
            'full_cost' : 300.00,
            'offer_cost' : 200.00,
            'imagen' : 'leds.jpg'
        },
        {
            'name' : 'Silla Gamer',
            'description' : 'Extrema comodidad para mil horas de juego',
            'full_cost' : 2500.00,
            'offer_cost' : 1500.00,
            'imagen' : 'silla_gamer.jpg'
        },
        {
            'name' : 'PC Gamer',
            'description' : 'Mil horas de juego sin limites',
            'full_cost' : 9000.00,
            'offer_cost' : 7500.00,
            'imagen' : 'pc_gamer.jpg'
        },
        {
            'name' : 'Focos Inteligentes',
            'description' : 'Controla el brillo a tu gusto',
            'full_cost' : 700.00,
            'offer_cost' : 500.00,
            'imagen' : 'focos_inteligentes.jpg'
        },
    ]

    for product in list_products:
        Product.objects.get_or_create(
            product_name = product['name'],
            product_description = product['description'],
            product_full_cost = product['full_cost'],
            product_offer_cost = product.get('offer_cost'),
            imagen = product.get('imagen', 'default.jpg')
        )

def add_to_cart(request, product_id):
    product = Product.objects.get(id = product_id)
    
    #Inicializar el carrito en la sesión si no existe
    if 'cart' not in request.session:
        request.session['cart'] = []
    
    #Agregar el ID del producto al carrito
    request.session['cart'].append(product.id)
    request.session.modified = True             #Guardar cambios en la sesión
    
    return redirect('cart')

def cart(request):
    #Obtener los productos del carrito desde la sesión
    cart_items = []
    if 'cart' in request.session:
        for item_id in request.session['cart']:
            try:
                product = Product.objects.get(id=item_id)
                cart_items.append(product)
            except Product.DoesNotExist:
                pass
    
    #Calcular total
    total = sum(item.product_offer_cost or item.product_full_cost for item in cart_items)
    
    return render(request, 'storeApp/carrito.html', {
        'cart_items': cart_items,
        'total': total
    })

def remove_from_cart(request, product_id):
    if 'cart' in request.session:
        #Elimina solo la primera ocurrencia del ID (evita duplicados)
        try:
            request.session['cart'].remove(product_id)
            request.session.modified = True             #Guarda los cambios
        except ValueError:
            pass                                        #Si el ID no está en el carrito
    return redirect('cart')                             #Redirige de vuelta al carrito

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id = product_id)
    reviews = Review.objects.filter(product = product).order_by('-date')
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit = False)
            review.user = request.user
            review.product = product
            review.save()
            return redirect('add_review', product_id = product.id)
    else:
        form = ReviewForm()

    return render(request, 'storeApp/add_review.html', {
        'form': form,
        'product': product,
        'reviews': reviews
    })

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id = review_id)
    
    #Verificar que el usuario es el autor o es superuser
    if request.user == review.user or request.user.is_superuser:
        review.delete()
    return redirect('add_review', product_id = review.product.id)

def product_details(request, product_id):
    product = get_object_or_404(Product, id = product_id)
    return render(request, 'storeApp/product_details.html', {
        'product': product,
        'reviews': product.reviews.all().order_by('-date')          #Más recientes primero
    })

def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            if user is not None:
                auth_login(request, user)
                return redirect('index')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})