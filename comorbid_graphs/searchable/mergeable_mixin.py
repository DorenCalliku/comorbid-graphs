from anytree import Node

class MergeableMixin(object):
    """Allow cutting and merging ancestors.
    - merge all of the nodes, merging with include-exclude
    TODO: Needs proper testing."""

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
        with_children: bool = False,
    ) -> Node:
        """Merges list of nodes into one main source,
        and re-order if none of ancestors in list.

        Parameters:
        node_list:     list of nodes to include
        node_type:     types of nodes, for creation of new node
        with_children: keep the children of the included nodes.
        """

        # create main node for keeping results
        result_node = node_type(name='Merged results')

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

                if not with_children:
                    node.children = [i for i in node.children if i in node_list]
            #else:
            #    self.remove_node(node)
        return result_node
