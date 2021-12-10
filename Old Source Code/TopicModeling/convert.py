import argparse
import os
import pathlib
import PyPDF2
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="directory of pdfs")
    parser.add_argument("-o", help="output directory")
    args = vars(parser.parse_args())

    if not os.path.exists(args["o"]):
        os.mkdir(args["o"])

    for path in pathlib.Path(args["path"]).glob("**/*.pdf"):
        try:
            print("Converting", path)
            reader = PyPDF2.PdfFileReader(open(str(path), "rb"))
            text = ""
            for page in reader.pages:
                text += page.extractText() + "\n"
            outpath = pathlib.Path(args["o"]) / path.with_suffix(".txt").name
            with outpath.open("w") as outfile:
                outfile.write(text)
        except Exception as exception:
            print("Error:", exception)
