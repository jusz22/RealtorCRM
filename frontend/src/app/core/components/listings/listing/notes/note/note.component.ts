import { Component, input, output, signal } from '@angular/core';
import { Note } from '../notes.model';
import { Card } from 'primeng/card';
import { DatePipe } from '@angular/common';
import { ButtonDirective } from 'primeng/button';
import { DialogModule } from 'primeng/dialog';

@Component({
  selector: 'app-note',
  templateUrl: './note.component.html',
  imports: [Card, DatePipe, ButtonDirective, DialogModule],
})
export class NoteComponent {
  readonly note = input.required<Note>();
  readonly onDelete = output<Note>();
  readonly onEdit = output<Note>();

  onClickDelete(note: Note) {
    this.onDelete.emit(note);
  }

  onClickEdit(note: Note) {
    this.onEdit.emit(note);
  }
}
