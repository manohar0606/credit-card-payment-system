from django.test import TestCase
from .models import User, Cards


class CardTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="carduser",
            email="carduser@gmail.com",
            password="Test@123"
        )

        login_response = self.client.post(
            "/api/login/",
            data={
                "username": "carduser",
                "password": "Test@123"
            },
            content_type="application/json"
        )

        self.token = login_response.json()["access_token"]

        self.auth_header = {
            "HTTP_AUTHORIZATION": f"Bearer {self.token}"
        }

    def test_add_card(self):
        response = self.client.post(
            "/api/add_card/",
            data={
                "card_type": "CREDIT",
                "card_number": "4111111111111111",
                "expiry_date": "12-28",
                "card_holder_name": "Test"
            },
            content_type="application/json",
            **self.auth_header
        )

        print(response.status_code)
        print(response.json())

        self.assertEqual(response.status_code, 201)

        self.assertTrue(
            Cards.objects.filter(
                user=self.user
            ).exists()
        )
    def test_view_cards(self):
        Cards.objects.create(
            user=self.user,
            card_type="CREDIT",
            card_number="************1111",
            last_four_digit="1111",
            expiry_data="12/28",
            card_holder_name="Test User"
        )

        response = self.client.get(
            "/api/view_card/",
            **self.auth_header
        )

        self.assertEqual(response.status_code, 200)

    def test_delete_card(self):
        card = Cards.objects.create(
            user=self.user,
            card_type="CREDIT",
            card_number="************1111",
            last_four_digit="1111",
            expiry_data="12/28",
            card_holder_name="Test User"
        )

        response = self.client.delete(
            f"/api/Delete_card/{card.id}/",
            **self.auth_header
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            Cards.objects.filter(id=card.id).exists()
        )