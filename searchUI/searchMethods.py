import whoosh
from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.spelling import ListCorrector
from whoosh.qparser import MultifieldParser
from PIL import Image
import imagehash

#Give Typo Suggestions
def giveSuggestions(text, ix):
	with ix.searcher() as s:
		corrector = s.corrector("content")
		x = text.split()
		return [ corrector.suggest(i,limit=1)[0] for i in x ]

#Image Search , returns an array of triples
def imgsearch(x):
	ix = open_dir("imageindex")
	with ix.searcher() as searcher:
		query = MultifieldParser(['title','imgname'], ix.schema).parse(x)
		results=searcher.search(query)
		return [ [i['imgname'], i['path'], i['imgpath']] for i in results]

#Reverse Image search
def revimg(x):	
	ix = open_dir("imageindex")
	with ix.searcher() as searcher:
		query = MultifieldParser(['imghash'], ix.schema).parse(str(imagehash.average_hash(Image.open(x))))
		results=searcher.search(query)
		return [ [i['imgname'], i['path'], i['imgpath']] for i in results]

#Docs and PDF searcher
#Flag indicates if typo has been corrected or not
def docsearch(x,flag=0):
	ix=open_dir("docindex")
	with ix.searcher() as searcher:
		query = MultifieldParser(['title','path','content'], ix.schema).parse(x)
		results = searcher.search(query)
		ans = [] 
		for i in results:
			try:
				ans.append([i['title'],i['path'],i.highlights("content", top=5) ])
			except(e):
				print e	
		#To handle typos		
		if len(ans)==0 and flag==0 and len(x)>0:
			sugg=" ".join(giveSuggestions(x, ix))
			ans = docsearch(sugg, 1)
			ans.append(['1',sugg,''])
		#Appends a triple to render the Did you mean in JS	
		elif (len(ans)>0 and flag==0) or len(x)==0:
			ans.append(['0', '', ''])		
		return ans

#Page and Content Searcher
def pagesearch(x,flag=0):
	ix=open_dir("pageindex")
	with ix.searcher() as searcher:
		query = MultifieldParser(['title','path','content'], ix.schema).parse(x)
		results = searcher.search(query)

		ans = [] 
		for i in results:
			try:
				ans.append([i['title'],i['path'],i.highlights("content", top=5) ])
			except(e):
				print e	
		#To handle typos		
		if len(ans)==0 and flag==0 and len(x)>0:
			sugg=" ".join(giveSuggestions(x, ix))
			ans = pagesearch(sugg, 1)
			ans.append(['1',sugg,''])
		elif (len(ans)>0 and flag==0) or len(x)==0:
			ans.append(['0', '', ''])		
		return ans
