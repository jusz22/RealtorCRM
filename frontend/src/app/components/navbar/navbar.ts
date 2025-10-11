import { Component, OnInit } from '@angular/core';
import { MenuItem, PrimeIcons } from 'primeng/api';
import { Menubar } from 'primeng/menubar';

@Component({
  selector: 'app-navbar',
  imports: [Menubar],
  templateUrl: './navbar.html',
  styleUrl: './navbar.css',
})
export class Navbar implements OnInit {
  items: MenuItem[] | undefined;

  ngOnInit() {
    this.items = [
      {
        label: 'Home',
        icon: PrimeIcons.HOME,
      },
      {
        label: 'Klienci',
        icon: PrimeIcons.USERS,
      },
      {
        label: 'Oferty',
        icon: PrimeIcons.WAREHOUSE,
      },
    ];
  }
}
