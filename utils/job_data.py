from jobs.remotive import get_data as get_remotive
from jobs.adzuna import get_adzuna_jobs, normalize_adzuna_jobs

def get_all_jobs():
    remotive = get_remotive()
    adzuna_raw = get_adzuna_jobs(page=1, results_per_page=50)
    adzuna = normalize_adzuna_jobs(adzuna_raw)
    return remotive + adzuna
