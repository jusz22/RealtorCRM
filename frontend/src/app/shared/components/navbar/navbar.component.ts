import { Component, inject, OnInit } from '@angular/core';
import { MenuItem, PrimeIcons } from 'primeng/api';
import { Menubar } from 'primeng/menubar';

@Component({
  selector: 'app-navbar',
  imports: [Menubar],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css',
  standalone: true,
})
export class NavbarComponent implements OnInit {
  items: MenuItem[] | undefined;

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
  }
}
