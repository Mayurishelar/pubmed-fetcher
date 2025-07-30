PubMed Fetcher
A Python program to fetch research papers from PubMed with at least one author affiliated with a pharmaceutical or biotech company.
Code Organization

pubmed_fetcher/fetcher.py: Module containing the PubMedFetcher class for API interactions and data processing.
scripts/get_papers_list.py: Command-line interface script using the pubmed_fetcher module.
pyproject.toml: Poetry configuration for dependencies and CLI setup.
.gitignore: Excludes virtual environments and build artifacts.

Installation

Install Poetry:pip install poetry


Clone the Repository:git clone https://github.com/Mayurishelar/pubmed-fetcher.git
cd pubmed-fetcher


Install Dependencies:poetry install


Activate Virtual Environment:poetry shell



Usage
Run the program using the get-papers-list command:
poetry run get-papers-list "cancer therapy" --email your.email@example.com

Options:

-f/--file <filename>: Save output to a CSV file (e.g., output.csv).
-d/--debug: Enable debug mode for detailed logging.
-e/--email <email>: Required email for PubMed API access.
-h/--help: Show help message.

Example with output file and debug mode:
poetry run get-papers-list "cancer therapy" --email your.email@example.com --file results.csv --debug

Tools Used

Poetry: Dependency management and packaging (poetry.eustace.io).
BioPython: PubMed API access (biopython.org).
Pandas: CSV handling (pandas.pydata.org).
Click: Command-line interface (click.palletsprojects.com).
Git: Version control (git-scm.com).
GitHub: Code hosting (github.com).
Grok: Assisted in code planning and debugging (x.ai).

Notes

The program uses heuristics to identify non-academic authors (e.g., affiliations containing "pharma", "biotech", excluding "university").
Ensure a valid email is provided for PubMed API compliance.
Results are filtered to include only papers with non-academic authors.
