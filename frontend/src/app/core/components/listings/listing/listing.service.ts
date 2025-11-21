import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Listing } from './listing.model';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ListingService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = 'http://localhost:8000/api/v1/listings/';

  getListing(listingId: string): Observable<Listing> {
    return this.http.get<Listing>(this.baseUrl + listingId);
  }

  updateListing(listingId: string, fieldToUpdate: Partial<Listing>) {
    return this.http.patch(this.baseUrl + listingId, fieldToUpdate);
  }
}
