## Сьогодні ми

**Створення інтернет-магазину - Кошик, Checkout та Email**

Привіт! Сьогодні ми переходимо до створення **ключових компонентів e-commerce** - тих функцій, які перетворюють звичайний сайт на повноцінний інтернет-магазин!

За статистикою, **69% користувачів покидають кошики без оплати**. Чому? Складний процес оформлення, незрозумілі форми, відсутність зворотного зв'язку. Сьогодні ви навчитеся створювати користувацький досвід, який конвертує відвідувачів у покупців.

Amazon, Rozetka, Prom - всі вони використовують ті самі принципи, які ми сьогодні вивчимо: зручний кошик, простий checkout процес та своєчасні email сповіщення.

```
Мета уроку: Навчитися створювати професійну систему покупок - від додавання товару в кошик до email підтвердження замовлення.
```

**Сьогодні ми:**

✅ Створимо два типи кошиків - session-based та database-based

✅ Реалізуємо повний checkout процес з адресами доставки

✅ Налаштуємо систему замовлень з транзакціями

✅ Впровадимо email сповіщення для користувачів

✅ З'єднаємо всі компоненти в єдину систему

🎯 **Після цього уроку ви зможете створювати повноцінні e-commerce рішення!**

## Архітектура інтернет магазину

**Архітектура інтернет магазину**

Django — це високорівневий Python веб-фреймворк, який заохочує швидку розробку та чистий, прагматичний дизайн. Його вбудовані функції, такі як аутентифікація, управління базою даних та маршрутизація URL, роблять його сильним вибором для проектів електронної комерції. З Django ви отримуєте надійний фреймворк, який є масштабованим, безпечним та гнучким — ідеальним для динамічної та зростаючої платформи електронної комерції.

Інтернет-магазин — це не просто "показати товари та додати в кошик". Це комплексна система, яка базується на патерні MVT (Model-View-Template) та включає:

```
┌─────────────────────────────────────────────────────────┐
│              E-COMMERCE АРХІТЕКТУРА                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. КАТАЛОГ ТОВАРІВ                                     │
│     ├── Категорії та фільтри                           │
│     ├── Пошук                                           │
│     └── Деталі товару                                   │
│                                                          │
│  2. КОШИК (CART)                                        │
│     ├── Session-based (для гостей)                     │
│     └── Database-based (для користувачів)              │
│                                                          │
│  3. CHECKOUT (Оформлення замовлення)                   │
│     ├── Адреса доставки                                │
│     ├── Спосіб оплати                                  │
│     └── Підтвердження                                  │
│                                                          │
│  4. ЗАМОВЛЕННЯ (ORDERS)                                 │
│     ├── Статуси замовлень                              │
│     ├── Історія замовлень                              │
│     └── Email notifications                             │
│                                                          │
│  5. УПРАВЛІННЯ (для адміністратора)                    │
│     ├── Товари та категорії                            │
│     ├── Замовлення та клієнти                          │
│     └── Звіти та статистика                            │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

**Ключові архітектурні особливості та компоненти Django для e-commerce:**

1. **Модульність та Розширюваність:** Дизайн Django дозволяє інтегрувати безліч сторонніх додатків для розширення функціональності. E-commerce платформи вимагають функціоналу, що включає управління продуктами, автентифікацію користувачів, обробку платежів та інше.
2. **Вбудований інтерфейс адміністратора (Admin Interface):** Django пропонує вбудований інтерфейс адміністратора, який є чудовою відправною точкою для ефективного управління продуктами, замовленнями та клієнтами.
3. **Безпека:** Фреймворк має вбудований захист від поширених веб-вразливостей, таких як CSRF (Cross-Site Request Forgery), SQL-ін'єкції та XSS (Cross-Site Scripting) атаки.
4. **Масштабованість:** Django може обробляти велику кількість користувачів і продуктів, що є важливим для зростаючих e-commerce платформ.
5. **Розділення Логіки:** У великих проектах рекомендується розділяти логіку на окремі додатки (Apps). Наприклад, можна мати додаток `core` для налаштування користувацької моделі та додаток `shop_app` або `cart` для логіки магазину.

## Моделі інтернет-магазину

**Моделі для інтернет-магазину**

**Модель продукту**

Ця модель є основою магазину і містить інформацію про товари.

Приклад моделі `Product` (з розширеними полями):

```
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=150)  # Назва продукту
    description = models.TextField(blank=True)  # Детальний опис
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Ціна
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)  # Зображення
    is_available = models.BooleanField(default=True)  # Чи доступний товар
    created_at = models.DateTimeField(auto_now_add=True)  # Дата створення
    modified_at = models.DateTimeField(auto_now=True)  # Дата останньої зміни


    def __str__(self) -> str:
        return str(self.name)


