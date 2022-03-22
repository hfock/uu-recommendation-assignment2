from enum import Enum
from nltk.stem.porter import PorterStemmer

import spacy
from tqdm.auto import tqdm


def spacy_text(texts):
    # the pipeline’s config.cfg tells spaCy to use the language "en" and the pipeline ["tok2vec", "tagger", "parser",
    # "ner", "attribute_ruler", "lemmatizer"]. spaCy will then initialize spacy.lang.en.English, and create each
    # pipeline component and add it to the processing pipeline. It’ll then load in the model data from the data
    # directory and return the modified Language class for you to use as the nlp object.
    # https://spacy.io/usage/processing-pipelines
    nlp = spacy.load("en_core_web_sm")

    # extract all values from the text column
    text_list = []
    if isinstance(texts, str):
        text_list.append(texts)
    else:
        text_list = texts.tolist()

    # When you call nlp on a text, spaCy first tokenizes the text to produce a Doc object. We disable {parser =
    # Assign dependency labels, ner = Detect and label named entities} out of reasons I frankly don't know but follow
    # as it is stated in the manual.
    disable = ["ner", "parser"]

    # Here the input (text) is transformed into spacy.tokens.doc.Doc.
    # In addition with tqdm the progress of the transformation is shown.
    return [text for text in tqdm(nlp.pipe(text_list, n_process=1, disable=disable), total=len(text_list))]


def pre_process(spacied_values, pos=False, base_form='lemma', rm_stopwords=True, min_length_word=2, token=False):
    """
    Pre processes spacied values.

    This function is able to
        - remove punctuation
            - is always removed
        - remove stopwords
            - removed when @param rm_stopwords = True
        - filter for specific token.pos (see SpacyPos for all possibilities)
            - does not filter for specific tokens if param is []
        - lemmatize the spacied values
            - lemmatize the values if lemma = True
        - stems the spacied values
            - stems the values if lemma = False
        - always lower cases all values

    @return a list of all preprocessed tokenized values
    """
    result = []
    for text in spacied_values:
        # removes all unnecessary text like punctuations and stop words
        processed_text = rm_unnecessary_text(text, rm_stopwords)
        # filters for specific words
        if pos:
            processed_text = filter_specific_pos(processed_text, pos)
        # transforms the base form depending on the base_form input
        if base_form == 'lemma':
            processed_text = lemmatization(processed_text)
        elif base_form == 'stem':
            processed_text = stemming(processed_text)
        else:
            processed_text = text_values(processed_text)
        # Lowers all the tokens
        processed_text = remove_words_with_length(min_length_word, processed_text)
        if token:
            result.append(processed_text)
        else:
            result.append(lower(processed_text))

    return result


def lower(values):
    return [token.lower() for token in values]


def rm_unnecessary_text(values, rm_stopwords):
    if rm_stopwords:
        return [token for token in values if not token.is_punct and not token.is_stop]
    else:
        return [token for token in values if not token.is_punct]


def filter_specific_pos(values, pos):
    pos_values = []
    for val in pos:
        if not isinstance(val, SpacyPos):
            raise TypeError('pos must be an instance of SpacyPos')
        pos_values.append(val.value)
    return [token for token in values if token.pos_ in pos_values]


def text_values(values):
    return [token.text for token in values]


def lemmatization(values):
    return [token.lemma_ for token in values]


def stemming(values):
    stemmer = PorterStemmer()
    return [stemmer.stem(token.text) for token in values]


def remove_words_with_length(min_length, values):
    return [token for token in values if len(token) >= min_length]


"""
I made a SpacyEnum so I assure that I do not get an exception when I accidentally misspelled a POS Tag.

URLs to remember:
- https://spacy.io/api/token
- https://universaldependencies.org/u/pos/
- https://web.archive.org/web/20190206204307/https://www.clips.uantwerpen.be/pages/mbsp-tags
"""


class SpacyPos(Enum):
    ADJ = 'ADJ'  # adjective                     e.g. nice, easy
    ADP = 'ADP'  # adposition
    ADV = 'ADV'  # adverb                        e.g. extremely, loudly, hard
    AUX = 'AUX'  # auxiliary                     e.g. may, should
    CCONJ = 'CCONJ'  # coordinating conjunction      e.g. and, or, but
    DET = 'DET'  # determiner                    e.g. the, a, these
    INTJ = 'INTJ'  # interjection                  e.g. oh, oops, gosh
    NOUN = 'NOUN'  # noun                          e.g. tiger, chair, laughter
    NUM = 'NUM'  # numeral
    PART = 'PART'  # particle                      e.g. about, off, up
    PRON = 'PRON'  # pronoun                       e.g. my, your, our
    PROPN = 'PROPN'  # proper noun                   e.g. Germany, God, Alice
    PUNCT = 'PUNCT'  # punctuation                   e.g. .;?*
    SCONJ = 'SCONJ'  # subordinating conjunction     e.g. whether or not
    SYM = 'SYM'  # symbol                        e.g. %
    VERB = 'VERB'  # verb                          e.g. think, eat, talk
    X = 'X'  # other
