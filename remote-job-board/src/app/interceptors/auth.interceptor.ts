import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthService } from '../services/auth.service';

export const authInterceptorFn: HttpInterceptorFn = (req, next) => {
  const auth = inject(AuthService);
  const token = auth.getToken();

  if (token) {
    console.log('✅ Attaching token:', token);
    req = req.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`
      },
    });
  } else {
    console.warn('❌ No token found in localStorage');
  }

  return next(req);
};
