import { Routes } from '@angular/router';
import { Login } from './shared/components/login/login';
import { authGuard } from './core/guards/auth-guard';
import { ClientsComponent } from './shared/components/clients/clients';
import { ListingsComponent } from './core/components/listings/listings.component';
import { HomeComponent } from './core/components/home/home.component';
import { ListingComponent } from './core/components/listings/listing/listing.component';

export const routes: Routes = [
  {
    path: 'listings/:id',
    component: ListingComponent,
    canActivate: [authGuard],
  },
  {
    path: 'listings',
    component: ListingsComponent,
    canActivate: [authGuard],
    title: 'Listings',
  },
  {
    path: 'clients',
    component: ClientsComponent,
    canActivate: [authGuard],
    title: 'Clients',
  },
  {
    path: 'login',
    component: Login,
    title: 'Sign in',
  },
  {
    path: '',
    component: HomeComponent,
    canActivate: [authGuard],
    title: 'RealtorCRM',
  },
];
