Multiple Python 3 scripts are provided. Run in the following order as shown:

- convert.py: Converts directory of PDFs to TXT files.
  [`python convert.py [path-to-pdf-directory] -o [path-to-output-directory]`
- merge.py: Merges directory of TXT files to a single TXT file.
  [`python merge.py [path-to-txt-directory] -o [path-to-output-file]``
- train.py: Generates Pickle model and list of discovered topics as CSV.
  [`python train.py [path-to-input-file] -o [path-to-output-csv-file] -m
  [ [path-to-output-pickle-file] -t [topics-count] -w [words-per-topic] -n
  [ [iterations-count]`

Ignore the additionally provided scripts for now.

If multiple Python versions are installed, the Python 3 version is likely
aliased, and the following commands should instead be prefixed with `python3`.
(This is especially likely on Linux/macOS.)

If a script displays a message indicating that a library is missing, run
`pip/pip3 install [the-missing-library-name]` to install it, then run the
script again. You will likely need to do this multiple times.

Example usage session on macOS:

```
python3 convert.py /Users/jared/svn/AUPs/Training -o ./AUPs
python3 merge.py ./AUPs -o aups.txt
python3 train.py aups.txt -o topics.csv -m topics.pkl -t 20 -w 20 -n 10000
```

The results of the above session are still saved here for reference.
