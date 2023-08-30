import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | NP VP NP | NP VP P NP | S Conj S | NP VP P NP Adv | VP NP 

NP -> N | Det NP | NP P NP | Adj NP
VP -> V | Adv VP | VP Adv
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    
    list = nltk.word_tokenize(sentence)

    words = []

    for word in list:
        word = word.lower()
        containsAlphabet = False
        for char in word:
            if char.isalpha():
                containsAlphabet = True
                break

        if containsAlphabet:
            words.append(word)

    return words


def containsNP(tree):
    """
    Recursive function to check if tree has any node NP inside it
    """

    # base case 1: the tree itself is a NP
    if tree.label() == 'NP':
        return True

    # base case 2: the tree has depth one (only terminal nodes remain), in which case we have reached the end of the tree
    if len(tree) == 1:
        return False

    # recursion
    for branch in tree:
        if containsNP(branch):
            return True

    return False


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """

    np_chunks = []

    for branch in tree:

        if not containsNP(branch):
            continue

        # if branch is non terminal, continue checking within its subBranches
        if branch.label() == "NP" or branch.label() == "VP" or branch.label() == "S":
            subsubtree = np_chunk(branch)
            for np in subsubtree:
                np_chunks.append(np)

    # if the tree itseld qualifies as a np_chunk
    if tree.label() == "NP" and not containsNP(branch):
        np_chunks.append(tree)

    return np_chunks



if __name__ == "__main__":
    main()
