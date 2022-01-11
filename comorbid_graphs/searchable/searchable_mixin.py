from anytree import Node, PostOrderIter

DIRECTION = ["inc_", "exc_"]
FILTERS = ["name", "content", "type", "text_longer", "ancestor", "parent"]
LBL_WARNING = """Warning:
This feature is assuming that you have a DATABASE which is doing the heavylifting.
If you do not have that, please use the normal version.
"""


class SearchableMixin(object):
    def select(self, node_name):
        node = self.find_node(node_name)
        if not node:
            return
        return type(self).from_tree(node, title=node_name)

    def get_query(self, query_str:str) -> dict:
        return self._build_query(query_str)

    def _build_query(self, query_str: str) -> dict:
        # init, fix
        query_str = query_str.replace("  ", " ").replace("\n", " ").rstrip().lstrip()
        if not query_str.startswith("inc_") and not query_str.startswith("exc_"):
            query_str = "inc_content:" + query_str

        if "inc_ancestor:" not in query_str:
            query_str += " inc_ancestor:" + str(self.tree.name)

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
                i.rstrip().lstrip().lower()
                for i in line[c_ind + 1 :].rstrip().lstrip().split(",")
                if i != ""
            ]

        # fix query
        for key, val in query_dict.items():
            if "inc" not in val:
                query_dict[key]["inc"] = []
            if "exc" not in val:
                query_dict[key]["exc"] = []
        return query_dict

    def search(
        self,
        query_str: str,
        title: str = None,
        select_from: str = None,
        filter_type: str = None,
        silent: bool = True,
        adv_form: bool = False,
    ):
        if 'inc_' in query_str or 'exc_' in query_str:
            raise Exception('Exception: For advanced queries use advanced_search.')
        if filter_type and isinstance(filter_type, str):
            query_str += ' inc_type:' + filter_type
        if select_from and isinstance(select_from, str):
            query_str += ' inc_ancestor:' + select_from
        if adv_form:
            print(query_str)
        return self.advanced_search(query_str, title=title, silent=silent)

    def advanced_search(
        self,
        query_str: str,
        node_type: Node = None,
        title: str = None,
        lbl: bool = False,
        silent: bool = True,
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
        title:           name for the search top
        groupby_type:        group results by type
                             keep in mind document:section differentiation

        late_body_loading:   takes care of late-loading of body for
                             performance improvement.
        silent_lbl_warning:  silent the warning of DATABASE required.
        """
        query_dict = self._build_query(query_str)
        if node_type == None:
            node_type = type(self.tree)
        nodes = []
        # content filtering
        if lbl:
            if not silent:
                print(LBL_WARNING)
            # content_filtered_nodes
            nodes.append(self.apply_lbl_filters(query_dict, late_body_loading=True))

        # nodes based on other filters
        for node in PostOrderIter(self.tree):
            node.advanced_scoring(
                query_dict, late_body_loading=lbl, strict=True
            )
        nodes.append(set([i for i in PostOrderIter(self.tree) if i.score]))

        # ancestor filtering
        if "ancestor" in query_dict:
            nodes.append(
                self.filter_subgraph(
                    inc_list=query_dict["ancestor"]["inc"],
                    exc_list=query_dict["ancestor"]["exc"],
                )
            )
        
        # merging
        # get count of nodes found
        # quickhack for skipping overlapping nodes
        def get_tuple_node(node):
            return (node.name, node.parent.name if node.parent else None)

        def get_tuple_list(nodes):
            return [
                set([get_tuple_node(i) for i in j])
                for j in nodes
            ]
        
        incl_tuple = set.intersection(*get_tuple_list(nodes))
        incl_nodes = [i for i in nodes[-1] if get_tuple_node(i) in incl_tuple]

        if not silent:
            print("Total Selected: ", len(nodes[-1]))
            print("Total Filtered: ", len(nodes[0]))
            print("--------------")
            print("Total Found: ", len(incl_nodes))
            print()

        # post processing
        ancestor_node = self.merge_nodes_into_tree(
            node_list=incl_nodes,
            node_type=node_type,
            with_children=with_children,
        )
        if not title:
            title = ancestor_node.name
        return type(self).from_tree(ancestor_node, title=title)
