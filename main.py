#!/usr/bin/env python3
import os
import xml.etree.ElementTree as ET

import requests

GOODREADS_KEY = None

def main():
    init()
    print(get_books_for_author(input("Tell me the author ya want. > ")))

def init():
    global GOODREADS_KEY
    try:
        GOODREADS_KEY = os.environ["KEY"]
    except KeyError as e:
        print("I need a key for this. Restart mate.")
        exit(1)

def get_books_for_author(author_name):
    global GOODREADS_KEY
    payload = {"key":GOODREADS_KEY, "q":author_name, "search[field]":"author"}
    response = requests.get("https://www.goodreads.com/search/index.xml", params=payload)
    return parse_response_from_goodreads(response.text)

def parse_response_from_goodreads(response):
    root = ET.fromstring(response)
    work = root.find("search").find("results").find("work")
    if work is None:
        return ":("
    return work.find("best_book").find("title").text

if __name__ == "__main__":
    main()

#Extra bits
#I have entered an author with more than one match in Goodreads and want
#to be told which author to pick from.

#I've been given a book, now I want to see what the average rating is for that. :thumbsup:
