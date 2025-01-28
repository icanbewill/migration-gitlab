import tkinter as tk
from tkinter import messagebox
from tkinter import Menu
from threading import Thread
import webbrowser
from .Migrator import Migrator
from utils.RepoManager import RepoManager

class MigratorApp:
    """Interface graphique pour orchestrer la migration des projets."""
    def __init__(self, root, gitlab_api, github_api):
        self.root = root
        gitlab_api.log = self.log
        github_api.log = self.log
        
        repo_manager = RepoManager(temp_dir="./temp_repos", github_username=github_api.username)
        repo_manager.log = self.log
        self.migrator = Migrator(gitlab_api, github_api, repo_manager, self.log)

        # Configuration de la fenêtre principale
        root.title("MigratorApp - Migration GitLab vers GitHub")
        root.geometry("590x650")
        
        # Centrer la fenêtre sur l'écran
        window_width = 590
        window_height = 650

        # Récupérer la largeur et la hauteur de l'écran
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculer la position X et Y pour centrer la fenêtre
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        # Appliquer la position à la fenêtre
        self.root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

        root.resizable(False, False)
        root.configure(bg="#f0f0f0")
        root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Couleur de texte et de fond
        label_bg = "#E1EFFF"
        entry_bg = "#FFFFFF"
        button_bg = "#4CAF50"
        button_fg = "#FFFFFF"
        button_hover_bg = "#45a049"
        text_bg = "#FFFFFF"
        text_fg = "#000000"

        # Création du menu "Aide"
        menu_bar = Menu(root)
        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="GitLab Token", command=self.open_gitlab_token_url)
        help_menu.add_command(label="GitHub Token", command=self.open_github_token_url)
        menu_bar.add_cascade(label="Aide", menu=help_menu)
        root.config(menu=menu_bar)

        # Configuration des tokens
        tk.Label(root, text="GitLab Token", bg=label_bg).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.gitlab_token = tk.Entry(root, width=70, bg=entry_bg)
        self.gitlab_token.insert(0, gitlab_api.token)
        self.gitlab_token.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(root, text="GitHub Token", bg=label_bg).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.github_token = tk.Entry(root, width=70, bg=entry_bg)
        self.github_token.insert(0, github_api.token)
        self.github_token.grid(row=1, column=1, padx=10, pady=5)

        # Configuration des utilisateurs
        tk.Label(root, text="GitLab Username", bg=label_bg).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.gitlab_username = tk.Entry(root, width=70, bg=entry_bg)
        self.gitlab_username.insert(0, gitlab_api.username)
        self.gitlab_username.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(root, text="GitHub Username", bg=label_bg).grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.github_username = tk.Entry(root, width=70, bg=entry_bg)
        self.github_username.insert(0, github_api.username)
        self.github_username.grid(row=3, column=1, padx=10, pady=5)

        # Serveur GitLab
        tk.Label(root, text="GitLab API URL", bg=label_bg).grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.gitlab_api_url = tk.Entry(root, width=70, bg=entry_bg)
        self.gitlab_api_url.insert(0, "https://gitlab.istic.univ-rennes1.fr/api/v4")
        self.gitlab_api_url.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(root, text="Projets à migrer", bg=label_bg).grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.projects_to_migrate = tk.Entry(root, width=70, bg=entry_bg)
        self.projects_to_migrate.grid(row=5, column=1, padx=10, pady=5)

        tk.Label(root, text="Projets à ignorer", bg=label_bg).grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.ignored_projects = tk.Entry(root, width=70, bg=entry_bg)
        self.ignored_projects.grid(row=6, column=1, padx=10, pady=5)


        # Mode "force"
        self.force_var = tk.BooleanVar()
        self.force_check = tk.Checkbutton(root, text="Forcer la migration", variable=self.force_var, bg="#f0f0f0")
        self.force_check.grid(row=7, column=1, padx=10, pady=5, sticky="w")

        self.info = tk.LabelFrame(root, text="Informations", bg=label_bg, padx=10, pady=10)
        self.info.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky="w")
        info_text = "Séparez les projets à migrer et/ou les projets à ignorer par des espaces."
        info_label = tk.Label(self.info, text=info_text, bg=label_bg, fg="red", wraplength=500)
        info_label.pack()


        # Boutons
        tk.Button(root, text="Lancer la migration", command=self.start_migration_thread, bg=button_bg, fg=button_fg, relief="flat", activebackground=button_hover_bg).grid(row=9, column=0, padx=10, pady=10)
        tk.Button(root, text="Voir les projets migrés", command=self.show_migrated_projects, bg=button_bg, fg=button_fg, relief="flat", activebackground=button_hover_bg).grid(row=9, column=1, padx=10, pady=10)

        # Logs
        tk.Label(root, text="Logs :", bg=label_bg).grid(row=10, column=0, padx=10, pady=5, sticky="nw")
        self.log_text = tk.Text(root, height=12, width=70, bg=text_bg, fg=text_fg, state=tk.DISABLED) 
        self.log_text.grid(row=10, column=0, columnspan=2, padx=10, pady=5)

    def start_migration_thread(self):
        """Lance la migration dans un thread séparé pour ne pas bloquer l'UI."""
        # Démarrer la migration dans un thread
        thread = Thread(target=self.start_migration)
        thread.start()

    def start_migration(self):
        """Lance la migration et met à jour l'UI avec les logs."""
        try:
            self.log("Démarrage de la migration...")
            projects_to_migrate = self.projects_to_migrate.get().split()
            
            ignored_projects = self.ignored_projects.get().split()
            force = self.force_var.get()

            # Mise à jour des tokens et configurations
            self.migrator.gitlab_api.token = self.gitlab_token.get()
            self.migrator.github_api.token = self.github_token.get()
            self.migrator.gitlab_api.username = self.gitlab_username.get()
            self.migrator.github_api.username = self.github_username.get()

            # Lancer la migration
            self.migrator.run(projects_to_migrate, ignored_projects, force)
            self.log("Migration terminée avec succès.")
        except Exception as e:
            self.log(f"Erreur : {e}")
            messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")

    def show_migrated_projects(self):
        """Affiche les projets migrés."""
        migrated_projects = self.migrator.repo_manager.migrated_projects
        if migrated_projects:
            # Trier les projets par timestamp
            sorted_projects = sorted(migrated_projects, key=lambda x: x[1], reverse=True)
            
            # Format de chaque projet migré avec son timestamp
            project_list = [f"{project} - Migré à {timestamp}" for project, timestamp in sorted_projects]
            
            # Affichage des projets migrés dans une boîte de dialogue
            messagebox.showinfo("Projets migrés", "\n".join(project_list))
        else:
            messagebox.showinfo("Projets migrés", "Aucun projet migré.")

    def log(self, message):
        """Ajoute un message dans la section des logs."""
        # Rendre temporairement activé pour insérer le texte
        self.log_text.config(state=tk.NORMAL)  
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        # Revenir à l'état désactivé après avoir inséré le texte
        self.log_text.config(state=tk.DISABLED)

    def open_gitlab_token_url(self):
        """Ouvre la page GitLab pour générer un token d'accès."""
        url = "https://gitlab.com/-/profile/personal_access_tokens"
        webbrowser.open(url)

    def open_github_token_url(self):
        """Ouvre la page GitHub pour générer un token d'accès."""
        url = "https://github.com/settings/tokens"
        webbrowser.open(url)

    def on_close(self):
        """Méthode pour demander une confirmation avant de fermer l'application."""
        # Boîte de dialogue pour confirmer la fermeture
        result = messagebox.askquestion("Confirmer la fermeture", 
                                        "Êtes-vous sûr de vouloir fermer l'application ?\nLes migrations en cours seront arrêtées.")
        if result == "yes":
            self.root.destroy()
        else:
            pass