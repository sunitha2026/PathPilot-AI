import requests


# ==========================================
# HIMALAYAS REMOTE JOBS
# ==========================================

def search_remote_jobs(query):
    url = "https://himalayas.app/jobs/api/search"

    params = {
        "q": query,
        "worldwide": "true",
        "sort": "recent",
        "page": 1
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        if response.status_code != 200:
            print("Himalayas API error:", response.status_code)
            return []

        data = response.json()

        jobs = []

        for job in data.get("jobs", []):

            jobs.append({
                "title": job.get("title", ""),
                "company": job.get("companyName", ""),
                "location": "Remote",
                "type": job.get("employmentType", ""),
                "updated": job.get("pubDate", ""),
                "link": job.get("applicationLink", ""),
                "source": "Himalayas"
            })

        return jobs

    except Exception as e:
        print("Himalayas search error:", e)
        return []


# ==========================================
# OPENINTERN INTERNSHIPS
# ==========================================

def search_internships(query):

    url = "https://openintern.dev/api/v1/jobs"

    params = {
        "q": query,
        "limit": 20
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        if response.status_code != 200:
            print("OpenIntern API error:", response.status_code)
            return []

        data = response.json()

        internships = []

        for job in data.get("jobs", []):

            for posting in job.get("postings", []):

                internships.append({
                    "title": job.get("title", ""),
                    "company": job.get("company", ""),
                    "location": posting.get("location", ""),
                    "type": "Internship",
                    "updated": posting.get("posted_at", ""),
                    "link": posting.get("apply_url", ""),
                    "source": "OpenIntern"
                })

        return internships

    except Exception as e:
        print("OpenIntern search error:", e)
        return []


# ==========================================
# MAIN JOB SEARCH FUNCTION
# ==========================================

def search_jobs(query, location="India"):

    all_jobs = []

    # Remote jobs
    remote_jobs = search_remote_jobs(query)
    all_jobs.extend(remote_jobs)

    # Internships
    internships = search_internships(query)
    all_jobs.extend(internships)

    # Remove duplicate links
    unique_jobs = []
    seen_links = set()

    for job in all_jobs:

        link = job.get("link", "").strip()

        if link and link not in seen_links:

            seen_links.add(link)
            unique_jobs.append(job)

    return unique_jobs[:20]