class Solution:
    def customSortString(self, order: str, s: str) -> str:
        order_weights = {k: v for v, k in enumerate(order)}
        return ''.join(sorted(s, key=lambda x: order_weights.get(x, len(order_weights))))