# Альтернативні поля:
# slug: для унікальних URL продуктів (unique=True)
# inventory: кількість товару на складі
```

**Модель Категорія товарів**

```
class Category(models.Model):
    name = models.CharField('Назва', max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField('Опис', blank=True)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='children',
        verbose_name='Батьківська категорія'
    )
    is_active = models.BooleanField('Активна', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
        ordering = ['name']
    
    def __str__(self):
        return self.name
```

**Модель Профіль користувача**

```
class UserProfile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='profile'
    )
    phone = models.CharField('Телефон', max_length=20, blank=True)
    date_of_birth = models.DateField('Дата народження', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Профіль користувача'
        verbose_name_plural = 'Профілі користувачів'
    
    def __str__(self):
        return f"Профіль {self.user.username}"
```

**Модель Адреса доставки**

```
class ShippingAddress(models.Model):
    """Адреса доставки"""
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='addresses'
    )
    full_name = models.CharField('ПІБ', max_length=200)
    phone = models.CharField('Телефон', max_length=20)
    
    # Адреса
    country = models.CharField('Країна', max_length=100, default='Україна')
    city = models.CharField('Місто', max_length=100)
    postal_code = models.CharField('Поштовий індекс', max_length=20)
    address_line1 = models.CharField('Адреса (рядок 1)', max_length=250)
    address_line2 = models.CharField('Адреса (рядок 2)', max_length=250, blank=True)
    
    is_default = models.BooleanField('За замовчуванням', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Адреса доставки'
        verbose_name_plural = 'Адреси доставки'
        ordering = ['-is_default', '-created_at']
    
    def __str__(self):
        return f"{self.full_name} - {self.city}"
    
    def save(self, *args, **kwargs):
        """Якщо це адреса за замовчуванням, зробити інші не за замовчуванням"""
        if self.is_default:
            ShippingAddress.objects.filter(
                user=self.user, 
                is_default=True
            ).update(is_default=False)
        super().save(*args, **kwargs)
```

## Створення корзини

**Моделі для кошика (База даних)**

Для постійного зберігання вмісту кошика (особливо для зареєстрованих користувачів або перед оформленням замовлення) використовують моделі **Cart** (Кошик) та **CartItem** (Елемент кошика).

Приклад моделі `Cart` та `CartItem` (з прив'язкою до користувача):

```
from django.db import models
from django.conf import settings # Для посилання на модель користувача 
# ... припускаючи, що Product вже визначений
from django.contrib.auth.models import User # Альтернативна модель користувача 

class Cart(models.Model):
    # Унікальний код для ідентифікації кошика (використовується, наприклад, для сесій анонімних користувачів) 
    cart_code = models.CharField(max_length=250) 
    # Прив'язка до користувача. Може бути null/blank для анонімних кошиків 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True) 
    paid_status = models.BooleanField(default=False) # Статус оплати 
    created_at = models.DateTimeField(auto_now_add=True) 
    modified_at = models.DateTimeField(auto_now=True) 

class CartItem(models.Model):
    # Прив'язка до самого кошика (зовнішній ключ) 
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items') 
    # Прив'язка до продукту 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1) # Кількість товару [12]
```

**Альтернативний простий приклад моделі елемента кошика, прив'язаного безпосередньо до користувача:**

```
from   django.db   import   models
from   django.contrib.auth.models   import   User
class   CartItem ( models . Model ):
    product   =   models . ForeignKey ( Product ,   on_delete = models . CASCADE ) [9]
    quantity   =   models . PositiveIntegerField ( default = 0 ) [9]
    user   =   models . ForeignKey ( User ,   on_delete = models . CASCADE ) [9]
    date_added   =   models . DateTimeField ( auto_now_add = True ) [9]
    def   __str__ ( self ):
        return   f ' { self . quantity }  x  { self . product . name } ' [9]
```

Альтернативна архітектура кошика: Використання сесій Django

Для тимчасового зберігання товарів, поки клієнти переглядають сайт, можна використовувати **фреймворк сесій Django**. Сесія зберігає дані у вигляді словника, де ключами є ID продуктів, а значеннями — їхня кількість. Цей підхід часто використовується для анонімних користувачів.

Приклад функції для додавання товару до кошика через сесії:

```
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {}) # Отримати кошик або створити порожній словник [5]
    cart[product_id] = cart.get(product_id, 0) + 1 # Збільшити кількість на 1 [5]
    request.session['cart'] = cart # Зберегти оновлений кошик у сесії [5]
    return redirect('cart_view') [5]
```

Для більш складної логіки кошика, що зберігається в сесії, можна створити спеціальний клас `Cart` (Сервіс кошика), який керує операціями додавання, видалення, підрахунку загальної ціни та очищення.

Приклад ініціалізації класу `Cart` з використанням сесій:

```
from   django.conf   import   settings

class   Cart :
    def   __init__ ( self ,   request ):
        """  initialize the cart  """
        self . session   =   request . session
        cart   =   self . session . get ( settings . CART_SESSION_ID )
        if   not   cart :
            # save an empty cart in session
            cart   =   self . session [ settings . CART_SESSION_ID ]   =   {}
        self . cart   =   cart

    def   save ( self ):
        self . session . modified   =   True [17]
    # ... інші методи (add, remove, __iter__, __len__, get_total_price, clear) [16]
```

У цьому прикладі використовується налаштування `CART_SESSION_ID`, яке має бути додане до `settings.py` (наприклад: `CART_SESSION_ID = 'cart'`).

Додаткова функціональність

* **Автентифікація користувачів:** Вбудований модуль `django.contrib.auth` надає функціональність для реєстрації, входу та виходу користувачів. У більш складних проектах може знадобитися кастомізувати модель користувача, створивши `CustomUser` та `UserAdmin`.
* **Транзакції:** Для відстеження платежів можна створити модель `Transaction`, яка фіксує унікальний референс, прив'язку до кошика, суму, валюту, статус (spending, completed, failed) та користувача.

```
# Приклад структури Transaction Model (на основі опису)
class Transaction(models.Model):
    reference = models.CharField(max_length=255) # Унікальний ID транзакції [21]
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE) # Прив'язка до кошика [21]
    amount = models.DecimalField(max_digits=10, decimal_places=2) # Сума [21]
    currency = models.CharField(max_length=10) [21]
    status = models.CharField(max_length=50) # Статус транзакції [21]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) [21]
    created_at = models.DateTimeField(auto_now_add=True) [21]
