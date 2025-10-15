import { Routes } from '@angular/router';
import { Login } from './shared/components/login/login';
import { NavbarComponent } from './shared/components/navbar/navbar.component';
import { authGuard } from './core/guards/auth-guard';

export const routes: Routes = [
  {
    path: '',
    component: NavbarComponent,
    canActivate: [authGuard],
  },
  {
    path: 'login',
    component: Login,
  },
];
