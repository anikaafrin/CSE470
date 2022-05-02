from django.test import TestCase
from core.models import *
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()


class DatabaseModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='dev2',
            email='dev2@test.com',
            password='123456',
            first_name='Test',
            last_name='Test'
        )

    def test_user_model(self):
        users = User.objects.all()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].username, self.user.username)
        self.assertEqual(users[0].__str__(), self.user.username)

    def test_item_model(self):
        item = Item.objects.create(
            title="Einstein's Universe",
            price=23.50,
            discount_price=19.99,
            category='S',
            label='P',
            slug='einsteins-universe',
            description='Awesome Book',
            image='/core/tests/img/98594.jpg'
        )
        items = Item.objects.all()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].__str__(), "Einstein's Universe")
        self.assertEqual(items[0].get_absolute_url(),
                         "/product/" + items[0].slug + '/')
        self.assertEqual(items[0].get_add_to_cart_url(),
                         "/add-to-cart/" + items[0].slug + '/')
        self.assertEqual(items[0].get_remove_from_cart_url(),
                         "/remove-from-cart/" + items[0].slug + '/')

    def test_order_item_model(self):
        item = Item.objects.create(
            title="Einstein's Universe",
            price=23.50,
            discount_price=19.99,
            category='S',
            label='P',
            slug='einsteins-universe',
            description='Awesome Book',
            image='/core/tests/img/98594.jpg'
        )

        order_item = OrderItem.objects.create(
            user=self.user,
            item=item
        )
        order_items = OrderItem.objects.all()
        self.assertEqual(len(order_items), 1)
        self.assertEqual(order_items[0].__str__(), "1 of " + item.title)
        self.assertEqual(order_items[0].get_total_item_price(), item.price)
        self.assertEqual(
            order_items[0].get_total_discount_item_price(), item.discount_price)
        self.assertEqual(order_items[0].get_amount_saved(
        ), item.price - item.discount_price)

        if item.discount_price:
            self.assertEqual(
                order_items[0].get_final_price(), order_items[0].get_total_discount_item_price())
        else:
            self.assertEqual(
                order_items[0].get_final_price(), order_items[0].get_total_item_price())

    def test_order_model(self):
        item = Item.objects.create(
            title="Einstein's Universe",
            price=23.50,
            discount_price=19.99,
            category='S',
            label='P',
            slug='einsteins-universe',
            description='Awesome Book',
            image='/core/tests/img/98594.jpg'
        )

        order_item = OrderItem.objects.create(
            user=self.user,
            item=item
        )
        address = Address.objects.create(
            user=self.user,
            street_address="123 Main Road",
            apartment_address="123 Main Road",
            country="BD",
            zip="6000",
            address_type="B"
        )
        address2 = Address.objects.create(
            user=self.user,
            street_address="123 Main Road",
            apartment_address="123 Main Road",
            country="BD",
            zip="6000",
            address_type="S"
        )
        payment = Payment.objects.create(
            stripe_charge_id="12345",
            user=self.user,
            amount=order_item.get_final_price()
        )
        order = Order(
            user=self.user,
            ref_code="TEST101",
            ordered_date=datetime.now(),
            shipping_address=address2,
            billing_address=address,
            payment=payment
        )
        order.save()
        order.items.add(order_item)

        self.assertEqual(Order.objects.count(), 1)
