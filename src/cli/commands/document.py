from pathlib import Path

import click
import duckdb


@click.group()
def document():
    """Document commands"""
    pass


@document.command()
@click.argument("directory", type=click.STRING, required=False, default="./")
@click.option("--file-patterns", "-p", default="*.txt", help="Regular expression of filename patterns to index")
@click.option("--stemmer", default="porter", help="The type of stemmer to be used")
@click.option(
    "--stopwords",
    default="english",
    help="Qualified name of table containing stopwords, or 'none' if no stopwords are to be used",
)
@click.option("--ignore", default="(\\.|[^a-z])+", help="Regular expression of patterns to be ignored")
@click.option(
    "--strip-accents/--no-strip-accents", default=True, help="Whether to remove accents (e.g., convert 'á' to 'a')"
)
@click.option("--lower/--no-lower", default=True, help="Whether to convert all text to lowercase")
@click.option("--overwrite/--no-overwrite", default=False, help="Whether to overwrite an existing index on a table")
def index(directory, file_patterns, output, stemmer, stopwords, ignore, strip_accents, lower, overwrite) -> None:
    """Create a DuckDB full-text search index from files"""

    directory_path = Path(directory)
    output_path = directory_path / "index.duckdb"

    if output_path.exists():
        raise FileExistsError(f"DuckDB index file already exists: {output_path}")

    conn = duckdb.connect(str(output_path))

    conn.execute("INSTALL fts")
    conn.execute("LOAD fts")

    # Create table with data from all matching file patterns
    conn.execute("""
        CREATE OR REPLACE TABLE documents (
            id INTEGER,
            file_path VARCHAR,
            file_name VARCHAR,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Insert data for each pattern
    conn.execute(f"""
        INSERT INTO documents (id, file_path, file_name, content, created_at)
        SELECT
            ROW_NUMBER() OVER () + (SELECT COALESCE(MAX(id), 0) FROM documents) as id,
            filename as file_path,
            regexp_extract(filename, '[^/]+$') as file_name,
            content,
            CURRENT_TIMESTAMP as created_at
        FROM read_text('{directory_path}/**/{file_patterns}')
        WHERE content IS NOT NULL AND trim(content) != '';
    """)

    conn.execute(f"""
        PRAGMA create_fts_index(
            'documents',
            'id',
            'content',
            stemmer='{stemmer}',
            stopwords='{stopwords}',
            ignore='{ignore}',
            strip_accents={str(strip_accents).lower()},
            lower={str(lower).lower()},
            overwrite={str(overwrite).lower()}
        );
    """)


@document.command()
@click.argument("directory", type=click.STRING, default="./")
@click.argument("terms", type=click.STRING)
@click.option("--limit", type=click.INT, default=10, help="Number of results to return")
@click.option("--tablefmt", type=click.STRING, default="fancy_grid", help="Tabulate table format")
def search(directory, terms, limit, tablefmt) -> None:
    """Query the DuckDB index"""

    conn = duckdb.connect(Path(directory) / "index.duckdb")

    query = f"""
        SELECT * FROM documents
        WHERE fts_main_documents.match_bm25(id, '{terms}'::string) IS NOT NULL
        ORDER BY fts_main_documents.match_bm25(id, '{terms}'::string) DESC
        LIMIT {limit}
    """

    df = conn.execute(query).fetchdf().set_index("id")
    click.echo(df.to_markdown(tablefmt=tablefmt))
