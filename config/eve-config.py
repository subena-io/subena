# -*- coding: utf-8-sig -*-
from base import URLS
from package.model.tables import Family,Criterion,Value,Stats,Alerts

SERVER_NAME= None
#lsof -i:5000
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI= URLS['SQL']
RESOURCE_METHODS= ['GET']
ITEM_METHODS= ['GET']
DEBUG=False
SQLALCHEMY_ECHO = False
EMBEDDING=True

ID_FIELD = 'id'
LAST_UPDATED = 'updated'
DATE_CREATED = 'created'
ETAG = 'etag'

DOMAIN= {
    'family': Family._eve_schema['family'],
    'criterion': Criterion._eve_schema['criterion'],
    'value': Value._eve_schema['value'],
    'stats': Stats._eve_schema['stats'],
    'alerts': Alerts._eve_schema['alerts']
}

DOMAIN['stats'].update({
    'item_title': 'stats',
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,
    'resource_methods': ['GET'],
    'item_methods': ['GET'],
    'pagination': False,
})

DOMAIN['family'].update({
    'item_title': 'family',
    'additional_lookup': {
        'url': '[0-9]+',
        'field': 'id',
    },
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,
    'resource_methods': ['GET'],
    'item_methods': ['GET'],
    'pagination': False,
})

DOMAIN['criterion'].update({
    'item_title': 'criterion',
    'additional_lookup': {
        'url': '[0-9]+',
        'field': 'id',
    },
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,
    'resource_methods': ['GET'],
    'item_methods': ['GET'],
    'pagination': False
})

DOMAIN['value'].update({
    'item_title': 'value',
    'additional_lookup': {
        'url': '[0-9]+',
        'field': 'id',
    },
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,
    'resource_methods': ['GET'],
    'item_methods': ['GET'],
    'pagination': False
})

DOMAIN['alerts'].update({
    'item_title': 'alerts',
    'additional_lookup': {
        'url': '[0-9]+',
        'field': 'id',
    },
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,
    'resource_methods': ['GET'],
    'item_methods': ['GET'],
    'pagination': False
})