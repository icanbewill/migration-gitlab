import argparse
from utils.GitLabAPI import GitLabAPI
from utils.GitHubAPI import GitHubAPI
from utils.RepoManager import RepoManager
from migrator.MigratorApp import MigratorApp
from migrator.Migrator import Migrator
import tkinter as tk


def main():
    parser = argparse.ArgumentParser(description="Migrer des projets de GitLab vers GitHub.")
    parser.add_argument("--gui", action="store_true", help="Lancer l'interface graphique.")
    args = parser.parse_args()

    gitlab_api = GitLabAPI(token="glpat-G_noC3ZEC6byrahdAtWK", username="watchi")
    github_api = GitHubAPI(token="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", username="icanbewill")

    # if args.gui:
    root = tk.Tk()
    app = MigratorApp(root, gitlab_api, github_api)
    root.mainloop()
    # else:
    #     migrator = Migrator(gitlab_api, github_api, repo_manager)
    #     migrator.run()


if __name__ == "__main__":
    main()
