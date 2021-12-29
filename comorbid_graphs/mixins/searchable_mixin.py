from anytree import PreOrderIter
from anytree.search import findall
from ..comorbid_graph_node import ComorbidGraphNode

class SearchableMixin(object):

    @staticmethod
    def add_node(node, include, source):
        # if parent not found, add directly
        if not node.parent or not node.parent:
            node.old_parent = None
            node.parent = result_node
        # if parent not found in list, add directly, but fix children issues
        elif node.parent.name not in [i.name for i in include]:
            node.old_parent = node.parent
            # fix parenting issues
            node.parent = source
            node.parent.children = list(
                [i for i in node.parent.children if i.name != node.name]
            ) + [node]
        else:
            # TODO: dont know why this works yet ..
            include.append(node)
        return include

    @staticmethod
    def remove_node(node):
        if node.parent:
            node.parent.children = list(
                [i for i in node.parent.children if i.name != node.name]
            )

    @staticmethod
    def get_node_list(base_node, list_words):
        return list(findall(
            base_node,
            filter_=lambda node: any(x in node.name for x in list_words)
        ))

    def subgraph_search(self, inc_list, exc_list, src_name="result", node_type=ComorbidGraphNode):
        """Does the ancestor filtering."""

        f = self.tree.deep_copy()
        result_node = node_type(name="result")

        exclude = self.get_node_list(f, exc_list)
        include = self.get_node_list(f, inc_list)

        for node in PreOrderIter(f):
            # which nodes crossover
            inc_ancestors = set(include) & set(list(node.ancestors) + [node])
            if inc_ancestors:
                inc_max_level = max([i.depth for i in inc_ancestors])
            else:
                inc_max_level = -1

            # find nodes that are excluding this node
            exc_ancestors = set(exclude) & set(list(node.ancestors) + [node])
            if exc_ancestors:
                exc_max_level = max([i.depth for i in exc_ancestors])
            else:
                exc_max_level = -1

            # add if index of inclusion > ind-of-exclusion
            if inc_max_level > exc_max_level:
                include = self.add_node(
                    node,
                    include,
                    result_node
                )
            else:
                self.remove_node(node)
        return result_node
