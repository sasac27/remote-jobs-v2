import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { SubscriptionService } from '../../services/subscription.service';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-subscription',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './subscription.component.html'
})
export class SubscriptionComponent {
  category = '';
  location = '';
  keyword = '';
  message = '';
  error = '';

  constructor(private subscriptionService: SubscriptionService) {}

  onSubmit() {
    this.subscriptionService.createSubscription({
      category: this.category,
      location: this.location,
      keyword: this.keyword
    }).subscribe({
      next: () => {
        this.message = '✅ Subscription saved!';
        this.error = '';
      },
      error: (err) => {
        this.message = '';
        this.error = err.error.msg || 'Failed to save subscription.';
      }
    });
  }
}
