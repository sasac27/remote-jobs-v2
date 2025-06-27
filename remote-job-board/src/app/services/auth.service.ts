import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { isPlatformBrowser } from '@angular/common';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private API_URL = 'http://localhost:5000/api/auth';
  private isBrowser: boolean;

  constructor(
    private http: HttpClient,
    private router: Router,
    @Inject(PLATFORM_ID) platformId: Object
  ) {
    this.isBrowser = isPlatformBrowser(platformId);
  }

  login(email: string, password: string) {
    return this.http.post<{ access_token: string }>(`${this.API_URL}/login`, {
      email,
      password
    });
  }

  register(email: string, password: string) {
    return this.http.post(`${this.API_URL}/register`, {
      email,
      password
    });
  }

  saveToken(token: string) {
    if (this.isBrowser) {
      localStorage.setItem('access_token', token);
    }
  }

  getToken(): string | null {
    return this.isBrowser ? localStorage.getItem('access_token') : null;
  }

  logout() {
    if (this.isBrowser) {
      localStorage.removeItem('access_token');
      this.router.navigate(['/login']);
    }
  }

  isLoggedIn(): boolean {
    return !!this.getToken();
  }
}
