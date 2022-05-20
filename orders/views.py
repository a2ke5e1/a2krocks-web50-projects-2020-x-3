from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, reverse, redirect

from .forms import SignUpForm
from .models import sub, pasta, salad, dinner_platter, pizza_types, cart, toppings, order



# Create your views here.
def index(request):
    context = {
        "subs_small": sub.objects.filter(size="S"),
        "subs_large": sub.objects.filter(size="L"),
        "pastas": pasta.objects.all(),
        "salads": salad.objects.all(),
        "dinner_platters_small": dinner_platter.objects.filter(size="S"),
        "dinner_platters_large": dinner_platter.objects.filter(size="L"),
        "pizza_small": pizza_types.objects.filter(type="S"),
        "pizza_large": pizza_types.objects.filter(type="L"),
        "toppings": toppings.objects.all(),
        "user": request.user,
        "user_is": request.user.is_anonymous,
        "user_is_staff": request.user.is_staff
    }
    return render(request, 'orders/index.html', context)


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'orders/register.html', {'form': form})


def cart_(request):

    if request.user.is_anonymous:
        return redirect("login")

    cart.objects.get_or_create(user=request.user)

    mCart = cart.objects.get(user=request.user)
    salad_names = mCart.salad_name[:-1].split(",")
    unique_salad_name = {}
    for salad_name in salad_names:
        if salad_name in unique_salad_name:
            unique_salad_name[salad_name] += 1
        else:
            unique_salad_name[salad_name] = 1

    pasta_names_ = mCart.pasta_name[:-1].split(",")
    unique_pasta_name = {}
    for pasta_name_ in pasta_names_:
        if pasta_name_ in unique_pasta_name:

            unique_pasta_name[pasta_name_] += 1
        else:
            unique_pasta_name[pasta_name_] = 1

    sub_names_ = mCart.sub_name[:-1].split(",")
    unique_sub_name = {}
    for sub_name_ in sub_names_:
        if sub_name_ in unique_sub_name:

            unique_sub_name[sub_name_] += 1
        else:
            unique_sub_name[sub_name_] = 1

    dp_names_ = mCart.dp[:-1].split(",")
    unique_dp_name = {}
    for dp_name_ in dp_names_:
        if dp_name_ in unique_dp_name:

            unique_dp_name[dp_name_] += 1
        else:
            unique_dp_name[dp_name_] = 1

    pizza_names = mCart.pizza_name[:-1].split(",")
    unique_pizza_name = {}
    for pizza_n in pizza_names:
        if pizza_n in unique_pizza_name:

            unique_pizza_name[pizza_n] += 1
        else:
            unique_pizza_name[pizza_n] = 1

    print(mCart)
    _cart = True

    if str(mCart) == " -  -  - -  - - 0.00":
        _cart = False

    print(_cart)

    context = {
        "salad_names": unique_salad_name,
        "pasta_names": unique_pasta_name,
        "sub_names": unique_sub_name,
        "dp_names": unique_dp_name,
        "pizza_names": unique_pizza_name,
        "total": mCart.total_cost,
        "order_id": mCart.id,
        "allow_order": _cart

    }

    return render(request, "orders/cart.html", context)


def myorders(request):
    if request.user.is_anonymous:
        return redirect("login")

    mCart = order.objects.filter(user=request.user).order_by('-id')

    mOrders = []



    for i in mCart:
        pizza_names = i.pizza_name[:-1].split(",")
        unique_pizza_name = {}
        for pizza_n in pizza_names:
            if pizza_n in unique_pizza_name:

                unique_pizza_name[pizza_n] += 1
            else:
                unique_pizza_name[pizza_n] = 1

        dp_names_ = i.dp[:-1].split(",")
        unique_dp_name = {}
        for dp_name_ in dp_names_:
            if dp_name_ in unique_dp_name:

                unique_dp_name[dp_name_] += 1
            else:
                unique_dp_name[dp_name_] = 1

        sub_names_ = i.sub_name[:-1].split(",")
        unique_sub_name = {}
        for sub_name_ in sub_names_:
            if sub_name_ in unique_sub_name:

                unique_sub_name[sub_name_] += 1
            else:
                unique_sub_name[sub_name_] = 1
        salad_names = i.salad_name[:-1].split(",")
        unique_salad_name = {}
        for salad_name in salad_names:
            if salad_name in unique_salad_name:
                unique_salad_name[salad_name] += 1
            else:
                unique_salad_name[salad_name] = 1

        pasta_names_ = i.pasta_name[:-1].split(",")
        unique_pasta_name = {}
        for pasta_name_ in pasta_names_:
            if pasta_name_ in unique_pasta_name:

                unique_pasta_name[pasta_name_] += 1
            else:
                unique_pasta_name[pasta_name_] = 1
        mOrders.append(
            {
                "orders_id": i.id,
                "pizza_name": unique_pizza_name,
                "dp_name": unique_dp_name,
                "sub_name": unique_sub_name,
                "pasta_name": unique_pasta_name,
                "salad_name": unique_salad_name,
                "status": i.status,
                "total": i.total_cost
            }
        )

    if mOrders == []:
        return  HttpResponse("No Orders")
    context = {
        "mOrders": mOrders,
    }

    return render(request, 'orders/my_order.html', context)


