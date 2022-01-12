import os, re, secrets, pickle
from collections import defaultdict

def get_source():
    with open("source.txt", "r", encoding="utf-8") as source:
        text = source.read()

    return text

def add_to_words_base(source):
    source = re.sub("\n|,", '', source)
    sentences = source.split('.')

    sentences.pop(-1)

    chains = defaultdict(list)

    for sentence in sentences:
        words = sentence.split(" ")
        words.append(".")
        chains["START"].append(words[0])
        for i in range(0, len(words) - 1):
            chains[words[i]].append(words[i+1])

    chains['.'].append(-1)
    chains["START"] = list(filter(None, chains["START"]))


    with open("base", "ab") as base:
        pickle.dump(chains, base)

def generate_chain():
    chains = defaultdict(list)

    with open("base", "rb") as base:
        chains = pickle.load(base)

    sentence = ""
    word = "START"
    variants = ""

    word = secrets.choice(chains[word])
    while word != -1:
        sentence = sentence + word + " "
        word = secrets.choice(chains[word])

    sentence = sentence.replace(" .", ".")

    return sentence

if __name__ == "__main__":
    source = get_source()

    add_to_words_base(source)

    sentence = generate_chain()

    print(sentence)
