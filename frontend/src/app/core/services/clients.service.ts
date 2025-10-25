import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Clients } from './clients.model';

@Injectable({ providedIn: 'root' })
export class ClientsService {
  http = inject(HttpClient);
  getClients() {
    return this.http.get<Clients[]>('http://localhost:8000/api/v1/clients');
  }
}
