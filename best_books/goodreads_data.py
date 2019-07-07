#!/usr/bin/env python3
import os
import xml.etree.ElementTree as ET
import datetime

import requests

GOODREADS_KEY = None

def init():
    global GOODREADS_KEY
    try:
        GOODREADS_KEY = os.environ["GOODREADS_KEY"]
    except KeyError as e:
        print("I need a Goodreads key for this. Restart mate.")
        exit(1)

def get_books(query, field="all"):
    global GOODREADS_KEY
    assert field in ('title', 'author', 'all')
    payload = {"key":GOODREADS_KEY, "q":query, "search[field]":field}
    response = requests.get("https://www.goodreads.com/search/index.xml", params=payload)
    #now deal with response
    root = ET.fromstring(response.text)
    results = root.find("search").find("results")
    #loop through works and add to books list.
    books = []
    for work_from_XML in results.findall("work"):
        work_as_dictionary = {}
        work_as_dictionary["author_name"]=work_from_XML.find("best_book").find("author").find("name").text
        work_as_dictionary["title"]=work_from_XML.find("best_book").find("title").text
        work_as_dictionary["original_publication_year"]= int(work_from_XML.find("original_publication_year").text or 0)
        work_as_dictionary["average_rating"]=float(work_from_XML.find("average_rating").text)
        books.append(work_as_dictionary)
    return books

def get_books_for_author(author_name):
    return {
            "books": get_books(author_name, field="author")
    }

if __name__ == "__main__":
    init()


##
#understand how to get user to enter form info, take that and use it.
#flask form submit
#

##Attempt to get ISBN Number for book using API query.
#create function
#understand API for ISBN
#attempt to return ISBN
#create format string for URL to decent booshop with ISBN in query.




#Extra bits
#I have entered an author with more than one match in Goodreads and want
#to be told which author to pick from.
