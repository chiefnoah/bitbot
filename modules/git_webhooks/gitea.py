from src import ModuleManager, utils
from . import colors

EVENT_CATEGORIES = {
    "ping": [
        "ping" # new webhook received
    ],
    "code": ["push"],
    "pr-minimal": [
        "pull_request/opened", "pull_request/closed", "pull_request/reopened"
    ],
    "pr": [
        "pull_request/opened", "pull_request/closed", "pull_request/reopened",
        "pull_request/edited", "pull_request/assigned",
        "pull_request/unassigned"
    ],
    "pr-all": ["pull_request"],
    "issue-minimal": [
        "issues/opened", "issues/closed", "issues/reopened", "issues/deleted"
    ],
    "issue": [
        "issues/opened", "issues/closed", "issues/reopened", "issues/deleted",
        "issues/edited", "issues/assigned", "issues/unassigned", "issue_comment"
    ],
    "issue-all": [
        "issues", "issue_comment"
    ],
    "issue-comment-minimal": [
        "issue_comment/created", "issue_comment/deleted"
    ],
    "repo": [
        "create", # a repository, branch or tag has been created
        "delete", # same as above but deleted
        "release",
        "fork",
        "repository"
    ]
}

COMMENT_ACTIONS = {
    "created": "commented",
    "edited":  "edited a comment",
    "deleted": "deleted a comment"
}


