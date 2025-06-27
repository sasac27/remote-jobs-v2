// src/app/routes.ts
import { Routes } from '@angular/router';
import { authGuard } from './auth.guard';
import { JobListComponent } from './pages/job-list/job-list.component';

export const routes: Routes = [
  {
    path: '',
    component: JobListComponent
  },
  {
    path: 'login',
    loadComponent: () =>
      import('./pages/login/login.component').then(m => m.LoginComponent)
  },
  {
    path: 'register',
    loadComponent: () =>
      import('./pages/register/register.component').then(m => m.RegisterComponent)
  },
  {
    path: 'subscribe',
    canActivate: [authGuard],
    loadComponent: () =>
      import('./pages/subscription/subscription.component').then(m => m.SubscriptionComponent)
  },
  {
    path: 'dashboard',
    canActivate: [authGuard],
    loadComponent: () =>
      import('./pages/dashboard/dashboard.component').then(m => m.DashboardComponent)
  }
];
