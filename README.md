# Migration de projets GitLab vers GitHub

## Introduction

Ce projet vise à simplifier la migration des projets hébergés sur une instance GitLab personnalisée vers GitHub. Il fournit un script Python facile à utiliser, extensible et personnalisable. Vous êtes invité à utiliser, modifier, et contribuer à ce projet !

---

## Configuration

### Variables de Configuration

Le script utilise les variables suivantes pour fonctionner (dans le fichier `Migrator.py`) :

- **GITLAB_TOKEN** : Le token d'accès GitLab (Personal Access Token).
- **GITHUB_TOKEN** : Le token d'accès GitHub (Personal Access Token).
- **GITLAB_USERNAME** : Votre nom d'utilisateur ou groupe GitLab.
- **GITHUB_USERNAME** : Votre nom d'utilisateur GitHub.
- **GITLAB_API_URL** *(optionnel)* : L'URL de l'API de votre serveur GitLab (par défaut `https://gitlab2.istic.univ-rennes1.fr/api/v4`).

---

## Utilisation

```bash
python main.py
```

## Description des Classes

- **`MigratorApp`**  
  Gère l'interface graphique de l'application. Permet aux utilisateurs de :
  - Configurer et lancer les migrations.
  - Visualiser les logs.
  - Accéder aux options d'aide et de documentation.

- **`Migrator`**  
  Contient la logique principale de migration.  
  - Orchestre les communications entre GitLab et GitHub.  
  - Gère les options comme les projets spécifiques, les exclusions, et le mode forcé.  
  - Enregistre les états des projets migrés.

- **`RepoManager`**  
  Gère les dépôts locaux.  
  - Clonage, migration, et suppression des dépôts.  
  - Offre des abstractions pour manipuler les dépôts durant le processus de migration.

- **`GitLabAPI`**  
  Fournit des méthodes pour interagir avec l'API de GitLab.  
  - Exemple : Récupération des projets ou de leurs informations.

- **`GitHubAPI`**  
  Fournit des méthodes pour interagir avec l'API de GitHub.  
  - Exemple : Vérification de l'existence des dépôts ou création de nouveaux dépôts.

---

**Nom** : [Wilfrand ATCHI] 
**Description** : Ce script a été développé pour simplifier la migration des projets hébergés sur une instance GitLab personnalisée vers GitHub. Vous êtes libre de l'utiliser, de le modifier et de le partager avec d'autres.