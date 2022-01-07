import numpy as np
import pandas as pd

from .utils import get_shared_annotations


class LabelHandlerMixin(object):

    @classmethod
    def compare_section_annotations(cls, node_list, include_stats=False):
        # create a row for each node:
        # node-Name, section-Set annotations, section2-Set2 annotations ...
        data = []
        for node in node_list:
            if node.type == "section":
                continue
            data.append(
                {
                    "node": node.name,
                    **{
                        child.name: set([ann["name"] for ann in child.annotation_list])
                        for child in node.children
                    },
                }
            )

        df = pd.DataFrame(data).replace({np.nan: set()}).set_index("node")

        # extend df with stats
        if include_stats:
            df = get_shared_annotations(df)
        return df
