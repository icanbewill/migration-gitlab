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
        print(f"Nettoyage du dépôt local : {repo_dir}")
        if os.path.exists(repo_dir):
            try:
                shutil.rmtree(repo_dir, onerror=self.handle_remove_readonly)
            except PermissionError as e:
                print(f"Erreur de permission lors de la suppression du répertoire {repo_dir}: {e}")
            except Exception as e:
                print(f"Erreur lors de la suppression du répertoire {repo_dir}: {e}")

    def migrate_repo(self, gitlab_project, ignored_projects):
        """Clone un dépôt GitLab et le pousse vers GitHub."""
        repo_name = gitlab_project["path"]
        gitlab_repo_url = gitlab_project["http_url_to_repo"]
        github_repo_url = f"https://github.com/{self.github_username}/{repo_name}.git"

        repo_dir = os.path.join(self.temp_dir, repo_name)
        os.makedirs(self.temp_dir, exist_ok=True)

        if repo_name in ignored_projects:
            print(f"Le dépôt '{repo_name}' est ignoré. Aucune action n'est effectuée.")
            return

        if os.path.exists(repo_dir):
            print(f"Le dépôt '{repo_name}' existe déjà. Mise à jour vers GitHub.")
        else:
            try:
                print(f"Clonage du dépôt GitLab : {repo_name}")
                run(["git", "clone", "--mirror", gitlab_repo_url, repo_dir], check=True)
            except Exception as e:
                print(f"Erreur lors du clonage du dépôt GitLab '{repo_name}': {e}")
                return

        try:
            print(f"Ajout du remote GitHub pour : {repo_name}")
            run(["git", "-C", repo_dir, "remote", "add", "github", github_repo_url], check=True)
            print(f"Migration vers GitHub : {repo_name}")
            run(["git", "-C", repo_dir, "push", "--mirror", "github"], check=True)
            self.migrated_projects.append(repo_name)
        except Exception as e:
            print(f"Erreur lors de la migration du projet '{repo_name}' : {e}")
        finally:
            self.delete_local_repo(repo_dir)
