import re
import nltk


def fix_sentences(sentences):
    fixed_sents = []
    for sentence in sentences:
        # print(sentence)
        s = re.sub(
            r"\n+", " ", sentence.strip()
        )  # Remove any extraneous newlines remaining after tokenizing (should be 0)
        s = re.sub(r"\s+", " ", s)  # convert all whitespace to spaces
        s = re.sub(r"[^\x00-\x7f]", " ", s)  # remove all non-ascii chars
        s = re.sub(r"\s*\.+", ".", s)  # deal with repeated periods
        s = re.sub(r"\s\d\s", " ", s)  # deal with lone numbers
        s = re.sub(r"<.*>", " ", s)  # remove html tags
        s = re.sub(
            r"(?<=[:;])\s+(?=[A-Za-z0-9][.):]*[0-9]*\s)", "\n", s
        )  # deal with malformatted lists
        s = re.sub(
            r"[;.]\s[A-Za-z0-9]{1,2}[).:][0-9]*\s", "\n", s
        )  # more malformatted lists
        s_split = s.split("\n")  # break into subsegments based on MY newlines
        for sent in s_split:
            s = re.sub(
                r"(\s+[A-Za-z0-9]{1,2}[).:][0-9]*\s*)$", " ", sent
            )  # remove list identifiers from end
            s = re.sub(
                r"^\s*[A-Za-z0-9]{1,3}[).:][0-9]*\s*", " ", s
            )  # remove list identifiers from front
            s = re.sub(r"[IVXivx]{1,3}[).:]", " ", s)  # remove roman numerals
            s = re.sub(r"^\s*\d", " ", s)  # deal with leading numbers
            s = re.sub(r"^\W+", " ", s)  # remove all leading non-word chars
            s = re.sub(r"\s(?=[,.:;()\]])", "", s)  # remove space before punctuation
            s = re.sub(r"\s+", " ", s)  # fix spaces
            if len(s) > 0:
                words = s.split(" ")
                if [re.match(r"^[A-Z]", w) for w in words].count(None) / len(
                    words
                ) < 0.5:
                    continue  # Deal with links at the bottom
                elif [re.match(r"\W", w) for w in words].count(None) / len(words) < 0.5:
                    continue  # Deal with bunches of punctuation
                elif list(s).count(" ") == 0:
                    continue  # Deal with broken strings
                elif re.search(r"\?xml", s) or re.search(r"__", s):
                    continue
                else:
                    fixed_sents.append(s.strip())
    return fixed_sents


def negative_filter(urls):
    urls_filtered = [
        url
        for url in urls
        if not re.search(
            r"phone|account|connect|catalog|book|housing|plan|report|student|manual|conference|residence|bulletin|syllabus|schedule|faq|copyright|guest|registration|gift|\.doc",
            url.lower(),
        )
    ]
    return urls_filtered


def positive_filter(urls, pdf=False):
    r = None
    if pdf:
        r = re.compile(r"(acceptable|wireless|network|aup).*\.pdf$")
    else:
        r = re.compile(r"(acceptable|wireless|network|aup).*(?!\.pdf$)")
    urls_filtered = [url for url in urls if re.search(r, url.lower())]
    return urls_filtered
