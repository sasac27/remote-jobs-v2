import hashlib

def generate_job_hash(title, company, created_at):
    raw = f"{title.lower().strip()}|{company.lower().strip()}|{created_at}"
    return hashlib.sha256(raw.encode()).hexdigest()