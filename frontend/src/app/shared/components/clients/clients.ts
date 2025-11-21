import { Component, inject } from '@angular/core';
import { ClientService } from '../../../core/services/clients.service';
import { AsyncPipe } from '@angular/common';
import { Column, TableComponent } from '../table/table.component';

@Component({
  selector: 'app-clients',
  templateUrl: './clients.html',
  styleUrl: './clients.css',
  imports: [AsyncPipe, TableComponent],
})
export class ClientsComponent {
  clientService = inject(ClientService);
  readonly clients$ = this.clientService.getClients();
  readonly columns: Column[] = [
    {
      field: 'full_name',
      header: 'Full name',
      allowSort: true,
    },
    {
      field: 'email',
      header: 'Email',
      allowSort: true,
    },
    {
      field: 'phone_number',
      header: 'Phone number',
      allowSort: false,
    },
  ];
}
