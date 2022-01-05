import re
from anytree import PostOrderIter


def flatten(lol: list) -> list:
    return [i for j in lol for i in j]


class ProcessableNodeMixin(object):
    def extract_labels(self, graphs=[]):
        if not hasattr(self, 'body'):
            return
        labels = flatten([self.extract_from_graph_tree(graph.tree) for graph in graphs])
        self.annotation_list = self.remove_overlapping_labels(labels+self.annotation_list)

    def extract_from_graph_tree(self, gtree):
        if not self.body:
            return []
        list_labels = []
        for node in PostOrderIter(gtree):
            if node == gtree:
                continue
            list_labels += [
                {
                    "name": node.name,
                    "parent": node.parent.name,
                    "ancestor": node.ancestors[0].name if len(node.ancestors) else None,
                    "start": int(i.span()[0]),
                    "end": int(i.span()[1]),
                }
                for i in re.finditer(
                    re.sub("[^ a-zA-Z\n]+", "", node.name.lower()),
                    self.body.lower(),
                    flags=re.MULTILINE | re.IGNORECASE,
                )
            ]
        return list_labels

    @staticmethod
    def remove_overlapping_labels(labels):
        """Overlapping labels are labels that are in multiple trees, and
        share the same or similar span."""
        if not len(labels):
            return []
        cleaned_labels = []
        sorted_labels = sorted(labels, key=lambda k: (k["start"]))
        base_item = sorted_labels[0]
        for item in sorted_labels[1:]:
            # if there is no crossing
            if item["start"] >= base_item["end"]:
                cleaned_labels.append(base_item)
                base_item = item
                continue
            # if there is crossing, get the largest one
            if len(item["name"]) > len(base_item["name"]):
                base_item = item
        cleaned_labels.append(base_item)
        return cleaned_labels

class ProcessableGraphMixin(object):
    def process_graph(self, cg_list):
        print(f"\nExtracting labels from {str(len(self.tree.descendants))} nodes.")
        count = 0
        for i in PostOrderIter(self.tree):
            if count % 100 == 0:
                print(f"Exctracted: {str(count)}")
            count += 1
            i.extract_labels(cg_list)