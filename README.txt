# DRF Ecommerce API

Учебный проект интернет-магазина на Django REST Framework.

## Что реализовано

- Категории и товары с рейтингом (average_rating).
- Корзина пользователя (добавление, обновление, удаление товаров).
- Оформление заказа (checkout).
- Отзывы к товарам (CRUD, один отзыв на пользователя).

## Как запустить

```bash
git clone https://github.com/<твой_логин>/drf-ecommerce.git
cd drf-ecommerce
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

Основные эндпоинты
Категории и товары
GET /shop/categories/ – список категорий.

GET /shop/categories/{slug}/products/ – товары в категории.

GET /shop/products/ – список товаров (c фильтрацией).

GET /shop/products/{slug}/ – детали товара.

Корзина и заказ
GET /shop/cart/ – содержимое корзины.

POST /shop/cart/ – добавить/обновить/убрать товар в корзине.

POST /shop/checkout/ – оформить заказ.

Отзывы к товарам
GET /shop/products/{slug}/reviews/ – список отзывов к товару.

POST /shop/products/{slug}/reviews/ – создать отзыв (только авторизованный пользователь, один отзыв на товар).

GET /shop/products/{slug}/reviews/{id}/ – получить конкретный отзыв.

PUT/PATCH /shop/products/{slug}/reviews/{id}/ – обновить свой отзыв.

DELETE /shop/products/{slug}/reviews/{id}/ – удалить свой отзыв.

Авторизация: JWT (SimpleJWT), токен передаётся в заголовке
Authorization: Bearer <access_token>.
