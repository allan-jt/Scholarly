from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Literal

class BaseQueryParams(BaseModel):
    model_config = {'extra': 'forbid'}
    
    # Config params shared between query and query_advanced endpoints
    boolean_operator: Literal['AND', 'OR', 'ANDNOT'] = 'AND'
    start: int = Field(0, ge=0)
    max_results: int = Field(5, ge=1)
    sort_by: Literal['relevance', 'lastUpdatedDate', 'submittedDate'] | None = None
    sort_order: Literal['ascending', 'descending'] | None = None

    @field_validator('*', mode='before')
    def clean_fields(cls, value):
        # Strip whitespace from all string fields and convert to None if empty
        if isinstance(value, str):
            value = value.strip()   # remove whitespace from strings
            if not value:
                return None # set empty strings to None
        return value
    
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

    @model_validator(mode='after')
    def validate_fields(cls, values):
        # Get all query fields that are not None
        query_fields = {
            key: value for key, value in values
            if key not in BaseQueryParams.model_fields.keys() and value is not None
        }

        if not query_fields:
            raise ValueError('At least one query field is required')
        return values

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
