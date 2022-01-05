import re
import nltk
import requests
from bs4 import BeautifulSoup

# nltk.download("stopwords")
nltk.download("wordnet")
from nltk.corpus import wordnet  # noqa


def extract_infobox(term):
    url = "https://en.wikipedia.org/wiki/" + term
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    tbl = soup.find("table", {"class": "infobox"})
    if not tbl:
        return {}
    list_of_table_rows = tbl.findAll("tr")
    info = {}
    for tr in list_of_table_rows:
        th = tr.find("th")
        td = tr.find("td")
        if th is not None and td is not None:
            innerText = ""
            for elem in td.recursiveChildGenerator():
                if isinstance(elem, str):
                    # remove references
                    clean = re.sub("([\[]).*?([\]])", "\g<1>\g<2>", elem.strip())
                    # add a simple space after removing references for word-separation
                    innerText += clean.replace("[]", "") + " "
                elif elem.name == "br":
                    innerText += "\n"
            info[th.text] = innerText
    return info


def synonyms(term):
    """
    returns the list of synonyms of the input
    word from thesaurus.com (https://www.thesaurus.com/)
    and wordnet (https://www.nltk.org/howto/wordnet.html)
    """
    synonyms = []
    response = requests.get("https://www.thesaurus.com/browse/{}".format(term))
    soup = BeautifulSoup(response.content, "html.parser")
    try:
        container = soup.find("div", {"id": "meanings"})
        row = container.find("ul")
        row = row.find_all("li")
        for x in row:
            synonyms.append(x.get_text())
    except Exception as e:
        print(e)
    for syn in wordnet.synsets(term):
        synonyms += syn.lemma_names()
    return set(synonyms)
