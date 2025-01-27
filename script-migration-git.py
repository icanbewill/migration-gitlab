import os
import shutil
import requests
import argparse
from subprocess import run

# Configurations
GITLAB_TOKEN = ""
GITHUB_TOKEN = ""
GITLAB_NAMESPACE = ""
GITHUB_USERNAME = ""
GITLAB_API_URL = "https://gitlab2.istic.univ-rennes1.fr/api/v4"

# Chemin temporaire pour cloner les dépôts
TEMP_DIR = "./temp_repos"

# Liste pour stocker les projets migrés
migrated_projects = []

def get_gitlab_projects():
    """Récupère la liste des projets GitLab."""
    url = f"{GITLAB_API_URL}/projects"
    headers = {"PRIVATE-TOKEN": GITLAB_TOKEN}
    params = {"membership": True, "simple": True, "per_page": 100} 

    projects = []
    while url:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        projects.extend(response.json())
        url = response.links.get("next", {}).get("url") 

    return projects


def create_github_repo(repo_name):
    """Crée un dépôt sur GitHub."""
    url = "https://api.github.com/user/repos"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data = {"name": repo_name, "private": True}

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print(f"Dépôt GitHub créé : {repo_name}")
    elif response.status_code == 422:
        print(f"Le dépôt GitHub '{repo_name}' existe déjà.")
    else:
        print(f"Erreur lors de la création du dépôt GitHub '{repo_name}': {response.json()}")


def migrate_repo(gitlab_project):
    """Clone un dépôt GitLab et le pousse vers GitHub."""
    repo_name = gitlab_project["path"]
    gitlab_repo_url = gitlab_project["http_url_to_repo"]
    github_repo_url = f"https://github.com/{GITHUB_USERNAME}/{repo_name}.git"

    repo_dir = os.path.join(TEMP_DIR, repo_name)
    os.makedirs(TEMP_DIR, exist_ok=True)

    # Vérifier si le dépôt est dans la liste des projets à ignorer
    if repo_name in ignored_projects:
        print(f"Le dépôt '{repo_name}' est ignoré. Aucune action n'est effectuée.")
        return

    # Vérifier si le dépôt a déjà été cloné
    if os.path.exists(repo_dir):
        print(f"Le dépôt '{repo_name}' existe déjà dans le répertoire. On passe à la mise à jour vers GitHub.")
    else:
        try:
            # Clone du dépôt GitLab
            print(f"Clonage du dépôt GitLab : {repo_name}")
            run(["git", "clone", "--mirror", gitlab_repo_url, repo_dir], check=True)
        except Exception as e:
            print(f"Erreur lors du clonage du dépôt GitLab '{repo_name}': {e}")
            return  # Si le clonage échoue, on arrête l'exécution pour ce projet

    try:
        # Ajout du remote GitHub
        print(f"Ajout du remote GitHub pour : {repo_name}")
        run(["git", "-C", repo_dir, "remote", "add", "github", github_repo_url], check=True)

        # Poussée vers GitHub
        print(f"Migration du dépôt vers GitHub : {repo_name}")
        run(["git", "-C", repo_dir, "push", "--mirror", "github"], check=True)

        # Ajouter à la liste des projets migrés
        migrated_projects.append(repo_name)
    except Exception as e:
        print(f"Erreur lors de la migration du projet '{repo_name}' vers GitHub: {e}")
    finally:
        # Nettoyage du répertoire local
        print(f"Nettoyage du dépôt local : {repo_name}")
        if os.path.exists(repo_dir):
            try:
                shutil.rmtree(repo_dir)  # Essaye de supprimer le répertoire si nécessaire
            except PermissionError as e:
                print(f"Erreur de permission lors de la suppression du répertoire {repo_dir}: {e}")
            except Exception as e:
                print(f"Erreur lors de la suppression du répertoire {repo_dir}: {e}")


def main():
    # Configuration de l'argument parser
    parser = argparse.ArgumentParser(description="Migrer des projets de GitLab vers GitHub.")
    parser.add_argument(
        '--projects', 
        nargs='*',  # Permet de passer une liste de projets à migrer
        help="Liste des projets à migrer (par nom). Si vide, tous les projets sont migrés."
    )
    parser.add_argument(
        '--ignore', 
        nargs='*',  # Permet de passer une liste de projets à ignorer
        help="Liste des projets à ignorer (par nom). Ces projets ne seront ni clonés ni poussés sur GitHub."
    )
    args = parser.parse_args()

    # Récupérer la liste des projets GitLab
    print("Récupération des projets GitLab...")
    projects = get_gitlab_projects()

    # Si une liste de projets est donnée, filtrer les projets
    if args.projects:
        projects = [proj for proj in projects if proj["path"] in args.projects]

    # Si une liste de projets à ignorer est donnée, l'affecter à la variable 'ignored_projects'
    global ignored_projects
    ignored_projects = args.ignore if args.ignore else []

    for project in projects:
        repo_name = project["path"]
        print(f"\nTraitement du projet : {repo_name}")

        # Créer le dépôt sur GitHub
        create_github_repo(repo_name)

        # Migrer le dépôt
        migrate_repo(project)

    # Afficher la liste des projets migrés
    print("\nMigration terminée ! Voici la liste des projets migrés :")
    for project in migrated_projects:
        print(f"- {project}")


if __name__ == "__main__":
    main()