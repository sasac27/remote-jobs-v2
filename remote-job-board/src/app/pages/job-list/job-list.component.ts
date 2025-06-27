import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { JobService } from '../../services/job.service';

interface Job {
  url: string;
  title: string;
  company: string;
  location: string;
  created: string;
  salary?: string;
  description: string;
  tags?: string[];
}

@Component({
  selector: 'app-job-list',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './job-list.component.html',
  styleUrls: ['./job-list.component.scss']
})
export class JobListComponent implements OnInit {
  jobs: Job[] = [];

  category = '';
  location = '';
  keyword = '';
  source = 'adzuna';
  page = 1;
  totalPages = 1;
  isLoading = false;

  constructor(private jobService: JobService) {}

  ngOnInit(): void {
    this.fetchJobs();
  }

  onSearch(): void {
    this.page = 1;
    this.fetchJobs();
  }

  goToPage(page: number): void {
    if (page < 1) return;
    this.page = page;
    this.fetchJobs();
  }

  fetchJobs(): void {
    this.isLoading = true;
    const params = {
      category: this.category,
      location: this.location,
      keyword: this.keyword,
      source: this.source,
      page: this.page.toString()
    };

    this.jobService.getJobs(params).subscribe({
      next: (response: any) => {
        this.jobs = response.jobs || response;
        this.totalPages = response.total_pages || 1; // Optional: update with real data if available
        console.log('[Angular] Jobs received:', this.jobs);
        this.isLoading = false;
      },
      error: (err) => {
        console.error('[Angular] Error loading jobs:', err);
        this.isLoading = false;
      }
    });
  }
}
