class OrderableMixin(object):
    @staticmethod
    def order_by_score(items):
        return sorted(items, key=lambda item: 
            item.score + sum(i.score for i in item.children) if item.score else 0
        )