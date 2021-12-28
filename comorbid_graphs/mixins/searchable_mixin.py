def get_node_list(f, list_words, name="name"):
    return list(
        findall(
            f, filter_=lambda node: any(x in getattr(node, name) for x in list_words)
        )
    )


def get_results(f, inc_list, exc_list, src_name="result"):
    """MUST BE RUN ONCE"""

    result_node = ComorbidGraphNode(name="result")

    exclude = get_node_list(f, exc_list)
    include = get_node_list(f, inc_list)

    def add_node(node):
        # if parent not found, add directly
        if not node.parent or not node.parent:
            node.old_parent = None
            node.parent = result_node
        # if parent not found in list, add directly, but fix children issues
        elif node.parent.name not in [i.name for i in include]:
            node.old_parent = node.parent
            # fix parenting issues
            node.parent = result_node
            node.parent.children = list(
                [i for i in node.parent.children if i.name != node.name]
            ) + [node]
        else:
            # TODO: dont know why this works yet ..
            include.append(node)

    def remove_node(node):
        node.parent.children = list(
            [i for i in node.parent.children if i.name != node.name]
        )

    for node in PreOrderIter(f):
        # which nodes crossover
        inc_ancestors = set(include) & set(list(node.ancestors) + [node])
        if inc_ancestors:
            inc_max_level = max([len(i.ancestors) for i in inc_ancestors])
        else:
            inc_max_level = -1

        # find nodes that are excluding this node
        exc_ancestors = set(exclude) & set(list(node.ancestors) + [node])
        if exc_ancestors:
            exc_max_level = max([len(i.ancestors) for i in exc_ancestors])
        else:
            exc_max_level = -1

        if inc_max_level > exc_max_level:
            add_node(node)
        else:
            remove_node(node)
    return result_node
