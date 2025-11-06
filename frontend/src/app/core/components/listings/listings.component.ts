import { Component, inject } from '@angular/core';
import { Column, TableComponent } from '../../../shared/components/table/table.component';
import { ListingsService } from './listings.service';
import { AsyncPipe } from '@angular/common';

@Component({
  templateUrl: './listings.component.html',
  imports: [TableComponent, AsyncPipe],
})
export class ListingsComponent {
  listingService = inject(ListingsService);
  readonly data$ = this.listingService.getListings();
  readonly columns: Column[] = [
    {
      header: 'Title',
      field: 'title',
      allowSort: true,
      type: 'text',
    },
    {
      header: 'Location',
      field: 'location',
      allowSort: true,
      type: 'text',
    },
    {
      header: 'Transaction type',
      field: 'transaction_type',
      allowSort: true,
      type: 'text',
    },
    {
      header: 'Build year',
      field: 'build_year',
      allowSort: true,
      type: 'date',
    },
    {
      header: 'Price',
      field: 'price',
      allowSort: true,
      type: 'numeric',
    },
    {
      header: 'Floor',
      field: 'floor',
      allowSort: true,
      type: 'numeric',
    },
    {
      header: 'Area',
      field: 'area',
      allowSort: false,
      type: 'numeric',
    },
    {
      header: 'Price per meter',
      field: 'price_per_area',
      allowSort: true,
      type: 'numeric',
    },
  ];
}