def confirm_order(request, order_id):
    mCart = cart.objects.get(pk=order_id)
    mOrder = order.objects.create(user=request.user)

    mOrder.pizza_name = mCart.pizza_name
    mOrder.sub_name = mCart.sub_name
    mOrder.pasta_name = mCart.pasta_name
    mOrder.dp = mCart.dp
    mOrder.total_cost = mCart.total_cost
    mOrder.salad_name = mCart.salad_name

    mOrder.status = "p"
    mOrder.save()

    mCart.delete()

    return HttpResponse("Done")


def add_salad(request, salad_id):
    try:
        cart.objects.get_or_create(user=request.user)
        mCart = cart.objects.get(user=request.user)
        mSalad = salad.objects.get(pk=salad_id)
        mCart.salad_name += f"{mSalad.name},"
        mCart.total_cost += mSalad.price

        mCart.save()
    except:
        return HttpResponse("bad")

    return HttpResponse("success")


def add_pasta(request, pasta_id):
    try:
        cart.objects.get_or_create(user=request.user)
        mCart = cart.objects.get(user=request.user)
        mPasta = pasta.objects.get(pk=pasta_id)

        mCart.pasta_name += f"{mPasta.name},"
        mCart.total_cost += mPasta.price

        mCart.save()
    except:
        return HttpResponse("bad")

    return HttpResponse("success")


def add_dinner_platter(request, dinner_id):
    try:
        cart.objects.get_or_create(user=request.user)
        mCart = cart.objects.get(user=request.user)
        mDP = dinner_platter.objects.get(pk=dinner_id)

        mCart.dp += f"{mDP.name}-{mDP.size},"
        mCart.total_cost += mDP.price

        mCart.save()
    except:
        return HttpResponse("bad")

    return HttpResponse("success")


def add_sub(request, sub_id):
    try:
        cart.objects.get_or_create(user=request.user)
        mCart = cart.objects.get(user=request.user)
        mSub = sub.objects.get(pk=sub_id)

        mCart.sub_name += f"{mSub.name}-{mSub.size},"
        mCart.total_cost += mSub.price

        mCart.save()
    except:
        return HttpResponse("bad")

    return HttpResponse("success")


def add_pizza_notopping(request, pizza_id):
    try:
        cart.objects.get_or_create(user=request.user)
        mCart = cart.objects.get(user=request.user)
        mPz = pizza_types.objects.get(pk=pizza_id)

        mCart.pizza_name += f"{mPz.name}-{mPz.type}-Cheese,"
        mCart.total_cost += mPz.base_price

        mCart.save()
    except:
        return HttpResponse("bad")

    return HttpResponse("success")

def add_special(request, pizza_id):
    try:
        cart.objects.get_or_create(user=request.user)
        mCart = cart.objects.get(user=request.user)
        mPz = pizza_types.objects.get(pk=pizza_id)

        mCart.pizza_name += f"{mPz.name}-{mPz.type}-Special,"
        mCart.total_cost += mPz.special_price

        mCart.save()
    except:
        return HttpResponse("bad")

    return HttpResponse("success")


def add_pizza_1topping(request, pizza_id, topping1_id):
    try:
        cart.objects.get_or_create(user=request.user)
        mCart = cart.objects.get(user=request.user)
        mPz = pizza_types.objects.get(pk=pizza_id)
        mTopp = toppings.objects.get(pk=topping1_id)

        mCart.pizza_name += f"{mPz.name}-{mPz.type}-Cheese-{mTopp.name},"
        mCart.total_cost += mPz.topping_price

        mCart.save()
    except:
        return HttpResponse("bad")

    return HttpResponse("success")


