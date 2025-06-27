import { Component, Inject, PLATFORM_ID, OnInit } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { ChartData, ChartOptions } from 'chart.js';
import { DashboardData } from './dashboard.types';
import { CommonModule } from '@angular/common';
import { NgChartsModule } from 'ng2-charts';
import { environment } from '../../../../environment';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, NgChartsModule],
  templateUrl: './dashboard.component.html'
})
export class DashboardComponent implements OnInit {
  isBrowser: boolean;
  loading = true;

  user = '';
  totalJobs = 0;
  averageSalary = 0;
  recentWeekCount = 0;
  recentMonthCount = 0;

  chartOptions: ChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: 'top'
      }
    }
  };

  categoriesChartData!: ChartData<'bar'>;
  salaryCoverageData!: ChartData<'pie'>;
  trendData!: ChartData<'line'>;
  salaryHistogramData!: ChartData<'bar'>;
  jobTypeChartData!: ChartData<'pie'>;
  commonTagsChartData!: ChartData<'bar'>;
  topCompaniesChartData!: ChartData<'bar'>;
  topSourcesChartData!: ChartData<'bar'>;

  constructor(
    @Inject(PLATFORM_ID) platformId: Object,
    private http: HttpClient
  ) {
    this.isBrowser = isPlatformBrowser(platformId);
  }

  ngOnInit() {
    if (this.isBrowser) {
      this.http.get<DashboardData>(`${environment.apiUrl}/dashboard`, { withCredentials: true }).subscribe(data => {
        this.user = data.user;
        this.totalJobs = data.total_jobs;
        this.averageSalary = data.average_salary;
        this.recentWeekCount = data.recent_week_count;
        this.recentMonthCount = data.recent_month_count;
        this.setupCharts(data);
        this.loading = false;
      });
    }
  }

  setupCharts(data: DashboardData) {
    // Top Categories
    const topCategories = data.top_categories ?? [];
    this.categoriesChartData = {
      labels: topCategories.map(item => item.label),
      datasets: [{
        data: topCategories.map(item => item.count),
        label: 'Top Categories'
      }]
    };

    // Salary Coverage
    this.salaryCoverageData = {
      labels: ['With Salary', 'Missing Salary'],
      datasets: [{
        data: [data.salary_coverage ?? 0, 100 - (data.salary_coverage ?? 0)],
        label: 'Salary Coverage'
      }]
    };

    // Job Trend
    this.trendData = {
      labels: data.trend_labels ?? [],
      datasets: [{
        data: data.trend_values ?? [],
        label: 'Jobs Posted Over Time',
        tension: 0.3,
        fill: false
      }]
    };

    // Salary Histogram
    if (data.salary_histogram?.counts?.length) {
      const bins = data.salary_histogram.bin_edges;
      const midpoints = bins.slice(0, -1).map((val, i) => {
        const next = bins[i + 1];
        return `$${Math.round(val)}–${Math.round(next)}`;
      });

      this.salaryHistogramData = {
        labels: midpoints,
        datasets: [{
          data: data.salary_histogram.counts,
          label: 'Salary Distribution'
        }]
      };
    } else {
      this.salaryHistogramData = { labels: [], datasets: [] };
    }

    // Job Types
    const jobTypes = data.job_type_distribution ?? [];
    this.jobTypeChartData = {
      labels: jobTypes.map(j => j.label),
      datasets: [{ data: jobTypes.map(j => j.count), label: 'Job Types' }]
    };

    // Common Tags
    const tags = data.common_tags ?? [];
    this.commonTagsChartData = {
      labels: tags.map(t => t.label),
      datasets: [{ data: tags.map(t => t.count), label: 'Common Tags' }]
    };

    // Top Companies
    const companies = data.top_companies ?? [];
    this.topCompaniesChartData = {
      labels: companies.map(c => c.label),
      datasets: [{ data: companies.map(c => c.count), label: 'Top Companies' }]
    };

    // Top Sources
    const sources = data.top_sources ?? [];
    this.topSourcesChartData = {
      labels: sources.map(s => s.label),
      datasets: [{ data: sources.map(s => s.count), label: 'Top Sources' }]
    };
}

}
