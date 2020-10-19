from __future__ import print_function
import xml.etree.ElementTree as ET
import datetime
import time
import sys
import json
import pandas as pd
from urllib.parse import urlencode
from urllib.request import urlopen
from urllib.error import HTTPError

OAI = '{http://www.openarchives.org/OAI/2.0/}'
ARXIV = '{http://arxiv.org/OAI/arXiv/}'
BASE = 'http://export.arxiv.org/oai2?verb=ListRecords&'


class Record(object):
    def __init__(self, xml_record):
        self.xml = xml_record
        self.id = self._get_text(ARXIV, 'id')
        self.url = 'https://arxiv.org/abs/' + self.id
        self.title = self._get_text(ARXIV, 'title')
        self.abstract = self._get_text(ARXIV, 'abstract')
        self.cats = self._get_text(ARXIV, 'categories')
        self.created = self._get_text(ARXIV, 'created')
        self.updated = self._get_text(ARXIV, 'updated')
        self.authors = self._get_authors()

    def _get_text(self, namespace, tag): #extract the tags content from xml
        try:
            return self.xml.find(namespace + tag).text.strip().lower().replace('\n', ' ')
        except:
            return ''

    def _get_name(self, parent, attribute): #extract the attributes of authors - firstname and lastname
        try:
            return parent.find(ARXIV + attribute).text.lower()
        except:
            return "n/a"

    def _get_authors(self): #extract the list of authors
        authors_xml = self.xml.findall(ARXIV + 'authors/' + ARXIV + 'author')
        last_names = [self._get_name(author, 'keyname') for author in authors_xml]
        first_names = [self._get_name(author, 'forenames') for author in authors_xml]
        full_names = [a + ' ' + b for a, b in zip(first_names, last_names)]
        return full_names

    def output(self): #the json output file format
        d = {
            'title': self.title,
            'id': self.id,
            'abstract': self.abstract,
            'categories': self.cats,
            'created': self.created,
            'updated': self.updated,
            'authors': self.authors,
            'url': self.url
        }
        return d


class Scraper(object):
    def __init__(self, category):
        self.cat = str(category)
        self.t = 30
        self.timeout = 300
        self.f = '2010-10-10'
        self.u = '2020-10-10'
        self.url = BASE + 'from=' + self.f + '&until=' + self.u + '&metadataPrefix=arXiv&set=%s' % self.cat

    def scrape(self): # scraping by reading the response and converting to xml and parsing the xml and extracting required info and converting it to json
        t0 = time.time()
        tx = time.time()
        elapsed = 0.0
        url = self.url
        ds = []
        k = 1
        while True:
            print('fetching up to ', 1000 * k, 'records...')
            try:
                response = urlopen(url)
            except HTTPError as e:
                if e.code == 503:
                    to = int(e.hdrs.get('retry-after', 30))
                    print('Got 503. Retrying after {0:d} seconds.'.format(self.t))
                    time.sleep(self.t)
                    continue
                else:
                    raise
            k += 1
            xml = response.read()
            root = ET.fromstring(xml)
            records = root.findall(OAI + 'ListRecords/' + OAI + 'record')
            for record in records:
                meta = record.find(OAI + 'metadata').find(ARXIV + 'arXiv')
                record = Record(meta).output()
                ds.append(record)
            try:
                token = root.find(OAI + 'ListRecords').find(OAI + 'resumptionToken')
            except:
                return 1
            if token is None or token.text is None:
                break
            else:
                url = BASE + 'resumptionToken=%s' % token.text
            ty = time.time()
            elapsed += (ty - tx)
            if elapsed >= self.timeout:
                break
            else:
                tx = time.time()
        t1 = time.time()
        print('fetching is completed in {0:.1f} seconds.'.format(t1 - t0))
        print('Total number of records {:d}'.format(len(ds)))
        return ds



# scraper = Scraper(category='physics')
#scraper = Scraper(category='stat')
# scraper = Scraper(category='math')
# scraper = Scraper(category='q-bio')
# scraper = Scraper(category='q-fin')
# scraper = Scraper(category='econ')
# scraper = Scraper(category='eess')
# scraper = Scraper(category='cs')
"""output = scraper.scrape()
with open("C:/Study/NinthSem/Information Retrieval/Package/researchpaper-searchengine/scrapper/data/stat.json",'w')as f:
    json.dump(output, f)"""
