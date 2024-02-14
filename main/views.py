from django.shortcuts import render, redirect
from . import models
from django.db.models import Q

def index(request):
    q = request.GET.get('q')
    if q:
        products = models.Product.objects.filter(Q(name__icontains=q) | Q(description__icontains=q))
    else: 
        products = models.Product.objects.filter(quantity__gt=0)
    categorys = models.Category.objects.all()
    category_id = request.GET.get('category_id')
    if category_id:
        products.filter(category_id=category_id)
    context = {
        'products':products,
        'categorys':categorys
    }
    return render(request, 'index.html', context)


def product_detail(request, id):
    product = models.Product.objects.get(id=id)
    categorys = models.Category.objects.all()
    recomendation = models.Product.objects.filter(
        category_id=product.category.id).exclude(id=product.id)[:3]
    images = models.ProductImage.objects.filter(product_id=product.id)
    is_saved = None
    
    # way 1
    # try:
    #     models.WishList.objects.get(user=request.user, product=product)
    #     is_saved = True
    # except:
    #     is_saved = False

    # way 2
    objects = models.WishList.objects.filter(user=request.user, product=product)
    if objects:
        is_saved = objects.first().id
    else:
        is_saved = False
    print(is_saved)

    # _,b = models.WishList.objects.get_or_create(user=request.user, product=product)
    # a,b = models.WishList.objects.get_or_create(user=request.user, product=product)
    # print(a)
    # print(b)
    context = {
        'product':product,
        'categorys':categorys,
        'recomendation':recomendation,
        'images':images,
        'range':range(product.review), # 0
        'range_passiv':range(5-product.review), # 5
        'is_saved':is_saved
    }
    return render(request, 'product/detail.html', context)


def carts(request):
    active = models.Cart.objects.filter(is_active=True, user=request.user)
    in_active = models.Cart.objects.filter(is_active=False, user=request.user)
    context = {
        'active':active,
        'in_active':in_active
    }
    return render(request, 'cart/carts.html', context)


def cart_detail(request, id):
    cart = models.Cart.objects.get(id=id)
    items = models.CartProduct.objects.filter(card=cart)
    context = {
        'cart':cart,
        'items':items
    }
    return render(request, 'cart/cart_detail.html', context)


def cart_detail_delete(request):
    item_id = request.GET['items_id']
    item = models.CartProduct.objects.get(id=item_id)
    cart_id = item.card.id
    item.delete()
    return redirect('main:cart_detail', cart_id)


def create_wish_list(request):
    # user = request.user
    # product = models.Product.objects.get(id=request.POST['product_id'])
    # models.WishList.objects.create(
    #     user=user,
    #     product=product # obj
    # )
    models.WishList.objects.create(
        user=request.user,
        product_id=request.GET['product_id'] # id
    )
    return redirect('main:index')


def list_wish_list(request):
    objects = models.WishList.objects.filter(user=request.user)
    return render(request, 'wish/list.html', {'objects':objects})


def delete_wish_list(request):
    models.WishList.objects.get(id=request.GET['id']).delete()
    return redirect('main:list_wish_list')



def edit_profile(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        email = request.POST['email']
        user = request.user
        user.username = username
        user.first_name = first_name
        user.email = email
        user.save()
    return render(request, 'profile/edit.html')


def set_password(request):

    old = request.POST['old']
    new = request.POST['new']
    confirm = request.POST['confirm']
    user = request.user
    if user.check_password(old) and new == confirm:
        user.set_password(new)
        user.save()
    return redirect('main:edit_profile')


