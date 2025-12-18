import { Component, inject, OnInit, signal, ViewChild } from '@angular/core';
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
import { FileUpload, FileUploadHandlerEvent } from 'primeng/fileupload';
import { Select } from 'primeng/select';
import { Client } from '../../../services/clients.model';
import { ExportService } from './export.service';
import { ClientService } from '../../../services/clients.service';

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
    FileUpload,
    Select,
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
  private readonly exportService = inject(ExportService);
  private readonly clientService = inject(ClientService);
  protected readonly listingId = signal('');
  protected readonly listingData = signal<Listing | null>(null);
  protected showingNoteDialog: boolean = false;
  protected showingPhotoDialog: boolean = false;
  protected showingExportDialog: boolean = false;
  protected selectedClient: Client | null = null;
  protected clientOptions: Client[] | null = null;
  protected noteFg!: FormGroup;
  @ViewChild('photoUpload') photoUpload!: FileUpload;

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
    this.clientService.getClients().subscribe({
      next: (clients) => {
        this.clientOptions = clients;
      },
    });
  }

  onNoteSubmit() {
    this.currentUser$.subscribe({
      next: (user) => {
        this.activatedRoute.params.subscribe({
          next: (params) => {
            this.notesService.addNote(params['id'], user.id, this.noteFg.value['note']).subscribe({
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
    this.showingNoteDialog = false;
  }

  onNoteCancel() {
    this.showingNoteDialog = false;
  }

  onAddNote() {
    this.noteFg = new FormGroup({ note: new FormControl('', Validators.required) });
    this.showingNoteDialog = true;
  }

  onAddPhoto() {
    this.showingPhotoDialog = true;
  }

  choose(event: any, callback: any) {
    callback();
  }

  onPhotoSubmit() {
    if (this.photoUpload.files.length == 0) return;
    this.photoUpload.uploader();
    this.showingPhotoDialog = false;
    this.photoUpload.clear();
  }

  onPhotoCancel() {
    this.photoUpload.clear();
    this.showingPhotoDialog = false;
  }

  handlePhotoUpload(event: FileUploadHandlerEvent) {
    if (!this.listingId()) return;
    this.listingService.uploadPhotos(this.listingId(), event.files).subscribe({
      next: () => {
        console.log('photos uploaded');
      },
    });
  }

  onExport() {
    this.showingExportDialog = true;
  }

  onExportCancel() {
    this.showingExportDialog = false;
    this.selectedClient = null;
  }

  handleEmailExport() {
    if (this.selectedClient) {
      if (this.listingId()) {
        this.exportService.sendEmail(this.listingId(), this.selectedClient.email).subscribe(() => {
          this.showingExportDialog = false;
        });
      }
    }
  }
}
