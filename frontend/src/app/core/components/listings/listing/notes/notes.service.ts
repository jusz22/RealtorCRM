import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Note } from './notes.model';

@Injectable({ providedIn: 'root' })
export class NotesService {
  private readonly http = inject(HttpClient);

  getNotes(listing_id: string) {
    return this.http.get<Note[]>(`http://localhost:8000/api/v1/notes/${listing_id}`);
  }

  addNote(listingId: string, userId: number, note: string) {
    const body = {
      note: note,
      listing_id: listingId,
      user_id: userId,
    };
    return this.http.post<Note>('http://localhost:8000/api/v1/notes', body);
  }

  deleteNote(noteId: string) {
    return this.http.delete<{ message: string }>(`http://localhost:8000/api/v1/notes/${noteId}`);
  }

  updateNote(noteId: string, note: string, listingId: string, userId: string) {
    const body = {
      note: note,
      listing_id: listingId,
      user_id: userId,
    };
    return this.http.put<Note>(`http://localhost:8000/api/v1/notes/${noteId}`, body);
  }
}