```

## Session-based vs Database-based кошики

**Session-based vs Database-based кошики**

**Порівняння підходів**

**Реалізація гібридного підходу**

Найкращий підхід — **комбінувати обидва методи**:

* Гості → Session-based cart
* Користувачі → Database-based cart
* При login → перенести товари з сесії в БД

```
# cart/cart.py
from decimal import Decimal
from django.conf import settings
from shop.models import Product, Cart, CartItem

class SessionCart:
    """Session-based кошик для анонімних користувачів"""
    
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        
        if not cart:
            # Створити порожній кошик в сесії
            cart = self.session[settings.CART_SESSION_ID] = {}
        
        self.cart = cart
    
    def add(self, product, quantity=1, update_quantity=False):
        """Додати товар в кошик"""
        product_id = str(product.id)
        
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        
        self.save()
    
    def save(self):
        """Зберегти зміни в сесії"""
        self.session.modified = True
    
    def remove(self, product):
        """Видалити товар з кошика"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def __iter__(self):
        """Ітерація по товарах в кошику"""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        
        for product in products:
            cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
    
    def __len__(self):
        """Підрахунок загальної кількості товарів"""
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        """Загальна сума кошика"""
        return sum(
            Decimal(item['price']) * item['quantity'] 
            for item in self.cart.values()
        )
    
    def clear(self):
        """Очистити кошик"""
        del self.session[settings.CART_SESSION_ID]
        self.save()

class DatabaseCart:
    """Database-based кошик для зареєстрованих користувачів"""
    
    def __init__(self, request):
        self.request = request
        self.user = request.user
        
        # Отримати або створити кошик
        self.cart, created = Cart.objects.get_or_create(user=self.user)
    
    def add(self, product, quantity=1, update_quantity=False):
        """Додати товар в кошик"""
        cart_item, created = CartItem.objects.get_or_create(
            cart=self.cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            if update_quantity:
                cart_item.quantity = quantity
            else:
                cart_item.quantity += quantity
            cart_item.save()
    
    def remove(self, product):
        """Видалити товар з кошика"""
        CartItem.objects.filter(
            cart=self.cart,
            product=product
        ).delete()
    
    def __iter__(self):
        """Ітерація по товарах"""
        for item in self.cart.items.select_related('product'):
            yield {
                'product': item.product,
                'quantity': item.quantity,
                'price': item.product.price,
                'total_price': item.get_total_price()
            }
    
    def __len__(self):
        """Кількість товарів"""
        return self.cart.get_total_items()
    
    def get_total_price(self):
        """Загальна сума"""
        return self.cart.get_total_price()
    
    def clear(self):
        """Очистити кошик"""
        self.cart.items.all().delete()

def get_cart(request):
    """Фабрика для отримання правильного типу кошика"""
    if request.user.is_authenticated:
        return DatabaseCart(request)
    else:
        return SessionCart(request)

def merge_carts(request):
    """Об'єднати session cart з database cart при login"""
    if not request.user.is_authenticated:
        return
    
    session_cart = SessionCart(request)
    db_cart = DatabaseCart(request)
    
    # Перенести товари з сесії в БД
    for item in session_cart:
        db_cart.add(
            product=item['product'],
            quantity=item['quantity'],
            update_quantity=False
        )
    
    # Очистити session cart
    session_cart.clear()
```

**Views для роботи з кошиком**

```
*# cart/views.py*
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import get_cart

def cart_detail(request):
    """Перегляд кошика"""
    cart = get_cart(request)
    
    return render(request, 'cart/detail.html', {
        'cart': cart
    })

@require_POST
def cart_add(request, product_id):
    """Додати товар в кошик"""
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    *# Перевірити наявність на складі*
    if not product.is_in_stock:
        messages.error(request, f'Товар "{product.name}" немає в наявності')
        return redirect('shop:product_detail', slug=product.slug)
    
    quantity = int(request.POST.get('quantity', 1))
    
    *# Перевірити, чи достатньо товару*
    if quantity > product.stock:
        messages.error(
            request, 
            f'Доступно тільки {product.stock} од. товару "{product.name}"'
        )
        return redirect('shop:product_detail', slug=product.slug)
    
    cart.add(product=product, quantity=quantity)
    messages.success(request, f'Товар "{product.name}" додано до кошика')
    
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    """Видалити товар з кошика"""
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    
    messages.success(request, f'Товар "{product.name}" видалено з кошика')
    return redirect('cart:cart_detail')

@require_POST
def cart_update(request, product_id):
    """Оновити кількість товару в кошику"""
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart.add(product=product, quantity=quantity, update_quantity=True)
        messages.success(request, 'Кошик оновлено')
    else:
        cart.remove(product)
        messages.success(request, 'Товар видалено з кошика')
    
    return redirect('cart:cart_detail')
