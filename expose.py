#!/usr/local/bin/python2.7
# -*-coding:UTF-8-sig -*-
from eve.flaskapp import Eve
from eve_sqlalchemy import SQL

from base import Base

app = Eve(auth=None, settings='config/eve-config.py', data=SQL)
db = app.data.driver
Base.metadata.bind = db.engine
db.Model = Base
db.create_all()

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)
    