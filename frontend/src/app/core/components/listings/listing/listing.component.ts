import { Component, inject, OnInit, signal } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ListingService } from './listing.service';
import { Listing } from './listing.model';
import { EditableFieldComponent } from '../../../../shared/components/editable-field/editable-field.component';

@Component({
  templateUrl: './listing.component.html',
  imports: [EditableFieldComponent],
  selector: 'app-listing',
})
export class ListingComponent implements OnInit {
  private readonly activatedRoute = inject(ActivatedRoute);
  private listingService = inject(ListingService);
  protected listingId = signal('');
  protected listingData = signal<Listing | null>(null);
  protected displayListingData = signal<
    Array<{ label: string; value: any; type: string; key: string }>
  >([]);

  ngOnInit() {
    this.activatedRoute.params.subscribe((params) => {
      this.listingId.set(params['id']);
      this.listingService.getListing(this.listingId()).subscribe((data) => {
        this.listingData.set(data);
        if (this.listingData()) {
          this.displayListingData.set(this.prepareData(this.listingData()!));
        }

        console.log(this.displayListingData());
      });
    });
  }
  prepareData(data: Listing) {
    const preparedData = Object.entries(data)
      .map(([key, value]) => ({
        label: key
          .split('_')
          .map((val) => val.charAt(0).toUpperCase() + val.slice(1))
          .join(' '),
        value: value,
        type: typeof value,
        key: key,
      }))
      .filter((val) => val.key !== 'id' && val.key !== 'client_id');
    return preparedData;
  }
  updateField(event: any) {
    console.log('dsada');

    this.listingService.updateListing(this.listingId(), event).subscribe();
  }
}
