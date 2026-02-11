# 🪟 Guide Windows - Sonar AI Agent

## 🚀 Installation Rapide

### Option 1 : Lancer directement (RECOMMANDÉ - 0 installation)

```powershell
# Depuis le dossier sonar-ai-agent
python run_agent.py run --dry-run --repo-path .
```

✅ **Avantage** : Marche immédiatement, rien à installer  
✅ **Parfait pour** : Test rapide

### Option 2 : Installer le package

```powershell
# Lancer le script d'installation
.\install.bat

# Ou manuellement
python -m pip install -e .

# Puis utiliser
python -m sonar_ai_agent.main run --dry-run
```

✅ **Avantage** : Import du module depuis n'importe où  
✅ **Parfait pour** : Utilisation régulière

### Option 3 : Utiliser PYTHONPATH

```powershell
# Une seule fois par session PowerShell
$env:PYTHONPATH = "src"

# Puis
python -m sonar_ai_agent.main run --dry-run
```

## 🎯 Test Complet Windows

### Étape 1 : Configurer .env

```powershell
# Copier le template
Copy-Item .env.example .env

# Éditer avec Notepad
notepad .env
```

Remplir avec vos vraies valeurs :
```env
SONAR_HOST_URL=http://localhost:9000
SONAR_PROJECT_KEY=votre-projet
SONAR_TOKEN=sqp_2382cf11aa4f67f4367a86669f2b2ebf0d0e19aa
GEMINI_API_KEY=votre-cle-gemini
```

### Étape 2 : Lancer le test

```powershell
# Method directe (pas d'installation nécessaire)
python run_agent.py run --dry-run --repo-path .
```

### Étape 3 : Voir les résultats

```powershell
# Ouvrir le rapport
notepad sonar_ai_report.md

# Voir les données JSON
Get-Content sonar_bundle.json | ConvertFrom-Json | ConvertTo-Json
```

## 🐛 Résolution Problèmes Windows

### "ModuleNotFoundError: No module named 'sonar_ai_agent'"

**Solution 1** (Recommandée) :
```powershell
python run_agent.py run --dry-run
```

**Solution 2** :
```powershell
python -m pip install -e .
python -m sonar_ai_agent.main run --dry-run
```

**Solution 3** :
```powershell
$env:PYTHONPATH = "src"
python -m sonar_ai_agent.main run --dry-run
```

### "python not recognized"

```powershell
# Essayer avec py
py run_agent.py run --dry-run

# Ou vérifier l'installation
py --version
```

### Problèmes d'encodage

```powershell
# Définir UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"
chcp 65001
```

### Script .bat ne s'exécute pas

```powershell
# Vérifier Execution Policy
Get-ExecutionPolicy

# Si nécessaire
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📋 Commandes Utiles Windows

### Vérifier l'environnement
```powershell
# Python installé ?
python --version

# pip fonctionnel ?
python -m pip --version

# Git installé ? (requis pour patches)
git --version

# Voir les variables d'environnement
Get-ChildItem Env: | Where-Object {$_.Name -like "*SONAR*" -or $_.Name -like "*GEMINI*"}
```

### Nettoyer l'environnement
```powershell
# Supprimer les fichiers générés
Remove-Item sonar_ai_report.md -ErrorAction SilentlyContinue
Remove-Item sonar_bundle.json -ErrorAction SilentlyContinue
Remove-Item code_context.json -ErrorAction SilentlyContinue

# Clean Python cache
Get-ChildItem -Recurse -Filter "__pycache__" | Remove-Item -Recurse -Force
Get-ChildItem -Recurse -Filter "*.pyc" | Remove-Item -Force
```

### Environnement virtuel Windows
```powershell
# Créer
python -m venv venv_sonar

# Activer
.\venv_sonar\Scripts\Activate.ps1

# Installer
python -m pip install -e .

# Utiliser
python src\sonar_ai_agent\main.py run --dry-run

# Désactiver
deactivate
```

## 🎨 Script PowerShell Personnalisé

Créer `run-sonar.ps1` :

```powershell
# run-sonar.ps1
param(
    [switch]$DryRun = $false,
    [string]$RepoPath = "."
)

Write-Host "🤖 Sonar AI Agent" -ForegroundColor Cyan
Write-Host "==================" -ForegroundColor Cyan
Write-Host ""

# Vérifier .env
if (-not (Test-Path ".env")) {
    Write-Host "❌ .env file not found!" -ForegroundColor Red
    Write-Host "Creating from template..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "✓ Please edit .env with your credentials" -ForegroundColor Green
    notepad .env
    exit 1
}

# Construire la commande
$cmd = "python run_agent.py run"

if ($DryRun) {
    $cmd += " --dry-run"
    Write-Host "🔍 Mode: DRY RUN (no changes)" -ForegroundColor Yellow
} else {
    Write-Host "🚀 Mode: PRODUCTION (will apply patches)" -ForegroundColor Green
}

$cmd += " --repo-path $RepoPath"

Write-Host ""
Write-Host "Executing: $cmd" -ForegroundColor Cyan
Write-Host ""

# Exécuter
Invoke-Expression $cmd

# Afficher résultats
if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Analysis complete!" -ForegroundColor Green
    Write-Host "📊 Report: sonar_ai_report.md" -ForegroundColor Cyan
    
    # Proposer d'ouvrir le rapport
    $open = Read-Host "Open report? (y/n)"
    if ($open -eq "y") {
        notepad sonar_ai_report.md
    }
} else {
    Write-Host ""
    Write-Host "❌ Analysis failed with exit code: $LASTEXITCODE" -ForegroundColor Red
}
```

Utilisation :
```powershell
# Dry run
.\run-sonar.ps1 -DryRun

# Production
.\run-sonar.ps1

# Autre repo
.\run-sonar.ps1 -DryRun -RepoPath "C:\path\to\project"
```

## ✅ Checklist Avant Test

- [ ] Python 3.8+ installé
- [ ] Git installé
- [ ] `.env` créé et configuré avec vraies valeurs
- [ ] SonarQube accessible (URL + Token valides)
- [ ] Clé Gemini API valide
- [ ] Projet SonarQube existe avec des issues

## 🎯 Premier Test Minimal

```powershell
# Juste pour vérifier que ça marche
python run_agent.py --help
```

Si ça affiche l'aide, tout est OK ! ✅

## 📞 Support

Si problème persiste :
1. Vérifier Python : `python --version`
2. Vérifier structure : `Get-ChildItem src\sonar_ai_agent\main.py`
3. Tester import : `python -c "import sys; sys.path.insert(0, 'src'); import sonar_ai_agent"`

---

**Méthode la plus simple** : `python run_agent.py run --dry-run` 🚀
