import dateutil.parser


class PullRequest:
    def __init__(self, data):
        self.number = data['number']
        self.title = data['title']
        self.url = data['url']
        self.created_at = dateutil.parser.parse(data['created_at'])
        if data['merged_at']:
            self.merged_at = dateutil.parser.parse(data['merged_at'])
        else:
            self.merged_at = None
        self.user = data['user']['login']
        self.state = data['state']
        self.raw = data

    @property
    def created_merged_delta(self):
        if self.merged_at:
            return self.merged_at - self.created_at

    def __str__(self):
        return 'Pull request #{number} by {user}'.format(
            number=self.number,
            user=self.user
        )
