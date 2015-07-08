from collections import Counter

from zonajobs_api import *



def publications_by_sector(sector_shortname):    
    sector_jobs_json = get_publications_sector(sector_shortname)
    ids = map(lambda job: job["id"], sector_jobs_json)    
    
    jobs_raw = [get_job(id) for id in ids]

    jobs = []
    c = Counter()
    for job in jobs_raw:
        location = None
        if job["job"]["location"].has_key("parent"):
            if job["job"]["location"]["parent"]["name"] == "Capital Federal":
                location = job["job"]["location"]["name"]
                c[location] += 1
        else:
            pass
            #~ print "__________________________________________________"
            #~ pprint(job["success"]["job"]["location"])
            #~ print(job["success"]["job"]["jobCompany"])
                                   
    
    return c
