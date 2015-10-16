import requests
import logging

from .pull_request import PullRequest
API_URI = 'https://api.github.com/repos/{owner}/{repo}'


_log = logging.getLogger(__name__)


class GithubFetcher:
    def __init__(self, user, password, owner, repo):
        self.auth = user, password
        self.uri = API_URI.format(owner=owner, repo=repo) + self.endpoint

    @property
    def endpoint(self):
        """Endpoint to visit in the API."""
        raise NotImplementedError

    def fetch(self):
        """Method to fetch the API endpoint."""
        return requests.get(self.uri, auth=self.auth).json()


class PullRequestFetcher(GithubFetcher):
    endpoint = '/pulls'

    def _fetch_recursive(self, page, raw_prs=[]):
        params = {
            'state': 'all',
            'page': page,
            'direction': 'asc'
        }

        response = requests.get(
            self.uri, params=params, auth=self.auth
        )

        if response.status_code == 401:
            raise ValueError('Wrong password')

        raw = response.json()

        # Until no content is returned, get more PRs
        if raw:
            for item in raw:
                raw_prs.append(item)

            _log.info('Got {} pull requests'.format(len(raw_prs)))
            return self._fetch_recursive(page=page+1, raw_prs=raw_prs)
        else:
            return raw_prs

    def fetch(self):
        raw_prs = self._fetch_recursive(1)
        pull_requests = []
        for pr in raw_prs:
            pull_requests.append(PullRequest(pr))

        return pull_requests


class TagFetcher(GithubFetcher):
    endpoint = '/git/refs/tags'
