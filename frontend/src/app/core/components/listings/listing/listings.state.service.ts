import { inject, Injectable, OnInit } from '@angular/core';
import { ListingsService } from '../listings.service';
import { Listing } from './listing.model';
import { BehaviorSubject } from 'rxjs';

@Injectable()
export class ListingsStateService {
  private listingsService = inject(ListingsService);
  private _state$ = new BehaviorSubject<Listing[]>([]);
  state$ = this._state$.asObservable();

  refresh() {
    this._state$.next([...this._state$.value]);
  }

  load() {
    this.listingsService.getListings().subscribe((data) => this._state$.next(data));
  }

  patchState(listing: Listing) {
    this._state$.next([...this._state$.value, listing]);
  }

  setState(listings: Listing[]) {
    this._state$.next(listings);
  }
}
