from dataclasses import dataclass

from sqlalchemy import UnaryExpression, asc, desc


@dataclass(init=False)
class SortOptions:
    column: str | None
    order: str | None

    def __init__(self, column, order):
        if order is None:
            self.order = 'asc'
        else:
            self.order = order
        self.column = column

    def get_sort_func(self) -> UnaryExpression:
        
        if self.column is None:
            return None
        
        return desc(self.column) if self.order.lower() == 'desc' else asc(self.column)
