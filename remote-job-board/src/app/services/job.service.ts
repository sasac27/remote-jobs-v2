import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environment';

export interface Job {
  url: string;
  title: string;
  company: string;
  location: string;
  created: string;
  salary?: string;
  description: string;
  tags?: string[];
  category?: string;
}

@Injectable({
  providedIn: 'root'
})
export class JobService {
  private apiUrl = `${environment.apiUrl}/jobs`;

  constructor(private http: HttpClient) {}

  getJobs(paramsObj: any): Observable<Job[]> {
    let params = new HttpParams();
    for (let key in paramsObj) {
      if (paramsObj[key]) {
        params = params.set(key, paramsObj[key]);
      }
    }
    return this.http.get<Job[]>(this.apiUrl, { params });
  }
}
