export interface DashboardData {
  user: string;
  total_jobs: number;
  top_categories: { label: string; count: number }[];
  top_locations: { label: string; count: number }[];
  top_sources: { label: string; count: number }[];
  top_companies: { label: string; count: number }[];
  common_tags: { label: string; count: number }[];
  job_type_distribution: { label: string; count: number }[];
  salary_coverage: number;
  average_salary: number;
  recent_week_count: number;
  recent_month_count: number;
  salary_histogram: {
    bin_edges: number[];
    counts: number[];
  };
  trend_labels: string[];
  trend_values: number[];
}
