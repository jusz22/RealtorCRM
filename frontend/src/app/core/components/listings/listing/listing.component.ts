import { Component, inject, model, OnInit, signal } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ListingService } from './listing.service';
import { Listing } from './listing.model';
import { EditableFieldComponent } from '../../../../shared/components/editable-field/editable-field.component';
import { GalleriaModule } from 'primeng/galleria';
import { SafeUrl } from '@angular/platform-browser';
import { forkJoin, of, switchMap } from 'rxjs';
import { Tag } from 'primeng/tag';
import { Select, SelectChangeEvent } from 'primeng/select';
import { FormsModule } from '@angular/forms';

export interface User {
  id: number;
  username: string;
  email: string;
}

@Component({
  templateUrl: './listing.component.html',
  imports: [EditableFieldComponent, GalleriaModule, Tag, Select, FormsModule],
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
  protected user!: User | null | undefined;
  protected users!: User[] | null;
  protected images: Array<{ source: SafeUrl; thumbnail: SafeUrl }> = [];
  protected galleriaFullScreen = false;

  ngOnInit() {
    this.activatedRoute.params.subscribe((params) => {
      this.listingId.set(params['id']);
      this.images = [];
      this.listingService
        .getImageMetadata(this.listingId())
        .pipe(
          switchMap((metadata) =>
            metadata.length
              ? forkJoin(metadata.map((item) => this.listingService.getImageUrls(item.id)))
              : of([])
          )
        )
        .subscribe((urls) => {
          this.images = urls.filter(Boolean).map((url) => ({ source: url!, thumbnail: url! }));
        });
      this.listingService.getListing(this.listingId()).subscribe((data) => {
        this.listingData.set(data);
        if (this.listingData()) {
          this.displayListingData.set(this.prepareData(this.listingData()!));
        }
        const userId = this.listingData()?.user_id;
        this.listingService.getUsers().subscribe({
          next: (users) => {
            this.users = users;
            this.user = users.find((user) => user.id === userId);
          },
        });
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
      .filter(
        (val) =>
          val.key !== 'id' &&
          val.key !== 'client_id' &&
          val.key !== 'status' &&
          val.key !== 'user_id' &&
          val.key !== 'description'
      );
    return preparedData;
  }

  updateField(event: any) {
    this.listingService.updateListing(this.listingId(), event).subscribe();
  }

  onFullScreenToggle() {
    this.galleriaFullScreen = true;
  }

  onUpdateUser(event: SelectChangeEvent) {
    this.listingService.updateListing(this.listingId(), { user_id: event.value['id'] }).subscribe();
  }
}
