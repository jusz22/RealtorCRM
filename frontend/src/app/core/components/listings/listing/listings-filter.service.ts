import { Injectable } from '@angular/core';
import { Listing } from './listing.model';

export interface ListingsFilter {
  title: string;
  priceFrom: number;
  priceTo: number;
  areaFrom: number;
  areaTo: number;
  priceAreaFrom: number;
  priceAreaTo: number;
  location: string;
  street: string;
  propertyType: string;
  transactionType: string;
}

@Injectable({ providedIn: 'root' })
export class ListingsFilterService {
  filter(listings: Listing[], filter: ListingsFilter): Listing[] {
    return listings.filter((listing) => {
      return (
        this.matchIncludes(listing.title, filter.title) &&
        this.matchMin(listing.price, filter.priceFrom) &&
        this.matchMax(listing.price, filter.priceTo) &&
        this.matchMin(listing.area, filter.areaFrom) &&
        this.matchMax(listing.area, filter.areaTo) &&
        this.matchMin(listing.price_per_area, filter.priceAreaFrom) &&
        this.matchMax(listing.price_per_area, filter.priceAreaTo) &&
        this.matchIncludes(listing.location, filter.location) &&
        this.matchIncludes(listing.street, filter.street) &&
        this.matchIncludes(listing.property_type, filter.propertyType) &&
        this.matchIncludes(listing.transaction_type, filter.transactionType)
      );
    });
  }

  sort(listings: Listing[], order: 'asc' | 'desc') {
    if (order === 'asc') {
      return listings.sort((a, b) => a.price - b.price);
    } else {
      return listings.sort((a, b) => b.price - a.price);
    }
  }

  private matchIncludes(text: string, includes: string): boolean {
    return includes ? text.toLowerCase().trim().includes(includes.toLowerCase().trim()) : true;
  }

  private matchMin(value: number, min: number) {
    return min ? value >= min : true;
  }

  private matchMax(value: number, max: number) {
    return max ? value <= max : true;
  }
}
