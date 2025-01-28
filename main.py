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

    gitlab_api = GitLabAPI(token="", username="")
    github_api = GitHubAPI(token="", username="")

    root = tk.Tk()
    app = MigratorApp(root, gitlab_api, github_api)
    root.mainloop()

if __name__ == "__main__":
    main()
