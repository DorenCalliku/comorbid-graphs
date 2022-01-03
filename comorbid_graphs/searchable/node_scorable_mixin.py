class ScorableNodeMixin(object):
    """Scorable graph nodes
      - score name
      - score parent name
      - score type
      - score body length
      - score content containing keywords

    # define functions as follows
    def _score_x(self, inc_list, exc_list, strict=False):
        if condition for failing:
            return False
        return True  # it passed the condition for failing
    """

    def simple_scoring(self, query_list, filter_type: str = "default"):
        """Random scoring for finding the term in name, parent.name or content.

        Explanation:
        filter_type:  filter nodes of specific type (ex. document)
        """

        if not hasattr(self, "type") or not self.type and self.type != filter_type:
            return 0
        score = 0
        if hasattr(self, "body") and self.body:
            score += sum([self.body.lower().count(i) for i in query_list]) / len(
                self.body.split(" ")
            )
        if self.name:
            score += sum([self.name.lower().count(i) for i in query_list]) / len(
                self.name.split(" ")
            )
        # if hasattr(node.parent, 'name') and search_for in node.parent.name.lower():
        #    score += node.parent.name.lower().count(search_for)/len(node.parent.name.split(' '))
        self.score = score

    def advanced_scoring(
        self, query_dict: dict, strict: bool = False, late_body_loading: bool = False
    ) -> bool:
        """Main iterative scoring, iterates through the necessary filters for running."""

        # define scoring functions for keeping the code clean, and consistent
        # TODO: find a more elegant way for this
        scoring_dict = {
            "name": self._score_name,
            "parent": self._score_parent,
            "type": self._score_type,
            "text_length": self._score_text_length,
            "content": self._score_content,
        }
        score = 0
        for scorer_ in ["name", "parent", "type", "text_length"]:
            if scorer_ in query_dict:
                single_score = scoring_dict[scorer_](
                    query_dict[scorer_]["inc"],
                    query_dict[scorer_]["exc"],
                )
                if not single_score and strict:
                    return 0
                else:
                    score += single_score

        # exceptional case of body filtering
        if not late_body_loading:
            for scorer_ in ["content"]:
                if scorer_ in query_dict:
                    single_score = scoring_dict[scorer_](
                        query_dict[scorer_]["inc"],
                        query_dict[scorer_]["exc"],
                    )
                    if not single_score and strict:
                        return 0
                    else:
                        score += single_score
        self.score = score

    def _score_name(
        self, inc_list: list, exc_list: list, strict_match: bool = False
    ) -> bool:
        if strict_match:
            if self.name in inc_list and self.name not in exc_list:
                return True
            return False
        if not any(i in self.name for i in exc_list):
            return sum([self.name.lower().count(i) for i in inc_list]) / len(
                self.name.split(" ")
            )
        return False

    def _score_parent(
        self, inc_list: list, exc_list: list, strict_match: bool = False
    ) -> bool:

        if not self.parent or not self.parent.name:
            return False
        if strict_match:
            if self.name in inc_list and self.name not in exc_list:
                return True
            return False
        if not any(i in self.parent.name for i in exc_list):
            return sum([self.parent.name.lower().count(i) for i in inc_list]) / len(
                self.parent.name.split(" ")
            )
        return False

    def _score_type(
        self, inc_list: list, exc_list: list, strict_match: bool = False
    ) -> bool:
        if not hasattr(self, "type"):
            return False
        if self.type in inc_list and self.type not in exc_list:
            return True
        return False

    def _score_text_length(self, inc_list: list, exc_list: list) -> bool:
        if not hasattr(self, "body"):
            return False
        if inc_list != [] and len(self.body) <= int(inc_list[0]):
            return False
        if exc_list != [] and len(self.body) > int(exc_list[0]):
            return False
        return True

    def _score_content(self, inc_list: list, exc_list: list) -> bool:
        """Filters content that has the phrases put in the included list."""
        if not hasattr(self, "body"):
            return False
        if not any(i in self.body for i in exc_list):
            return sum([self.body.lower().count(i)*len(i) for i in inc_list])/len(self.body)
        return False

    @staticmethod
    def order_by_score(items):
        return sorted(items, key=lambda item: item.score + sum(i.score for i in item.children))