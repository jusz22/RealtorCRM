import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Client } from './clients.model';

@Injectable({ providedIn: 'root' })
export class ClientService {
  http = inject(HttpClient);
  getClients() {
    return this.http.get<Client[]>('http://localhost:8000/api/v1/clients');
  }
}
