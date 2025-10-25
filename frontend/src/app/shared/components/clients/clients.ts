import { Component, inject } from '@angular/core';
import { ClientsService } from '../../../core/services/clients.service';
import { AsyncPipe } from '@angular/common';
import { map, pipe } from 'rxjs';
import { Clients } from '../../../core/services/clients.model';

@Component({
  templateUrl: './clients.html',
  styleUrl: './clients.css',
  imports: [],
})
export class ClientsComponent {
  clientService = inject(ClientsService);
  clients: Clients[] = [];
  readonly clients$ = this.clientService.getClients().subscribe({
    next: (res) => console.log(res),
  });
}
