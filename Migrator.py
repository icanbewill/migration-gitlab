import argparse
from subprocess import run
from utils.GitLabAPI import GitLabAPI
from utils.GitHubAPI import GitHubAPI
from utils.RepoManager import RepoManager
import time


# Configurations
GITLAB_TOKEN = "glpat--jxgve_mDs3W_k9-aNxb"
GITHUB_TOKEN = "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"
GITHUB_USERNAME = "icanbewill"
GITLAB_USERNAME = "watchi"

class Migrator:
    """Classe principale pour orchestrer la migration."""
    def __init__(self, gitlab_api, github_api, repo_manager):
        self.gitlab_api = gitlab_api
        self.github_api = github_api
        self.repo_manager = repo_manager

    def run(self, projects_to_migrate=None, ignored_projects=None, force=False):
        print("Récupération des projets GitLab...")
        projects = self.gitlab_api.get_projects()

        if projects_to_migrate:
            projects = [proj for proj in projects if proj["path"] in projects_to_migrate]

        ignored_projects = ignored_projects or []

        print(f"Nombre total de projets à migrer : {len(projects)}")
    
        # Décompte de 5 secondes
        print("Démarrage de la migration dans :")
        for i in range(5, 0, -1):
            print(f"{i}...", end="\r", flush=True)
            time.sleep(1)
        print("Migration en cours...\n")

        for project in projects:
            repo_name = project["path"]
            print(f"\nTraitement du projet : {repo_name}")
            self.github_api.create_repo(repo_name, force)
            self.repo_manager.migrate_repo(project, ignored_projects)

        print("\nMigration terminée ! Projets migrés :")
        for project in self.repo_manager.migrated_projects:
            print(f"- {project}")


def main():
    # Argument parser
    parser = argparse.ArgumentParser(description="Migrer des projets de GitLab vers GitHub.")
    parser.add_argument(
        '--projects', 
        nargs='*',
        help="Liste des projets à migrer (par nom). Si vide, tous les projets sont migrés."
    )
    parser.add_argument(
        '--ignore', 
        nargs='*',
        help="Liste des projets à ignorer (par nom)."
    )
    parser.add_argument(
        '-f', '--force', 
        action='store_true',
        help="Force la suppression des dépôts existants sur GitHub avant de les recréer."
    )
    args = parser.parse_args()

    # Configuration
    gitlab_api = GitLabAPI(token=GITLAB_TOKEN, username=GITLAB_USERNAME)
    github_api = GitHubAPI(token=GITHUB_TOKEN, username=GITHUB_USERNAME)
    repo_manager = RepoManager(temp_dir="./temp_repos", github_username=GITHUB_USERNAME)

    # Exécution
    migrator = Migrator(gitlab_api, github_api, repo_manager)
    migrator.run(projects_to_migrate=args.projects, ignored_projects=args.ignore, force=args.force)


if __name__ == "__main__":
    main()