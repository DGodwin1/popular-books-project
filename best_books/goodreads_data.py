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
        work_as_dictionary["author_name"] = work_from_XML.find("best_book").find("author").find("name").text
        work_as_dictionary["title"] = work_from_XML.find("best_book").find("title").text
        work_as_dictionary["original_publication_year"] = int(work_from_XML.find("original_publication_year").text or 0)
        work_as_dictionary["average_rating"] = float(work_from_XML.find("average_rating").text)
        work_as_dictionary["book_id"] = int(work_from_XML.find("best_book").find("id").text)
        books.append(work_as_dictionary)
    return books

def get_books_for_author(author_name):
    return {
            "books": get_books(author_name, field="author")
    }

def get_data_for_book_id(book_id):
    global GOODREADS_KEY
    payload = {"key":GOODREADS_KEY, "id":book_id}
    response = requests.get("https://www.goodreads.com/book/show.xml",params=payload)
    data_for_book = {}
    root = ET.fromstring(response.text)
    book_from_XML = root.find("book")
    data_for_book["title"] = book_from_XML.find("title").text
    data_for_book["author_name"] = book_from_XML.find("authors").find("author").find("name").text
    data_for_book["ISBN13"] = book_from_XML.find("isbn13").text
    data_for_book["average_rating"] = float(book_from_XML.find("average_rating").text)
    data_for_book["original_publication_year"] = int(book_from_XML.find("work").find("original_publication_year").text or 0)
    data_for_book["publisher"] = book_from_XML.find("publisher").text
    data_for_book["description"] = book_from_XML.find("description").text
    data_for_book["page_count"] = book_from_XML.find("num_pages").text
    data_for_book["book_id"] = book_id
    return data_for_book

if __name__ == "__main__":
    init()
    works = get_books("pynchon")
    goodreads_info = works[0]["book_id"]
    print(get_data_for_book_id(goodreads_info))
