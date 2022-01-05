from anytree import PostOrderIter, findall


class FilterableNodeMixin(object):
    """Filterable graph nodes
      - filter name
      - filter parent name
      - filter type
      - filter body length
      - filter content containing keywords

    # define functions as follows
    def _filter_x(self, inc_list, exc_list, strict=False):
        if condition for failing:
            return False
        return True  # it passed the condition for failing
    """

    def accumulative_score(self):
        return self.score + sum(i.score for i in self.children) if self.score else 0

    def advanced_scoring(
        self, query_dict: dict, strict: bool = False, late_body_loading: bool = False
    ) -> bool:
        """Main iterative scoring, iterates through the necessary filters for running."""

        # define scoring functions for keeping the code clean, and consistent
        # TODO: find a more elegant way for this
        scoring_dict = {
            "name": self._filter_name,
            "parent": self._filter_parent,
            "type": self._filter_type,
            "text_longer": self._filter_text_longer,
            "content": self._filter_content,
        }
        self.score = 0
        score = 0
        for filterr_ in ["name", "parent", "type", "text_longer"]:
            if filterr_ in query_dict:
                single_score = scoring_dict[filterr_](
                    query_dict[filterr_]["inc"],
                    query_dict[filterr_]["exc"],
                )
                if not single_score and strict:
                    return
                else:
                    score += single_score

        # exceptional case of body filtering
        if not late_body_loading:
            for filterr_ in ["content"]:
                if filterr_ in query_dict:
                    single_score = scoring_dict[filterr_](
                        query_dict[filterr_]["inc"],
                        query_dict[filterr_]["exc"],
                    )
                    if not single_score and strict:
                        return 0
                    else:
                        score += single_score
        self.score = score

    def _filter_name(self, inc_list: list, exc_list: list) -> bool:
        """Cases of inclusion:
        name in inc_list, exc=[] or name not in exc
        """
        if inc_list != []:
            if exc_list != []:
                if any(i in self.name.lower() for i in exc_list):
                    return False
            return sum([len(i)/len(self.name) for i in inc_list if i in self.name.lower()])
        else:
            if exc_list != []:
                if any(i in self.name.lower() for i in exc_list):
                    return False
        return 10**(-4)

    def _filter_parent(self, inc_list: list, exc_list: list) -> bool:
        if not self.parent or not self.parent.name:
            return False
        return self.parent._filter_name(inc_list=inc_list, exc_list=exc_list)

    def _filter_type(self, inc_list: list, exc_list: list) -> bool:
        if not hasattr(self, "type"):
            return False
        if (inc_list == [] or self.type in inc_list) and (
            exc_list == [] or self.type not in exc_list
        ):
            return True
        return False

    def _filter_text_longer(self, inc_list: list, exc_list: list) -> bool:
        if not hasattr(self, "body") or not self.body:
            return False
        if inc_list != [] and len(self.body) <= int(inc_list[0]):
            return False
        if exc_list != [] and len(self.body) > int(exc_list[0]):
            return False
        return True

    def _filter_content(self, inc_list: list, exc_list: list) -> bool:
        """Filters content that has the phrases put in the included list."""
        if not hasattr(self, "body") or not self.body:
            return False
        if not any(i in self.body for i in exc_list):
            return sum([self.body.lower().count(i) * len(i) for i in inc_list]) / len(
                self.body
            )
        return False


class FilterableGraphMixin(object):
    @staticmethod
    def get_node_list(base_node, list_words, strict: bool = False) -> list:
        return list(
            findall(
                base_node,
                filter_=lambda node: any(x in node.name.lower() for x in list_words)
                if not strict
                else any(x == node.name.lower() for x in list_words),
            )
        )

    def filter_subgraph(
        self,
        inc_list,
        exc_list,
        strict: bool = False,
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
        return include_nodes
