#! -*- coding: utf8 -*-

#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

from trytond.pool import *
from trytond.model import fields
from trytond.pyson import Eval
from trytond.pyson import Id
from trytond.pyson import Bool, Eval
from trytond.transaction import Transaction

__all__ = ['Address']
__metaclass__ = PoolMeta

class Address:
    __name__ = 'party.address'

    @classmethod
    def __setup__(cls):
        super(Address, cls).__setup__()
        cls.street.size = 70
        cls.city.size = 50

    @staticmethod
    def default_country():
        return Id('country', 'ec').pyson()

    @staticmethod
    def default_street():
        Company = Pool().get('company.company')
        company = None
        company = Transaction().context.get('company')
        if company:
            companys = Company.search([('id', '=', company)])
            for c in companys:
                comp = c
            if comp:
                if comp.party.addresses[0]:
                    return comp.party.addresses[0].street
                else:
                    return "ECUADOR"
        else:
            return "ECUADOR"

    @staticmethod
    def default_subdivision():
        Subdivision = Pool().get('country.subdivision')
        Company = Pool().get('company.company')
        company = None
        company = Transaction().context.get('company')
        if company:
            companys = Company.search([('id', '=', company)])
            for c in companys:
                comp = c
            if comp:
                if comp.party.addresses[0].subdivision:
                    sub= Subdivision.search([('code','=',comp.party.addresses[0].subdivision.code)])
                    return sub[0].id
