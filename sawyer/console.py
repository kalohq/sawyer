import argparse
import dateutil.parser
import datetime
import getpass
import os
import pytz
import requests
import sawyer
import logging

from .changelog import render_changelog
from .github import PullRequestFetcher, TagFetcher


def configure_logging(quiet):
    log_level = logging.ERROR if quiet else logging.INFO
    logging.basicConfig(
        format='%(message)s', level=log_level
    )
    logging.getLogger("requests").setLevel(logging.WARNING)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', dest='github-user', action='store')
    parser.add_argument('-t', dest='github-token', action='store')
    parser.add_argument('-q', dest='quiet', action='store_true', default=False)
    parser.add_argument('--all-prs', dest='all-prs', action='store_const',
                        const=True, default=False)
    parser.add_argument('repo')
    parser.add_argument('previous-tag')
    parser.add_argument('current-tag')

    args = vars(parser.parse_args())

    user = args['github-user']
    token = args['github-token']
    all_prs = args['all-prs']
    owner, repo = args['repo'].split('/')
    previous_tag = args['previous-tag']
    current_tag = args['current-tag']
    quiet = args['quiet']

    configure_logging(quiet)

    if not token:
        token = getpass.getpass()

    pr_fetcher = PullRequestFetcher(user, token, owner, repo)
    tag_fetcher = TagFetcher(user, token, owner, repo)
    prs = pr_fetcher.fetch()
    tags = tag_fetcher.fetch()

    def correct_tag(tag):
        return tag if tag['ref'].split('/')[-1] == previous_tag else None

    tag = list(filter(None, map(correct_tag, tags)))

    try:
        url = tag[0]['object']['url']
    except IndexError:
        raise ValueError('Couldn\'t find previous tag. '
                         'Did you use a version prefix?')

    commit = requests.get(url, auth=(user, token)).json()

    if all_prs:
        previous_date = pytz.utc.localize(datetime.datetime.fromtimestamp(0))
    else:
        field = 'author' if 'author' in commit else 'tagger'
        previous_date = dateutil.parser.parse(commit[field]['date'])

    merged_prs_since = sorted(
        [pr for pr in prs if (pr.merged_at and pr.merged_at > previous_date)],
        key=lambda pr: pr.merged_at,
        reverse=True
    )

    context = {
        'current_tag': current_tag,
        'previous_tag': previous_tag,
        'owner': owner,
        'repo': repo,
        'pull_requests': merged_prs_since
    }

    print(render_changelog(context))
