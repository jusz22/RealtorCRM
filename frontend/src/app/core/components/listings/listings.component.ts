import { Component, inject, OnInit, signal } from '@angular/core';
import { ListingsService } from './listings.service';
import { ListingElement } from './listing-element/listing-element.component';
import { Listing, propertyType, transactionType } from './listing/listing.model';
import { FormControl, FormGroup, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { InputText } from 'primeng/inputtext';
import { ButtonDirective, ButtonIcon, ButtonLabel } from 'primeng/button';
import { ListingsFilterService } from './listing/listings-filter.service';
import { Select } from 'primeng/select';

@Component({
  templateUrl: './listings.component.html',
  styleUrl: './listings.component.css',
  imports: [
    ListingElement,
    InputText,
    FormsModule,
    ReactiveFormsModule,
    ButtonDirective,
    Select,
    ButtonIcon,
    ButtonLabel,
  ],
})
export class ListingsComponent implements OnInit {
  private readonly listingsService = inject(ListingsService);
  private readonly listings$ = this.listingsService.getListings();
  private readonly filterService = inject(ListingsFilterService);
  protected readonly data = signal<Listing[]>([]);
  protected readonly filteredData = signal<Listing[]>([]);
  protected displayFilterModule = false;
  protected sortOrder: 'asc' | 'desc' | null = null;
  protected filterFg!: FormGroup;
  protected propertyOptions = Object.values(propertyType);
  protected transactionOptions = Object.values(transactionType);

  ngOnInit(): void {
    this.listings$.subscribe({
      next: (listings) => {
        this.data.set(listings);
        this.filteredData.set(listings);
      },
    });

    this.filterFg = new FormGroup({
      title: new FormControl<string | null>(null),
      priceFrom: new FormControl<number | null>(null),
      priceTo: new FormControl<number | null>(null),
      areaFrom: new FormControl<number | null>(null),
      areaTo: new FormControl<number | null>(null),
      priceAreaFrom: new FormControl<number | null>(null),
      priceAreaTo: new FormControl<number | null>(null),
      location: new FormControl<string | null>(null),
      street: new FormControl<string | null>(null),
      propertyType: new FormControl<string | null>(null),
      transactionType: new FormControl<string | null>(null),
    });
  }

  onFilterModuleDisplay() {
    this.displayFilterModule = !this.displayFilterModule;
  }

  onSubmit() {
    this.filteredData.set(this.filterService.filter(this.data(), this.filterFg.value));
  }

  onReset() {
    this.filterFg.reset();
    this.filteredData.set(this.data());
  }

  onSort(order: 'asc' | 'desc') {
    this.sortOrder = order;
    this.filteredData.set(this.filterService.sort(this.filteredData(), order));
  }
}
