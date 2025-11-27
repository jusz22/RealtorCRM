import { Component, inject, OnInit, signal } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { DialogModule } from 'primeng/dialog';
import { TextareaModule } from 'primeng/textarea';
import {
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  FormControl,
  Validators,
} from '@angular/forms';
import { NotesStateService } from '../../../../services/notes-state.service';
import { NotesService } from './notes.service';
import { Note } from './notes.model';
import { NoteComponent } from './note/note.component';
import { ButtonModule } from 'primeng/button';
import { Message } from 'primeng/message';

@Component({
  selector: 'app-notes',
  templateUrl: './notes.component.html',
  imports: [
    DialogModule,
    TextareaModule,
    FormsModule,
    ReactiveFormsModule,
    NoteComponent,
    ButtonModule,
    Message,
  ],
})
export class NotesComponent implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly notesService = inject(NotesService);
  private readonly notesStateService = inject(NotesStateService);
  protected readonly listingId = signal<string>('');
  protected showingEditDialog = false;
  protected formGroup!: FormGroup;
  readonly notes = this.notesStateService.notes;

  ngOnInit(): void {
    this.route.parent?.params.subscribe({
      next: (params) => {
        const listingId = params['id'];
        this.listingId.set(listingId);
        this.notesService.getNotes(listingId).subscribe({
          next: (notes) => {
            this.notesStateService.setNotes(notes);
          },
        });
      },
    });
  }

  onEdit(editNote: Note) {
    this.formGroup = new FormGroup({
      id: new FormControl(editNote.id),
      note: new FormControl(editNote.note, Validators.required),
    });
    this.showingEditDialog = true;
  }

  onSubmit() {
    if (this.formGroup.valid) {
      const oldNote = this.notesStateService.getNote(this.formGroup.get('id')?.value);
      if (oldNote) {
        this.notesService
          .updateNote(
            oldNote.id,
            this.formGroup.get('note')?.value,
            oldNote.listing_id,
            oldNote.user_id
          )
          .subscribe({
            next: (note) => {
              this.notesStateService.updateNote(note.id, { note: note.note });
            },
          });
      }
      this.showingEditDialog = false;
    }
  }

  onCancelEdit() {
    this.showingEditDialog = false;
  }

  onDelete(noteDel: Note) {
    this.notesService.deleteNote(noteDel.id).subscribe({
      next: (mess) => {
        this.notesStateService.deleteNote(noteDel.id);
        console.log(mess.message);
      },
    });
  }
}
