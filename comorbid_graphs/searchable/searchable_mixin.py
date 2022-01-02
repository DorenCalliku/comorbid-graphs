from anytree import Node, findall, PostOrderIter
import collections

DIRECTION = ["inc_", "exc_", "include_", "exclude_"]
FILTERS = ["name", "content", "type", "text_length", "ancestor", "parent"]
LBL_WARNING = """Warning:
This feature is assuming that you have a DATABASE which is doing the heavylifting.
If you do not have that, please use the normal version.
"""


def flatten(lol: list) -> list:
    return [i for j in lol for i in j]


def flatten_wname(lol: list) -> list:
    return [i.name for j in lol for i in j]


class SearchableMixin(object):
    @staticmethod
    def build_query(query_str: str) -> dict:
        # init, fix
        query_str = query_str.replace("  ", " ").replace("\n", " ").rstrip().lstrip()
        if not query_str.startswith("inc_") and not query_str.startswith("exc_"):
            query_str = "inc_content:" + query_str

        # break into lines
        for i in DIRECTION:
            query_str = query_str.replace(i, "_BREAK_" + i)
        values = [
            i.rstrip().lstrip()
            for i in query_str.split("_BREAK_")
            if i.rstrip().lstrip() != ""
        ]

        # build query
        query_dict = {}
        for line in values:
            u_ind = line.find("_")  # underline index
            c_ind = line.find(":")  # comma index
            key = line[u_ind + 1 : c_ind]
            if key not in FILTERS:
                continue
            if key not in query_dict:
                query_dict[key] = {}
            query_dict[key][line[:u_ind]] = [
                i for i in line[c_ind + 1 :].rstrip().lstrip().split(",") if i != ""
            ]

        # fix query
        for key, val in query_dict.items():
            if "inc" not in val:
                query_dict[key]["inc"] = []
            if "exc" not in val:
                query_dict[key]["exc"] = []
        return query_dict

    def advanced_search(
        self,
        query_str: str,
        node_type: Node,
        base_name: str = "search results",
        late_body_loading: bool = False,
        silent_lbl_warning: bool = False,
        with_children: bool = False,
    ) -> Node:
        """Deals with the independent steps of searching
        - filter-content
        - filter-others
        - filter-ancestors
        - merge

        For performance we can have this feature enabled: late_body_loading
        - which considers a potential missing body if loading from db.
        This is for cases of large-text bodies that can block the memory.
        For this, we do the filtering in the engine of the DATABASE that we are using.
        Write WARNING when using this feature.
        Otherwise, we load KnowledgeGraph with Body.

        Parameters:
        full_tree:           keep the full tree of ancestors
        base_name:           name for the search top
        node_type:           allows different type of results
                             - maybe if extra properties needed.
        groupby_type:        group results by type
                             keep in mind document:section differentiation

        late_body_loading:   takes care of late-loading of body for
                             performance improvement.
        silent_lbl_warning:  silent the warning of DATABASE required.
        """
        query_dict = self.build_query(query_str)

        nodes = []

        # content filtering
        if late_body_loading:
            if not silent_lbl_warning:
                print(LBL_WARNING)
            # content_filtered_nodes
            nodes.append(self.apply_lbl_filters(query_dict, late_body_loading=True))

        # nodes based on other filters
        nodes.append(
            set(
                findall(
                    self.tree,
                    filter_=lambda node: node.apply_filters(
                        query_dict, late_body_loading=late_body_loading
                    ),
                )
            )
        )

        # ancestor filtering
        if "ancestor" in query_dict:
            ancestor_node = self.filter_subgraph(
                inc_list=query_dict["ancestor"]["inc"],
                exc_list=query_dict["ancestor"]["exc"],
                node_type=node_type,
                base_name=base_name,
            )
            nodes.append([i for i in PostOrderIter(ancestor_node)])
        else:
            ancestor_node = node_type(name=base_name)

        # merging
        # get count of nodes found
        all_nodes = [i.name for j in nodes for i in j]

        # filter out nodes that appear less than expected
        baseline = {node.name: node for node in nodes[-1]}

        count_nodes = len(nodes)
        for name_key, count in collections.Counter(all_nodes).items():
            if count < count_nodes and name_key in baseline:
                del baseline[name_key]

        # post processing
        incl_list = set([i.name for i in list(baseline.values())])
        ancestor_node = self.filter_subgraph(
            inc_list=incl_list,
            exc_list=list(set(all_nodes) - incl_list),
            node_type=node_type,
            base_name=base_name,
            strict=True,
            with_children=with_children,
        )
        result_cg = type(self)({}, node_type=node_type)
        result_cg.tree = ancestor_node
        return result_cg
