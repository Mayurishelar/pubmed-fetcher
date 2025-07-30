import click
from pubmed_fetcher.fetcher import PubMedFetcher
from typing import Optional

@click.command()
@click.argument("query", type=str)
@click.option("-f", "--file", type=str, help="Output CSV filename")
@click.option("-d", "--debug", is_flag=True, help="Enable debug mode")
@click.option("-e", "--email", type=str, required=True, help="Email for PubMed API")
def get_papers_list(query: str, file: Optional[str], debug: bool, email: str) -> None:
    """Fetch PubMed papers with non-academic authors and save to CSV or print to console.
    
    QUERY: PubMed search query (supports full PubMed syntax).
    """
    try:
        fetcher = PubMedFetcher(email=email, debug=debug)
        pubmed_ids = fetcher.search_papers(query)
        results = fetcher.process_papers(pubmed_ids)
        fetcher.save_to_csv(results, file)
    except Exception as e:
        if debug:
            print(f"Error: {str(e)}")
        raise click.ClickException(str(e))

if __name__ == "__main__":
    get_papers_list()