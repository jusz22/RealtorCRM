import { Component, inject, input, OnInit, signal } from '@angular/core';
import { CurrencyPipe, DatePipe, DecimalPipe } from '@angular/common';
import { Card } from 'primeng/card';
import { Listing } from '../listing/listing.model';
import { ActivatedRoute, Router } from '@angular/router';
import { ListingService } from '../listing/listing.service';
import { User } from '../listing/listing.component';
import { SafeUrl } from '@angular/platform-browser';

@Component({
  selector: 'app-listing-elem',
  templateUrl: './listing-element.component.html',
  imports: [Card, DatePipe, CurrencyPipe, DecimalPipe],
})
export class ListingElement implements OnInit {
  private readonly router = inject(Router);
  private readonly route = inject(ActivatedRoute);
  private readonly listingService = inject(ListingService);
  protected user = signal<User | null>(null);
  readonly listing = input.required<Listing>();
  imageUrl: SafeUrl | null = null;

  ngOnInit() {
    const userId = this.listing().user_id;

    if (userId) {
      this.listingService.getUser(userId).subscribe({
        next: (user) => {
          this.user.set(user);
        },
      });
    }
    const listingId = this.listing().id;
    if (listingId) {
      this.listingService.getImageMetadata(listingId).subscribe({
        next: (metadata) => {
          if (metadata['0']) {
            this.listingService.getImageUrls(metadata['0'].id).subscribe({
              next: (imageUrl) => (this.imageUrl = imageUrl),
            });
          }
        },
      });
    }
  }

  handleSelectRedirect() {
    this.router.navigate([this.listing().id], { relativeTo: this.route });
  }
}
