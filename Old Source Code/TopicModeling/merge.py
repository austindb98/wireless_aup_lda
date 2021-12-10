import argparse
import pathlib

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="directory of text files")
    parser.add_argument("-o", help="output file")
    args = vars(parser.parse_args())

    text = ""
    for path in pathlib.Path(args["path"]).glob("**/*.txt"):
        with path.open() as file:
            text += file.read() + "\n"
    with open(args["o"], "w") as outfile:
        outfile.write(text)
