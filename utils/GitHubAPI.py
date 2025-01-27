
import requests

class GitHubAPI:
    GITHUB_USER_API_URL = "https://api.github.com/user/repos"
    GITHUB_REPO_API_URL = "https://api.github.com/repos/{username}/{repo_name}"

    """Classe pour interagir avec l'API GitHub."""
    def __init__(self, token, username):
        self.token = token
        self.username = username

    def create_repo(self, repo_name, force=False):
        """Crée un dépôt sur GitHub. Supprime un dépôt existant si force=True."""
        headers = {"Authorization": f"token {self.token}"}
        data = {"name": repo_name, "private": True}

        response = requests.post(self.GITHUB_USER_API_URL, headers=headers, json=data)
        if response.status_code == 201:
            print(f"Dépôt GitHub créé : {repo_name}")
        elif response.status_code == 422 and force:
            print(f"Le dépôt GitHub '{repo_name}' existe déjà. Suppression en cours...")
            if self.delete_repo(repo_name):
                print(f"Dépôt GitHub '{repo_name}' supprimé avec succès. Création d'un nouveau dépôt...")
                self.create_repo(repo_name, force=False)  # Recréation sans boucle infinie
            else:
                print(f"Échec de la suppression du dépôt '{repo_name}'.")
        elif response.status_code == 422:
            print(f"Le dépôt GitHub '{repo_name}' existe déjà. Utilisez 'force=True' pour le recréer.")
        else:
            print(f"Erreur lors de la création du dépôt GitHub '{repo_name}': {response.json()}")

    def delete_repo(self, repo_name):
        """Supprime un dépôt GitHub existant."""
        url = self.GITHUB_REPO_API_URL.format(username=self.username, repo_name=repo_name)
        headers = {"Authorization": f"token {self.token}"}

        response = requests.delete(url, headers=headers)
        if response.status_code == 204:
            return True
        else:
            print(f"Erreur lors de la suppression du dépôt '{repo_name}': {response.json()}")
            return False