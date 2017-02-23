#! -*- coding: utf8 -*-
from trytond.pool import *
from trytond.model import fields
from trytond.pyson import Eval
from trytond.pyson import Id
from trytond.pyson import Bool, Eval
from trytond.transaction import Transaction

__all__ = ['Address']


class Address:
    __name__ = 'party.address'
    __metaclass__ = PoolMeta
    
    @classmethod
    def __setup__(cls):
        super(Address, cls).__setup__()
        cls.street.size = 70
        cls.city.size = 50

    @staticmethod
    def default_country():
        return Id('country', 'ec').pyson()

    @fields.depends('street')
    def on_change_street(self):
        if self.street:
            street = self.street.strip()
            street = street.replace("\n","")
            self.street = street

    @fields.depends('city')
    def on_change_city(self):
        if self.city:
            city = self.city.strip()
            city = city.replace("\n","")
            self.city = city

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
