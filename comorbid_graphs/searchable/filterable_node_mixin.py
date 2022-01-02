class FilterableNodeMixin(object):
    """Filterable graph nodes
      - filter by name
      - filter by parent name
      - filter by type
      - filter by body length
      - filter by content containing keywords

    # define functions as follows
    def _filter_x(self, inc_list, exc_list, strict=False):
        if condition for failing:
            return False
        return True  # it passed the condition for failing
    """

    def apply_filters(
        self, query_dict: dict, strict: bool = False, late_body_loading: bool = False
    ) -> bool:
        """Main iterative filter, iterates through the necessary filters for running."""

        # define filter functions
        # for keeping the code clean, and consistent
        # TODO: find a more elegant way for this
        filters_dict = {
            "name": self._filter_name,
            "parent": self._filter_parent,
            "type": self._filter_type,
            "text_length": self._filter_text_length,
        }
        for filter_ in ["name", "parent", "type", "text_length"]:
            if filter_ in query_dict and not filters_dict[filter_](
                query_dict[filter_]["inc"], query_dict[filter_]["exc"], strict=strict
            ):
                return False

        # exceptional case of body filtering
        if not late_body_loading:
            if "content" in query_dict and not self._filter_content(
                query_dict["content"]["inc"], query_dict["content"]["exc"]
            ):
                return False
        return True

    def _filter_name(
        self, inc_list: list, exc_list: list, strict: bool = False
    ) -> bool:
        """Checks if the name is in the included list, and not in the excluded."""
        if strict:
            if self.name in inc_list and self.name not in exc_list:
                return True
            return False
        if any(i in self.name for i in inc_list) and not any(
            i in self.name for i in exc_list
        ):
            return True
        return False

    def _filter_parent(
        self, inc_list: list, exc_list: list, strict: bool = False
    ) -> bool:
        if not self.parent or not self.parent.name:
            return False
        if strict:
            if self.name in inc_list and self.name not in exc_list:
                return True
            return False
        if any(i in self.parent.name for i in inc_list) and not any(
            i in self.parent.name for i in exc_list
        ):
            return True
        return False

    def _filter_type(
        self, inc_list: list, exc_list: list, strict: bool = False
    ) -> bool:
        if not hasattr(self, "type"):
            return False
        if self.type in inc_list and self.type not in exc_list:
            return True
        return False

    def _filter_text_length(
        self, inc_list: list, exc_list: list, strict: bool = False
    ) -> bool:
        if not hasattr(self, "body"):
            return False
        if inc_list != [] and len(self.body) <= int(inc_list[0]):
            return False
        if exc_list != [] and len(self.body) > int(exc_list[0]):
            return False
        return True

    def _filter_content(
        self, inc_list: list, exc_list: list, strict: bool = False
    ) -> bool:
        """Filters content that has the phrases put in the included list."""

        if not hasattr(self, "body"):
            return False
        if any(i in self.body for i in inc_list) and not any(
            i in self.body for i in exc_list
        ):
            return True
        return False