def add_pizza_2topping(request, pizza_id, topping1_id, topping2_id):
    try:
        cart.objects.get_or_create(user=request.user)
        mCart = cart.objects.get(user=request.user)
        mPz = pizza_types.objects.get(pk=pizza_id)
        mTopp1 = toppings.objects.get(pk=topping1_id)
        mTopp2 = toppings.objects.get(pk=topping2_id)

        mCart.pizza_name += f"{mPz.name}-{mPz.type}-Cheese-{mTopp1.name}-{mTopp2.name},"
        mCart.total_cost += mPz.topping_price2

        mCart.save()
    except:
        return HttpResponse("bad")

    return HttpResponse("success")


def add_pizza_3topping(request, pizza_id, topping1_id, topping2_id, topping3_id):
    try:
        cart.objects.get_or_create(user=request.user)
        mCart = cart.objects.get(user=request.user)
        mPz = pizza_types.objects.get(pk=pizza_id)
        mTopp1 = toppings.objects.get(pk=topping1_id)
        mTopp2 = toppings.objects.get(pk=topping2_id)
        mTopp3 = toppings.objects.get(pk=topping3_id)

        mCart.pizza_name += f"{mPz.name}-{mPz.type}-Cheese-{mTopp1.name}-{mTopp2.name}-{mTopp3.name},"
        mCart.total_cost += mPz.topping_price3

        mCart.save()
    except:
        return HttpResponse("bad")
    return HttpResponse("success")


def loginuser(request):

    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        username = request.POST["username"]
        pasw = request.POST["passw"]

        user = authenticate(username=username, password=pasw)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return  HttpResponse("Incorrect Credentials")


    return render(request, "orders/login.html")

def logoutuser(request):
    logout(request)
    return  redirect('login')

def deleted_cart(request):
    mCart = cart.objects.get(user=request.user)
    mCart.delete()
    return redirect("index")

def up_orders(request):
    if not request.user.is_staff:
        return redirect("index")

    mCart = order.objects.all().order_by('-id')

    mOrders = []

    for i in mCart:
        pizza_names = i.pizza_name[:-1].split(",")
        unique_pizza_name = {}
        for pizza_n in pizza_names:
            if pizza_n in unique_pizza_name:

                unique_pizza_name[pizza_n] += 1
            else:
                unique_pizza_name[pizza_n] = 1

        dp_names_ = i.dp[:-1].split(",")
        unique_dp_name = {}
        for dp_name_ in dp_names_:
            if dp_name_ in unique_dp_name:

                unique_dp_name[dp_name_] += 1
            else:
                unique_dp_name[dp_name_] = 1

        sub_names_ = i.sub_name[:-1].split(",")
        unique_sub_name = {}
        for sub_name_ in sub_names_:
            if sub_name_ in unique_sub_name:

                unique_sub_name[sub_name_] += 1
            else:
                unique_sub_name[sub_name_] = 1
        salad_names = i.salad_name[:-1].split(",")
        unique_salad_name = {}
        for salad_name in salad_names:
            if salad_name in unique_salad_name:
                unique_salad_name[salad_name] += 1
            else:
                unique_salad_name[salad_name] = 1

        pasta_names_ = i.pasta_name[:-1].split(",")
        unique_pasta_name = {}
        for pasta_name_ in pasta_names_:
            if pasta_name_ in unique_pasta_name:

                unique_pasta_name[pasta_name_] += 1
            else:
                unique_pasta_name[pasta_name_] = 1
        mOrders.append(
            {
                "orders_id": i.id,
                "user": i.user,
                "pizza_name": unique_pizza_name,
                "dp_name": unique_dp_name,
                "sub_name": unique_sub_name,
                "pasta_name": unique_pasta_name,
                "salad_name": unique_salad_name,
                "status": i.status,
                "total": i.total_cost
            }
        )

    if mOrders == []:
        return HttpResponse("No Orders")
    context = {
        "mOrders": mOrders,
    }

    return render(request, 'orders/up_order.html', context)

def mark_complete(request, id_order):

    if request.user.is_staff:
        try:
            mOrder = order.objects.get(pk=id_order)
            mOrder.status = "c"
            mOrder.save()
            return HttpResponse("success")
        except:
            return HttpResponse("bad")
    else:
        return HttpResponse("You are not allowed")