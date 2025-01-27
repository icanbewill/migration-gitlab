# Migration de projets GitLab vers GitHub

## Configuration

### Variables de Configuration

Le script utilise les variables suivantes pour fonctionner :

- **GITLAB_TOKEN** : Le token d'accès GitLab (Personal Access Token).
- **GITHUB_TOKEN** : Le token d'accès GitHub (Personal Access Token).
- **GITLAB_USERNAME** : Votre nom d'utilisateur ou groupe GitLab.
- **GITHUB_USERNAME** : Votre nom d'utilisateur GitHub.
- **GITLAB_API_URL** *(optionnel)* : L'URL de l'API de votre serveur GitLab (par défaut `https://gitlab.com/api/v4`).

### Répertoire Temporaire

Le script crée un répertoire temporaire `./temp_repos` pour cloner les projets avant de les pousser vers GitHub. Assurez-vous que ce répertoire existe et que vous avez les droits d'écriture. Le script nettoie ce répertoire après la migration des projets.

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

## Fonctionnement du Script

### 1. Récupération des projets GitLab
Le script utilise l'API GitLab pour obtenir la liste des projets auxquels vous avez accès. Il récupère uniquement les projets où vous êtes membre ou propriétaire. La pagination est gérée automatiquement pour s'assurer que tous les projets sont inclus.

### 2. Filtrage des projets à migrer
- Si une liste de projets est spécifiée avec l'option `--projects`, seuls ces projets sont pris en compte.
- Si une liste de projets à ignorer est spécifiée avec l'option `--ignore`, ces projets sont complètement exclus du processus.

### 3. Création des dépôts GitHub
Pour chaque projet GitLab sélectionné, le script tente de créer un dépôt privé sur GitHub avec le même nom. Si le dépôt existe déjà sur GitHub, il passe à l'étape suivante sans erreur.

### 4. Migration des dépôts
- **Clonage** : Le dépôt GitLab est cloné localement en mode "mirror" dans le répertoire temporaire `./temp_repos`. Si le dépôt a déjà été cloné, cette étape est ignorée.
- **Ajout du remote GitHub** : Un remote GitHub nommé `github` est ajouté au dépôt local.
- **Push vers GitHub** : Le contenu du dépôt est poussé intégralement (branches, tags, etc.) vers GitHub.

### 5. Nettoyage
Une fois la migration d'un projet terminée, le script supprime le répertoire temporaire utilisé pour cloner le dépôt. Si le répertoire ne peut pas être supprimé (par exemple, en raison d'un problème de permission), un message d'erreur est affiché, mais l'exécution continue.

### 6. Liste des projets migrés
À la fin du script, une liste des projets migrés avec succès est affichée dans la console.

---

**Nom** : [Wilfrand ATCHI] 
**Description** : Ce script a été développé pour simplifier la migration des projets hébergés sur une instance GitLab personnalisée vers GitHub. Vous êtes libre de l'utiliser, de le modifier et de le partager avec d'autres.