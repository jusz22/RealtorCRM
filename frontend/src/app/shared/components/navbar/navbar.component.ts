import { Component, inject, OnInit, Signal } from '@angular/core';
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
  propertyType,
  transactionType,
} from '../../../core/components/listings/listing/listing.model';
import { InputTextModule } from 'primeng/inputtext';
import { DatePickerModule } from 'primeng/datepicker';

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
  ],
  templateUrl: './navbar.component.html',
  standalone: true,
})
export class NavbarComponent implements OnInit {
  protected items: MenuItem[] | undefined;
  private authService = inject(AuthService);
  private router = inject(Router);
  isSignedIn: Signal<boolean> = this.authService.isAuthenticated;
  protected showingDialog = false;
  protected formGroup!: FormGroup;
  protected propertyOptions = Object.values(propertyType);
  protected transactionOptions = Object.values(transactionType);

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
      numOfFloors: new FormControl('', Validators.required),
      description: new FormControl('', Validators.required),
      price: new FormControl('', Validators.required),
      area: new FormControl('', Validators.required),
      floor: new FormControl('', Validators.required),
      propertyType: new FormControl('', Validators.required),
      transactionType: new FormControl('', Validators.required),
      buildYear: new FormControl(null),
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
    console.log(this.formGroup.value);
  }
  onCancel() {}
}
