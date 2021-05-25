import re

def clean(value, prefix, sufix=None):
    """Remove caracteres especiais do inicio da string"""
    nvalue = value
    if nvalue.startswith(prefix):
        nvalue = nvalue[len(prefix):]
    if sufix is not None and nvalue.endswith(sufix):
        nvalue = nvalue[:-1*len(sufix)]
    return nvalue

def trim(value):
    return value.strip()

def commaToPoint(value):
    return re.sub(r',', '.', value)

def nulls(value):
    return re.sub(r'^NULL$', '', value)

def nullToZero(value):
    if value == '':
        return "0"
    return re.sub(r'^NULLS', '0', value)