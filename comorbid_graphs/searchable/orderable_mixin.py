class OrderableMixin(object):
    @staticmethod
    def order_by_score(items):
        return sorted(items, key=lambda item: item.accumulative_score(), reverse=True)
