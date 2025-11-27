import { Component, inject, model, OnInit, signal } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ListingService } from './listing.service';
import { Listing } from './listing.model';
import { EditableFieldComponent } from '../../../../shared/components/editable-field/editable-field.component';
import { GalleriaModule } from 'primeng/galleria';

@Component({
  templateUrl: './listing.component.html',
  imports: [EditableFieldComponent, GalleriaModule],
  selector: 'app-listing',
})
export class ListingComponent implements OnInit {
  private readonly activatedRoute = inject(ActivatedRoute);
  private readonly listingService = inject(ListingService);
  protected readonly listingId = signal('');
  protected readonly listingData = signal<Listing | null>(null);
  protected readonly displayListingData = signal<
    Array<{ label: string; value: any; type: string; key: string }>
  >([]);
  protected image = [
    {
      source:
        'https://images.pexels.com/photos/2014422/pexels-photo-2014422.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940',
      thumbnail:
        'https://images.pexels.com/photos/2014422/pexels-photo-2014422.jpeg?auto=compress&cs=tinysrgb&dpr=1&fit=crop&h=200&w=280',
      alt: 'aa',
    },
  ];

  ngOnInit() {
    this.activatedRoute.params.subscribe((params) => {
      this.listingId.set(params['id']);
      this.listingService.getListing(this.listingId()).subscribe((data) => {
        this.listingData.set(data);
        if (this.listingData()) {
          this.displayListingData.set(this.prepareData(this.listingData()!));
        }
      });
    });
    this.listingService.getImageMetadata().subscribe((metadata) => {});
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
