# Migration de projets GitLab vers GitHub

## Configuration

### Variables de Configuration

Le script utilise les variables suivantes pour fonctionner (dans le fichier Migrator.py):

- **GITLAB_TOKEN** : Le token d'accès GitLab (Personal Access Token).
- **GITHUB_TOKEN** : Le token d'accès GitHub (Personal Access Token).
- **GITLAB_USERNAME** : Votre nom d'utilisateur ou groupe GitLab.
- **GITHUB_USERNAME** : Votre nom d'utilisateur GitHub.

- **GITLAB_API_URL** *(optionnel)* : L'URL de l'API de votre serveur GitLab (par défaut `https://gitlab2.istic.univ-rennes1.fr/api/v4`).

## Utilisation

### Clonage et migration de tous les projets

Exécutez le script sans arguments pour migrer tous les projets de votre GitLab vers GitHub :

```
python Migrator.py
```
### Clonage et migration de projets spécifiques

Vous pouvez fournir une liste de projets spécifiques à migrer en utilisant l'option --projects suivie de noms de projets séparés par des espaces :

```
python Migrator.py --projects projet1 projet2 projet3
```

### Ignorer certains projets

Si vous souhaitez ignorer certains projets et ne pas les migrer (ni les cloner, ni les pousser vers GitHub), vous pouvez utiliser l'option --ignore suivie des noms de projets à ignorer :

```
python Migrator.py --ignore mmm-tp1 sbd-tp3 sir-tp10 sir-tp7 sir-tp6 sir-tp2 sir-tp1 csr-tp5 mob-tp-start csr-tp4 csr-tp3 csr-tp2 aco-tp-editeur mob-tp-network csr-tp1 mob-tp-calculator
```

### Suppression des Dépôts GitHub Existants

Si vous souhaitez **forcer la suppression d'un dépôt GitHub existant et le recréer** avant de le recréer, vous pouvez utiliser l'option `-f` ou `--force`.

---

**Nom** : [Wilfrand ATCHI] 
**Description** : Ce script a été développé pour simplifier la migration des projets hébergés sur une instance GitLab personnalisée vers GitHub. Vous êtes libre de l'utiliser, de le modifier et de le partager avec d'autres.