import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Listing, ListingInput } from './listing/listing.model';

@Injectable({ providedIn: 'root' })
export class ListingsService {
  private readonly http = inject(HttpClient);

  getListings() {
    return this.http.get<Listing[]>('http://localhost:8000/api/v1/listings');
  }

  addListing(listing: ListingInput) {
    return this.http.post<Listing>('http://localhost:8000/api/v1/listings', listing);
  }
}
