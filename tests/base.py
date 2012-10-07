# -*- coding: utf-8 -*-
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite://', echo=False)
Session = sessionmaker(engine)
Base = declarative_base()
session = Session()


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(engine)
        super(BaseTestCase, self).setUp()

    def tearDown(self):
        super(BaseTestCase, self).tearDown()
        Base.metadata.drop_all(engine)

    @classmethod
    def tearDownClass(cls):
        Base.metadata.clear()
        Base._decl_class_registry = {}  # Tiny hack that cleans up the registry
