import { CommonModule } from '@angular/common';
import { Component, inject, input } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { TableModule, TableRowSelectEvent } from 'primeng/table';

export interface Column {
  field: string;
  header: string;
  allowSort: boolean;
  type?: 'numeric' | 'text' | 'date';
}

interface HasId {
  id: string;
}

@Component({
  templateUrl: './table.component.html',
  imports: [TableModule, CommonModule],
  selector: 'sha-table',
})
export class TableComponent<T extends HasId> {
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  readonly columns = input<Column[]>();
  readonly data = input<T[]>();
  readonly selectable = input<boolean>(false);

  onSelect(event: TableRowSelectEvent<T>) {
    if (Array.isArray(event.data)) {
      console.log(event.data.map((val) => val.id));
    } else {
      this.router.navigate([event.data?.id], { relativeTo: this.route });
    }
  }
}
