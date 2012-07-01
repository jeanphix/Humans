# -*- coding: utf-8 -*-
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from fixture import DataTestCase, SQLAlchemyFixture, TrimmedNameStyle


engine = create_engine('sqlite:////tmp/test.db', echo=False)
Session = sessionmaker(engine)
Base = declarative_base()

fixture = SQLAlchemyFixture(engine=engine,
        style=TrimmedNameStyle(suffix="Data"))


class Models(object):
    pass


class BaseTestCase(DataTestCase, unittest.TestCase):
    fixture = fixture

    def setUp(self):
        fixture.env = self
        Base.metadata.create_all(engine)
        super(BaseTestCase, self).setUp()
        self.session = Session()

    def tearDown(self):
        super(BaseTestCase, self).tearDown()
        Base.metadata.drop_all(engine)

    @classmethod
    def tearDownClass(cls):
        Base.metadata.clear()
        Base._decl_class_registry = {}  # Tiny hack that cleans up the registry