```

**Шаблон кошика з можливістю оновлення кількості**

```
*{# cart/detail.html #}*
{% extends 'base.html' %}
{% load static %}

{% block title %}Кошик{% endblock %}

{% block content %}
<div class="container my-5">
    <h1>Ваш кошик</h1>
    
    {% if cart %}
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Товар</th>
                        <th>Ціна</th>
                        <th>Кількість</th>
                        <th>Сума</th>
                        <th>Дії</th>
                    </tr>
                </thead>
                <tbody>
                    {% for item in cart %}
                        <tr>
                            <td>
                                <div class="d-flex align-items-center">
                                    {% if item.product.images.first %}
                                        <img src="{{ item.product.images.first.image.url }}" 
                                             alt="{{ item.product.name }}"
                                             class="img-thumbnail me-3"
                                             style="width: 80px;">
                                    {% endif %}
                                    <div>
                                        <h6 class="mb-0">{{ item.product.name }}</h6>
                                        <small class="text-muted">{{ item.product.category }}</small>
                                    </div>
                                </div>
                            </td>
                            <td>{{ item.price }} грн</td>
                            <td>
                                <form method="post" 
                                      action="{% url 'cart:cart_update' item.product.id %}"
                                      class="d-flex align-items-center">
                                    {% csrf_token %}
                                    <button type="button" class="btn btn-sm btn-outline-secondary"
                                            onclick="decreaseQuantity(this)">-</button>
                                    <input type="number" 
                                           name="quantity" 
                                           value="{{ item.quantity }}"
                                           min="1"
                                           max="{{ item.product.stock }}"
                                           class="form-control mx-2"
                                           style="width: 70px;"
                                           onchange="this.form.submit()">
                                    <button type="button" class="btn btn-sm btn-outline-secondary"
                                            onclick="increaseQuantity(this)">+</button>
                                </form>
                            </td>
                            <td><strong>{{ item.total_price }} грн</strong></td>
                            <td>
                                <form method="post" 
                                      action="{% url 'cart:cart_remove' item.product.id %}">
                                    {% csrf_token %}
                                    <button type="submit" class="btn btn-sm btn-danger">
                                        <i class="fas fa-trash"></i> Видалити
                                    </button>
                                </form>
                            </td>
                        </tr>
                    {% endfor %}
                </tbody>
                <tfoot>
                    <tr>
                        <td colspan="3" class="text-end"><strong>Загальна сума:</strong></td>
                        <td colspan="2"><strong>{{ cart.get_total_price }} грн</strong></td>
                    </tr>
                </tfoot>
            </table>
        </div>
        
        <div class="d-flex justify-content-between mt-4">
            <a href="{% url 'shop:product_list' %}" class="btn btn-outline-primary">
                <i class="fas fa-arrow-left"></i> Продовжити покупки
            </a>
            <a href="{% url 'orders:checkout' %}" class="btn btn-primary btn-lg">
                Оформити замовлення <i class="fas fa-arrow-right"></i>
            </a>
        </div>
    {% else %}
        <div class="alert alert-info">
            <i class="fas fa-shopping-cart"></i> Ваш кошик порожній
        </div>
        <a href="{% url 'shop:product_list' %}" class="btn btn-primary">
            Перейти до покупок
        </a>
    {% endif %}
</div>

<script>
function decreaseQuantity(button) {
    const input = button.nextElementSibling;
    if (input.value > 1) {
        input.value = parseInt(input.value) - 1;
        input.form.submit();
    }
}

function increaseQuantity(button) {
    const input = button.previousElementSibling;
    const max = parseInt(input.max);
    if (parseInt(input.value) < max) {
        input.value = parseInt(input.value) + 1;
        input.form.submit();
    }
}
</script>
{% endblock %}
```

## Практичні завдання

**Завдання 1: Створення простого session-based кошика**

Створи базовий кошик який зберігає дані в сесії:

**Що потрібно зробити:**

1. Створи новий Django проект "simple\_shop"
2. Додай один застосунок "cart"
3. Створи просту модель Product з полями: name, price, image
4. Реалізуй клас SessionCart з методами:

* `__init__(request)` - ініціалізація з сесією
* `add(product, quantity)` - додавання товару
* `remove(product)` - видалення товару
* `get_total_price()` - загальна сума
* `clear()` - очищення кошика

5.Створи три view:

* `product_list` - список товарів з кнопкою "Додати в кошик"
* `cart_add` - обробка додавання товару
* `cart_detail` - відображення вмісту кошика

6.Зроби простий шаблон де показується список товарів у кошику

**Завдання 2: Додавання функції оновлення кількості**

Розшири попереднє завдання функцією зміни кількості:

**Що додати:**

1. В шаблоні cart\_detail додай форму для кожного товару з:

* Поле input type="number" для кількості
* Кнопки "+" та "-" для зміни кількості
* Кнопка "Оновити" для збереження змін
* Кнопка "Видалити" для видалення товару

2.Створи view `cart_update(request, product_id)` який:

* Отримує нову кількість з POST запиту
* Оновлює кількість товару в кошику
* Якщо кількість = 0, видаляє товар
* Перенаправляє назад на cart\_detail

3.Додай перевірки:

* Кількість має бути більше 0
* Максимальна кількість - 99 штук одного товару

**Очікуваний результат:** Користувач може змінювати кількість товарів без перезавантаження сторінки (через form submit)

## Checkout процес (Оформлення замовлення)

**Checkout процес (Оформлення замовлення)**

Процес оформлення замовлення (Checkout) в архітектурі Django є критично важливим етапом, який слідує за створенням і наповненням кошика. Він передбачає автентифікацію користувача, підтвердження деталей замовлення, інтеграцію з платіжними шлюзами та, зрештою, запис транзакції та оновлення статусу замовлення.

Перш ніж користувач зможе здійснити оплату, він **повинен бути авторизований**.

Якщо користувач не авторизований, він буде перенаправлений на сторінку входу (`/login`), а після успішного входу — автоматично повернений на сторінку оформлення замовлення (`/checkout`), яку він намагався відвідати

**Структура сторінки оформлення замовлення (Checkout Page)**

Сторінка оформлення замовлення (Checkout Page) відображає фінальні деталі перед оплатою:

1. **Order Summary (Order Summary)**: Список товарів та фінальні розрахунки (сума, податок, загальна сума).
2. **Payment Section (Payment Section)**: Вибір платіжного шлюзу (наприклад, PayPal або Flutterwave).

Важливо, що на цій сторінці **не можна** змінювати кількість товарів або видаляти їх — це можна зробити лише на сторінці кошика.

Дані для сторінки оформлення замовлення можна отримувати з бекенду (Django) за допомогою API, аналогічно тому, як це робиться для стошинки кошика, використовуючи, наприклад, кастомний хук `useCartData`

**Forms для Checkout**

```
*# orders/forms.py*
from django import forms
from .models import Order, ShippingAddress

class ShippingAddressForm(forms.ModelForm):
    """Форма адреси доставки"""
    
    class Meta:
        model = ShippingAddress
        fields = [
            'full_name', 'phone', 'country', 'city',
            'postal_code', 'address_line1', 'address_line2',
            'is_default'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Прізвище Ім\\'я По батькові'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+380...'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Місто'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '01001'
            }),
            'address_line1': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Вулиця, будинок, квартира'
            }),
            'address_line2': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Додаткова інформація (необов\\'язково)'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Зробити всі поля обов'язковими, окрім address_line2
        for field_name, field in self.fields.items():
            if field_name != 'address_line2' and field_name != 'is_default':
                field.required = True

class OrderCheckoutForm(forms.Form):
    """Форма для фінального підтвердження замовлення"""
    
    PAYMENT_CHOICES = [
        ('cash', 'Готівкою при отриманні'),
        ('card', 'Оплата карткою онлайн'),
        ('bank', 'Банківський переказ'),
    ]
    
    payment_method = forms.ChoiceField(
        label='Спосіб оплати',
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
    
    notes = forms.CharField(
        label='Коментар до замовлення',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Додаткова інформація для кур\\'єра...'
        })
    )
    
    agree_terms = forms.BooleanField(
        label='Я погоджуюсь з умовами доставки та оплати',
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
```

## Views для Checkout процесу

**Views для Checkout процесу**

```
# orders/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from cart.cart import get_cart
from .models import Order, OrderItem, ShippingAddress, OrderStatusHistory
from .forms import ShippingAddressForm, OrderCheckoutForm

@login_required
def checkout(request):
    """Крок 1: Вибір/додавання адреси доставки"""
    cart = get_cart(request)
    
    # Перевірити, чи кошик не порожній
    if len(cart) == 0:
        messages.warning(request, 'Ваш кошик порожній')
        return redirect('shop:product_list')
    
    # Отримати існуючі адреси
    addresses = ShippingAddress.objects.filter(user=request.user)
    
    # Форма для нової адреси
    if request.method == 'POST':
        if 'select_address' in request.POST:
            # Вибрана існуюча адреса
            address_id = request.POST.get('address_id')
            request.session['shipping_address_id'] = address_id
            return redirect('orders:checkout_confirm')
        
        elif 'add_new_address' in request.POST:
            # Додати нову адресу
            form = ShippingAddressForm(request.POST)
            if form.is_valid():
                address = form.save(commit=False)
                address.user = request.user
                address.save()
                
                request.session['shipping_address_id'] = address.id
                messages.success(request, 'Адресу додано успішно')
                return redirect('orders:checkout_confirm')
    else:
        form = ShippingAddressForm()
    
    return render(request, 'orders/checkout.html', {
        'cart': cart,
        'addresses': addresses,
        'form': form,
    })

@login_required
def checkout_confirm(request):
    """Крок 2: Підтвердження замовлення"""
    cart = get_cart(request)
    
    # Перевірити наявність адреси
    address_id = request.session.get('shipping_address_id')
    if not address_id:
        messages.warning(request, 'Будь ласка, оберіть адресу доставки')
        return redirect('orders:checkout')
    
    address = get_object_or_404(ShippingAddress, id=address_id, user=request.user)
    
    if request.method == 'POST':
        form = OrderCheckoutForm(request.POST)
        if form.is_valid():
            # Створити замовлення
            order = create_order(
                request=request,
                cart=cart,
                address=address,
                payment_method=form.cleaned_data['payment_method'],
                notes=form.cleaned_data['notes']
            )
            
            if order:
                # Відправити email
                send_order_confirmation_email(order)
                
                # Очистити кошик та сесію
                cart.clear()
                del request.session['shipping_address_id']
                
                messages.success(
                    request, 
                    f'Замовлення #{order.order_number} успішно створено!'
                )
                return redirect('orders:order_success', order_number=order.order_number)
            else:
                messages.error(request, 'Помилка створення замовлення')
    else:
        form = OrderCheckoutForm()
    
    return render(request, 'orders/checkout_confirm.html', {
        'cart': cart,
        'address': address,
        'form': form,
    })

@transaction.atomic
def create_order(request, cart, address, payment_method, notes):
    """Створення замовлення (з транзакцією)"""
    try:
        # Створити замовлення
        order = Order.objects.create(
            user=request.user,
            shipping_full_name=address.full_name,
            shipping_phone=address.phone,
            shipping_country=address.country,
            shipping_city=address.city,
            shipping_postal_code=address.postal_code,
            shipping_address_line1=address.address_line1,
            shipping_address_line2=address.address_line2,
            total_amount=cart.get_total_price(),
            notes=notes
        )
        
        # Створити товари замовлення
        for item in cart:
            product = item['product']
            
            # Перевірити наявність на складі
            if product.stock < item['quantity']:
                raise ValueError(f'Недостатньо товару {product.name} на складі')
            
            # Створити OrderItem
            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                price=product.price,
                quantity=item['quantity']
            )
            
            # Зменшити кількість на складі
            product.stock -= item['quantity']
            product.save()
        
        # Створити запис в історії статусів
        OrderStatusHistory.objects.create(
            order=order,
            status='pending',
            note=f'Замовлення створено. Спосіб оплати: {payment_method}',
            created_by=request.user
        )
        
        return order
        
    except Exception as e:
        messages.error(request, f'Помилка: {str(e)}')
        return None

