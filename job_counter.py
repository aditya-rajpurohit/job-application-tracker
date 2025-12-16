from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, List, Set

from gmail_service import list_all_messages, get_message_metadata


def build_job_query(
    days_back: int | None = 365,
    start_date: str | None = None,
) -> str:
    """
    Build a Gmail search query string to roughly match job application emails.

    - If `start_date` is provided, it must be a string like "YYYY/MM/DD" or "YYYY-MM-DD"
      and will be used directly.
    - Otherwise, `days_back` is used to compute the starting date.
    """
    if start_date:
        after_str = start_date  # assume user passes valid format
    else:
        if days_back is None:
            raise ValueError("Either days_back or start_date must be provided.")
        since_date = datetime.now() - timedelta(days=days_back)
        after_str = since_date.strftime("%Y/%m/%d")

    # You can tweak these keywords and filters based on what your emails look like.
    query_parts: List[str] = [
        f"after:{after_str}",
        '("your application" OR "thanks for applying" OR "application received" OR "We received your application")',
        "-category:promotions",
        "-category:social",
    ]

    # Example: if you want to add job platforms, uncomment and edit:
    # query_parts.append(
    #     "from:(indeed.com OR linkedin.com OR greenhouse.io OR workday.com OR lever.co)"
    # )

    return " ".join(query_parts)


def count_job_emails_and_threads(service: Any, query: str) -> Dict[str, int]:
    """
    Given an authorized Gmail API service and a search query,
    return a dict with:
      - total_emails: number of matching emails
      - unique_threads: approximate number of distinct job applications
    """
    messages = list_all_messages(service, query=query)
    total_emails = len(messages)

    # To approximate "unique job applications", we count unique thread IDs
    thread_ids: Set[str] = set()

    for msg in messages:
        msg_id = msg["id"]
        msg_meta = get_message_metadata(service, msg_id)
        thread_id = msg_meta.get("threadId")
        if thread_id:
            thread_ids.add(thread_id)

    result = {
        "total_emails": total_emails,
        "unique_threads": len(thread_ids),
    }
    return result
