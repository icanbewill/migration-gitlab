import os
import shutil
from subprocess import run
import stat

class RepoManager:
    """Classe pour gérer la migration et la suppression des dépôts."""
    def __init__(self, temp_dir, github_username):
        self.temp_dir = temp_dir
        self.github_username = github_username
        self.migrated_projects = []

    @staticmethod
    def handle_remove_readonly(func, path, exc):
        """Supprime l'attribut de lecture seule et réessaie."""
        os.chmod(path, stat.S_IWRITE)
        func(path)

    def delete_local_repo(self, repo_dir):
        """Supprime le dépôt local."""
        self.log(f"Nettoyage du dépôt local : {repo_dir}")
        if os.path.exists(repo_dir):
            try:
                shutil.rmtree(repo_dir, onerror=self.handle_remove_readonly)
            except PermissionError as e:
                self.log(f"Erreur de permission lors de la suppression du répertoire {repo_dir}: {e}")
            except Exception as e:
                self.log(f"Erreur lors de la suppression du répertoire {repo_dir}: {e}")

    def migrate_repo(self, gitlab_project, force, github_api):
        repo_name = gitlab_project["path"]
        gitlab_repo_url = gitlab_project["http_url_to_repo"]
        github_repo_url = f"https://github.com/{self.github_username}/{repo_name}.git"
        repo_dir = os.path.join(self.temp_dir, repo_name)

        os.makedirs(self.temp_dir, exist_ok=True)

        # pas besoin de push si le projet pas force
        if not force and github_api.repo_exists(repo_name):
            return

        if os.path.exists(repo_dir):
            self.delete_local_repo(repo_dir)

        try:
            self.log(f"Clonage du dépôt GitLab : {repo_name}")
            run(["git", "clone", "--mirror", gitlab_repo_url, repo_dir], check=True)

            self.log(f"Migration vers GitHub : {repo_name}")
            run(["git", "-C", repo_dir, "remote", "add", "github", github_repo_url], check=True)
            run(["git", "-C", repo_dir, "push", "--mirror", "github"], check=True)

            self.migrated_projects.append(repo_name)
        except Exception as e:
            self.log(f"Erreur lors de la migration du dépôt '{repo_name}' : {e}")
        finally:
            self.delete_local_repo(repo_dir)
