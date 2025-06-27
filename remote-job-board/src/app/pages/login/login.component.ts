import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './login.component.html'
})
export class LoginComponent implements OnInit {
  email = '';
  password = '';
  error = '';

  constructor(private auth: AuthService, private router: Router) {}

  ngOnInit(): void {
    if (this.auth.isLoggedIn()) {
      this.router.navigate(['/dashboard']); // ✅ redirect logged-in user
    }
  }

  onSubmit(): void {
    this.error = '';
    if (!this.email || !this.password) {
      this.error = 'Please fill in both fields.';
      return;
    }

    this.auth.login(this.email, this.password).subscribe({
      next: (res) => {
        console.log("Login sucessful, token:", res.access_token);
        this.auth.saveToken(res.access_token); // save token
        this.router.navigate(['/dashboard']);   // redirect
      },
      error: (err) => {
        this.error = err.error?.msg || 'Login failed. Please try again.';
        console.error('Login error:', err);
      }
    });
  }
}
