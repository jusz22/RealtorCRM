import { Injectable, signal, computed } from '@angular/core';
import { Note } from '../components/listings/listing/notes/notes.model';

@Injectable({
  providedIn: 'root',
})
export class NotesStateService {
  private readonly notesSignal = signal<Note[]>([]);
  readonly notes = computed(() => this.notesSignal());
  readonly notesCount = computed(() => this.notesSignal().length);

  setNotes(notes: Note[]): void {
    this.notesSignal.set(notes);
  }

  addNote(note: Note): void {
    this.notesSignal.update((notes) => {
      notes.push(note);
      return notes;
    });
  }

  /**
   * Update a note
   */
  updateNote(noteId: string, updatedNote: Partial<Note>): void {
    this.notesSignal.update((notes) => {
      const index = notes.findIndex((n) => n.id === noteId);
      if (index !== -1) {
        notes[index] = { ...notes[index], ...updatedNote };
      }
      return notes;
    });
  }

  /**
   * Delete a note by id
   */
  deleteNote(noteId: string): void {
    this.notesSignal.update((notes) => {
      return notes.filter((note) => note.id !== noteId);
    });
  }

  /**
   * Get a single note by id
   */
  getNote(noteId: string): Note | undefined {
    return this.notesSignal().find((note) => note.id === noteId);
  }

  /**
   * Clear all notes
   */
  clearNotes(): void {
    this.notesSignal.set([]);
  }

  /**
   * Get notes for a specific listing
   */
  getNotesByListingId(listingId: string): Note[] {
    return this.notesSignal().filter((note) => note.listing_id === listingId);
  }
}
