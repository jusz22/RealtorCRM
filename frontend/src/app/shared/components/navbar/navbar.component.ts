import { Component, inject, OnInit, Signal, ViewChild } from '@angular/core';
import { MenuItem, PrimeIcons } from 'primeng/api';
import { Menubar } from 'primeng/menubar';
import { ButtonDirective } from 'primeng/button';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';
import { PopoverModule } from 'primeng/popover';
import { DialogModule } from 'primeng/dialog';
import {
  FormControl,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { TextareaModule } from 'primeng/textarea';
import { Select } from 'primeng/select';
import {
  Listing,
  propertyType,
  transactionType,
} from '../../../core/components/listings/listing/listing.model';
import { InputTextModule } from 'primeng/inputtext';
import { DatePickerModule } from 'primeng/datepicker';
import { FileSelectEvent, FileUpload, FileUploadHandlerEvent } from 'primeng/fileupload';
import { ListingService } from '../../../core/components/listings/listing/listing.service';

@Component({
  selector: 'app-navbar',
  imports: [
    Menubar,
    ButtonDirective,
    RouterLink,
    PopoverModule,
    DialogModule,
    FormsModule,
    ReactiveFormsModule,
    TextareaModule,
    Select,
    InputTextModule,
    DatePickerModule,
    FileUpload,
  ],
  templateUrl: './navbar.component.html',
  standalone: true,
})
export class NavbarComponent implements OnInit {
  protected items: MenuItem[] | undefined;
  private readonly authService = inject(AuthService);
  private readonly listingService = inject(ListingService);
  private router = inject(Router);
  isSignedIn: Signal<boolean> = this.authService.isAuthenticated;
  protected showingDialog = false;
  protected formGroup!: FormGroup;
  protected propertyOptions = Object.values(propertyType);
  protected transactionOptions = Object.values(transactionType);
  protected lastSubmitResponse: Listing[] | null = null;
  @ViewChild('fu') fileUpload!: FileUpload;

  ngOnInit() {
    this.items = [
      {
        label: 'Home',
        icon: PrimeIcons.HOME,
        routerLink: '/',
      },
      {
        label: 'Klienci',
        icon: PrimeIcons.USERS,
        routerLink: '/clients',
      },
      {
        label: 'Oferty',
        icon: PrimeIcons.WAREHOUSE,
        routerLink: '/listings',
      },
    ];

    this.formGroup = new FormGroup({
      title: new FormControl('', Validators.required),
      street: new FormControl('', Validators.required),
      location: new FormControl('', Validators.required),
      num_of_floors: new FormControl('', Validators.required),
      description: new FormControl('', Validators.required),
      price: new FormControl('', Validators.required),
      area: new FormControl('', Validators.required),
      floor: new FormControl('', Validators.required),
      property_type: new FormControl('', Validators.required),
      transaction_type: new FormControl('', Validators.required),
      build_year: new FormControl(null, Validators.required),
    });
  }

  onSignOut() {
    this.authService.deleteToken();
    this.router.navigate(['/login']);
  }

  onAddListing() {
    this.showingDialog = true;
  }

  onSubmit() {
    if (this.formGroup.invalid) {
      return;
    }

    this.listingService.addListing(this.formGroup.value).subscribe({
      next: (res) => {
        this.showingDialog = false;
        this.formGroup.reset();
        this.lastSubmitResponse = res;
        this.fileUpload.uploader();
      },
      error(err) {
        console.log(err);
      },
    });
  }

  onUpload(event: FileUploadHandlerEvent) {
    if (!this.lastSubmitResponse) {
      return;
    }

    this.listingService.uploadPhotos(this.lastSubmitResponse[0].id, event.files).subscribe({
      next: (res) => console.log(res),
      error: () => console.log('Error uplading photos'),
    });
  }

  onCancel() {
    this.showingDialog = false;
  }
}
