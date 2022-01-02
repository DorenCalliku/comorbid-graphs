from anytree import Node, findall, PostOrderIter


class FilterableSubgraphMixin(object):
    """Allow cutting and merging ancestors.
    - get the names of these, include-exclude
    - merge all of the nodes, merging with include-exclude

    TODO: Needs proper testing."""

    @staticmethod
    def get_node_list(base_node, list_words, strict: bool = False) -> list:
        return list(
            findall(
                base_node,
                filter_=lambda node: any(x in node.name for x in list_words)
                if not strict
                else any(x == node.name for x in list_words),
            )
        )

    def filter_subgraph(
        self,
        inc_list,
        exc_list,
        node_type,
        base_name,
        strict: bool = False,
        with_children: bool = True,
    ):
        """Does the ancestor filtering.
        Gets only subparts of a tree, and merges them into a result-node.
        """

        # copying because of reference-issues
        f = self.tree.deep_copy()
        exclude_nodes = self.get_node_list(f, exc_list, strict=strict)
        include_nodes = self.get_node_list(f, inc_list, strict=strict)

        for node in PostOrderIter(f):
            # which nodes crossover
            inc_ancestors = set(include_nodes) & set(list(node.ancestors) + [node])
            if inc_ancestors:
                inc_max_level = max([i.depth for i in inc_ancestors])
            else:
                inc_max_level = -1

            # find nodes that are excluding this node
            exc_ancestors = set(exclude_nodes) & set(list(node.ancestors) + [node])
            if exc_ancestors:
                exc_max_level = max([i.depth for i in exc_ancestors])
            else:
                exc_max_level = -1

            # add if index of inclusion > ind-of-exclusion
            if inc_max_level > exc_max_level:
                include_nodes.append(node)
            else:
                if node.parent:
                    # connect children to previous
                    for i in node.children:
                        i.parent = node.parent
                    node.parent.children += node.children

                    # remove this node
                    node.parent.children = list(
                        [i for i in node.parent.children if i.name != node.name]
                    )
                # deleting its reference just in case
                del node
        return self.merge_nodes_into_tree(
            include_nodes, base_name=base_name, node_type=node_type, with_children=with_children
        )

    @staticmethod
    def remove_node(node):
        if node.parent:
            node.parent.children = list(
                [i for i in node.parent.children if i.name != node.name]
            )

    @staticmethod
    def get_closest_included_ancestor(node: Node, node_list: list) -> Node:
        included_ancestors = set(node_list) & set(node.ancestors)
        if hasattr(node, "old_parent") and node.old_parent:
            included_ancestors = included_ancestors | (
                set(node_list) & set(node.old_parent.ancestors)
            )
        if included_ancestors:
            closest_index = max([i.depth for i in included_ancestors])
            return [i for i in included_ancestors if i.depth == closest_index][0]
        else:
            return None

    def merge_nodes_into_tree(
        self,
        node_list: list,
        node_type: Node,
        base_name: str = "source",
        with_children: bool = True,
    ) -> Node:
        """Merges list of nodes into one main source,
        and re-order if none of ancestors in list.

        Parameters:
        node_list:     list of nodes to include
        node_type:     types of nodes, for creation of new node
        base_name:     for the source node
        with_children: keep the children of the included nodes.
        """

        # create main node for keeping results
        result_node = node_type(name=base_name)

        if not with_children:
            for i, node in enumerate(node_list):
                # deal with children stuff
                included_children = set(node.children) & set(node_list)
                node.children = [i for i in node.children if i in included_children]

                # deal with parents
                closest_ancestor = self.get_closest_included_ancestor(node, node_list)
                if closest_ancestor:
                    node.parent = closest_ancestor
                else:
                    node.parent = result_node
                node.parent.children = list(set(node.parent.children) | set([node]))
            return result_node

        for node in node_list:
            closest_ancestor = self.get_closest_included_ancestor(node, node_list)

            # if parent not found, add directly
            if not node.parent or not node.parent:
                node.old_parent = None
                node.parent = result_node
            elif closest_ancestor and closest_ancestor == node.parent:
                pass

            # if parent not found in list, add directly, but fix children issues
            elif node.parent.name not in [i.name for i in node_list]:
                node.old_parent = node.parent

                # fix parenting issues
                if closest_ancestor:
                    node.parent = closest_ancestor
                else:
                    node.parent = result_node

                # add if not already existing
                node.parent.children = list(
                    [i for i in node.parent.children if i.name != node.name]
                ) + [node]

            else:
                self.remove_node(node)
        return result_node
