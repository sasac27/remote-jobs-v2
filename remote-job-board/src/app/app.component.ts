//app.component.ts
import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { NavbarComponent } from './components/navbar/navbar.component';
import { FooterComponent } from './components/footer/footer.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, NavbarComponent, FooterComponent],
  template: `
    <app-navbar></app-navbar>

    <main class="max-w-7xl mx-auto px-4 py-10">
      <router-outlet></router-outlet>
    </main>

    <app-footer></app-footer>
  `
})
export class AppComponent {}
