#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
#! -*- coding: utf8 -*-
from trytond.pool import *
from trytond.model import fields
from trytond.pyson import Eval
from trytond.pyson import Id
from trytond.pyson import Bool, Eval

__all__ = ['Configuration']

class Configuration:
    __name__ = 'party.configuration'
    __metaclass__ = PoolMeta

    @classmethod
    def default_party_lang(cls):
        Lang = Pool().get('ir.lang')
        langs = Lang.search([('code','=','es_EC')])
        return langs[0].id
