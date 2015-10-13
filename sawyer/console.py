import argparse
import dateutil.parser
import getpass
import os
import requests
import sawyer

import changelog


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', dest='github-user', action='store')
    parser.add_argument('-t', dest='github-token', action='store')
    parser.add_argument('repo')
    parser.add_argument('previous-tag')
    parser.add_argument('current-tag')

    args = vars(parser.parse_args())

    user = args['github-user']
    token = args['github-token']
    owner, repo = args['repo'].split('/')
    previous_tag = args['previous-tag']
    current_tag = args['current-tag']

    if not token:
        token = getpass.getpass()

    pr_fetcher = changelog.github.PullRequestFetcher(user, token, owner, repo)
    tag_fetcher = changelog.github.TagFetcher(user, token, owner, repo)
    prs = pr_fetcher.fetch()
    tags = tag_fetcher.fetch()

    def correct_tag(tag):
        return tag if tag['ref'].split('/')[-1] == previous_tag else None

    tag = list(filter(None, map(correct_tag, tags)))

    try:
        url = tag[0]['object']['url']
    except IndexError:
        raise ValueError('Couldn\'t find previous tag')

    commit = requests.get(url, auth=(user, token)).json()
    previous_date = dateutil.parser.parse(commit['author']['date'])

    merged_prs_since = [pr for pr in prs
                        if (pr.merged_at and pr.merged_at > previous_date)]

    context = {
        'current_tag': current_tag,
        'previous_tag': previous_tag,
        'owner': owner,
        'repo': repo,
        'pull_requests': merged_prs_since
    }

    print(changelog.render_changelog(context))
