import ast
from datetime import datetime, timezone
import json
from typing import List, Optional
from sqlmodel import SQLModel, and_, or_
from sqlmodel.sql.expression import Select, SelectOfScalar

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
        parsed_terms = ast.literal_eval(columnFilters)  # list tuple parse
        columnFilters = [tuple(sublist) for sublist in parsed_terms]
        for col, value in columnFilters:
            if isinstance(value, str):
                filters.append(getattr(Model, col).ilike(f"%{value}%"))
            else:
                filters.append(getattr(Model, col) == value)
        statement = statement.where(and_(*filters))

    # Number range
    if numberRange:
        # number_range should be like ("amount", "0", "100000")
        parsed = tuple(json.loads(numberRange))
        column_name = parsed[0]  # column name
        min_val = parsed[1]  # min value
        max_val = parsed[2]  # max value

        # Ensure numeric types
        try:
            min_val = float(min_val)
            max_val = float(max_val)
        except ValueError:
            raise ValueError("numberRange must contain numeric values")

        column = getattr(Model, column_name)
        statement = statement.where(column.between(min_val, max_val))

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
