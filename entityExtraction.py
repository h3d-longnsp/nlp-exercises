# -*- coding: utf-8 -*-
import re
from pyvi import ViUtils
from underthesea import word_tokenize

entities = []

if __name__ == "__main__":
    textFile = open("document.txt", "r", encoding="utf-8")
    text = textFile.read()

    # Perform segmentation first before extract entity
    tokens = word_tokenize(text)

    # Must add `?:` to turn all capturing groups to non-capturing
    # bacause `re.findall` returns capture tuple lists when 
    # multiple capture groups are defined in the pattern
    patterns = r'''(?x)                       # set flag to allow verbose regexps
                (?:[A-Z][a-zA-Z]*[-\s\w\s]*)  # Capitalized words with optinal hyphens
              | (?:19|2[0-9])\d{2}            # year in range 1900-2999 
              | \b(?:[^.\sa-z]*\d)+\b         # numbers
              | (?:(?:https?:\/\/)*[a-zA-Z0-9-]+(?:\.[a-zA-Z]+)+(?:\/[a-zA-Z0-9\/_?=&+-]+)*)   # URLs
                '''

    for token in tokens:
        # Remove accents to get entities with Unicode characters
        accentsRemoved = ViUtils.remove_accents(token).decode("utf-8") # Decode the bytes object to produce a string
        
        output = re.findall(patterns, accentsRemoved) 
        if output:
            entities.append(output)

    with open("entities.txt", "w") as save:
        print(entities, file=save)
        save.close()