#!/usr/bin/python
# -*- coding: utf-8 -*-
from whoosh.index import create_in
from whoosh.fields import *
import os
import json

imageschema = Schema(title=NGRAMWORDS(stored=True),
                     path=TEXT(stored=True),
                     imgname=NGRAMWORDS(stored=True),
                     imghash=ID(stored=True), imgpath=TEXT(stored=True))

if not os.path.exists('imageindex'):
    os.mkdir('imageindex')

ix = create_in('imageindex', imageschema)

with open('ultimate6.json', 'r') as f:
    doc = json.load(f)

writer = ix.writer()
for page in doc:
    images = page['Images'].split(' || ')
    for image in images:
        try:
            arr = image.split(' :: ')
            if len(arr) > 1:

                print arr, page['Title'], page['URL']
                writer.add_document(title=page['Title'], 
					path=page['URL'], 
					imgpath=arr[0], 
					imgname=arr[1],
                                    	imghash=arr[2])
        except:
            pass

writer.commit()

pageschema = Schema(title=NGRAMWORDS(stored=True, field_boost=2.0),
                    path=ID(stored=True), content=TEXT(stored=True,
                    field_boost=1.5))

if not os.path.exists('pageindex'):
    os.mkdir('pageindex')
ix = create_in('pageindex', pageschema)

writer = ix.writer()

with open('ultimate.json', 'r') as f1:
    doc1 = json.load(f1)

for page in doc1:
    writer.add_document(title=page['Title'], 
    					path=page['URL'],
                        content=page['Content'])
writer.commit()

docschema = Schema(title=NGRAMWORDS(stored=True, field_boost=2.0),
                   path=ID(stored=True), content=TEXT(stored=True,
                   field_boost=1.5))

if not os.path.exists('docindex'):
    os.mkdir('docindex')

ix = create_in('docindex', docschema)

writer = ix.writer()

with open('docs.json', 'r') as f2:
    doc2 = json.load(f2)
for page in doc2:
    writer.add_document(title=page['Title'], 
    					path=page['URL'],
                        content=page['Content'])

writer.commit()

			
