#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
#! -*- coding: utf8 -*-
from trytond.pool import *
from trytond.model import fields
from trytond.pyson import Eval
from trytond.pyson import Id
from trytond.pyson import Bool, Eval

__all__ = ['Party']
__metaclass__ = PoolMeta

class Party:
    __name__ = 'party.party'

    commercial_name = fields.Char('Commercial Name')
    supplier = fields.Boolean('Supplier')
    customer = fields.Boolean('Customer')
    type_document = fields.Selection([
                ('', ''),
                ('04', 'RUC'),
                ('05', 'Cedula'),
                ('06', 'Pasaporte'),
                ('07', 'Consumidor Final'),
            ], 'Type Document', states={
                'readonly': ~Eval('active', True),
            },  depends=['active'])

    @classmethod
    def __setup__(cls):
        super(Party, cls).__setup__()
        cls._error_messages.update({
                'invalid_vat_number': ('Invalid VAT Number "%s".')})
        cls._sql_constraints += [
            ('vat_number', 'UNIQUE(vat_number)',
                'VAT Number already exists!'),
        ]
        cls.vat_number.states['readonly'] |= Eval('type_document') == '07'
        cls.vat_number.depends.append('type_document')

    @staticmethod
    def default_type_document():
        return '05'

    @staticmethod
    def default_supplier():
        return False

    @staticmethod
    def default_customer():
        return False

    @fields.depends('type_document', 'vat_number')
    def on_change_type_document(self):
        res = {}
        if self.type_document == '07':
            res ['vat_number']= '9999999999999'
        else:
            if self.vat_number:
                res ['vat_number']= self.vat_number
            else:
                res ['vat_number']= ''
        return res

    @classmethod
    def search_rec_name(cls, name, clause):
        parties = cls.search([
                ('vat_number',) + tuple(clause[1:]),
                ], limit=1)
        if parties:
            return [('vat_number',) + tuple(clause[1:])]
        return [('name',) + tuple(clause[1:])]

    @classmethod
    def validate(cls, parties):
        for party in parties:
            if party.type_document == '04' and bool(party.vat_number):
                super(Party, cls).validate(parties)

    def pre_validate(self):
        if self.type_document == '':
            pass
        elif self.type_document == '06':
            pass
        else:
            if not self.vat_number:
                return
            if self.vat_number == '9999999999999':
                return
            vat_number = self.vat_number.replace(".", "")
            if vat_number.isdigit() and len(vat_number) > 9:
                is_valid = self.compute_check_digit(vat_number)
                if is_valid:
                    return
            self.raise_user_error('invalid_vat_number', (self.vat_number,))

    def compute_check_digit(self, raw_number):
        factor = 2
        x = 0
        set_check_digit = None

        if self.type_document == '04':
            # Si es RUC valide segun el tipo de tercero
            if int(raw_number[2]) < 6:
                type_party='persona_natural'
            if int(raw_number[2]) == 6:
                type_party='entidad_publica'
            if int(raw_number[2]) == 9:
                type_party='persona juridica'

            if type_party == 'persona_natural':
                if len(raw_number) != 13 or int(raw_number[2]) > 5 or raw_number[-3:] != '001':
                    return
                number = raw_number[:9]
                set_check_digit = raw_number[9]
                for n in number:
                    y = int(n) * factor
                    if y >= 10:
                        y = int(str(y)[0]) + int(str(y)[1])
                    x += y
                    if factor == 2:
                        factor = 1
                    else:
                        factor = 2
                res = (x % 10)
                if res ==  0:
                    value = 0
                else:
                    value = 10 - (x % 10)
                return (set_check_digit == str(value))

            elif type_party == 'entidad_publica':
                if not len(raw_number) == 13 or raw_number[2] != '6' \
                    or raw_number[-3:] != '001':
                    return
                number = raw_number[:8]
                set_check_digit = raw_number[8]
                for n in reversed(number):
                    x += int(n) * factor
                    factor += 1
                    if factor == 8:
                        factor = 2
                value = 11 - (x % 11)
                if value == 11:
                    value = 0
                return (set_check_digit == str(value))

            else:
                if len(raw_number) != 13 or \
                    (type_party in ['persona_juridica'] \
                    and int(raw_number[2]) != 9) or raw_number[-3:] != '001':
                    return
                number = raw_number[:9]
                set_check_digit = raw_number[9]
                for n in reversed(number):
                    x += int(n) * factor
                    factor += 1
                    if factor == 8:
                        factor = 2
                value = 11 - (x % 11)
                if value == 11:
                    value = 0
                return (set_check_digit == str(value))
        else:
            #Si no tiene RUC valide: cedula, pasaporte, consumidor final (cedula)
            if len(raw_number) != 10:
                return
            number = raw_number[:9]
            set_check_digit = raw_number[9]
            for n in number:
                y = int(n) * factor
                if y >= 10:
                    y = int(str(y)[0]) + int(str(y)[1])
                x += y
                if factor == 2:
                    factor = 1
                else:
                    factor = 2
            res = (x % 10)
            if res ==  0:
                value = 0
            else:
                value = 10 - (x % 10)
            return (set_check_digit == str(value))
