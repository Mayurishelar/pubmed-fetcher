from typing import List, Dict, Optional
import re
from Bio import Entrez
import pandas as pd
from datetime import datetime

class PubMedFetcher:
    """Class to fetch and process PubMed papers."""
    
    def __init__(self, email: str, debug: bool = False):
        """Initialize with user email for PubMed API and debug flag."""
        self.email = email
        self.debug = debug
        Entrez.email = email
    
    def search_papers(self, query: str, max_results: int = 100) -> List[str]:
        """Search PubMed for papers matching the query."""
        try:
            if self.debug:
                print(f"Searching PubMed with query: {query}")
            handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
            record = Entrez.read(handle)
            handle.close()
            return record["IdList"]
        except Exception as e:
            if self.debug:
                print(f"Error in search: {str(e)}")
            raise ValueError(f"Failed to search PubMed: {str(e)}")

    def fetch_paper_details(self, pubmed_ids: List[str]) -> List[Dict]:
        """Fetch details for a list of PubMed IDs."""
        try:
            if self.debug:
                print(f"Fetching details for {len(pubmed_ids)} papers")
            handle = Entrez.efetch(db="pubmed", id=",".join(pubmed_ids), retmode="xml")
            records = Entrez.read(handle)
            handle.close()
            return records["PubmedArticle"]
        except Exception as e:
            if self.debug:
                print(f"Error fetching details: {str(e)}")
            raise ValueError(f"Failed to fetch paper details: {str(e)}")

    def is_non_academic(self, affiliation: str) -> bool:
        """Heuristic to identify non-academic affiliations (pharma/biotech)."""
        if not affiliation:
            return False
        academic_keywords = ["university", "college", "institute", "laboratory", "school"]
        pharma_keywords = ["pharma", "biotech", "pharmaceutical", "inc.", "corp", "llc"]
        affiliation_lower = affiliation.lower()
        return (
            any(keyword in affiliation_lower for keyword in pharma_keywords) and
            not any(keyword in affiliation_lower for keyword in academic_keywords)
        )

    def extract_email(self, article: Dict) -> Optional[str]:
        """Extract corresponding author's email from article."""
        try:
            for author in article["MedlineCitation"]["Article"]["AuthorList"]:
                if "AffiliationInfo" in author:
                    for aff in author["AffiliationInfo"]:
                        if "Email" in aff:
                            return aff["Email"]
            return None
        except KeyError:
            return None

    def process_papers(self, pubmed_ids: List[str]) -> List[Dict]:
        """Process papers to extract required fields."""
        papers = self.fetch_paper_details(pubmed_ids)
        results = []
        
        for paper in papers:
            try:
                article = paper["MedlineCitation"]["Article"]
                pubmed_id = paper["MedlineCitation"]["PMID"]
                title = article.get("ArticleTitle", "N/A")
                
                # Extract publication date
                pub_date = article["Journal"]["JournalIssue"].get("PubDate", {})
                year = pub_date.get("Year", "N/A")
                month = pub_date.get("Month", "N/A")
                day = pub_date.get("Day", "N/A")
                pub_date_str = f"{year}-{month}-{day}"
                
                # Extract authors and affiliations
                non_academic_authors = []
                company_affiliations = []
                for author in article["AuthorList"]:
                    if "AffiliationInfo" in author:
                        for aff in author["AffiliationInfo"]:
                            if self.is_non_academic(aff.get("Affiliation", "")):
                                last_name = author.get("LastName", "")
                                fore_name = author.get("ForeName", "")
                                author_name = f"{fore_name} {last_name}".strip()
                                non_academic_authors.append(author_name)
                                company_affiliations.append(aff["Affiliation"])
                
                if non_academic_authors:  # Only include papers with non-academic authors
                    email = self.extract_email(paper)
                    results.append({
                        "PubmedID": str(pubmed_id),
                        "Title": title,
                        "Publication Date": pub_date_str,
                        "Non-academic Author(s)": "; ".join(non_academic_authors),
                        "Company Affiliation(s)": "; ".join(company_affiliations),
                        "Corresponding Author Email": email if email else "N/A"
                    })
                
                if self.debug:
                    print(f"Processed paper {pubmed_id}: {title}")
                    
            except Exception as e:
                if self.debug:
                    print(f"Error processing paper {pubmed_id}: {str(e)}")
                continue
                
        return results

    def save_to_csv(self, data: List[Dict], filename: Optional[str]) -> None:
        """Save results to CSV or print to console."""
        df = pd.DataFrame(data)
        if filename:
            df.to_csv(filename, index=False)
            if self.debug:
                print(f"Saved results to {filename}")
        else:
            print(df.to_string(index=False))