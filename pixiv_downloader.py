#!/usr/bin/env python3
"""
Pixiv App Downloader
Downloads artwork from Pixiv using the Pixiv API via pixivpy3.

Usage:
    python pixiv_downloader.py --refresh-token <token> --illust-id <id>
    python pixiv_downloader.py --refresh-token <token> --user-id <id>
    python pixiv_downloader.py --refresh-token <token> --ranking
"""

import argparse
import os
import sys

from pixivpy3 import AppPixivAPI


def login(refresh_token: str) -> AppPixivAPI:
    """Authenticate with the Pixiv API using a refresh token."""
    api = AppPixivAPI()
    try:
        api.auth(refresh_token=refresh_token)
    except Exception as exc:
        print(f"Authentication failed: {exc}", file=sys.stderr)
        sys.exit(1)
    return api


def download_illust(api: AppPixivAPI, illust_id: int, output_dir: str) -> None:
    """Download a single illustration by its ID."""
    detail = api.illust_detail(illust_id)
    if detail.get("error"):
        print(f"Error fetching illust {illust_id}: {detail['error']['message']}", file=sys.stderr)
        return

    illust = detail["illust"]
    _download_illust_pages(api, illust, output_dir)


def _download_illust_pages(api: AppPixivAPI, illust: dict, output_dir: str) -> None:
    """Download all pages of an illustration."""
    os.makedirs(output_dir, exist_ok=True)
    title = illust.get("title", str(illust["id"]))

    if illust["page_count"] == 1:
        url = illust["meta_single_page"]["original_image_url"]
        filename = os.path.basename(url)
        dest = os.path.join(output_dir, filename)
        print(f"Downloading: {title} -> {dest}")
        api.download(url, path=output_dir, name=filename)
    else:
        for page in illust["meta_pages"]:
            url = page["image_urls"]["original"]
            filename = os.path.basename(url)
            dest = os.path.join(output_dir, filename)
            print(f"Downloading: {title} (page) -> {dest}")
            api.download(url, path=output_dir, name=filename)


def download_user_illusts(api: AppPixivAPI, user_id: int, output_dir: str) -> None:
    """Download all illustrations by a user."""
    print(f"Fetching illustrations for user {user_id}...")
    result = api.user_illusts(user_id)

    while True:
        if result.get("error"):
            print(f"Error: {result['error']['message']}", file=sys.stderr)
            break

        for illust in result.get("illusts", []):
            _download_illust_pages(api, illust, output_dir)

        next_url = result.get("next_url")
        if not next_url:
            break
        result = api.no_auth_requests_handler(next_url)


def download_ranking(api: AppPixivAPI, mode: str, output_dir: str, limit: int) -> None:
    """Download top-ranking illustrations."""
    print(f"Fetching ranking ({mode})...")
    result = api.illust_ranking(mode=mode)
    count = 0

    while count < limit:
        if result.get("error"):
            print(f"Error: {result['error']['message']}", file=sys.stderr)
            break

        for illust in result.get("illusts", []):
            if count >= limit:
                break
            _download_illust_pages(api, illust, output_dir)
            count += 1

        next_url = result.get("next_url")
        if not next_url or count >= limit:
            break
        result = api.no_auth_requests_handler(next_url)

    print(f"Downloaded {count} illustrations from ranking.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download artwork from Pixiv",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--refresh-token",
        required=True,
        help="Pixiv refresh token for authentication",
    )
    parser.add_argument(
        "--output-dir",
        default="downloads",
        help="Directory to save downloaded files (default: downloads)",
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--illust-id",
        type=int,
        metavar="ID",
        help="Download a single illustration by ID",
    )
    group.add_argument(
        "--user-id",
        type=int,
        metavar="ID",
        help="Download all illustrations by a user",
    )
    group.add_argument(
        "--ranking",
        action="store_true",
        help="Download top-ranking illustrations",
    )

    parser.add_argument(
        "--ranking-mode",
        default="day",
        choices=["day", "week", "month", "day_male", "day_female", "week_original", "week_rookie"],
        help="Ranking mode (default: day)",
    )
    parser.add_argument(
        "--ranking-limit",
        type=int,
        default=30,
        metavar="N",
        help="Maximum number of ranking illustrations to download (default: 30)",
    )

    args = parser.parse_args()

    api = login(args.refresh_token)

    if args.illust_id:
        download_illust(api, args.illust_id, args.output_dir)
    elif args.user_id:
        download_user_illusts(api, args.user_id, args.output_dir)
    elif args.ranking:
        download_ranking(api, args.ranking_mode, args.output_dir, args.ranking_limit)


if __name__ == "__main__":
    main()
