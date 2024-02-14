from itertools import chain

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.exceptions import FieldError

from main import models
from . funcs import search_with_fields, pagenator_page



def dashboard(request):
    categorys = models.Category.objects.all().count()
    products = models.Product.objects.all().count()
    users = User.objects.all().count()
    context = {
        'categorys':categorys,
        'products':products,
        'users':users,
    }
    return render(request, 'dashboard/index.html', context)


def category_list(request):
    categorys = models.Category.objects.all()
    return render(request, 'category/list.html', {'categorys':categorys})


def category_detail(request, id):
    category = models.Category.objects.get(id=id)
    products = models.Product.objects.filter(category=category, is_active=True)
    context = {
        'category':category,
        'products':products
    }
    return render(request, 'category/list.html', context)


def category_update(request, id):
    category = models.Category.objects.get(id=id)
    category.name = request.POST['name']
    category.save()
    return redirect('category_detail', category.id)


def category_delete(request, id):
    category = models.Category.objects.get(id=id)
    category.delete()
    return redirect('category_list')




# products

def products(request):
    products = models.Product.objects.all()
    return render(request, 'dashboard/products/list.html', {'products':products})


def product_create(request):
    categorys = models.Category.objects.all()
    context = {
        'categorys':categorys
    }
    if request.method == "POST":
        name = request.POST['name']
        description = request.POST['description']
        quantity = request.POST['quantity']
        price = request.POST['price']
        currency = request.POST['currency']
        baner_image = request.FILES['baner_image']
        category_id = request.POST['category_id']
        images = request.FILES.getlist('images')
        product = models.Product.objects.create(
            name=name,
            description = description,
            quantity=quantity,
            price=price,
            currency=currency,
            baner_image=baner_image,
            category_id=category_id
        )
        for image in images:
            models.ProductImage.objects.create(
                image=image,
                product=product
            )

    return render(request, 'dashboard/products/create.html', context)


def product_detail(request, id):
    product = models.Product.objects.get(id=id)
    enters = models.EnterProduct.objects.filter(product=product)
    outs = models.CartProduct.objects.filter(product=product, card__is_active=False)
    query_set = sorted(
        chain(
            enters,
            outs
        ),
        key = lambda x : x.created_at
    )
    # for i in query_set:
    #     try:
    #         i.card
    #         print(f"chiqish {i}")
    #     except:
    #         print(f"kirish {i}")

    return render(request, 'dashboard/products/detail.html', {'query_set':query_set})

def create_enter(request):
    if request.method == 'POST':
        product_id = request.POST['product_id']
        quantity = int(request.POST['quantity'])
        models.EnterProduct.objects.create(
            product_id=product_id,
            quantity=quantity
        )
        return redirect('dashboard:list_enter')
    return render(request, 'dashboard/enter/create.html', {'products':models.Product.objects.all()})


def update_enter(request, id):
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        enter = models.EnterProduct.objects.get(id=id)
        enter.quantity = quantity
        enter.save()
    return redirect('dashboard:list_enter')


def delete_enter(request, id):
    models.EnterProduct.objects.get(id=id).delete()
    return redirect('dashboard:list_enter')



def list_enter(request):
    result = search_with_fields(request)
    try: 
        enters = models.EnterProduct.objects.filter(**result)

    except FieldError as err:
        del result[err.__doc__.split()[3][1:-1]]
        enters = models.EnterProduct.objects.filter(**result)

    context = {'enters': pagenator_page(enters, 1, request)}
    return render(request, 'dashboard/enter/list.html', context)

# required
# def list_enter(request):
#     name = request.GET.get('name')
#     quantity = request.GET.get('quantity')
#     created_at = request.GET.get('created_at')
#     if name and quantity and created_at:
#         enters = models.EnterProduct.objects.filter(
#             product__name=name,
#             quantity=quantity,
#             created_at__gt = created_at,
#             created_at__lte = created_at,
#         )
#     else:
#         enters = models.EnterProduct.objects.all()
#     context = {'enters':enters}
#     return render(request, 'dashboard/enter/list.html', context)