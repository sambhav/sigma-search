#!/usr/bin/python
# -*- coding: utf-8 -*-
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
import urllib2
import docx
import json


def getTextFromDocx(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec,
                           laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ''
    maxpages = 0
    caching = True
    pagenos = set()
    for page in PDFPage.get_pages(
        fp,
        pagenos,
        maxpages=maxpages,
        password=password,
        caching=caching,
        check_extractable=True,
        ):

        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text


with open('docs.txt', 'r') as f:
    content = f.readlines()

docs = []
for line in content:
    line = line.split(' , ')
    try:
        docs.append([line[0], line[1]])
    except:
        docs.append([line[0], ''])
x = []

for doc in docs:
    url = doc[0]
    title = doc[1]
    content = ''
    try:
        response = urllib2.urlopen(url)
        if url.endswith('.docx'):
            with open('temp.docx', 'w') as f:
                f.write(response.read())
            content = ' '.join(getTextFromDocx('temp.docx').split())
        elif url.endswith('.pdf'):
            with open('temp.pdf', 'w') as f:
                f.write(response.read())
            content = ' '.join(convert_pdf_to_txt('temp.pdf').split())
    except:
        pass
    print title
    x.append({'URL': url, 'Title': title, 'Content': content})

with open('docs.json', 'w') as f:
    json.dump(x, f)

			