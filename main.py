from __future__ import annotations

from typing import Dict, List

from gmail_service import get_service
from job_counter import build_job_query, count_job_emails_and_threads


def main() -> None:
    # Define the 3 accounts you want to use.
    # - label: used for token_<label>.json
    # - display_name/email: just for logging (change these to your real emails)
    accounts: List[Dict[str, str]] = [
        {
            "label": "professional",
            "display_name": "Professional Account",
            "email": "heyadityarajpurohit@gmail.com",
        },
        {
            "label": "university",
            "display_name": "University Account",
            "email": "aditya.rajpurohit@sjsu.edu",
        },
        {
            "label": "personal",
            "display_name": "Personal Account",
            "email": "adi.at.internet@gmail.com",
        },
    ]

    # ---------------------------
    # Time window / date settings
    # ---------------------------

    # OPTION A: use a relative window (e.g. last 365 days)
    days_back = 500
    query = build_job_query(days_back=days_back)


    print("=" * 60)
    print("Job Application Email Counter (Gmail API)")
    print("=" * 60)
    print("\nUsing Gmail search query:")
    print(f"  {query}")
    print()

    total_emails_all = 0
    total_threads_all = 0

    for idx, account in enumerate(accounts, start=1):
        label = account["label"]
        display_name = account["display_name"]
        email = account["email"]

        print("-" * 60)
        print(f"[{idx}/3] Processing account: {display_name}")
        print(f"Label      : {label}")
        print(f"Email note : {email}")
        print("-" * 60)

        # Build/refresh service for this account
        service = get_service(account_label=label)

        print(f"[{label}] Fetching and counting job-related emails...")
        stats = count_job_emails_and_threads(service, query=query)

        print(f"[{label}] Done.")
        print(f"[{label}] Total matching emails      : {stats['total_emails']}")
        print(f"[{label}] Approx. unique job threads : {stats['unique_threads']}")
        print()

        total_emails_all += stats["total_emails"]
        total_threads_all += stats["unique_threads"]

    print("=" * 60)
    print("Combined Summary (All 3 Accounts)")
    print("=" * 60)
    print(f"Total matching emails across accounts      : {total_emails_all}")
    print(
        "Total approx. unique job threads (sum of each account): "
        f"{total_threads_all}"
    )
    print("=" * 60)
    print("Note: each account is counted separately; threads are not merged across accounts.")
    print()


if __name__ == "__main__":
    main()
