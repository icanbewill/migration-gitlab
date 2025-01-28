import argparse
from migrator.MigratorApp import MigratorApp
import tkinter as tk


def main():
    parser = argparse.ArgumentParser(description="Migrer des projets de GitLab vers GitHub.")
    parser.add_argument("--gui", action="store_true", help="Lancer l'interface graphique.")

    root = tk.Tk()
    app = MigratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
