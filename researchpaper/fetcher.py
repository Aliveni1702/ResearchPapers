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
    title = root.findtext(".//ArticleTitle")
    pub_date = root.findtext(".//PubDate/Year")
    authors = root.findall(".//Author")
    non_academic_authors = []
    company_affiliations = []

    for author in authors:
        affiliation = author.findtext(".//Affiliation")
        if affiliation and not any(kw in affiliation.lower() for kw in ["university", "college", "institute"]):
            non_academic_authors.append(author.findtext("LastName"))
            company_affiliations.append(affiliation)

    corresponding_email = root.findtext(".//ElectronicAddress")

    return {
        "PubmedID": pmid,
        "Title": title,
        "Publication Date": pub_date,
        "Non-academic Authors": ", ".join(non_academic_authors),
        "Company Affiliations": ", ".join(company_affiliations),
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
