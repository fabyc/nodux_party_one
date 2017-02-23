#! -*- coding: utf8 -*-
import string
from trytond.model import ModelView, ModelSQL, fields, Workflow
from trytond.pyson import Eval
from trytond.pool import Pool, PoolMeta
import hashlib
import base64

__all__ = ['Company']


class Company():
    'Company'
    __name__ = 'company.company'
    __metaclass__ = PoolMeta
    
    logo = fields.Binary('Logo de su empresa')

    @classmethod
    def __setup__(cls):
        super(Company, cls).__setup__()

    @staticmethod
    def default_sequence_sale():
        return 1

    @classmethod
    def default_currency(cls):
        Currency = Pool().get('currency.currency')
        usd= Currency.search([('code','=','USD')])
        return usd[0].id

    @staticmethod
    def default_timezone():
        return 'America/Guayaquil'
