# 🚨 IMPORTANT : Configuration du chemin du projet

## ❌ Problème rencontré

```
File not found: .\src/main/java/tn/skillswap/skillswap/Controller/...
```

Cela signifie que l'agent cherche les fichiers au mauvais endroit.

## ✅ Solution : Spécifier le bon chemin

### Option 1 : Trouver automatiquement le projet

```powershell
.\find_project.bat
```

Ce script liste les projets Java trouvés autour du dossier actuel.

### Option 2 : Spécifier manuellement le chemin

```powershell
# Trouver où est votre projet Java PaiementManagement
# Puis l'utiliser comme --repo-path

python run_agent.py run --dry-run --repo-path "C:\chemin\complet\vers\PaiementManagement"
```

### Exemples de chemins valides

```powershell
# Si le projet est à côté de sonar-ai-agent
python run_agent.py run --dry-run --repo-path "..\PaiementManagement"

# Chemin absolu
python run_agent.py run --dry-run --repo-path "C:\Users\jawhe\projects\PaiementManagement"

# OneDrive
python run_agent.py run --dry-run --repo-path "C:\Users\jawhe\.symfony5\OneDrive\Bureau\AI-Agent bootcamp\PaiementManagement"
```

## 🔍 Comment trouver le bon chemin ?

### Méthode 1 : Depuis l'explorateur Windows

1. Ouvrir l'explorateur Windows
2. Naviguer vers votre projet Java (celui qui contient `src/main/java`)
3. Cliquer dans la barre d'adresse
4. Copier le chemin complet
5. L'utiliser dans `--repo-path "..."`

### Méthode 2 : Depuis PowerShell

```powershell
# Aller dans le dossier du projet Java
cd "C:\Users\jawhe\.symfony5\OneDrive\Bureau\AI-Agent bootcamp"

# Lister les dossiers
Get-ChildItem -Directory

# Trouver celui qui contient src/main/java
Get-ChildItem -Recurse -Directory -Filter "java" | Where-Object {$_.FullName -like "*\src\main\java"}

# Obtenir le chemin complet
(Get-Item .).FullName
```

### Méthode 3 : Vérifier la structure

Le projet Java doit avoir cette structure :
```
PaiementManagement/
├── src/
│   └── main/
│       └── java/
│           └── tn/
│               └── skillswap/
│                   └── skillswap/
│                       └── Controller/
└── pom.xml
```

## ✅ Une fois le bon chemin trouvé

```powershell
# Exemple avec le chemin réel
python run_agent.py run --dry-run --repo-path "C:\Users\jawhe\.symfony5\OneDrive\Bureau\AI-Agent bootcamp\PaiementManagement"
```

## 🎯 Test rapide

Pour vérifier que le chemin est bon :

```powershell
# Remplacer "CHEMIN_PROJET" par votre chemin
$projet = "C:\chemin\vers\PaiementManagement"

# Vérifier que le dossier existe
Test-Path $projet

# Vérifier qu'il contient src/main/java
Test-Path "$projet\src\main\java"

# Si les deux retournent "True", le chemin est bon!
```

## 📊 Rapport généré même sans fichiers

**Bonne nouvelle** : Même si les fichiers ne sont pas trouvés, l'agent a quand même :
- ✅ Récupéré les issues de SonarQube (30 issues)
- ✅ Effectué le triage (7 P0, 23 P2)
- ✅ Généré `sonar_bundle.json`

Il manque juste l'analyse Gemini (qui nécessite le contexte code).

## 🔧 Relancer avec le bon chemin

Une fois le chemin trouvé :

```powershell
# Mettre à jour .env (optionnel mais recommandé)
$env:REPO_PATH = "C:\chemin\vers\PaiementManagement"

# Ou directement dans la commande
python run_agent.py run --dry-run --repo-path "C:\chemin\vers\PaiementManagement"
```

---

**Besoin d'aide ?** Lancez `.\find_project.bat` pour chercher automatiquement les projets Java.
