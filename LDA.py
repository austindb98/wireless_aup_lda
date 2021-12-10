import pickle
import re
import numpy as np
import spacy
import lda
import os
import argparse
from sklearn.feature_extraction.text import CountVectorizer
import time
from datetime import datetime
import nltk


nlp = spacy.load("en_core_web_md")


def lemmatize(line):
    doc = nlp(line.strip())
    lemmas = []
    for tok in doc:
        token = tok.lemma_.lower()
        if re.fullmatch(r"[\w_]+|endif", token):
            lemmas.append(token)
    return " ".join(lemmas)


parser = argparse.ArgumentParser()
parser.add_argument("-m", "--model", default=None)
parser.add_argument("-i", "--iterations", default=2000)
parser.add_argument("-w", "--words", default=15)
parser.add_argument("-t", "--topics", default=20)
parser.add_argument(
    "-d",
    "--document",
    default=None,
    help="Specify a document to vectorize after the model has been trained",
)

args = parser.parse_args()

v = None
model = None

if not args.model:
    print(
        "n_topics:",
        args.topics,
        "n_iter:",
        args.iterations,
        "words per topic:",
        args.words,
    )

    text = []
    filepath = "AUPs.txt"
    with open(filepath, "r") as f:
        text = f.read()
    print("read file")

    sents = [lemmatize(line) for line in text.split("\n")]
    print("lemmatized")

    v = CountVectorizer(stop_words=nltk.corpus.stopwords.words("english"))
    matrix = v.fit_transform(sents)
    print(matrix.shape)
    print("vectorized")

    model = lda.LDA(n_topics=args.topics, n_iter=args.iterations)
    lda_matrix = model.fit_transform(matrix)
    print("fit model")

    terms = v.get_feature_names_out()
    items = sorted(v.vocabulary_.items(), key=lambda x: x[1])
    vocab = [item[0] for item in items]

    output = "ID,Words\n"
    words_per_topic = args.words
    for i, topic_distribution in enumerate(model.components_):
        topic = np.array(vocab)[np.argsort(topic_distribution)]
        words = topic[: -(words_per_topic + 1) : -1]
        print("Topic {}: {}".format(i + 1, " ".join(words)))
        output += str(i + 1) + "," + ",".join(words) + "\n"
        output += (
            ","
            + ",".join(
                [
                    str(x)
                    for x in np.sort(topic_distribution)[: -(words_per_topic + 1) : -1]
                ]
            )
            + "\n"
        )

    if not os.path.exists("output/"):
        os.mkdir("output")

    dt = datetime.fromtimestamp(time.time())
    dt_str = datetime.strftime(dt, "%Y-%m-%d_%H:%M:%S")

    with open("output/" + "LDA_Topics_" + dt_str + ".csv", "w") as outfile:
        outfile.write(output)

    with open("output/" + "LDA_Vectorizer_Model_" + dt_str + ".pkl", "wb") as outfile:
        pickle.dump((v, model), outfile)

else:
    if not args.document:
        print("No doc specified")
        exit(-1)
    with open(args.model, "rb") as f:
        t = pickle.load(f)
        v = t[0]
        model = t[1]
        if type(model) != lda.LDA or type(v) != CountVectorizer:
            print("Specified file is not the proper format")
            exit(-1)


if args.document:
    with open(args.document, "r") as f:
        vectorized_doc = v.transform([lemmatize(f.read())])
        print("doc vector shape:", vectorized_doc.shape)
        lda_vector = model.transform(vectorized_doc, max_iter=200, tol=1e-16)
        print("lda vector shape:", lda_vector.shape)
        print(lda_vector)

        if not os.path.exists("output/"):
            os.mkdir("output")

        dt = datetime.fromtimestamp(time.time())
        dt_str = datetime.strftime(dt, "%Y-%m-%d_%H:%M:%S")

        filename = args.document.split("/")[-1]
        filename = filename.split(".")[0]

        with open("output/Vector_" + filename + "_" + dt_str + ".txt", "w") as outfile:
            outfile.write(str(lda_vector))
