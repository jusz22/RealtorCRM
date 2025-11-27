import { HttpClient, HttpParams } from '@angular/common/http';
import { computed, inject, Injectable, signal } from '@angular/core';
import { Token } from './auth.model';

export interface CurrentUser {
  id: number;
  username: string;
  email: string;
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  http = inject(HttpClient);
  tokenSignal = signal<string | null>(localStorage.getItem('token'));
  isAuthenticated = computed(() => {
    return !!this.tokenSignal();
  });

  login(username: string, password: string) {
    const body = new HttpParams().appendAll({
      'username': username,
      'password': password,
    });

    return this.http.post<Token>('http://localhost:8000/api/v1/login', body, {
      headers: {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
  }

  saveToken(token: Token) {
    const expiresAt = JSON.parse(atob(token.access_token.split('.')[1])).exp;

    localStorage.setItem('token', JSON.stringify(token.access_token));
    localStorage.setItem('token_expires', expiresAt);
    this.tokenSignal.set(JSON.stringify(token.access_token));
  }

  deleteToken() {
    localStorage.removeItem('token');
    localStorage.removeItem('token_expires');
    this.tokenSignal.set(null);
  }

  getAuthToken() {
    return JSON.parse(localStorage.getItem('token') || '""');
  }

  getCurrentUser() {
    return this.http.get<CurrentUser>('http://localhost:8000/api/v1/me');
  }
}
