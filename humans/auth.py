# -*- coding: utf-8 -*-
import datetime
from passlib.context import CryptContext
from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime,\
        ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy.sql.expression import or_

from base import compute_join_table_name, Model, Query


class UserQuery(Query):
    """Query class for users."""
    @property
    def base(self):
        base = self
        if hasattr(self.model, 'permissions'):
            base = base.options(joinedload('permissions'))
        return base

    def by_username_or_email_address(self, value):
        """Retrieves a user by `username` or `email`.
        """
        return self.base.filter(or_(self.model.username==value,
            self.model.email_address==value)).first()


def user_factory(base, table_name='user', crypt_schemes = ['bcrypt'],
        query_class=UserQuery):
    """Creates a class that represents local users.

    :param base: The SQLAlchemy declarative base.
    :param table_name: The name of table where to store users.
    :param crypt_schemes: The passlib crypt schemes.
    """
    class User(base, Model):
        __tablename__ = table_name

        id = Column(Integer, primary_key=True)
        username = Column(String(80), unique=True, nullable=False)
        email_address = Column(String(80), unique=True)
        password = Column(String(80),  nullable=False)
        is_active = Column(Boolean, default=False, nullable=False)
        is_admin = Column(Boolean, default=False, nullable=False)
        created_at = Column(DateTime, default=datetime.datetime.now,
                nullable=False)
        updated_at = Column(DateTime, onupdate=datetime.datetime.now)

        def __init__(self, username=None, email_address=None, password=None,
                is_active=False, is_admin=False):
            self.username = username
            self.email_address = email_address
            if password is not None:
                self.set_password(password)
            self.is_active = is_active
            self.is_admin = is_admin

        def __new__(cls, *args, **kwargs):
            cls.crypt_context = CryptContext(schemes=crypt_schemes)
            return super(User, cls).__new__(cls, *args, **kwargs)

        def add_group(self, group):
            pass

        def check_password(self, password):
            return self.crypt_context.verify(password, self.password)

        def set_password(self, password):
            self.password = self.crypt_context.encrypt(password)


    User.set_query_class(query_class)


    return User


def permission_factory(base, table_name='permission', user_class=None,
        group_class=None):
    """Creates a class that represents permission.
    Those permission can be linked to users or groups.

    :param base: The SQLAlchemy delarative base.
    :param table_name: The name of the table where to store permission.
    :param user_class: The user class that requires permissions.
    :param group_class: The group class that requires permissions.
    """
    class Permission(base):
        __tablename__ = 'permission'

        id = Column(Integer, primary_key=True)
        name = Column(String(80), unique=True)
        if user_class is not None:
            users = relationship(user_class,
                secondary=lambda: user_permission,
                backref='permissions')
        if group_class is not None:
            groups = relationship(group_class,
                secondary=lambda: group_permission,
                backref='permissions')

        def __init__(self, name):
            self.name = name

        def __unicode__(self):
            return unicode(self.name)


    if user_class is not None:
        #  Adds `permissions_list` property to the user class
        def permissions_list(self):
            return [unicode(permission) for permission in self.permissions]

        user_class.permissions_list = property(permissions_list)

        # Adds `has_permission` method to the user class
        def has_permission(self, permission):
            return permission in self.permissions_list

        user_class.has_permission = has_permission

        #  Creates the associative table between user an permission
        user_permission = Table(
            compute_join_table_name(user_class, Permission),
            base.metadata,
            Column('user_id', Integer, ForeignKey(user_class.id)),
            Column('permission_id', Integer, ForeignKey(Permission.id))
        )

        UniqueConstraint(user_permission.c.user_id, user_permission.c.permission_id)


    if group_class is not None:
        #  Creates the associative class between group and permission
        group_permission = Table(
            compute_join_table_name(group_class, Permission),
            base.metadata,
            Column('permission_id', Integer, ForeignKey(Permission.id)),
            Column('group_id', Integer, ForeignKey(group_class.id))
        )

        UniqueConstraint(group_permission.c.permission_id, group_permission.c.group_id)


    return Permission


def group_factory(base, user_class, table_name='group'):
    """Creates a class that reprensents user groups.

    :param base: The SQLAlchemy declarative base.
    :param user_class: The user class.
    :param table_name: The name of the table where to store groups.
    """
    class Group(base):
        __tablename__ = table_name

        id = Column(Integer, primary_key=True)
        name = Column(String(80), unique=True)
        users = relationship(user_class,
            secondary=lambda: user_group,
            backref='groups')

        def __init__(self, name=None):
            self.name = name

        def __unicode__(self):
            return unicode(self.name)

        @classmethod
        def by_name(cls, name):
            return cls.query(session).filter(cls.name==name).first()


    user_group = Table(
        compute_join_table_name(user_class, Group),
        base.metadata,
        Column('user_id', Integer, ForeignKey(user_class.id)),
        Column('group_id', Integer, ForeignKey(Group.id))
    )


    UniqueConstraint(user_group.c.user_id, user_group.c.group_id)


    return Group
