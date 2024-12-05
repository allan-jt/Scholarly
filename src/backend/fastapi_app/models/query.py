from pydantic import BaseModel

class BaseQueryParams(BaseModel):
    # Config params shared between query and query_advanced endpoints
    boolean_operator: str | None = 'AND'
    start: int | None = 0
    max_results: int | None = 5
    sort_by: str | None = None
    sort_order: str | None = None

    def to_arxiv(self, fields: dict) -> dict:
        # Combine query fields and config into a structured dict for arxiv.fetch
        return {
            'query_fields': {key: value for key, value in fields.items() if value is not None},
            'query_config': {
                'boolean_operator': self.boolean_operator,
                'start': self.start,
                'max_results': self.max_results,
                'sort_by': self.sort_by,
                'sort_order': self.sort_order,
            }
        }

class QueryParams(BaseQueryParams):
    all: str

    def to_arxiv(self) -> dict:
        fields = {
            'all': self.all
        }
        return super().to_arxiv(fields)

class AdvancedQueryParams(BaseQueryParams):
    title: str | None = None
    author: str | None = None
    abstract: str | None = None
    comment: str | None = None
    journal_reference: str | None = None
    subject_category: str | None = None
    report_number: str | None = None
    id_list: str | None = None

    def to_arxiv(self) -> dict:
        fields = {
            'ti': self.title,
            'au': self.author,
            'abs': self.abstract,
            'co': self.comment,
            'jr': self.journal_reference,
            'cat': self.subject_category,
            'rn': self.report_number,
            'id': self.id_list
        }
        return super().to_arxiv(fields)
