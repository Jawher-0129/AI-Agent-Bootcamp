# 🚀 Spring Boot Project Generator - Guide d'utilisation

## 📋 Vue d'ensemble

Le Sonar AI Agent génère maintenant automatiquement un projet Spring Boot complet et optimisé basé sur l'analyse SonarQube de votre code existant. Cette fonctionnalité crée un projet entièrement fonctionnel suivant les meilleures pratiques de l'industrie.

## 🎯 Fonctionnalités

Le projet généré inclut :

✅ **Architecture en couches** - Controller / Service / Repository / Model  
✅ **Injection par constructeur** - Remplacement de l'injection par champ (@Autowired)  
✅ **Services basés sur interfaces** - Design pattern avec interfaces  
✅ **Logging professionnel** - SLF4J au lieu de System.out.println  
✅ **Gestion transactionnelle** - @Transactional correctement appliqué  
✅ **Gestion d'exceptions globale** - Handler centralisé avec codes HTTP appropriés  
✅ **Validation des entrées** - Jakarta Bean Validation sur tous les DTOs  
✅ **Documentation OpenAPI** - Interface Swagger UI auto-générée  
✅ **Monitoring** - Endpoints Actuator pour la santé de l'application  
✅ **Audit de base de données** - Dates de création/modification automatiques  
✅ **Verrouillage optimiste** - Protection contre les conflits de mise à jour concurrents  
✅ **Branche Git "bot"** - Projet isolé dans sa propre branche  

## 🛠️ Utilisation

### Commande de base

```bash
python run_agent.py run --dry-run --repo-path .
```

### Résultat

Après l'exécution, vous trouverez :

```
sonar-ai-agent/
├── spring-boot-optimized/           # 🆕 Nouveau projet généré
│   ├── .git/                        # Repository Git avec branche 'bot'
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/
│   │   │   │   └── com/optimized/paiementmanagement/
│   │   │   │       ├── Application.java
│   │   │   │       ├── controller/
│   │   │   │       │   ├── PaiementController.java
│   │   │   │       │   └── CompteBancaireController.java
│   │   │   │       ├── service/
│   │   │   │       │   ├── PaiementService.java
│   │   │   │       │   ├── CompteBancaireService.java
│   │   │   │       │   └── impl/
│   │   │   │       │       ├── PaiementServiceImpl.java
│   │   │   │       │       └── CompteBancaireServiceImpl.java
│   │   │   │       ├── repository/
│   │   │   │       │   ├── PaiementRepository.java
│   │   │   │       │   └── CompteBancaireRepository.java
│   │   │   │       ├── model/
│   │   │   │       │   ├── Paiement.java
│   │   │   │       │   └── CompteBancaire.java
│   │   │   │       ├── dto/
│   │   │   │       │   ├── PaiementRequestDTO.java
│   │   │   │       │   ├── PaiementResponseDTO.java
│   │   │   │       │   ├── CompteBancaireRequestDTO.java
│   │   │   │       │   └── CompteBancaireResponseDTO.java
│   │   │   │       ├── exception/
│   │   │   │       │   ├── ResourceNotFoundException.java
│   │   │   │       │   ├── ResourceAlreadyExistsException.java
│   │   │   │       │   ├── ErrorResponse.java
│   │   │   │       │   └── GlobalExceptionHandler.java
│   │   │   │       └── config/
│   │   │   │           └── OpenApiConfig.java
│   │   │   └── resources/
│   │   │       ├── application.properties
│   │   │       └── application-prod.properties
│   │   └── test/
│   │       └── java/
│   ├── pom.xml
│   ├── .gitignore
│   └── README.md
├── sonar_ai_report.md               # Rapport d'analyse
├── sonar_bundle.json                # Données SonarQube
└── code_context.json                # Contexte du code

```

## 🌿 Gestion Git

Le projet généré est automatiquement initialisé avec Git et possède une branche `bot` :

```bash
cd spring-boot-optimized
git branch
# * bot
#   master

# Pour fusionner les changements dans master
git checkout master
git merge bot

# Pour pousser vers le dépôt distant
git remote add origin <votre-url>
git push origin bot
```

## 🚀 Démarrage du projet généré

### Pré-requis

