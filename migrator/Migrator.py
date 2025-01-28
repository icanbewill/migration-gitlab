import time

class Migrator:
    """Classe principale pour orchestrer la migration des dépôts GitLab vers GitHub."""
    def __init__(self, gitlab_api, github_api, repo_manager, log):
        self.gitlab_api = gitlab_api
        self.github_api = github_api
        self.repo_manager = repo_manager
        self.log = log

    def validate_config(self):
        """Valide que les configurations nécessaires sont présentes."""
        if not self.gitlab_api.token or not self.github_api.token:
            raise ValueError("Les tokens GitLab et GitHub doivent être définis.")

    def run(self, projects_to_migrate=None, ignored_projects=None, force=False):
        """Exécute le processus de migration."""
        self.log("Validation de la configuration...")
        self.validate_config()

        # Gestion des projets ignorés
        ignored_projects = ignored_projects or []

        projects = self.gitlab_api.get_projects()
        
        # Filtrage des projets à migrer
        if projects_to_migrate:
            projects = [proj for proj in projects if proj["path"] in projects_to_migrate]

        # Vérification si des projets restent à migrer
        if not projects:
            self.log("Aucun projet à migrer après filtrage. Processus arrêté.")
            return

        self.log(f"Nombre total de projets à migrer : {len(projects)}")

        self.log("Démarrage de la migration dans :")
        for i in range(5, 0, -1):
            self.log(f"{i}...")
            time.sleep(1)

        for project in projects:
            repo_name = project["path"]

            if repo_name in ignored_projects:
                self.log(f"Projet ignoré : {repo_name}")
                continue

            self.log(f"\nTraitement du projet : {repo_name}")
            try:
                self.github_api.create_repo(repo_name, force)
                self.repo_manager.migrate_repo(project, force, self.github_api)
            except Exception as e:
                self.log(f"Erreur lors de la migration du projet {repo_name} : {e}")

        self.log("\nMigration terminée ! Projets migrés :")
        for project in self.repo_manager.migrated_projects:
            self.log(f"- {project}")
