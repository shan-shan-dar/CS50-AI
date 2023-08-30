from os import link
import random

corpus = {
    "1.html": {"2.html", "3.html"},
    "2.html": {"3.html"},
    "3.html": {"2.html"},
}
page = "1.html"
damping_factor = 0.85
n = 100


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    probabilityDistribution = {}

    for p in corpus:
        # With probability '1 - damping_factor', choose a link at random chosen from all pages in the corpus.
        probabilityDistribution[p] = (1 - damping_factor) * 1 / len(corpus)

    linkedPages = corpus[page]

    if len(linkedPages) == 0:
        linkedPages = set()
        for p1 in corpus:
            linkedPages.add(p1)

    for p2 in linkedPages:
        # With probability 'damping_factor', choose a link at random linked to by 'page'
        probabilityDistribution[p2] += damping_factor * (1 / len(linkedPages))

    return probabilityDistribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    proportionDistribution = {}

    for p in corpus:
        proportionDistribution[p] = 0

    sample = random.choice(list(proportionDistribution.keys()))
    proportionDistribution[sample] += 1

    for i in range(n - 1):
        probabilityDistribution = transition_model(corpus, sample, damping_factor)

        sequence = list(probabilityDistribution.keys())
        weights = list(probabilityDistribution.values())

        sample = random.choices(sequence, weights)[0]
        proportionDistribution[sample] += 1

    for p1 in proportionDistribution:
        proportionDistribution[p1] = proportionDistribution[p1] / n

    return proportionDistribution


print(len(corpus["3.html"]))
