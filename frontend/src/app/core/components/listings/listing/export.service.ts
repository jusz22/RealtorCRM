import { HttpClient, HttpParams } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class ExportService {
  private readonly http = inject(HttpClient);

  sendEmail(listingId: string, email: string) {
    const params = new HttpParams().set('email_address', email).set('listing_id', listingId);
    return this.http.post('http://localhost:8000/api/v1/email', '', { params });
  }
}
