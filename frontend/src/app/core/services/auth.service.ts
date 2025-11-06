import { HttpClient, HttpErrorResponse, HttpParams } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Token } from './auth.model';

@Injectable({ providedIn: 'root' })
export class AuthService {
  http = inject(HttpClient);

  login(username: string, password: string) {
    const body = new HttpParams().appendAll({
      'username': username,
      'password': password,
    });

    this.http
      .post<Token>('http://localhost:8000/api/v1/login', body, {
        headers: {
          'accept': 'application/json',
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      })
      .subscribe({
        next(res) {
          AuthService.saveToken(res);
        },
        error: (err: HttpErrorResponse) => {
          if (err.status === 401) {
            return { error: 'Wrong login or password' };
          }
          if (err.status && err.status !== 401) return { error: 'Error' };
          return;
        },
      });
  }

  isAuthenticated() {
    if (localStorage.getItem('token')) {
      return true;
    }
    return false;
  }

  static saveToken(token: Token) {
    const expiresAt = JSON.parse(atob(token.access_token.split('.')[1])).exp;

    localStorage.setItem('token', JSON.stringify(token.access_token));
    localStorage.setItem('token_expires', expiresAt);
  }

  getAuthToken() {
    return JSON.parse(localStorage.getItem('token') || '""');
  }
}
