import { HttpEvent, HttpHandlerFn, HttpRequest } from '@angular/common/http';
import { inject } from '@angular/core';
import { Observable } from 'rxjs';
import { AuthService } from '../services/auth.service';

export function authInterceptor(
  req: HttpRequest<unknown>,
  next: HttpHandlerFn
): Observable<HttpEvent<unknown>> {
  const authService = inject(AuthService);
  const token = authService.getAuthToken();

  if (
    req.url ===
      'https://images.pexels.com/photos/2014422/pexels-photo-2014422.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940' ||
    req.url === 'https://api.pexels.com/v1/photos/186077'
  ) {
    return next(req);
  }
  if (token === '') {
    return next(req);
  }
  const authRequest = req.clone({
    headers: req.headers.set('Authorization', `Bearer ${token}`),
  });

  return next(authRequest);
}
