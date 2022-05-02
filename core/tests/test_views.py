from django.test import TestCase
from core.models import *
from django.contrib.auth import get_user_model

User = get_user_model()


class CoreTests(TestCase):
    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000'
        self.user = User.objects.create_user(
            username='dev',
            email='dev@test.com',
            password='123456',
            first_name='Test',
            last_name='Test'
        )

        Item.objects.create(
            title="Einstein's Universe",
            price=23.50,
            discount_price=19.99,
            category='S',
            label='P',
            slug='einsteins-universe',
            description='Awesome Book',
            image='/core/tests/img/98594.jpg'
        )
        Item.objects.create(
            title="Mathematics for Computer Science",
            price=56.50,
            discount_price=34.99,
            category='S',
            label='P',
            slug='mathematics-for-computer-science',
            description='Awesome Computer Science Book',
            image='/core/tests/img/cs_book.jpg'
        )
        self.login()

    def login(self):
        self.client.login(username='dev', password='123456')

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertEqual(len(response.context['object_list']), 2)

    def test_product_details(self):
        # Get all item
        items = Item.objects.all()

        # Test Product details
        for item in items:
            response = self.client.get('/product/' + item.slug + '/')
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'product.html')
            self.assertContains(response, item.description)

        # Test add to cart
        response = self.client.get('/add-to-cart/' + items[0].slug + '/')
        self.assertRedirects(response, '/order-summary/', status_code=302,
                             target_status_code=200, msg_prefix='', fetch_redirect_response=True)

        # Test cart page
        response = self.client.get('/order-summary/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order_summary.html')
        self.assertContains(response, 'Order Summary')
        self.assertEqual(
            response.context['object'].user.username, "dev")

        # Test how many order placed
        self.assertEqual(OrderItem.objects.count(), 1)

        # Test checkout
        response = self.client.get('/checkout/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout.html')
        self.assertContains(response, 'Checkout form')
        self.assertContains(response, items[0].description)

        # Test Checking out
        data = {
            'shipping_address': 'Rajshahi, Bangladesh',
            'shipping_address2': '',
            'shipping_country': 'BD',
            'shipping_zip': '6205',
            'billing_address': '',
            'billing_address2': '',
            'billing_country': '',
            'billing_zip': '',
            'same_billing_address': True,
            'set_default_shipping': False,
            'use_default_shipping': False,
            'set_default_billing': False,
            'use_default_billing': False,
            'payment_option': 'S'
        }

        response = self.client.post('/checkout/', data=data)
        self.assertRedirects(response, '/payment/stripe/', status_code=302,
                             target_status_code=200, msg_prefix='', fetch_redirect_response=True)

        # Test payment method
        response = self.client.get('/payment/stripe/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payment.html')
        self.assertContains(response, 'Payment')

        # Test Coupon
        coupon = Coupon.objects.create(code="TEST101", amount=9.99)
        response = self.client.post('/add-coupon/', data={'code': 'TEST101'})
        self.assertRedirects(response, '/checkout/', status_code=302,
                             target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        response = self.client.get('/checkout/')
        self.assertContains(response, items[0].discount_price - 9.99)

        # Test remove from cart
        response = self.client.get('/remove-from-cart/' + items[0].slug + '/')
        self.assertRedirects(response, '/order-summary/', status_code=302,
                             target_status_code=200, msg_prefix='', fetch_redirect_response=True)

        # Test removed order from cart
        self.assertEqual(OrderItem.objects.count(), 0)
