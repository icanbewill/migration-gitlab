import requests
from subprocess import run


class GitLabAPI:
    
    GITLAB_API_URL = "https://gitlab.istic.univ-rennes1.fr/api/v4"

    """Classe pour interagir avec l'API GitLab."""
    def __init__(self, token, username):
        self.token = token
        self.username = username
        self.api_url = self.GITLAB_API_URL

    def get_projects(self):
        """Récupère la liste des projets GitLab."""
        url = f"{self.api_url}/projects"
        headers = {"PRIVATE-TOKEN": self.token}
        params = {"membership": True, "simple": True, "per_page": 100}

        projects = []
        while url:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            projects.extend(response.json())
            url = response.links.get("next", {}).get("url")

        return projects