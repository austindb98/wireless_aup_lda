import argparse
import lda
import numpy
import operator
import pickle
import re
import sys

from sklearn.feature_extraction.text import CountVectorizer

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="training file path")
    parser.add_argument("-o", help="output csv file path")
    parser.add_argument("-m", help="output pickle model file path")
    parser.add_argument("-t", type=int, help="topics count", default=10)
    parser.add_argument("-w", type=int, help="words per topic", default=25)
    parser.add_argument("-n", type=int, help="iterations count", default=2000)
    args = vars(parser.parse_args())

    with open(args["path"]) as file:
        tf = CountVectorizer(stop_words="english")
        matrix = tf.fit_transform(file)
        items = sorted(tf.vocabulary_.items(), key=operator.itemgetter(1))
        vocab = [item[0] for item in items]
        model = lda.LDA(n_topics=args["t"], n_iter=args["n"], random_state=1)
        model.fit_transform(matrix)

        items = sorted(tf.vocabulary_.items(), key=operator.itemgetter(1))
        vocab = [item[0] for item in items]

        output = "ID,Words\n"
        for i, topic_distribution in enumerate(model.topic_word_):
            topic = numpy.array(vocab)[numpy.argsort(topic_distribution)]
            words = topic[: -(args["w"] + 1) : -1]
            print("Topic {}: {}".format(i + 1, " ".join(words)))
            output += str(i + 1) + "," + ",".join(words) + "\n"

        with open(args["o"], "w") as outfile:
            outfile.write(output)

        with open(args["m"], "wb") as outfile:
            pickle.dump(model, outfile)