def send_order_confirmation_email(order):
    """Відправка email підтвердження замовлення"""
    subject = f'Підтвердження замовлення #{order.order_number}'
    
    # Рендеримо HTML шаблон
    html_message = render_to_string('orders/emails/order_confirmation.html', {
        'order': order,
    })
    
    # Текстова версія
    plain_message = f"""
    Дякуємо за замовлення!
    
    Номер замовлення: {order.order_number}
    Дата: {order.created_at.strftime('%d.%m.%Y %H:%M')}
    Загальна сума: {order.total_amount} грн
    
    Товари:
    {chr(10).join([f'- {item.product_name} x {item.quantity} = {item.get_total_price()} грн' for item in order.items.all()])}
    
    Адреса доставки:
    {order.shipping_full_name}
    {order.shipping_address_line1}
    {order.shipping_city}, {order.shipping_postal_code}
    
    Дякуємо за покупку!
    """
    
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[order.user.email],
        html_message=html_message,
        fail_silently=True,
    )

@login_required
def order_success(request, order_number):
    """Сторінка успішного замовлення"""
    order = get_object_or_404(
        Order, 
        order_number=order_number, 
        user=request.user
    )
    
    return render(request, 'orders/order_success.html', {
        'order': order
    })

@login_required
def order_list(request):
    """Список замовлень користувача"""
    orders = Order.objects.filter(
        user=request.user
    ).prefetch_related('items__product').order_by('-created_at')
    
    return render(request, 'orders/order_list.html', {
        'orders': orders
    })

