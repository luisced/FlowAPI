from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import User

class UserApiTests(APITestCase):
    def setUp(self):
        # Set up any objects you need here
        self.user = User.objects.create(name='Test User', email='testuser@example.com')

    def test_create_user(self):
        url = reverse('create_user')
        data = {'name': 'New User', 'email': 'newuser@example.com'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # POST should return HTTP 201 Created
        self.assertEqual(User.objects.count(), 2)  # Assuming you start with one user in setUp

    def test_get_users(self):
        url = reverse('get_users')  # Make sure to define the name in your urls.py
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), User.objects.count())

    def test_get_user(self):
        url = reverse('get_user', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.user.name)
        self.assertEqual(response.data['email'], self.user.email)

    def test_update_user(self):
        url = reverse('update_user', kwargs={'pk': self.user.pk})
        data = {'name': 'Updated User', 'email': 'updateduser@example.com'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, 'Updated User')
        self.assertEqual(self.user.email, 'updateduser@example.com')

    def test_delete_user(self):
        url = reverse('delete_user', kwargs={'pk': self.user.pk})
        response = self.client.delete(url)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

    # Add tearDown method if you need to clean up after tests
    def tearDown(self):
        pass
