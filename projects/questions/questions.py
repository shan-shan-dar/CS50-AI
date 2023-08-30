import math
import os
import nltk
import sys
import string

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    
    mapping = {}

    for page in os.listdir(directory):

        filepath = os.path.join(directory, page)

        # i had problems with the encoding, so decided to standardize it to UTF-8 when opening the file
        content = open(filepath, 'r', encoding="utf8")
        mapping[page] = content.read()

    return mapping


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    
    list = nltk.word_tokenize(document)

    tokens = []

    punctuations = set(string.punctuation)
    stopwords = set(nltk.corpus.stopwords.words("english"))

    for word in list:
        word = word.lower()
        if word in punctuations:
            continue
        elif word in stopwords:
            continue
        else:
            tokens.append(word)

    return tokens


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    
    count = {}

    for page in documents.keys():
        for word in documents[page]:

            # if word is new, create a key in count as well as idfs
            if word not in count.keys():
                count[word] = 0

            # increment the count of the word
            count[word] += 1

    idfs = {}

    for word in count:

        # calculate idf using formula
        idf = math.log(len(documents.keys())/count[word])

        idfs[word] = idf
    
    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """

    scores = {}
    bestPages = []

    for page in files.keys():
        score = 0
        for word in query:
            if word in files[page]:
                # compute tf
                tfidf = files[page].count(word) * idfs[word]
                score += tfidf
        scores[page] = score

    rankedPages = {key: value for key, value in sorted(scores.items(), key=lambda item: item[1])}
    
    for page in rankedPages.keys():
        bestPages.append(page)

    return bestPages[0 : n]



def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """

    scores = {}
    bestSentences = []

    for sentence in sentences.keys():
        score = 0
        for word in query:
            if word in sentences[sentence]:
                score += idfs[word]

        qtd = 0
        queryWords = 0
        for word in sentences[sentence]:
            if word in query:
                queryWords += 1
        qtd = queryWords/len(sentences[sentence])

        scores[sentence] = (score, qtd)

    rankedPages = {key: value for key, value in sorted(scores.items(), key=lambda item: item[1])}

    for page in rankedPages.keys():
        bestSentences.append(page)
    
    bestSentences.reverse()

    return bestSentences[0 : n]


if __name__ == "__main__":
    main()
