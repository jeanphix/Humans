# -*- coding: utf-8 -*-
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from humans.auth import user_factory, permission_factory, group_factory

from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:////tmp/test.db', echo=True)
Session = sessionmaker(engine)


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.Base = declarative_base()
        self.session = Session()
        if hasattr(self, 'models_setup'):
            self.models_setup()
        self.Base.metadata.create_all(engine)
        if hasattr(self, 'add_fixtures'):
            self.add_fixtures()
        self.session.commit()

    def tearDown(self):
        self.Base.metadata.drop_all(engine)
        self.Base.metadata.clear()


class UserFactoryTest(BaseTestCase):
    def models_setup(self):
        self.User = user_factory(self.Base)

    def add_fixtures(self):
        jeanphix = self.User('jeanphix', 'serafinjp@gmail.com', 'mypassword')
        self.session.add(jeanphix)
        admin = self.User('admin', 'admin@domain.tld', 'password')
        self.session.add(admin)

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


class GroupFactoryTest(BaseTestCase):
    pass


class PermissionFactoryWithUserTest(BaseTestCase):
    def models_setup(self):
        self.User = user_factory(self.Base)
        self.Permission = permission_factory(self.Base,
                user_class=self.User)

    def add_fixtures(self):
        admin = self.User('admin', 'admin@domain.tld', 'password')
        self.session.add(admin)
        create_user = self.Permission('create_user')
        admin.permissions.append(create_user)
        self.session.add(create_user)

    def test_user_permission_list(self):
        admin = self.User.query(self.session)\
                .by_username_or_email_address('admin')
        self.assertIn('create_user', admin.permissions_list)


class PermissionFactoryWithGroup(BaseTestCase):
    pass



if __name__ == '__main__':
        unittest.main()
