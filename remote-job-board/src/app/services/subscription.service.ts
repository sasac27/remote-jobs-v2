import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';


@Injectable({
  providedIn: 'root'
})
export class SubscriptionService {
  private API_URL = `${environment.apiUrl}/subscriptions`;

  constructor(private http: HttpClient) {}

  createSubscription(data: { category: string; location: string; keyword: string }) {
    return this.http.post(this.API_URL, data);
  }

  getSubscriptions() {
    return this.http.get(this.API_URL);
  }
}
