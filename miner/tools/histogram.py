#!/usr/bin/env python
#---------- histogram.py----------#
# histogram.py code borrows from code in 'Text Processing in Python' by David Mertz.
# Copyright is public domain, and I derived from that code.
# This stuff is copyrighted by AW (except the code samples which are released to the public domain

# Create occurrence counts of words or characters
# A few utility functions for presenting results
# Avoids requirement of recent Python features

from string import split, maketrans, translate, punctuation, digits
import sys
from types import *
import types

def word_histogram(source):
    """Create histogram of normalized words (no punct or digits)
	scale that in terms of percentage"""
    hist = {}
    trans = maketrans('','')
    if type(source) in (StringType,UnicodeType):  # String-like src
        for word in split(source):
            word = translate(word, trans, punctuation+digits)
	    word=word.lower()
            if len(word) > 0:
                hist[word] = hist.get(word,0) + 1
    elif hasattr(source,'read'):                  # File-like src
        try:
            from xreadlines import xreadlines     # Check for module
            for line in xreadlines(source):
                for word in split(line):
                    word = translate(word, trans, punctuation+digits)
                    word=word.lower()
                    if len(word) > 0:
                        hist[word] = hist.get(word,0) + 1
        except ImportError:                       # Older Python ver
            line = source.readline()          # Slow but mem-friendly
            while line:
                for word in split(line):
                    word = translate(word, trans, punctuation+digits)
                    word=word.lower()
                    if len(word) > 0:
                        hist[word] = hist.get(word,0) + 1
                line = source.readline()
    else:
        raise TypeError, \
              "source must be a string-like or file-like object"
    return hist

def char_histogram(source, sizehint=1024*1024):
    hist = {}
    if type(source) in (StringType,UnicodeType):  # String-like src
        for char in source:
            hist[char] = hist.get(char,0) + 1
    elif hasattr(source,'read'):                  # File-like src
        chunk = source.read(sizehint)
        while chunk:
            for char in chunk:
                hist[char] = hist.get(char,0) + 1
            chunk = source.read(sizehint)
    else:
        raise TypeError, \
              "source must be a string-like or file-like object"
    return hist

def most_common(hist, num=1):
    pairs = []
    for pair in hist.items():
        pairs.append((pair[1],pair[0]))
    pairs.sort()
    pairs.reverse()
    return pairs[:num]

def all_sorted(hist, num=1):
    num=len(hist)
    all_normal(hist)
    pairs = []
    for pair in hist.items():
        pairs.append((pair[1],pair[0]))
    pairs.sort()
    pairs.reverse()
    return pairs[:num]

def all_normal(hist):
	numwords=0
	for eachword in hist:
		numwords+=hist[eachword]
	for eachword in hist:
		hist[eachword]=100.0*(float(hist[eachword])/numwords)
	return hist

def first_things(hist, num=1):
    pairs = []
    things = hist.keys()
    things.sort()
    for thing in things:
        pairs.append((thing,hist[thing]))
    pairs.sort()
    return pairs[:num]

if __name__ == '__main__':
    if len(sys.argv) > 1:
        hist = word_histogram(open(sys.argv[1]))
    else:
        hist = word_histogram(sys.stdin)
    stopwords = word_histogram(open('stopwords.txt'))
	#sorted = all_sorted(hist, len(hist))
	# BUG HERE, FIX THIS!!!!!
	# sorted is no longer a useful dictionary, because the floats are the key, not the value
	# sorted is being truncated in the dict() conversion
	#sorted = dict (sorted) # <--- is float:word should be word:float
	#print 'sorted:',sorted
	#for each in sorted:
	#	print each
	#print each,',',sorted[each]
    total = 0
    for each in hist:
	total += hist[each]
	total = total*1.0
    stopped = 0
    oldHistlen = len(hist)
    for stop in stopwords:
	if stop in hist:
		stopped += 1
		hist.pop(stop)	
    if stopped > 0:
	print 'histogram: Total words not displayed because they are stopwords:',stopped
    print 'histogram: Total count word in input stream:',int(total)
    print 'histogram: Number of unique words input:',oldHistlen
    print 'histogram: Number of words after stopwords are removed:',len(hist)
    print 'histogram: Word, count, % of total words (100*wordcount/totalwords)'
    for each in hist:
	print '%s,%d,%f'%(each,hist[each],100.0*(hist[each]/total))
    sys.exit()
