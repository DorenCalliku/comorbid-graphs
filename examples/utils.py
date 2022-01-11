import re
import json
import nltk
import requests
from bs4 import BeautifulSoup
from comorbid_graphs import ComorbidGraph, ComorbidGraphNode


def generate_test_data(data_file, analysis_files=[]):
    with open(data_file) as f:
        data = json.load(f)
    cg = ComorbidGraph(
        data, node_type=ComorbidGraphNode, assign_ids=True, root_name="dsm-v"
    )
    # analyse
    analysis_cgs = []
    for file in analysis_files:
        with open(file) as f:
            data = json.load(f)
        name = file[file.rfind("/") + 1 :].replace(".json", "")
        analysis_cgs.append(
            ComorbidGraph(
                data, node_type=ComorbidGraphNode, assign_ids=True, root_name=name
            )
        )
    print(f"Analysing with {len(analysis_cgs)} analysis graphs.")
    cg.process_graph(analysis_cgs)
    with open(data_file.replace(".json", "_labelled.json"), "w+") as f:
        json.dump(cg.export(), f)
    return cg


def open_existing_data(data_file):
    with open(data_file.replace(".json", "_labelled.json")) as f:
        data = json.load(f)
    return ComorbidGraph(
        data, node_type=ComorbidGraphNode, assign_ids=True, root_name="dsm-v"
    )


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
