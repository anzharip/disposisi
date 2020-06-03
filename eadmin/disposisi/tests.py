from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User, Group, Permission, ContentType
from django.contrib.auth.hashers import make_password

from .models import MemoSimple

GROUPS = ["tu", "kabag", "kasubag", "operasional"]
USERS = ["tu1", "kabag1", "kasubag1", "operasional1"]
PERMISSIONS = ["to_status_distribusi_kabag", "to_status_disposisi_kasubag", "to_status_disposisi_pelaksana"]
USERS_TO_GROUP = [
    {
        "user": USERS[0],
        "group": GROUPS[0],
        "permission": PERMISSIONS[0]
    },
    {
        "user": USERS[1],
        "group": GROUPS[1],
        "permission": PERMISSIONS[1]
    },
    {
        "user": USERS[2],
        "group": GROUPS[2],
        "permission": PERMISSIONS[2]
    },
]
USERS_TOKENS = []

MEMOSIMPLES = [
    {
        "subject": "subject1",
        "information": "information1",
        "sender": "sender1"
    }
]


class UserModelTests(APITestCase):
    def tearDown(self):
        User.objects.all().delete()
        Group.objects.all().delete()
        Permission.objects.all().delete()
        MemoSimple.objects.all().delete()

    def test_create_user(self):
        """
        Create a new user.
        :return:
        """
        pwd = make_password('password_model_01')
        new_user = User.objects.create(username='user_model_01', password=pwd)
        new_user.save()
        self.assertTrue(self.client.login(username='user_model_01', password='password_model_01'))

    def test_create_many_users(self):
        """
        Create many users
        :return:
        """
        for user in USERS:
            pwd = make_password("password_".join(user))
            new_user = User.objects.create(username=user, password=pwd)
            new_user.save()
            self.assertTrue(self.client.login(username=user, password="password_".join(user)))


class GroupModelTests(APITestCase):
    def tearDown(self):
        User.objects.all().delete()
        Group.objects.all().delete()
        Permission.objects.all().delete()
        MemoSimple.objects.all().delete()

    def test_create_group(self):
        """
        Create a new group.
        :return:
        """
        new_group = Group.objects.create(name="Group1")
        new_group.save()
        for group in Group.objects.filter(name="Group1"):
            self.assertTrue(group, "Group1")

    def test_create_many_group(self):
        """
        Create many groups from list.
        :return:
        """
        for group in GROUPS:
            new_group = Group.objects.create(name=group)
            new_group.save()
            for group_filter in Group.objects.filter(name=group):
                self.assertTrue(group_filter, group)


class PermissionModelTests(APITestCase):
    def tearDown(self):
        User.objects.all().delete()
        Group.objects.all().delete()
        Permission.objects.all().delete()
        MemoSimple.objects.all().delete()

    def test_create_permission(self):
        content_type = ContentType.objects.get_for_model(MemoSimple)
        new_permission = Permission.objects.create(name="permission1", content_type=content_type,
                                                   codename="code_permission1")
        new_permission.save()
        for permission in Permission.objects.filter(name="permission1"):
            self.assertTrue(permission, "permission1")

    def test_create_many_permissions(self):
        for permission in PERMISSIONS:
            content_type = ContentType.objects.get_for_model(MemoSimple)
            new_permission = Permission.objects.create(name=permission, content_type=content_type,
                                                       codename=permission)
            new_permission.save()
            for permission_filter in Permission.objects.filter(name=permission):
                self.assertTrue(permission_filter, permission)


class MemoSimpleModelTests(TestCase):
    def tearDown(self):
        User.objects.all().delete()
        Group.objects.all().delete()
        Permission.objects.all().delete()
        MemoSimple.objects.all().delete()

    def test_create_model(self):
        """
        """
        memosimple_subject1 = MemoSimple.objects.create(subject="Subject 1", information="Information 1",
                                                        sender="Sender 1")
        self.assertIs(memosimple_subject1.subject, "Subject 1")

    def test_default_state_for_created_module(self):
        """
        """
        memosimple_subject1 = MemoSimple.objects.create(subject="Subject 1", information="Information 1",
                                                        sender="Sender 1")
        self.assertIs(memosimple_subject1.state, 0)


