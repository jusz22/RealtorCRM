from dataclasses import dataclass

from sqlalchemy import asc, desc


@dataclass
class SortOptions:
    column: str | None = None
    order: str | None = 'asc'

    def get_sort_func(self):
        
        if self.column is None:
            return None
        
        return desc(self.column) if self.order.lower() == 'desc' else asc(self.column)
