import csv

import spacy
from pandas import read_csv

nlp = spacy.load("en_core_web_lg")
def get_index_of_verb(verb_form: str, dep_set: set,
                      sent: str) -> int:
    doc = nlp(sent)
    for token in doc:
        token_deps = list([
            child for child in token.children
            if
            child.dep_ != "punct"])
        token_form = token.text

        token_deps = set([child.dep_ for child in token_deps])

        if token_form == verb_form  \
                and token_deps == dep_set:
            return token.i
    return -1

data = read_csv("100_random_sents.csv", encoding="ISO-8859-1")
f = open('csv_file.csv', 'w', )

# create the csv writer
writer = csv.writer(f)



# close the file

for index, row in data:
    verb_index = get_index_of_verb(lemma=None, verb_form=row["verb"], dep_set = row["dep set"],
                                   sent=row["sentence"])
    # write a row to the csv file
    writer.writerow(row)

f.close()
