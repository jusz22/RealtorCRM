import { Component, inject, OnInit, signal } from '@angular/core';
import { ActivatedRoute, RouterOutlet } from '@angular/router';
import { ListingService } from './listing.service';
import { Listing } from './listing.model';
import { Menubar } from 'primeng/menubar';
import { MenuItem, MessageService } from 'primeng/api';
import { TextareaModule } from 'primeng/textarea';
import { ButtonDirective } from 'primeng/button';
import { PopoverModule } from 'primeng/popover';
import { AuthService } from '../../../services/auth.service';
import { NotesService } from './notes/notes.service';
import { NotesStateService } from '../../../services/notes-state.service';
import { DialogModule } from 'primeng/dialog';
import { ToastModule } from 'primeng/toast';
import {
  FormControl,
  FormGroup,
  FormsModule,
  Validators,
  ReactiveFormsModule,
} from '@angular/forms';

@Component({
  selector: 'app-listing-layout',
  templateUrl: './listing-layout.component.html',
  imports: [
    Menubar,
    RouterOutlet,
    ButtonDirective,
    PopoverModule,
    DialogModule,
    FormsModule,
    ReactiveFormsModule,
    TextareaModule,
    ToastModule,
  ],
  providers: [MessageService],
})
export class ListingLayoutComponent implements OnInit {
  private readonly activatedRoute = inject(ActivatedRoute);
  private readonly listingService = inject(ListingService);
  private readonly notesService = inject(NotesService);
  private readonly currentUser$ = inject(AuthService).getCurrentUser();
  private readonly notesStateService = inject(NotesStateService);
  private readonly messageService = inject(MessageService);
  protected readonly listingId = signal('');
  protected readonly listingData = signal<Listing | null>(null);
  protected showingDialog: boolean = false;
  protected fg!: FormGroup;

  protected readonly menubarItems: MenuItem[] = [
    {
      label: 'Details',
      icon: 'pi pi-info-circle',
      routerLink: ['.'],
      routerLinkActiveOptions: { exact: true },
    },
    {
      label: 'Notes',
      icon: 'pi pi-clipboard',
      routerLink: ['notes'],
      routerLinkActiveOptions: { exact: true },
    },
    {
      label: 'Client details',
    },
  ];

  ngOnInit() {
    this.activatedRoute.params.subscribe((params) => {
      this.listingId.set(params['id']);
      this.listingService.getListing(this.listingId()).subscribe((data) => {
        this.listingData.set(data);
      });
    });
  }

  onSubmit() {
    this.currentUser$.subscribe({
      next: (user) => {
        this.activatedRoute.params.subscribe({
          next: (params) => {
            this.notesService.addNote(params['id'], user.id, this.fg.value['note']).subscribe({
              next: (value) => {
                this.notesStateService.addNote(value);
                this.messageService.add({
                  severity: 'success',
                  summary: 'Success',
                  detail: 'Note added',
                  life: 2000,
                });
              },
            });
          },
        });
      },
    });
    this.showingDialog = false;
  }

  onCancel() {
    this.showingDialog = false;
  }

  onAddNote() {
    this.fg = new FormGroup({ note: new FormControl('', Validators.required) });
    this.showingDialog = true;
  }
}
