# from django.contrib.auth import get_user_model
# from django.test import TestCase


# class UsersManagersTests(TestCase):
#     def test_create_user(self):
#         User = get_user_model()
#         user = User.objects.create_user(email="user@email.com", password="123")
#         self.assertEqual(user.email, "user@email.com")
#         self.assertTrue(user.is_active)
#         self.assertFalse(user.is_staff)
#         self.assertFalse(user.is_superuser)

#         try:
#             # username is None for the AbstractUser
#             self.assertIsNone(user.username)
#         except AttributeError:
#             pass
#         with self.assertRaises(TypeError):
#             User.objects.create_user()
#         with self.assertRaises(TypeError):
#             User.objects.create_user(email="")
#         with self.assertRaises(ValueError):
#             User.objects.create_user(email="", password="123")

#     def test_create_user(self):
#         User = get_user_model()
#         user = User.objects.create_user(email="user@email.com", password="123")
#         self.assertEqual(user.email, "user@email.com")
#         self.assertTrue(user.is_active)
#         self.assertTrue(user.is_staff)
#         self.assertTrue(user.is_superuser)

#         try:
#             # username is None for the AbstractUser
#             self.assertIsNone(user.username)
#         except AttributeError:
#             pass
#         with self.assertRaises(ValueError):
#             User.objects.create_superuser(
#                 email="admin@email.com", password="123", is_superuser=False
#             )
