
# -*- coding: UTF-8 -*-

"""vsm.py implements a toy search engine to illustrate the vector
space model for documents.

It asks you to enter a search query, and then returns all documents
matching the query, in decreasing order of cosine similarity,
according to the vector space model."""

from collections import defaultdict
import math
import sys


class vsm:


  def __init__(self, sent_filename="./documents/COCO_sentense.txt"):
    # get sentence dump
    self.sent_filename = sent_filename
    try:
      self.document_filenames = dict([item.strip().split(',') \
      for item in open(self.sent_filename, 'r')])
      # The size of the corpus
      self.N = len(self.document_filenames)
      print('sents filename: %s' % self.sent_filename)
      print('total # of sents: %d' % self.N)
    except Exception as err:
      print('Error vsm.__init__(%s)', self.sent_filename)
      print(err)
      sys.exit(-1)

    # dictionary: a set to contain all terms (i.e., words) in the document corpus.
    self.dictionary = set()

    # postings: a defaultdict whose keys are terms, and whose
    # corresponding values are the so-called "postings list" for that
    # term, i.e., the list of documents the term appears in.
    #
    # The way we implement the postings list is actually not as a Python
    # list.  Rather, it's as a dict whose keys are the document ids of
    # documents that the term appears in, with corresponding values equal
    # to the frequency with which the term occurs in the document.
    #
    # As a result, postings[term] is the postings list for term, and
    # postings[term][id] is the frequency with which term appears in
    # document id.
    self.postings = defaultdict(dict)

    # document_frequency: a defaultdict whose keys are terms, with
    # corresponding values equal to the number of documents which contain
    # the key, i.e., the document frequency.
    self.document_frequency = defaultdict(int)

    # length: a defaultdict whose keys are document ids, with values equal
    # to the Euclidean length of the corresponding document vector.
    self.length = defaultdict(float)

    # The list of characters (mostly, punctuation) we want to strip out of
    # terms in the document.
    self.characters = " .,!#$%^&*();:\n\t\\\"?!{}[]<>"

    self.initialize_terms_and_postings()
    self.initialize_document_frequencies()
    self.initialize_lengths()

    print('Init VSM for %s done' % self.sent_filename)


  def initialize_terms_and_postings(self):
    """Reads in each document in document_filenames, splits it into a
    list of terms (i.e., tokenizes it), adds new terms to the global
    dictionary, and adds the document to the posting list for each
    term, with value equal to the frequency of the term in the
    document."""
    for id,sent in self.document_filenames.iteritems():
      terms = self.tokenize(sent)
      unique_terms = set(terms)
      self.dictionary = self.dictionary.union(unique_terms)
      for term in unique_terms:
        # the value is the frequency of the term in the document
        self.postings[term][id] = terms.count(term)


  def tokenize(self, document):
    """Returns a list whose elements are the separate terms in
    document.  Something of a hack, but for the simple documents we're
    using, it's okay.  Note that we case-fold when we tokenize, i.e.,
    we lowercase everything."""
    terms = document.lower().split()
    return [term.strip(self.characters) for term in terms]


  def initialize_document_frequencies(self):
    """For each term in the dictionary, count the number of documents
    it appears in, and store the value in document_frequncy[term]."""
    for term in self.dictionary:
      self.document_frequency[term] = len(self.postings[term])


  def initialize_lengths(self):
    """Computes the length for each document."""
    for id in self.document_filenames:
      l = 0
      for term in self.dictionary:
        l += self.imp(term,id)**2
      self.length[id] = math.sqrt(l)


  def imp(self, term,id):
    """Returns the importance of term in document id.  If the term
    isn't in the document, then return 0."""
    if id in self.postings[term]:
      return self.postings[term][id]*self.inverse_document_frequency(term)
    else:
      return 0.0


  def inverse_document_frequency(self, term):
    """Returns the inverse document frequency of term.  Note that if
    term isn't in the dictionary then it returns 0, by convention."""
    if term in self.dictionary:
      return math.log(self.N/self.document_frequency[term],2)
    else:
      return 0.0


  def do_search(self, query_string=None):
    """Asks the user what they would like to search for, and returns a
    list of relevant documents, in decreasing order of cosine
    similarity."""
    if query_string == None:
      query = self.tokenize(raw_input("Search query >> "))
    else:
      query = self.tokenize(query_string.strip())
    if query == []:
      sys.exit()
    # find document ids containing all query terms.  Works by
    # intersecting the posting lists for all query terms.
    relevant_document_ids = self.intersection(
        [set(self.postings[term].keys()) for term in query])
    if not relevant_document_ids:
      print "No documents matched all query terms."
      return None
    else:
      scores = sorted([(id,self.similarity(query,id))
        for id in relevant_document_ids],
        key=lambda x: x[1],
        reverse=True)
      result_dic = {'result': True}
      retrieved_item = {}
      item_count = 0
      print "Score: sentense, id"
      for (id,score) in scores:
        print str(score)+": "+self.document_filenames[id]+", "+id
        retrieved_item[item_count] = {}
        retrieved_item[item_count]['url'] = id
        retrieved_item[item_count]['sentense'] = self.document_filenames[id]
        retrieved_item[item_count]['score'] = score
        item_count+=1
      result_dic['retrieved_item'] = retrieved_item

    return result_dic


  def intersection(self, sets):
    """Returns the intersection of all sets in the list sets. Requires
    that the list sets contains at least one element, otherwise it
    raises an error."""
    return reduce(set.intersection, [s for s in sets])


  def similarity(self, query, id):
    """Returns the cosine similarity between query and document id.
    Note that we don't bother dividing by the length of the query
    vector, since this doesn't make any difference to the ordering of
    search results."""
    similarity = 0.0
    for term in query:
      if term in self.dictionary:
        similarity += self.inverse_document_frequency(term)*self.imp(term,id)
    similarity = similarity / self.length[id]
    return similarity

"""
import sys
vsm_root = "./"
sys.path.insert(0, vsm_root)
from vsm import vsm

vsm = vsm()

vsm.initialize_terms_and_postings()
vsm.initialize_document_frequencies()
vsm.initialize_lengths()
while True:
  vsm.do_search()
"""

