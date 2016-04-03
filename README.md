# sigma_search

Installing:

git clone https://github.com/samj1912/sigma_search.git


cd sigma_search


pip install -r requirements.txt

This will install all the requirements.

open search/search/spiders/spider.py

Change the start url, domains and rules of the spider according to your needs.

Change the parse docs method according to your needs.

Currently it processes all the images on a domain and calculates their hash to store.

Launch the crawler

Go to the directory sigma_search/search

Execute

scrapy crawl $spidername -o Output.json

Go to sigma_share/search/createindex.py

Edit the json file paths according to your needs.

Simply run createindex.py to create the index.

Once index has been created link the index folders in sigma_share/searchUI to allow searchMethods.py to search the files.

Add uploads/ folder to searchUI

Run app.py

Enjoy instant search results.


Go to  Reverse Search to upload files to do a reverse search among indexed images.

