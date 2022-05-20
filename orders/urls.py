from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("cart", views.cart_, name="cart"),
    path("add/salad/<int:salad_id>", views.add_salad, name="salad"),
    path("add/pasta/<int:pasta_id>", views.add_pasta, name="pasta"),
    path("add/dinner_platter/<int:dinner_id>", views.add_dinner_platter, name="dinner_platter"),
    path("add/subs/<int:sub_id>", views.add_sub, name="sub"),
    path("add/pizza/<int:pizza_id>", views.add_pizza_notopping, name="pizza"),
    path("add/1/pizza/<int:pizza_id>/<int:topping1_id>", views.add_pizza_1topping, name="pizza1"),
    path("add/2/pizza/<int:pizza_id>/<int:topping1_id>/<int:topping2_id>", views.add_pizza_2topping, name="pizza2"),
    path("add/3/pizza/<int:pizza_id>/<int:topping1_id>/<int:topping2_id>/<int:topping3_id>", views.add_pizza_3topping,
         name="pizza3"),
    path("add/special/<int:pizza_id>", views.add_special, name="special"),
    path("confirm/<int:order_id>", views.confirm_order, name="confirm_order"),
    path('orders', views.myorders, name="m_order"),
    path("login", views.loginuser, name="login"),
    path("logout", views.logoutuser, name="logout"),
    path("register", views.register_user, name="reguser"),
    path("del/cart", views.deleted_cart, name="delete_cart"),
    path("coming_orders", views.up_orders , name="uporders"),
    path("markCompleted/<int:id_order>", views.mark_complete)
]
