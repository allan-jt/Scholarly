from pydantic import BaseModel

class QueryPrefixes(BaseModel):
    title: str | None = None
    author: str | None = None
    abstract: str | None = None
    comment: str | None = None
    journal_reference: str | None = None
    subject_category: str | None = None
    report_number: str | None = None
    id_list: str | None = None
    all: str | None = None

class QueryConfig(BaseModel):
    boolean_operator: str | None = 'AND'    # AND, OR, ANDNOT
    start: int | None = 0
    max_results: int | None = 5
    sort_by: str | None = None              # relevance, lastUpdatedDate, submittedDate
    sort_order: str | None = None           # ascending, descending
