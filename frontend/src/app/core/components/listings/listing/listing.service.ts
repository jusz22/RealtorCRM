import { HttpClient, httpResource } from '@angular/common/http';
import { inject, Injectable, SecurityContext } from '@angular/core';
import { Listing, ListingInput } from './listing.model';
import { map, Observable } from 'rxjs';
import { Image } from './image.model';
import { DomSanitizer } from '@angular/platform-browser';

@Injectable({ providedIn: 'root' })
export class ListingService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = 'http://localhost:8000/api/v1/listings/';
  private readonly sanitizer = inject(DomSanitizer);

  getListing(listingId: string): Observable<Listing> {
    return this.http.get<Listing>(this.baseUrl + listingId);
  }

  updateListing(listingId: string, fieldToUpdate: Partial<Listing>) {
    return this.http.patch(this.baseUrl + listingId, fieldToUpdate);
  }

  addListing(listing: ListingInput) {
    const build_year = listing.build_year as unknown as Date;
    listing.build_year = String(build_year.getFullYear());
    const body = JSON.stringify([listing]);
    return this.http.post<Listing[]>(this.baseUrl, body, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  uploadPhotos(listingId: string, photos: File[]) {
    const formData = new FormData();

    photos.forEach((photo) => formData.append('files', photo));

    return this.http.post(
      `http://localhost:8000/api/v1/listings/${listingId}/photos/batch`,
      formData
    );
  }

  getImageMetadata(listingId: string) {
    return this.http.get<Image[]>(this.baseUrl + listingId + '/photos');
  }

  getImageUrls(imageId: string) {
    return this.http
      .get(`http://localhost:8000/api/v1/photos/${imageId}/file`, { responseType: 'blob' })
      .pipe(
        map((blob) => {
          const url = URL.createObjectURL(blob);
          return this.sanitizer.bypassSecurityTrustUrl(url);
        })
      );
  }
}
