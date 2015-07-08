import sys
import re
import urllib2
import json

from pprint import pprint
from urllib import urlencode
from collections import Counter, OrderedDict

base_url = "https://www.zonajobs.com.ar"


def _correct_shortname(shortname):
    '''Some fixes to shortname'''
    fixed_shortname = shortname.replace('_', '-')
    return fixed_shortname
    


def get_job(jobid):
    
    query_args = {'jobId' : str(jobid)}
    encoded_args = urlencode(query_args)
    
    try:
        response = urllib2.urlopen(
            base_url + "/postulante/empleos.json?" + encoded_args)
        data = response.read()
    except urllib2.HTTPError, e:
        if e.getcode() == 500:
            data = "{}"
        else:
            raise
            
    parsed_data = json.loads(data)
    if parsed_data.has_key("success"):
        parsed_data = parsed_data["success"]
    
    return parsed_data


def get_areas():
    response = urllib2.urlopen(base_url + "/jobseeker/api/v1/areas")
    return json.loads(response.read())


def get_sector(area_shortname):    
    query_args = {'areaId' : _correct_shortname(area_shortname)}
    encoded_args = urlencode(query_args)
    
    response = urllib2.urlopen(
        base_url + "/jobseeker/api/v1/areas/sectors?" + encoded_args)
    return json.loads(response.read())
    

def get_all_areas_sectors():
    response = urllib2.urlopen(
        base_url + "/jobseeker/api/v1/areas/searchables?expand=true")
    return json.loads(response.read())
    
       

def get_publications_sector(sector_shortname):
    '''Get all publications from a sector or a full area'''
    totalpages = 1
    currentpage = 1
    
    fixed_sector_shortname = _correct_shortname(sector_shortname)
    
    jobs = []
    
    while currentpage <= totalpages:
        response = urllib2.urlopen(
            base_url + "/empleos/area=" + fixed_sector_shortname + \
            ("_pagina=" + str(currentpage) if currentpage > 1
                                           else "") + \
            "?format=json"
            )

        r = response.read()
        r = ''.join(r.split("\n"))
        r = ''.join(r.split("\t"))
        
        data_json = json.loads(r.decode('utf8'))
        totalpages = int(data_json["paging"]["totalPages"])
        if totalpages < currentpage:
            raise Exception("Error: External API returned " + \
                            "totalPages < currentPage")
        currentpage += 1
    
        jobs_partial = data_json['jobs']
        jobs += jobs_partial
    
    return jobs
