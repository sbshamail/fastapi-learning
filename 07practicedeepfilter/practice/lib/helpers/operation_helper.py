import ast
from datetime import datetime, timezone
import json
from typing import List, Optional
from sqlmodel import SQLModel, and_, or_
from sqlmodel.sql.expression import Select, SelectOfScalar
from sqlalchemy.orm import RelationshipProperty

from practice.lib.helpers.utility import parse_date


def filterSearchTerms(
    Model,
    searchTerm: str | None,
    searchTerms: list[str],
    statement,
):
    if not searchTerm:
        return statement  # Don't change it if no search term

    searchFilters = [
        getattr(Model, field).ilike(f"%{searchTerm}%") for field in searchTerms
    ]
    return statement.where(or_(*searchFilters))



def resolve_column(Model, col: str, statement):
    """
    Given 'product.owner.role.title', return (attr, updated_statement).
    """
    parts = col.split(".")
    current_model = Model
    attr = None

    for i, part in enumerate(parts):
        mapper_attr = getattr(current_model, part)

        if hasattr(mapper_attr, "property") and hasattr(mapper_attr.property, "mapper"):
            # It's a relationship -> join it
            related_model = mapper_attr.property.mapper.class_
            statement = statement.join(mapper_attr, isouter=True)
            current_model = related_model
        else:
            # It's a column
            attr = mapper_attr

    return attr, statement



def applyFilters(
    statement: SelectOfScalar,
    Model: type[SQLModel],
    searchTerm: Optional[str] = None,
    searchFields: Optional[List[str]] = None,
    columnFilters: Optional[List[List[str]]] = None,
    dateRange: Optional[List[str]] = None,
    numberRange: Optional[List[str]] = None,
):
    # Global search
    if searchTerm and searchFields:
        search_filters = [
            getattr(Model, col).ilike(f"%{searchTerm}%") for col in searchFields
        ]
        statement = statement.where(or_(*search_filters))

    # Column-specific search
    if columnFilters:
        filters = []
        parsed_terms = ast.literal_eval(columnFilters)
        columnFilters = [tuple(sublist) for sublist in parsed_terms]

        for col, value in columnFilters:
            parts = col.split(".")
            # if len(parts) > 1:
            #     # e.g., Product.owner.full_name
            #     rel_name, rel_col = parts[0], parts[1]
            #     rel_model = getattr(Model, rel_name).property.mapper.class_
            #     statement = statement.join(getattr(Model, rel_name))  # JOIN relation
            #     attr = getattr(rel_model, rel_col)
            current_model = Model
            attr = None
            # nested object filter
            for i, part in enumerate(parts):  #enumerate = index + value in one go
                if i < len(parts) - 1:
                    # Relation → JOIN
                    rel = getattr(current_model, part)
                    rel_model = rel.property.mapper.class_
                    statement = statement.join(rel)  # Add join
                    current_model = rel_model
                else:
                    # Last part → actual column
                    attr = getattr(current_model, part)

            if isinstance(value, str):
                filters.append(attr.ilike(f"%{value}%"))
            else:
                filters.append(attr == value)

        statement = statement.where(and_(*filters))

    return statement

    # Number range
    if numberRange:
        # number_range should be like ("amount", "0", "100000")
        parsed = tuple(json.loads(numberRange))
        column_name, *values = parsed  # first element is column name, rest are values

        # Assign safely
        min_val = float(values[0]) if len(values) >= 1 and values[0] else None
        max_val = float(values[1]) if len(values) >= 2 else None
      
        # Ensure numeric types

        column = getattr(Model, column_name)
        if min_val is not None and max_val is not None:
            statement = statement.where(column.between(min_val, max_val))
        elif min_val is not None:
            statement = statement.where(column >= min_val)
        elif max_val is not None:
            statement = statement.where(column <= max_val)

    # Date range
    if dateRange:
        dateRangeParse = json.loads(dateRange)
        dateRange = tuple(dateRangeParse)

        column_name = dateRange[0]  # e.g. "created_at"
        column = getattr(Model, column_name)  # map to SQLModel column

        start_date = parse_date(dateRange[1])
        end_date = (
            parse_date(dateRange[2])
            if len(dateRange) > 2 and dateRange[2]
            else datetime.now(timezone.utc)
        )

        # If user didn’t specify end time, set to 23:59:59
        if (
            end_date.hour == 0
            and end_date.minute == 0
            and end_date.second == 0
            and end_date.microsecond == 0
        ):
            end_date = end_date.replace(
                hour=23, minute=59, second=59, microsecond=999999
            )

        statement = statement.where(and_(column >= start_date, column <= end_date))

    return statement