@login_required
def order_detail(request, order_number):
    """Деталі замовлення"""
    order = get_object_or_404(
        Order.objects.select_related('user').prefetch_related(
            'items__product',
            'status_history'
        ),
        order_number=order_number,
        user=request.user
    )
    
    return render(request, 'orders/order_detail.html', {
        'order': order
    })
```

## Ініціація платежу (Initiate Payment)

**Ініціація платежу (Initiate Payment)**

Для відстеження факту оплати та її статусу необхідна модель `Transaction`.

**Модель Transaction**

```
class Transaction(models.Model):
    reference = models.CharField(max_length=255)  # Унікальний ID транзакції
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)  # Прив'язка до кошика
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Сума транзакції
    currency = models.CharField(max_length=10)  # Валюта (USD, NGN тощо)
    status = models.CharField(max_length=50)  # Статус ('spending', 'completed', 'failed')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Користувач-ініціатор
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

Процес ініціації платежу (на прикладі Flutterwave або PayPal) виконується на бекенді Django.

**Функція initiate\_payment (приклад логіки для Flutterwave):**

1. **Отримання даних та розрахунок:**

◦ Генерація унікального ID транзакції (`tx_ref` / `UUID`).

◦ Отримання `cart_code` та об'єкта `Cart`.

◦ Розрахунок `total_amount` (сума товарів + податок, наприклад, $4.00).

◦ Визначення валюти (наприклад, `USD` або `NGN`).

**2.Створення запису транзакції:**

◦ Створення нового об'єкта `Transaction` зі статусом **"spending"**.

**3.Формування запиту до платіжного шлюзу:**

◦ Створення `payload` (даних, що передаються платіжному шлюзу, включаючи суму, валюту та URL для редиректу після оплати).

◦ Встановлення `headers`, включаючи секретний ключ платіжного шлюзу (який зберігається в `settings.py`).

**4.Надсилання запиту:**

◦ Надсилання `POST`-запиту на API платіжного шлюзу (використовуючи, наприклад, бібліотеку `requests` в Python).

**5.Отримання посилання для редиректу:**

◦ Платіжний шлюз повертає посилання (наприклад, `hosted_link` або `approval URL`).

◦ Цей лінк повертається фронтенду у відповідь JSON.

**6.Редирект на фронтенді:**

◦ Фронтенд використовує отриманий `hosted_link` для перенаправлення користувача на сторінку платіжного шлюзу, де він вводить свої дані.

**Приклад коду для ініціації платежу (витяг):**

