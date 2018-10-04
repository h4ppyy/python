# -*- coding: utf-8 -*-
import MySQLdb as mdb
from bson.objectid import ObjectId
from pymongo import MongoClient

database_ip = '127.0.0.1'
client = MongoClient(database_ip, 27017)
db = client.edxapp

# course-v1:KHUk+KH303+2018_KH303_1
o = 'CAUk'
c = 'FD_CAU04K'
r = '2018_1'

cursor_active_versions = db.modulestore.active_versions.find_one({'org': o, 'course': c, 'run': r})
pb = cursor_active_versions.get('versions').get('published-branch')
structure = db.modulestore.structures.find_one({'_id': ObjectId(pb)})
blocks = structure.get('blocks')
for block in blocks:
    block_type = block.get('block_type')
    if block_type == 'course':
        field = block.get('fields')
        for n in field:
            print n
