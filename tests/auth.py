# -*- coding: utf-8 -*-
import unittest

from fixture import DataSet
from fixture.dataset import SuperSet

from base import Base, Models, BaseTestCase
from humans.auth import user_factory, permission_factory, group_factory



class UserData(DataSet):
    class jeanphix:
        username = 'jeanphix'
        email_address = 'serafinjp@gmail.com'
        password = 'mypassword'

    class admin:
        username = 'admin'
        email_address = 'admin@domain.tld'
        password = 'password'


class UserFactoryTest(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        cls.User = user_factory(Base)

    datasets = [UserData]

    def test_by_username_or_email_address_from_email_address(self):
        admin = self.User.query(self.session)\
                .by_username_or_email_address('admin@domain.tld')
        self.assertEqual(admin.username, 'admin')

    def test_by_username_or_email_address_from_username(self):
        jeanphix = self.User.query(self.session)\
                .by_username_or_email_address('jeanphix')
        self.assertEqual(jeanphix.email_address, 'serafinjp@gmail.com')

    def test_check_invalid_password(self):
        user = self.User(password='password')
        self.assertFalse(user.check_password('invalid'))

    def test_check_valid_password(self):
        user = self.User(password='password')
        self.assertTrue(user.check_password('password'))

    def test_permissions_list_should_not_exist(self):
        user = self.User()
        with self.assertRaises(AttributeError):
            user.permissions_list

    def test_init(self):
        user = self.User('username', 'user@domain.tld', 'password')
        self.assertEqual(user.username, 'username')
        self.assertEqual(user.email_address, 'user@domain.tld')
        self.assertTrue(user.check_password('password'))


class GroupData(DataSet):
    class admin:
        name = 'admin'
        users = [UserData.jeanphix]


class GroupFactoryTest(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        cls.User = user_factory(Base)
        cls.Group = group_factory(Base, cls.User)

    datasets = [UserData, GroupData]

    def test_has_group_name(self):
        self.assertTrue(self.data.UserData.jeanphix.has_group('admin'))

    def test_has_group_name_false(self):
        self.assertFalse(self.data.UserData.jeanphix.has_group('user'))


class PermissionData(DataSet):
    class Meta:
        storable_name = 'Permission'

    class create_user:
        name = 'create_user'
        users = [UserData.admin]


class PermissionFactoryWithUserTest(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        cls.User = user_factory(Base)
        cls.Permission = permission_factory(Base,
                user_class=cls.User)

    datasets = [UserData, PermissionData]

    def test_user_permission_list(self):
        self.assertIn('create_user', self.data.UserData.admin.permissions_list)

    def test_user_has_permission_name(self):
        self.assertTrue(self.data.UserData.admin.has_permission('create_user'))

    def test_user_has_permission_name_false(self):
        self.assertFalse(self.data.UserData.admin\
                .has_permission('create_group'))


class PermissionFactoryWithGroup(BaseTestCase):
    pass



if __name__ == '__main__':
        unittest.main()
