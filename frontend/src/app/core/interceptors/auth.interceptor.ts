import { HttpEvent, HttpEventType, HttpHandlerFn, HttpRequest } from '@angular/common/http';
import { inject } from '@angular/core';
import { Observable, tap } from 'rxjs';
import { AuthService } from '../services/auth.service';

export function authInterceptor(
  req: HttpRequest<unknown>,
  next: HttpHandlerFn
): Observable<HttpEvent<unknown>> {
  const authService = inject(AuthService);
  const token = authService.getAuthToken();

  if (token === '') {
    return next(req);
  }
  const authRequest = req.clone({
    headers: req.headers.set('Authorization', `Bearer ${token}`),
  });

  return next(authRequest);
}