class MemoSimpleAPITests(APITestCase):

    def setUp(self):
        """
        Setup user for testing
        """
        pwd = make_password('password_01')
        user = User.objects.create(username='username_01', password=pwd)
        user.save()
        """
        Obtain JWT token for endpoint requiring auth
        """
        url = reverse("token_obtain_pair")
        response = self.client.post(url, {'username': 'username_01', 'password': 'password_01'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.token = response.data['access']
        """
        Create test users
        """
        for user in USERS:
            pwd = make_password(user)
            new_user = User.objects.create(username=user, password=pwd)
            new_user.save()
            self.assertTrue(self.client.login(username=user, password=user))
        """
        Create test groups
        """
        for group in GROUPS:
            new_group = Group.objects.create(name=group)
            new_group.save()
            for group_filter in Group.objects.filter(name=group):
                self.assertTrue(group_filter, group)
        """
        Create test permissions
        """
        for permission in PERMISSIONS:
            content_type = ContentType.objects.get_for_model(MemoSimple)
            new_permission = Permission.objects.create(name=permission, content_type=content_type,
                                                       codename=permission)
            new_permission.save()
            for permission_filter in Permission.objects.filter(name=permission):
                self.assertTrue(permission_filter, permission)
        """
        Assign permissions to groups
        """
        group_tu = Group.objects.get(name="tu")
        to_status_distribusi_kabag = Permission.objects.get(name="to_status_distribusi_kabag")
        group_tu.permissions.add(to_status_distribusi_kabag)
        group_tu.save()

        group_kabag = Group.objects.get(name="kabag")
        to_status_disposisi_kasubag = Permission.objects.get(name="to_status_disposisi_kasubag")
        group_kabag.permissions.add(to_status_disposisi_kasubag)
        group_kabag.save()

        group_kasubag = Group.objects.get(name="kasubag")
        to_status_disposisi_pelaksana = Permission.objects.get(name="to_status_disposisi_pelaksana")
        group_kasubag.permissions.add(to_status_disposisi_pelaksana)
        group_kasubag.save()

        """
        Assign users to groups
        """
        for user_to_group in USERS_TO_GROUP:
            user = User.objects.get(username=user_to_group["user"])
            group = Group.objects.get(name=user_to_group["group"])
            user.groups.add(group)
            user.save()
            self.assertTrue(User.objects.get(username=user_to_group["user"]).get_all_permissions(),
                            "disposisi.".join(user_to_group["permission"]))

        """
        Obtain JWT token for for all users
        """
        for user in USERS:
            url = reverse("token_obtain_pair")
            response = self.client.post(url, {'username': user, 'password': user}, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue('access' in response.data)
            access_token = response.data['access']
            user_token = {
                "user": user,
                "access_token": access_token
            }
            USERS_TOKENS.append(user_token)

    def tearDown(self):
        User.objects.all().delete()
        Group.objects.all().delete()
        Permission.objects.all().delete()
        MemoSimple.objects.all().delete()

    def test_create_memosimple_unauthenticated(self):
        """
        Ensure we can create a new memosimple object but unauthenticated.
        """
        url = reverse("disposisi:memosimple-api-list-create")
        data = {
            "subject": "Subject 1",
            "information": "Information 1",
            "sender": "Sender 1"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_and_get_jwt_token(self):
        """
        Ensure login process is working and tokens is retrieved
        :return:
        """
        url = reverse("token_obtain_pair")
        response = self.client.post(url, {'username': 'username_01', 'password': 'password_01'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        token = response.data['access']

    def test_create_memosimple_authenticated(self):
        """
        Ensure we can create a new memosimple object but authenticated.
        """
        url = reverse("disposisi:memosimple-api-list-create")
        data = {
            "subject": "Subject 1",
            "information": "Information 1",
            "sender": "Sender 1"
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MemoSimple.objects.count(), 1)
        self.assertEqual(MemoSimple.objects.get().subject, 'Subject 1')

    def test_change_memosimple_state_to_status_distribusi_kabag(self):
        """
        Change state of a memosimple model, from 0 to 1.
        :return:
        """
        memosimple_to_status_distribusi_kabag = MemoSimple.objects.create(subject="Subject To Distribusi Kabag",
                                                                          information="Information",
                                                                          sender="Sender")
        self.assertIs(memosimple_to_status_distribusi_kabag.subject, "Subject To Distribusi Kabag")
        self.assertIs(memosimple_to_status_distribusi_kabag.state, 0)
        memosimple_to_status_distribusi_kabag.save()

        modelpk = memosimple_to_status_distribusi_kabag.id
        url = reverse("disposisi:memosimple-api-update-state", kwargs={"pk": modelpk})
        data = {
            "transition": "0",
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + USERS_TOKENS[0]["access_token"])
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        check_model = MemoSimple.objects.get(id=modelpk)
        self.assertIs(check_model.state, 1)

    def test_change_memosimple_state_to_status_disposisi_kasubag(self):
        """
        Change state of a memosimple model, from 1 to 2.
        :return:
        """
        memosimple_to_status_disposisi_kasubag = MemoSimple.objects.create(subject="Subject To Disposisi Kasubag",
                                                                           information="Information",
                                                                           sender="Sender")
        self.assertIs(memosimple_to_status_disposisi_kasubag.state, 0)
        memosimple_to_status_disposisi_kasubag.save()

        """
        Update state from 0 to 1.
        """
        modelpk = memosimple_to_status_disposisi_kasubag.id
        url = reverse("disposisi:memosimple-api-update-state", kwargs={"pk": modelpk})
        data = {
            "transition": "0",
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + USERS_TOKENS[0]["access_token"])
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        check_model = MemoSimple.objects.get(id=modelpk)
        self.assertIs(check_model.state, 1)

        """
        Update state from 1 to 2.
        """
        modelpk = memosimple_to_status_disposisi_kasubag.id
        url = reverse("disposisi:memosimple-api-update-state", kwargs={"pk": modelpk})
        data = {
            "transition": "1",
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + USERS_TOKENS[1]["access_token"])
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        check_model = MemoSimple.objects.get(id=modelpk)
        self.assertIs(check_model.state, 2)

    def test_change_memosimple_state_to_status_disposisi_pelaksana(self):
        """
        Change state of a memosimple model, from 2 to 3.
        :return:
        """
        memosimple_to_status_disposisi_pelaksana = MemoSimple.objects.create(subject="Subject To Disposisi Pelaksana",
                                                                             information="Information",
                                                                             sender="Sender")
        self.assertIs(memosimple_to_status_disposisi_pelaksana.state, 0)
        memosimple_to_status_disposisi_pelaksana.save()

        """
        Update state from 0 to 1.
        """
        modelpk = memosimple_to_status_disposisi_pelaksana.id
        url = reverse("disposisi:memosimple-api-update-state", kwargs={"pk": modelpk})
        data = {
            "transition": "0",
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + USERS_TOKENS[0]["access_token"])
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        check_model = MemoSimple.objects.get(id=modelpk)
        self.assertIs(check_model.state, 1)

        """
        Update state from 1 to 2.
        """
        modelpk = memosimple_to_status_disposisi_pelaksana.id
        url = reverse("disposisi:memosimple-api-update-state", kwargs={"pk": modelpk})
        data = {
            "transition": "1",
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + USERS_TOKENS[1]["access_token"])
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        check_model = MemoSimple.objects.get(id=modelpk)
        self.assertIs(check_model.state, 2)

        """
        Update state from 2 to 3.
        """
        modelpk = memosimple_to_status_disposisi_pelaksana.id
        url = reverse("disposisi:memosimple-api-update-state", kwargs={"pk": modelpk})
        data = {
            "transition": "2",
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + USERS_TOKENS[2]["access_token"])
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        check_model = MemoSimple.objects.get(id=modelpk)
        self.assertIs(check_model.state, 3)

    def test_change_memosimple_state_to_invalid_status(self):
        """
        Change state of a memosimple model to invalid status.
        :return:
        """
        memosimple_to_invalid_status = MemoSimple.objects.create(subject="Subject To Distribusi Kabag",
                                                                 information="Information",
                                                                 sender="Sender")
        self.assertIs(memosimple_to_invalid_status.subject, "Subject To Distribusi Kabag")
        self.assertIs(memosimple_to_invalid_status.state, 0)
        memosimple_to_invalid_status.save()

        modelpk = memosimple_to_invalid_status.id
        url = reverse("disposisi:memosimple-api-update-state", kwargs={"pk": modelpk})
        data = {
            "transition": "999",
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        check_model = MemoSimple.objects.get(id=modelpk)
        self.assertIs(check_model.state, 0)

    def test_change_memosimple_state_to_status_distribusi_kabag_with_wrong_permission(self):
        """
        Change state of a memosimple model, from 0 to 1, but with wrong permission.
        :return:
        """
        memosimple_to_status_distribusi_kabag = MemoSimple.objects.create(subject="Subject To Distribusi Kabag",
                                                                          information="Information",
                                                                          sender="Sender")
        self.assertIs(memosimple_to_status_distribusi_kabag.subject, "Subject To Distribusi Kabag")
        self.assertIs(memosimple_to_status_distribusi_kabag.state, 0)
        memosimple_to_status_distribusi_kabag.save()

        modelpk = memosimple_to_status_distribusi_kabag.id
        url = reverse("disposisi:memosimple-api-update-state", kwargs={"pk": modelpk})
        data = {
            "transition": "0",
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + USERS_TOKENS[1]["access_token"])
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        check_model = MemoSimple.objects.get(id=modelpk)
        self.assertIs(check_model.state, 0)

    def test_change_memosimple_state_to_status_disposisi_kasubag_with_wrong_permission(self):
        """
        Change state of a memosimple model, from 1 to 2, but with wrong permission.
        :return:
        """
        memosimple_to_status_disposisi_kasubag = MemoSimple.objects.create(subject="Subject To Disposisi Kasubag",
                                                                           information="Information",
                                                                           sender="Sender")
        self.assertIs(memosimple_to_status_disposisi_kasubag.state, 0)
        memosimple_to_status_disposisi_kasubag.save()

        """
        Update state from 0 to 1.
        """
        modelpk = memosimple_to_status_disposisi_kasubag.id
        url = reverse("disposisi:memosimple-api-update-state", kwargs={"pk": modelpk})
        data = {
            "transition": "0",
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + USERS_TOKENS[0]["access_token"])
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        check_model = MemoSimple.objects.get(id=modelpk)
        self.assertIs(check_model.state, 1)

        """
        Update state from 1 to 2.
        """
        modelpk = memosimple_to_status_disposisi_kasubag.id
        url = reverse("disposisi:memosimple-api-update-state", kwargs={"pk": modelpk})
        data = {
            "transition": "1",
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + USERS_TOKENS[0]["access_token"])
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        check_model = MemoSimple.objects.get(id=modelpk)
        self.assertIs(check_model.state, 1)

    def test_change_memosimple_state_to_status_disposisi_pelaksana_with_wrong_permission(self):
        """
        Change state of a memosimple model, from 2 to 3, but with the wrong permission.
        :return:
        """
        memosimple_to_status_disposisi_pelaksana = MemoSimple.objects.create(subject="Subject To Disposisi Pelaksana",
                                                                             information="Information",
                                                                             sender="Sender")
        self.assertIs(memosimple_to_status_disposisi_pelaksana.state, 0)
        memosimple_to_status_disposisi_pelaksana.save()

        """
        Update state from 0 to 1.
        """
        modelpk = memosimple_to_status_disposisi_pelaksana.id
        url = reverse("disposisi:memosimple-api-update-state", kwargs={"pk": modelpk})
        data = {
            "transition": "0",
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + USERS_TOKENS[0]["access_token"])
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        check_model = MemoSimple.objects.get(id=modelpk)
        self.assertIs(check_model.state, 1)

        """
        Update state from 1 to 2.
        """
        modelpk = memosimple_to_status_disposisi_pelaksana.id
        url = reverse("disposisi:memosimple-api-update-state", kwargs={"pk": modelpk})
        data = {
            "transition": "1",
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + USERS_TOKENS[1]["access_token"])
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        check_model = MemoSimple.objects.get(id=modelpk)
        self.assertIs(check_model.state, 2)

        """
        Update state from 2 to 3.
        """
        modelpk = memosimple_to_status_disposisi_pelaksana.id
        url = reverse("disposisi:memosimple-api-update-state", kwargs={"pk": modelpk})
        data = {
            "transition": "2",
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + USERS_TOKENS[3]["access_token"])
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        check_model = MemoSimple.objects.get(id=modelpk)
        self.assertIs(check_model.state, 2)