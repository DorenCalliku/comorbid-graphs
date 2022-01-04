from anytree import Node, PostOrderIter


class SimpleSearchMixin(object):
    def simple_search(
        self,
        query_str: str,
        node_type: Node,
        base_name="search_results",
        filter_type="default",
        with_children=False,
    ):
        def clean_query_i(i):
            return i.rstrip().lstrip().replace('\n','')
        query_list = [clean_query_i(i) for i in query_str.split(',') if clean_query_i(i) != '']
        # get involved nodes
        for node in PostOrderIter(self.tree):
            node.simple_scoring(query_list, filter_type=filter_type)

        incl_list = set([i.name for i in PostOrderIter(self.tree) if i.score])
        all_nodes = [i.name for i in PostOrderIter(self.tree)]

        # post processing
        ancestor_node = self.filter_subgraph(
            inc_list=incl_list,
            exc_list=list(set(all_nodes) - incl_list),
            base_name=base_name,
            strict=True,
            with_children=with_children,
        )
        return type(self).from_tree(ancestor_node, parent_name=base_name)
