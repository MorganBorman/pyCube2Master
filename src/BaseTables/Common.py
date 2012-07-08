from DatabaseManager import database_manager, Session

from sqlalchemy import or_
from sqlalchemy import SmallInteger, Integer, BigInteger, String, Boolean
from sqlalchemy import DateTime
from sqlalchemy import Column, Sequence, ForeignKey

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.orm import relation, mapper, relationship, backref
from sqlalchemy.schema import UniqueConstraint

class enum(object):
    def __init__(self, *items, **kwitems):
        i = 0
        for item in items:
            self.__setattr__(item, i)
            i += 1
            
        for item, value in kwitems.items():
            self.__setattr__(item, value)