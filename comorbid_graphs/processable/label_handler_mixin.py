from itertools import groupby


class LabelHandlerMixin(object):
    @staticmethod
    def group_lol_stats(stats):
        grouped_vals = {}
        for each in stats:
            each[1] = each[1].replace(" ", "_")
            if each[1] in grouped_vals:
                grouped_vals[each[1]].append(each)
            if each[1] not in grouped_vals:
                grouped_vals[each[1]] = [each]
        return grouped_vals

    @staticmethod
    def generate_label_stats(labels, sort_count=True):
        stats = []
        labels = sorted(labels, key=lambda k: (k["name"], k["ancestor"]))
        for key, group in groupby(labels, lambda k: (k["name"], k["ancestor"])):
            stats.append([key[0], key[1], sum(1 for _ in group)])
        if sort_count:
            stats = sorted(stats, key=lambda k: k[-1], reverse=True)
        return stats

    @classmethod
    def generate_common_stats(cls, all_labels):
        """Sorry for the quality of this code.
        Its being written while in class.
        TODO: fix this"""

        sets = []
        for label_list in all_labels:
            sets.append(set([i["name"] for i in label_list]))
        if sets == []:
            return {}
        common_labels = set.intersection(*sets)
        # generate label stats for each document
        grouped_labels = []
        for labels in all_labels:
            grouped_labels.append(
                [
                    i
                    for i in cls.generate_label_stats(labels, sort_count=False)
                    if i[0] in common_labels
                ]
            )
        stats = []
        for i_ in range(len(grouped_labels[0])):
            # get min of labels
            cnt = min([j_[i_][-1] for j_ in grouped_labels])
            grouped_labels[0][i_][-1] = cnt
            stats.append(grouped_labels[0][i_])
        stats = sorted(stats, key=lambda k: k[-1], reverse=True)
        return stats