```
# Фрагмент views.py для ініціації платежу (спрощено)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initiate_payment(request):
    # ... (Отримання cart_code, розрахунок amount, tax, currency)

    # Створення унікального ID транзакції
    tx_ref = uuid.uuid4()

    # ... (Розрахунок total_amount)

    # Створення запису транзакції
    transaction = Transaction.objects.create(
        reference=tx_ref,
        cart=cart,
        amount=total_amount,
        currency=currency,
        user=request.user,
        status='spending'
    )

    # URL, куди користувача перенаправлять після оплати
    redirect_url = settings.REACT_BASE_URL + "/payment_status"

    # Формування payload для Flutterwave (або іншого шлюзу)
    payload = {
        "tx_ref": str(tx_ref),
        "amount": str(total_amount),
        "currency": currency,
        # ... (інші деталі, включаючи customer info та redirect_url)
    }

    # ... (Виконання requests.post на API Flutterwave)
    # ... (Отримання response та повернення hosted link)

    return Response(response.json(), status=status.HTTP_200_OK)
```

**5. Верифікація платежу (Callback and Verification)**

Після того, як користувач успішно ввів дані на сторінці платіжного шлюзу, його повертає на сторінку статусу платежу (наприклад, `/payment_status/`) з параметрами запиту (`status`, `tx_ref` тощо).

**Функція payment\_callback (Callback View):**

Ця функція в Django відповідає за фінальну перевірку, щоб підтвердити, що платіж був не лише здійснений, але й відповідає очікуваній сумі та валюті.

**1.Отримання Query Parameters:** Бекенд отримує параметри (`status`, `tx_ref`, `transaction_id`) з URL.

**2.Фінальна перевірка через API:** Надсилається ще один запит до платіжного шлюзу (наприклад, Flutterwave Verify Endpoint) для отримання офіційних даних про транзакцію.

**3.Перевірка умов (Core Logic):**

◦ Перевірка, чи статус відповіді від шлюзу є `success`.

◦ Перевірка, чи сплачена **сума дорівнює** очікуваній `transaction.amount`.

◦ Перевірка, чи **валюта** відповідає `transaction.currency`.

**4.Оновлення статусу та завершення замовлення:**

◦ Якщо всі перевірки пройдені, статус об'єкта `Transaction` оновлюється на **completed**.

◦ Статус пов'язаного `Cart` оновлюється: `cart.paid_status = True`.

◦ Повідомлення про успіх повертається фронтенду.

**Відображення історії замовлень (Order History)**

Після успішного оформлення замовлення товари стають частиною історії покупок користувача.

На сторінці профілю користувача (`/profile`) Django view, що відображає історію, має фільтрувати кошики та пов'язані з ними товари, щоб відображати **лише ті CartItem, які належать до Cart зі статусом paid\_status=True**.

Це гарантує, що в історії відображаються лише **сплачені** замовлення.

**Приклад серіалізатора для історії замовлень (на бекенді):**

Серіалізатор `UserSerializer` може мати метод, який отримує лише сплачені товари:

```
# Фрагмент UserSerializer для отримання історії замовлень
class UserSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField() # Custom field для отримання історії замовлень

    class Meta:
        # ... (поля користувача)

    def get_items(self, user):
        # Фільтруємо CartItem, пов'язані з Cart, що мають paid_status=True
        paid_cart_items = CartItem.objects.filter(
            cart__user=user,
            cart__paid_status=True
        ).order_by('-date_added')[:10] # Обмеження до 10 останніх

        # Використовуємо спеціальний серіалізатор для відображення деталей
        return NewCartItemSerializer(paid_cart_items, many=True).data
```

Цей підхід забезпечує відображення замовлення, а не просто кошика, на фінальному етапі

## Email сповіщення

**Email сповіщення**

Django пропонує вбудовану функціональність для надсилання електронних листів через модуль `django.core.mail`.

**1. Конфігурація налашту**

**явань електронної пошти**

Для надсилання пошти через SMTP (Simple Mail Transfer Protocol) необхідно налаштувати відповідні параметри у файлі `settings.py`:

Під час розробки рекомендується використовувати спеціалізовані бекенди, наприклад, **Console backend** (який виводить листи у стандартний вивід) або **File backend** (який записує листи у файл), щоб уникнути надсилання реальних листів.

**Приклад конфігурації для розробки (Console Backend):**

```
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend" [17]
```

**Основні функції для надсилання Email**

Django надає кілька легких обгорток над модулем `smtplib`. Найбільш поширеною є функція `send_mail()`.

```
Надсилання простого текстового листа send_mail() використовується для простого надсилання електронної пошти.
```

**Обов'язкові параметри:** `subject` (тема), `message` (тіло листа), `from_email` (адреса відправника) та `recipient_list` (список одержувачів).

**Приклад коду:**

```
from   django.core.mail   import   send_mail

send_mail(
    'Subject of the Email',      # Тема листа [2]
    'Body of the Email',         # Повідомлення (текст) [2]
    'sender@goit.com',           # Адреса відправника [4]
    ['recipient@goit.com'],      # Список одержувачів (список рядків) [4]
    fail_silently=False,         # Якщо False, при помилці буде викликано виняток [4, 10, 11]
)
```

**Надсилання листа з HTML-вмістом**

Якщо потрібен HTML-формат листа, використовуйте аргумент `html_message` у функції `send_mail()` або клас `EmailMultiAlternatives`.

Якщо надано `html_message`, лист буде складатися з декількох частин/альтернативного листа, де `message` буде типом вмісту `text/plain`, а `html_message` — типом вмісту `text/html`.

