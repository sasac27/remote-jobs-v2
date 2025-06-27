import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './navbar.component.html'
})
export class NavbarComponent {
  userEmail: string | null = null;

  constructor(public auth: AuthService, private router: Router) {
    if (auth.isLoggedIn()) {
      const token = auth.getToken();
      if (token) {
        try {
          const payload = JSON.parse(atob(token.split('.')[1]));
          this.userEmail = payload.sub || payload.email || null;
        } catch {
          this.userEmail = null;
        }
      }
    }
  }

  logout() {
    this.auth.logout();
  }
}
