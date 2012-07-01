# -*- coding: utf-8 -*-
from sqlalchemy.orm import Query


def compute_join_table_name(from_, to):
    """Computes the many to many table name between two models.
    """
    return "%s_%s" % (from_.__tablename__, to.__tablename__)


class Model(object):
    """Base class for models."""
    query_class = None

    @classmethod
    def query(cls, session=None):
        if cls.query_class is None:
            raise NotImplementedError('You must define a query class')
        return cls.query_class(cls, session)

    @classmethod
    def set_query_class(cls, query_class):
        """Model - query class has to be bidirectional.
        """
        cls.query_class = query_class
        query_class.model = cls


class Query(Query):
    """Base class for queries.
    """
    @property
    def base(self):
        """Return the base query.
        """
        return self
