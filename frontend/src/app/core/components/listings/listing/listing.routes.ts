import { Routes } from '@angular/router';

export const listingRoutes: Routes = [
  {
    path: 'notes',
    loadComponent: () => import('./notes/notes.component').then((m) => m.NotesComponent),
  },
];