class Gitea(object):
    def names(self, data, headers):
        full_name = None
        repo_username = None
        repo_name = None
        if "repository" in data:
            full_name = data["repository"]["full_name"]
            repo_username, repo_name = full_name.split("/", 1)

        organisation = None
        if "organization" in data:
            organisation = data["organization"]["login"]
        return full_name, repo_username, repo_name, organisation

    def branch(self, data, headers):
        if "ref" in data:
            return data["ref"].rpartition("/")[2]
        return None

    def event(self, data, headers):
        event = headers["X-Gitea-Event"]
        event_action = None
        if "action" in data:
            event_action = "%s/%s" % (event, data["action"])
        return event, event_action

    def event_categories(self, event):
        return EVENT_CATEGORIES.get(event, [event])

    def webhook(self, full_name, event, data, headers):
        if event == "push":
            return self.push(full_name, data)
        elif event == "pull_request":
            return self.pull_request(full_name, data)
        elif event == "pull_request_comment":
            return self.pull_request_comment(full_name, data)
        elif event == "issues":
            return self.issues(full_name, data)
        elif event == "issue_comment":
            return self.issue_comment(full_name, data)
        elif event == "create":
            return self.create(full_name, data)
        elif event == "delete":
            return self.delete(full_name, data)
        elif event == "repository":
            return self.repository(full_name, data)
        elif event == "release":
            return self.release(full_name, data)
        elif event == "fork":
            return self.fork(full_name, data)
        elif event == "ping":
            return self.ping(data)
    def _short_url(self, url):
        try:
            page = utils.http.request("https://git.io", method="POST",
                post_data={"url": url})
            return page.headers["Location"]
        except utils.http.HTTPTimeoutException:
            self.log.warn(
                "HTTPTimeoutException while waiting for github short URL", [])
            return url

    def _iso8601(self, s):
        return datetime.datetime.strptime(s, utils.ISO8601_PARSE)

    def ping(self, data):
        return ["Received new webhook"]

    def _change_count(self, n, symbol, color):
        return utils.irc.color("%s%d" % (symbol, n), color)+utils.irc.bold("")
    def _added(self, n):
        return self._change_count(n, "+", colors.COLOR_POSITIVE)
    def _removed(self, n):
        return self._change_count(n, "-", colors.COLOR_NEGATIVE)
    def _modified(self, n):
        return self._change_count(n, "~", utils.consts.PURPLE)

    def _short_hash(self, hash):
        return hash[:8]

    def _flat_unique(self, commits, key):
        return set(itertools.chain(*(commit[key] for commit in commits)))

    def push(self, full_name, data):
        outputs = []
        branch = data["ref"].split("/", 2)[2]
        branch = utils.irc.color(branch, colors.COLOR_BRANCH)
        author = utils.irc.bold(data["pusher"]["login"])

        if len(data["commits"]) <= 3:
            for commit in data["commits"]:
                hash = commit["id"]
                hash_colored = utils.irc.color(self._short_hash(hash), colors.COLOR_ID)
                message = commit["message"].split("\n")[0].strip()
                url = commit["url"]

                outputs.append(
                    "%s %spushed %s to %s: %s - %s"
                    % (author, forced, hash_colored, branch, message, url))
        else:
            first_id = data["before"]
            last_id = data["commits"][-1]["id"]
            url = data["compare_url"]

            outputs.append("%s %spushed %d commits to %s - %s"
                % (author, forced, len(data["commits"]), branch, url))

        return outputs

    def pull_request(self, full_name, data):
        number = utils.irc.color("#%s" % data["pull_request"]["number"],
            colors.COLOR_ID)
        action = data["action"]
        action_desc = "%s %s" % (action, number)
        branch = data["pull_request"]["base"]["ref"]
        colored_branch = utils.irc.color(branch, colors.COLOR_BRANCH)

        if action == "opened":
            action_desc = "requested %s merge into %s" % (number,
                colored_branch)
        elif action == "closed":
            if data["pull_request"]["merged"]:
                action_desc = "%s %s into %s" % (
                    utils.irc.color("merged", colors.COLOR_POSITIVE), number,
                    colored_branch)
            else:
                action_desc = "%s %s" % (
                    utils.irc.color("closed", colors.COLOR_NEGATIVE), number)
        elif action == "ready_for_review":
            action_desc = "marked %s ready for review" % number
        elif action == "synchronize":
            action_desc = "committed to %s" % number

        pr_title = data["pull_request"]["title"]
        author = utils.irc.bold(data["sender"]["login"])
        url = self._short_url(data["pull_request"]["html_url"])
        return ["[PR] %s %s: %s - %s" % (
            author, action_desc, pr_title, url)]


    def issues(self, full_name, data):
        number = utils.irc.color("#%s" % data["issue"]["number"],
            colors.COLOR_ID)
        action = data["action"]
        issue_title = data["issue"]["title"]
        author = utils.irc.bold(data["sender"]["login"])
        url = "%s/issues/%d" % (data["repository"]["html_url"],
            data["issue"]["number"])

        return ["[issue] %s %s %s: %s - %s" %
            (author, action, number, issue_title, url)]
    def issue_comment(self, full_name, data):
        if "changes" in data:
            # don't show this event when nothing has actually changed
            if data["changes"]["body"]["from"] == data["comment"]["body"]:
                return

        number = utils.irc.color("#%s" % data["issue"]["number"], colors.COLOR_ID)
        action = data["action"]
        issue_title = data["issue"]["title"]
        type = "PR" if data["issue"]["pull_request"] else "issue"
        commenter = utils.irc.bold(data["sender"]["login"])
        url = self._short_url(data["comment"]["html_url"])
        return ["[%s] %s %s on %s: %s - %s" %
            (type, commenter, COMMENT_ACTIONS[action], number, issue_title,
            url)]

    def create(self, full_name, data):
        ref = data["ref"]
        ref_color = utils.irc.color(ref, colors.COLOR_BRANCH)
        type = data["ref_type"]
        sender = utils.irc.bold(data["sender"]["login"])
        url = self._short_url(CREATE_URL % (full_name, ref))
        return ["%s created a %s: %s - %s" % (sender, type, ref_color, url)]

    def delete(self, full_name, data):
        ref = data["ref"]
        ref_color = utils.irc.color(ref, colors.COLOR_BRANCH)
        type = data["ref_type"]
        sender = utils.irc.bold(data["sender"]["login"])
        return ["%s deleted a %s: %s" % (sender, type, ref_color)]

    def repository(self, full_name, data):
        return []

    def release(self, full_name, data):
        action = data["action"]
        tag = data["release"]["tag_name"]
        name = data["release"]["name"] or ""
        if name:
            name = ": %s" % name
        author = utils.irc.bold(data["release"]["author"]["login"])
        return ["%s %s a release%s" % (author, action, name)]

    def fork(self, full_name, data):
        forker = utils.irc.bold(data["sender"]["login"])
        fork_full_name = utils.irc.color(data["repository"]["full_name"],
            utils.consts.LIGHTBLUE)
        url = self._short_url(data["repository"]["html_url"])
        return ["%s forked into %s - %s" %
            (forker, fork_full_name, url)]
