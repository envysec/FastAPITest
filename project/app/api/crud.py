"""
Contains functions related to database interactions

project/app/api/crud.py
"""
from typing import List, Dict, Union

from app.models.pydantic import SummaryPayloadSchema
from app.models.tortoise import TextSummary

async def post(payload: SummaryPayloadSchema) -> int:
  summary = TextSummary(
    url=payload.url,
    summary='dummy summary',
  )
  await summary.save()
  return summary.id


async def get(id: int) -> Union[Dict, None]: # pylint: disable=redefined-builtin,unsubscriptable-object
  summary = await TextSummary.filter(id=id).first().values()
  if summary:
    return summary[0]
  return None


async def get_all() -> List:
  summaries = await TextSummary.all().values()
  return summaries
