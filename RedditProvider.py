import praw


class RedditProvider:

    def __init__(self):
        self.r = praw.Reddit(user_agent="hatespeech-analyzer")

    def get_controversial_comments(self, thread_id, sort_by="score", reverse=True):
        """
        Returns the most controversial comments from a given thread.

        :param thread_id: Thread id
        :param sort_by: sorting value, defaults to score
        :param reverse: sorting order
        :return: list of praw.objects.Comment
        """
        submission = self.r.get_submission(submission_id=thread_id)
        flat_comments = praw.helpers.flatten_tree(submission.comments)
        flat_comments = [comment for comment in flat_comments if isinstance(comment, praw.objects.Comment)]
        flat_comments.sort(key=lambda comment: getattr(comment, sort_by), reverse=reverse)

        return flat_comments

    def get_from_subreddit(self, subreddit, sort_by="score"):
        """
        Returns comments sorted by given categorie for the 5 hottest post on the given subreddit.

        :param subreddit: name of the subreddit
        :param sort_by:
        :return: list of list of praw.objects.Comment
        """
        subreddit = self.r.get_subreddit(subreddit)
        comments = []
        for submission in subreddit.get_hot(limit=5):
            comments.append(self.get_controversial_comments(submission.id, sort_by=sort_by))

        return comments

