import { Routes } from '@angular/router';
import { Login } from './shared/components/login/login';
import { NavbarComponent } from './shared/components/navbar/navbar.component';
import { authGuard } from './core/guards/auth-guard';
import { ClientsComponent } from './shared/components/clients/clients';
import { App } from './app';

export const routes: Routes = [
  {
    path: '',
    component: App,
    canActivate: [authGuard],
  },
  {
    path: 'clients',
    component: ClientsComponent,
    canActivate: [authGuard],
  },
  {
    path: 'login',
    component: Login,
  },
];
