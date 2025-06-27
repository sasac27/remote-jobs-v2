import { Component, OnInit } from '@angular/core';
import { JobService, Job } from '../../services/job.service';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-job-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './job-list.component.html',
})
export class JobListComponent implements OnInit {
  jobs: Job[] = [];
  isLoading = false;

  // Filters
  keyword = '';
  category = '';
  location = '';
  source = 'adzuna';
  jobType = '';
  tags = '';
  salaryMin?: number;
  salaryMax?: number;
  daysPosted?: number;

  // Sorting
  sortBy = 'created';
  sortOrder = 'desc';

  // Pagination
  page = 1;
  totalPages = 1;

  constructor(private jobService: JobService) {}

  ngOnInit(): void {
    this.fetchJobs();
  }

  onSearch(): void {
    this.page = 1;
    this.fetchJobs();
  }

  goToPage(newPage: number): void {
    if (newPage < 1 || newPage > this.totalPages) return;
    this.page = newPage;
    this.fetchJobs();
  }

  fetchJobs(): void {
    console.log('[Angular] fetchJobs() called');
    this.isLoading = true;

    const params: any = {
      category: this.category,
      location: this.location,
      keyword: this.keyword,
      source: this.source,
      job_type: this.jobType,
      tags: this.tags,
      salary_min: this.salaryMin,
      salary_max: this.salaryMax,
      days_posted: this.daysPosted,
      sort_by: this.sortBy,
      sort_order: this.sortOrder,
      page: this.page.toString()
    };

    this.jobService.getJobs(params).subscribe({
      next: (response: any) => {
        console.log('[Angular] Raw API response:', response);

        this.jobs = response.jobs || [];
        this.totalPages = response.total_pages || 1;
        this.isLoading = false;

        console.log('[Angular] Jobs extracted:', this.jobs);
      },
      error: error => {
        this.isLoading = false;
        console.error('[Angular] API error:', error);
      }
    });
  }
}