**Приклад використання EmailMultiAlternatives (для HTML-сповіщення про замовлення):**

Цей підхід дозволяє використовувати шаблони Django для генерації HTML-вмісту.

```
from   django.core.mail   import   EmailMultiAlternatives
from   django.template.loader   import   render_to_string

# 1. Створення простого текстового вмісту з шаблону
text_content   =   render_to_string (
    "templates/emails/order_confirmation.txt",
    context = { "order_id" : 12345 }
)

# 2. Створення HTML-вмісту з шаблону
html_content   =   render_to_string (
    "templates/emails/order_confirmation.html",
    context = { "order_id" : 12345 }
)

# 3. Створення екземпляру EmailMultiAlternatives
msg   =   EmailMultiAlternatives (
    "Confirmation Subject",     # Тема
    text_content,               # Тіло (Plain Text)
    "from@example.com",         # Від
    ["customer@example.com"],   # Кому
)

# 4. Прикріплення HTML-вмісту
msg.attach_alternative(html_content, "text/html") [23, 24]

# 5. Надсилання
msg.send() [23, 25]
```

**Захист від ін'єкцій заголовків**

Для запобігання експлойту безпеки, відомому як ін'єкція заголовка (Header injection), Django забороняє використання символів нового рядка у значеннях заголовків (`subject`, `from_email`, `recipient_list`).

Якщо будь-який з цих параметрів містить новий рядок, функція `send_mail()` викличе виняток `django.core.mail.BadHeaderError` (підклас `ValueError`), і лист не буде надіслано.

**Приклад захисту в View-функції (для контактної форми):**

```
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect


def send_email(request):
    subject = request.POST.get("subject", "")
    message = request.POST.get("message", "")
    from_email = request.POST.get("from_email", "")


    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, ["admin@goit.com"])
        except BadHeaderError:
            return HttpResponse("Invalid header found.")
        return HttpResponseRedirect("/contact/thanks/")
    else:
        return HttpResponse("Make sure all fields are entered and valid.")
```

Цей код демонструє, як обробляти потенційні помилки, пов'язані з недійсними заголовками, використовуючи блок `try...except BadHeaderError`.

**Типові Email сповіщення для E-commerce**

Для інтернет-магазину зазвичай потрібні наступні сповіщення, які можуть бути реалізовані за допомогою `send_mail()` або `EmailMultiAlternatives`:

1. **Підтвердження замовлення (Order Confirmation):** Надсилається користувачу після успішної оплати.
2. **Сповіщення про активацію облікового запису/реєстрацію (Account Activation/Registration):** Надсилається новим користувачам.
3. **Скидання пароля (Password Reset):** Стандартний функціонал, часто інтегрований з вбудованим модулем `django.contrib.auth`.
4. **Сповіщення адміністратору (Admin Notification):** Використовується для сповіщення адміністраторів про нові замовлення або запити через контактну форму. Для цього можна використовувати функцію `mail_admins()`, яка надсилає листа адміністраторам, визначеним у налаштуваннях `ADMINS`


## Коли краще використовувати session-based кошик?

No Text

## Яка правильна послідовність checkout процесу?

No Text

## Який backend НЕ варто використовувати в production?

No Text

## Практичні завдання

**Завдання 1: Форма адреси доставки**

Створи просту форму для введення адреси доставки:

**Що зробити:**

1.Створи модель ShippingAddress з полями:

* full\_name (ім'я отримувача)
* phone (телефон)
* city (місто)
* address (адреса)

2.Створи ModelForm для цієї моделі з Bootstrap класами

3.Створи view `checkout_address` який:

* Показує форму при GET запиті
* Обробляє форму при POST
* Зберігає адресу в сесії: `request.session['shipping_address_id'] = address.id`
* Перенаправляє на сторінку підтвердження

4.Створи простий шаблон з формою

**Очікуваний результат:** Користувач може ввести адресу доставки і вона збережеться

**Завдання 2: Email підтвердження замовлення**

Налаштуй відправку email при створенні замовлення:

**Що зробити:**

1. В [settings.py](http://settings.py) додай:

python

`EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`

1. Створи функцію `send_order_email(order)` яка:

* Формує тему листа: "Замовлення #ORDER\_NUMBER підтверджено"
* Створює текст листа з деталями:
* Номер замовлення
* Список товарів
* Загальна сума
* Адреса доставки
* Відправляє через `send_mail()`

2.Викликай цю функцію після створення замовлення

3.Протестуй - email має з'явитись в консолі

**Очікуваний результат:** Після створення замовлення в консолі з'являється текст email з деталями

## Підсумки

**📋 Підсумки уроку**

Вітаємо! Ви щойно освоїли **ключові компоненти e-commerce розробки** і готові створювати професійні інтернет-магазини!

**Що ви освоїли:**

* **Двоїсті кошики:** Session-based для гостей та database-based для користувачів
* **Checkout процес:** Багатокроковий процес від вибору адреси до підтвердження
* **Система замовлень:** Атомарні транзакції для надійності даних
* **Email інтеграція:** Автоматичні сповіщення для користувачів
* **Повний цикл покупки:** Від додавання в кошик до email підтвердження

**Що далі?**

На наступному уроці ми вивчимо **Django та Docker** - навчимося контейнеризувати Django додатки, створювати docker-compose конфігурації та готувати проекти до deployment в будь-яке середовище. Це критично важливі навички для сучасної розробки!