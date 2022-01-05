# Read Data

```python
# use utils to turn your folders into data for Comorbid-Graphs
from comorbid_graphs.utils import read_folder
data = read_folder('my-local-folder')

# download directly from source
from comorbid_graphs.utils import read_wiki_category
data = read_wiki_category(url='https://en.wikipedia.org/wiki/Category:Neuropsychology')

# search in pages/apis
from comorbid_graphs.utils.search import search_courtlistener, search_pubmed
data = search_courtlistener('search-term')
# or
data = search_pubmed('search-term')
```

### Expected JSON
The json structure should be as following.

```json
 {
    "name": "a",
    "children":[
        {
            "name": "b",
            "body": "CGs do not solve the question 't0 b | ~t0 b'."
        },
        {
            "name": "c",
            "body": "Comorbid Graphs are cool.",
            "children":[
                {
                    "name": "d",
                    "body": "My name starts with D",
                }
            ]
        }
    ]
}
```
### Expected Yaml
```yaml
- name: grandparent
  body: Not a ruminator.
  children:
  - name: parent's sibling
    body: Genetically related, might be good to check history.
    children:
    - name: cousin
  - name: parent
    body: Major factor in mental health disorders and love. Ruminator.
    children:
    - name: I
      body: a person with free time, ruminating on existence.
    - name: sibling
      body: similar genetic inheritance
```