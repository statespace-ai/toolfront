from toolfront.tools.api import api_get_endpoints, api_inspect_endpoint, api_request
from toolfront.tools.database import (
    db_inspect_table,
    db_query,
    db_sample_table,
    db_search_tables,
)
from toolfront.tools.library import library_read, library_search_documents

database_tools = [
    db_inspect_table,
    db_query,
    db_sample_table,
    db_search_tables,
]

api_tools = [api_get_endpoints, api_inspect_endpoint, api_request]

library_tools = [library_search_documents, library_read]
