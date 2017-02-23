from trytond.pool import Pool
from .party import *
from .address import *
from .configuration import *
from .company import *

def register():
    Pool.register(
        Party,
        Company,
        Address,
        Configuration,
        module='nodux_party_one', type_='model')
