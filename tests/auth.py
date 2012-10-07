# -*- coding: utf-8 -*-
import unittest

from distillery import lazy, Set, SQLAlchemyDistillery as Distillery

from base import Base, BaseTestCase, session
from humans.auth import user_factory, permission_factory, group_factory


class UserSet(Set):
    class __distillery__(Distillery):
        __session__ = session

        @lazy
        def password(cls, instance, *args):
            instance.set_password('password')
            return instance.password

    class jeanphix:
        username = 'jeanphix'
        email_address = 'serafinjp@gmail.com'

    class admin:
        username = 'admin'
        email_address = 'admin@domain.tld'


class UserFactoryTest(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        cls.User = user_factory(Base)
        UserSet.__distillery__.__model__ = cls.User

    def test_by_username_or_email_address_from_email_address(self):
        UserSet().admin  # Creates the admin
        admin = self.User.query(session)\
                .by_username_or_email_address('admin@domain.tld')
        self.assertEqual(admin.username, 'admin')

    def test_by_username_or_email_address_from_username(self):
        UserSet().jeanphix  # Creates jeanphix
        jeanphix = self.User.query(session)\
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


class GroupSet(Set):
    class __distillery__(Distillery):
        __session__ = session

    class admin:
        name = 'admin'
        users = [UserSet.jeanphix]


class GroupFactoryTest(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        cls.User = user_factory(Base)
        UserSet.__distillery__.__model__ = cls.User
        cls.Group = group_factory(Base, cls.User)
        GroupSet.__distillery__.__model__ = cls.Group

    def test_has_group_name(self):
        users = UserSet()
        GroupSet().admin
        self.assertTrue(users.jeanphix.has_group('admin'))

    def test_has_group_name_false(self):
        users = UserSet()
        GroupSet().admin
        self.assertFalse(users.jeanphix.has_group('user'))


class PermissionSet(Set):
    class __distillery__(Distillery):
        __session__ = session

    class create_user:
        name = 'create_user'
        users = [UserSet.admin]


class PermissionFactoryWithUserTest(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        cls.User = user_factory(Base)
        UserSet.__distillery__.__model__ = cls.User
        cls.Permission = permission_factory(Base,
                user_class=cls.User)
        PermissionSet.__distillery__.__model__ = cls.Permission

    def test_user_permission_list(self):
        users, permissions = UserSet(), PermissionSet()
        self.assertIn(permissions.create_user.name,
            users.admin.permissions_list)

    def test_user_has_permission_name(self):
        users, permissions = UserSet(), PermissionSet()
        self.assertTrue(users.admin.has_permission(
            permissions.create_user.name))

    def test_user_has_permission_name_false(self):
        users, permissions = UserSet(), PermissionSet()
        self.assertFalse(users.admin.has_permission('create_group'))


class PermissionFactoryWithGroup(BaseTestCase):
    pass


if __name__ == '__main__':
        unittest.main()