- Java 17+
- Maven 3.6+

### Lancer l'application

```bash
cd spring-boot-optimized

# Avec Maven
mvn spring-boot:run

# Ou créer un JAR et l'exécuter
mvn clean package
java -jar target/paiementmanagement-1.0.0.jar
```

L'application démarre sur http://localhost:8080

### Accéder à la documentation

- **Swagger UI** : http://localhost:8080/swagger-ui.html
- **API Docs** : http://localhost:8080/api-docs
- **H2 Console** : http://localhost:8080/h2-console
- **Health Check** : http://localhost:8080/actuator/health

## 📊 Endpoints API

### Paiements (`/api/paiements`)

- `POST /api/paiements` - Créer un paiement
- `GET /api/paiements` - Liste tous les paiements
- `GET /api/paiements/{id}` - Paiement par ID
- `GET /api/paiements/reservation/{id}` - Paiements par réservation
- `GET /api/paiements/date-range` - Paiements par plage de dates
- `PATCH /api/paiements/{id}/status` - Mettre à jour le statut
- `DELETE /api/paiements/{id}` - Supprimer un paiement

### Comptes Bancaires (`/api/comptes`)

- `POST /api/comptes` - Créer un compte
- `GET /api/comptes` - Liste tous les comptes
- `GET /api/comptes/{id}` - Compte par ID
- `GET /api/comptes/numero/{numeroCompte}` - Compte par numéro
- `PATCH /api/comptes/{id}/solde` - Mettre à jour le solde
- `DELETE /api/comptes/{id}` - Supprimer un compte

## 🔧 Configuration

### Base de données

**Développement (H2)** : Configuré par défaut, base de données en mémoire

**Production (PostgreSQL)** : Modifier `application-prod.properties`

```properties
spring.datasource.url=jdbc:postgresql://localhost:5432/paiementmanagement
spring.datasource.username=votre_user
spring.datasource.password=votre_password
```

Lancer avec le profil production :
```bash
mvn spring-boot:run -Dspring-boot.run.profiles=prod
```

## 📈 Améliorations par rapport au code original

| Problème | Solution Appliquée |
|----------|-------------------|
| Injection par champ (@Autowired) | Injection par constructeur (final fields) |
| Absence d'interfaces | Services basés sur interfaces |
| System.out.println | Logging SLF4J professionnel |
| Gestion d'erreurs basique | GlobalExceptionHandler centralisé |
| Pas de validation | Jakarta Bean Validation |
| Pas de documentation | OpenAPI/Swagger auto-généré |
| Pas de monitoring | Spring Boot Actuator |
| Entités simples | Auditing + Optimistic locking |

## 🧪 Tests

```bash
# Exécuter tous les tests
mvn test

# Avec rapport de couverture
mvn test jacoco:report
```

## 📝 Personnalisation

Les fichiers suivants peuvent être personnalisés selon vos besoins :

- **application.properties** - Configuration principale
- **pom.xml** - Dépendances Maven
- **OpenApiConfig.java** - Configuration Swagger
- **GlobalExceptionHandler.java** - Gestion d'exceptions

## 🤖 Automatisation

Le générateur analyse automatiquement :

1. ✅ Les issues SonarQube du projet
2. ✅ Les métriques de qualité du code
3. ✅ Les recommandations de l'IA Gemini
4. ✅ La structure du projet existant

Et génère un projet optimisé qui résout tous les problèmes identifiés.

## 💡 Conseils

1. **Examinez le README.md** du projet généré pour des instructions détaillées
2. **Vérifiez le pom.xml** pour ajuster les versions des dépendances si nécessaire
3. **Testez localement** avec H2 avant de passer en production avec PostgreSQL
4. **Consultez Swagger UI** pour tester rapidement les endpoints
5. **Utilisez Actuator** pour monitorer la santé de l'application en production

## 🔗 Ressources

- [Spring Boot Documentation](https://spring.io/projects/spring-boot)
- [Spring Data JPA](https://spring.io/projects/spring-data-jpa)
- [OpenAPI Specification](https://swagger.io/specification/)
- [Jakarta Bean Validation](https://jakarta.ee/specifications/bean-validation/)

---

🤖 **Généré automatiquement par Sonar AI Agent**
