from anytree import findall


class LBLNodeMixin(object):
    """Example of Late Loading: Late Body Loading (LBL)

    Title: Filtering the body for keywords.
    Description: Shouldnt be like the python-anytree-filter case,
    because loading the body of many of instances will be not performant -
    so will have to allow a filtering done
    by an en engine (like `sqlite`-engine) which are optimized for these."""

    def apply_lbl_content_filter(
        self, query_dict: dict, strict: bool = False, late_body_loading: bool = False
    ) -> bool:
        """In case the lbl-loading-filter hasnt been updated, this will be run.
        Preparing in case there is an error."""

        if "content" in query_dict and not self._filter_content(
            query_dict["content"]["inc"], query_dict["content"]["exc"]
        ):
            return False
        return True


class LBLGraphMixin(object):
    """For Future Performance Issues"""

    def apply_lbl_filters(
        self, query_dict: dict, late_body_loading: bool = True
    ) -> dict:
        """OVERWRITE THIS FOR DB PERFORMANCE.
        Late Body Loading filter content.

        Get ids of contents that have the query
        - overwritable function to fit with database-prepared query
        """
        return set(
            findall(
                self.tree,
                filter_=lambda node: node.apply_lbl_content_filter(
                    query_dict, late_body_loading=late_body_loading
                ),
            )
        )
