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
S -> NP VP
NP -> N | JJ N | Det N | Det JJ N | NP P NP | NP Conj NP | NP Adv
JJ -> Adj | Adj JJ
VP ->  V OP | Adv V OP | V Adv OP | V
OP -> OP Conj S | OP Conj VP | OP Conj NP | Conj S | Conj NP | Conj VP | P OP | NP
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
    result = []
    # nltk.download('punkt')
    preresult = nltk.tokenize.word_tokenize(sentence)
    for i in range(len(preresult)):
        preresult[i] = preresult[i].lower()
        alpha = False
        for j in range(len(preresult[i])):
            if preresult[i][j] <= 'z' and preresult[i][j] >= 'a':
                alpha = True
                break
        if(alpha):
            result.append(preresult[i])

    return result


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    result = []
    for sub in tree.subtrees(filter=lambda t: t.label() == "NP" and t != tree):
        other = False
        for _ in sub.subtrees(filter=lambda t: t.label() == "NP" and t != sub):
            other = True
        if other:
            continue
            # print(f"found an NP inside {sub}")
            # result += np_chunk2(sub)
        else:
            # print(f"appending in loop 1 {sub}")
            result.append(sub)
    return result


# def np_chunk2(tree):
#     result = []
#     parent = tree
#     for sub in parent.subtrees(filter=lambda t: t != parent):
#         other = False
#         print(f"inside {sub} ")
#         for _ in sub.subtrees(filter=lambda t: t.label() == "NP" and t != sub):
#             other = True
#         if other:
#             print(f"go inside {sub}")
#             result += np_chunk2(sub)
#         elif sub.height() <= 2:
#             print(f"appending in loop 2 {sub}")
#             result.append(sub)

#     return result


if __name__ == "__main__":
    main()
