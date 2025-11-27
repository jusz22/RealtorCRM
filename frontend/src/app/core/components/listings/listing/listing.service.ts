import { HttpClient, httpResource } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Listing } from './listing.model';
import { Observable } from 'rxjs';
import { Image } from './image.model';

@Injectable({ providedIn: 'root' })
export class ListingService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = 'http://localhost:8000/api/v1/listings/';
  private readonly API_KEY = '';
  private readonly photoUrl = 'https://api.pexels.com/v1/photos/';

  getListing(listingId: string): Observable<Listing> {
    return this.http.get<Listing>(this.baseUrl + listingId);
  }

  updateListing(listingId: string, fieldToUpdate: Partial<Listing>) {
    return this.http.patch(this.baseUrl + listingId, fieldToUpdate);
  }

  getImageMetadata() {
    return this.http.get<Image>(this.photoUrl + '186077', {
      headers: {
        'Authorization': this.API_KEY,
      },
    });
  }
}
