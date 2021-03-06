#!/usr/local/bin/python2.7
# -*- coding: utf-8-sig -*-
import argparse
import logging
import os

import sqlalchemy
from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy.orm.session import sessionmaker

#if no env variable has been defined, a default one is set
if not(os.environ.has_key("SUBDB")):
    os.environ['SUBDB'] = 'mysql://root:cnim@127.0.0.1:3306/sub_ai'

URLS = {
    'SQL':os.environ['SUBDB'],
}

#print message or not
parser = argparse.ArgumentParser()
parser.add_argument('-v','--verbose',action='store_true')
parser.add_argument('-a','--alerts',action='store_true')
args = parser.parse_args()

if args.verbose:
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)
else:
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.WARNING)

try:
    engine = sqlalchemy.create_engine(URLS['SQL'])
    Session = sessionmaker(bind=engine)
    Base = declarative_base(bind=engine)
    DBSession = sessionmaker(bind = engine)
    Base.metadata.create_all(engine)
except Exception:
    logging.error('Database is not reachable with provided path : %s',URLS['SQL'])
    logging.error('Please check database instance is running and database name exists')
    exit(0)    
