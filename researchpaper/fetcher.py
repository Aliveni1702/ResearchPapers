import requests
import xml.etree.ElementTree as ET
from typing import List, Dict

SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

def search_pubmed(query: str) -> List[str]:
    """Search PubMed for papers related to the query."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "xml",
        "retmax": 10
    }
    response = requests.get(SEARCH_URL, params=params)
    if response.status_code != 200:
        raise Exception("Error fetching data from PubMed")
    root = ET.fromstring(response.text)
    return [id_elem.text for id_elem in root.findall(".//Id")]

def fetch_paper_details(pmid: str) -> Dict:
    """Fetch details of a paper given its PubMed ID."""
    params = {
        "db": "pubmed",
        "id": pmid,
        "retmode": "xml"
    }
    response = requests.get(FETCH_URL, params=params)
    if response.status_code != 200:
        return None
    root = ET.fromstring(response.text)
    
    title = root.findtext(".//ArticleTitle") or "Unknown Title"
    pub_date = root.findtext(".//PubDate/Year") or "Unknown Date"
    authors = root.findall(".//Author")
    non_academic_authors = []
    company_affiliations = []

    for author in authors:
        last_name = author.findtext("LastName") or "Unknown"
        first_name = author.findtext("ForeName") or ""
        full_name = f"{first_name} {last_name}".strip()
        affiliation = author.findtext(".//AffiliationInfo/Affiliation")

        if affiliation:
            if not any(kw in affiliation.lower() for kw in ["university", "college", "institute", "hospital"]):
                non_academic_authors.append(full_name)
                company_affiliations.append(affiliation)

    corresponding_email = root.findtext(".//AuthorList/Author/Email") or "Not Available"

    return {
        "PubmedID": pmid,
        "Title": title,
        "Publication Date": pub_date,
        "Non-academic Authors": non_academic_authors,
        "Company Affiliations": company_affiliations,
        "Corresponding Author Email": corresponding_email
    }

def fetch_and_filter_papers(query: str) -> List[Dict]:
    """Fetch and filter papers based on a query."""
    pmids = search_pubmed(query)
    papers = []
    for pmid in pmids:
        paper = fetch_paper_details(pmid)
        if paper and paper['Non-academic Authors']:
            papers.append(paper)
    return papers
