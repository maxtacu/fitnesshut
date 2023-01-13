from jira import JIRA

class JIRA_ticket(object):
    def __init__(self, server, token):
        # Connect to Jira
        self.jira = JIRA(server=server, token_auth=token)

    def add_attachment(self, issue, attachment):
        with open(attachment, 'rb') as file:
            self.jira.add_attachment(issue, file)
        print(f"File {attachment} attached to {issue.key}.")

    def create_ticket(self, project_key, summary, description, issuetype):
        # Create new issue
        issue_dict = {
            'project': {'key': project_key},
            'summary': summary,
            'description': description,
            'issuetype': {'name': issuetype},
        }
        new_issue = self.jira.create_issue(fields=issue_dict)
        print(f'New issue created successfully. Link: {new_issue.permalink()}')
        return new_issue

