import { HttpInterceptorFn } from '@angular/common/http';
import { inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { AuthService } from '../services/auth.service';

export const authInterceptorFn: HttpInterceptorFn = (req, next) => {
  const platformId = inject(PLATFORM_ID);

  if (isPlatformBrowser(platformId)) {
    const auth = inject(AuthService);
    const token = auth.getToken();

    if (token) {
      console.log('✅ Attaching token:', token);
      req = req.clone({
        setHeaders: {
          Authorization: `Bearer ${token}`,
        },
      });
    } else {
      console.warn('❌ No token found in localStorage');
    }
  }

  return next(req);
};
