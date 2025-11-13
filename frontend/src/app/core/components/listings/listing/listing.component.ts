import { Component, inject, OnInit, signal } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ListingService } from './listing.service';
import { Listing } from '../listing.model';
import { EditableFieldComponent } from '../../../../shared/components/editable-field/editable-field.component';
import { KeyValuePipe } from '@angular/common';

@Component({
  templateUrl: './listing.component.html',
  imports: [EditableFieldComponent, KeyValuePipe],
  selector: 'app-listing',
})
export class ListingComponent implements OnInit {
  private readonly activatedRoute = inject(ActivatedRoute);
  private listingService = inject(ListingService);
  protected listingId = signal('');
  protected listingData = signal<Listing | null>(null);

  ngOnInit() {
    this.activatedRoute.params.subscribe((params) => this.listingId.set(params['id']));
    this.listingService
      .getListing(this.listingId())
      .subscribe((data) => this.listingData.set(data));
  }
  updateField(event: any) {
    console.log('dsada');

    this.listingService.updateListing(this.listingId(), event).subscribe();
  }
}
