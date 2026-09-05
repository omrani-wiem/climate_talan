# 📋 Préparation Entretien RH — Typhoon2-Alpha

## 1️⃣ RÉSUMÉ EXÉCUTIF DU PROJET

### Qu'est-ce que Typhoon?
**Diagnostic climatique et jumeau numérique du bâti**
- Système qui évalue l'exposition d'une maison aux risques climatiques (inondation, sécheresse, mouvement de terrain)
- Génère des recommandations de travaux de résilience basées sur une base documentaire (RAG)
- Représentation 3D interactive (jumeau numérique) pour visualiser les zones de risque

### Statut du projet
- MVP en cours de spécification (phase de cadrage)
- Déploiement prioritaire sur région PACA
- Architecture production-ready avec orchestration multi-agents

---

## 2️⃣ ARCHITECTURE & STACK TECHNIQUE

### Architecture Multi-Agents (LangGraph)
```
Collector Agent → Scoring Agent → RAG Agent → Digital Twin Agent
```

**4 agents séquencés** qui communiquent via un état partagé (`TyphoonState`):

| Agent | Fonction | Détail |
|-------|----------|--------|
| **Collector** | Collecte de données | Parallélise 5 appels API (BDNB, Géorisques, IGN, Open-Meteo, CATNAT) + lookups locaux (DVF, Copernicus) |
| **Scoring** | Calcul des risques | Score par aléa et par partie du bâtiment |
| **RAG** | Recommandations | Retrieval documentaire + génération avec Mistral |
| **Digital Twin** | Assemblage 3D | Crée le contrat JSON pour la scène Three.js |

### Stack Technique

**Backend:**
- **Framework**: FastAPI + Uvicorn
- **Orchestration**: LangGraph (StateGraph)
- **LLM**: Anthropic + Mistral (recommandations)
- **Persistance**: SQLite (local) / Postgres (prod)
- **Data processing**: Pandas, XArray, NetCDF4 (données climatiques Copernicus)
- **RAG**: ChromaDB (base documentaire)

**Frontend:**
- **Core**: TypeScript + React/Vue
- **Build**: Vite
- **3D**: Three.js
- **Cartographie**: MapLibre GL
- **Geospatial**: Turf.js

**Données externes:**
- BDNB (données du bâti + géocodage)
- Géorisques v1 (risques naturels)
- IGN Altitude & données géographiques
- Open-Meteo (projections climatiques)
- CATNAT (catastrophes naturelles)
- Copernicus (données climatiques PACA)

---

## 3️⃣ POINTS CLÉS À MAÎTRISER

### Cas d'usage / Market Fit
1. **Assurance immobilière**: Diagnostic + score → devis personnalisé + filtrage clients à risque
2. **Banque**: Évaluation risque climatique → arbitrage dossier de prêt
3. **Agents/Promoteurs immobiliers**: Recherche biens résilients + argumentaire de vente

### Points Techniques Importants
- ✅ **État partagé** (TypedDict) = bus de communication inter-agents (pas d'appels directs)
- ✅ **Checkpointer LangGraph** = audit trail + reprise sur interruption
- ✅ **Collector interne parallélisé** = temps quasi instantanés requis par spec
- ✅ **Digital Twin = orchestration finale** (assemblage sans recalcul)

### Challenges Actuels
- Phase MVP → beaucoup de points "open" (roadmap)
- Intégration données climatiques complexe (Copernicus, NetCDF)
- RAG en cours d'implémentation (base documentaire MRN, BRGM, CEPRI, ADEME)
- Scalabilité: gestion concurrence diagnostics multiples
- Performance: parallélisation critique du Collector

---

## 4️⃣ VOS CONTRIBUTIONS / RESPONSABILITÉS

### À préciser avec votre manager, mais généralement:

**Domaines probables:**
- [ ] Architecture backend / orchestration LangGraph
- [ ] Intégration APIs externes (BDNB, Géorisques, etc.)
- [ ] Implémentation agents (Collector, Scoring, RAG, Digital Twin)
- [ ] RAG + retrieval documentaire
- [ ] Data pipelines (lookups DVF, projections climatiques Copernicus)
- [ ] Frontend (composants React/Vue, scène 3D, routing cas d'usage)
- [ ] Tests & validation
- [ ] Déploiement / CI-CD

**À préparer**: Lister **précisément** vos 3-5 contributions majeures avec impact mesurable.

---

## 5️⃣ QUESTIONS RH POTENTIELLES & RÉPONSES

### A. **QUESTIONS GÉNÉRALISTES**

#### Q1: Décrivez le projet Typhoon en 30 secondes
**Réponse modèle:**
> "Typhoon est un système de diagnostic climatique qui évalue l'exposition d'une maison aux risques naturels (inondation, sécheresse, mouvements de terrain) et génère des recommandations de travaux de résilience. Le système utilise une architecture multi-agents orchestrée avec LangGraph, intègre des données d'APIs publiques et privées, et restitue le diagnostic sous forme d'un jumeau numérique 3D interactif. Le produit cible 3 segments: l'assurance, la banque et l'immobilier."

#### Q2: Quel est votre rôle dans ce projet?
**Réponse modèle:**
> "[Adapter selon vos contributions réelles] J'ai contribué principalement à [domaine 1], [domaine 2], [domaine 3]. Par exemple, j'ai implémenté [exemple concret 1], ce qui a permis [impact]. J'ai aussi travaillé sur [exemple concret 2], responsable de [détail technique]."

#### Q3: Quels sont les défis techniques majeurs du projet?
**Réponse modèle:**
> "Plusieurs défis:
> - **Performance**: Le Collector doit être quasi instantané → parallélisation critique des 5 appels API externes
> - **Intégration données**: Fusion de sources hétérogènes (APIs, lookups locaux, projections climatiques NetCDF)
> - **Scalabilité**: Gestion d'une concurrence de diagnostics multiples via le Checkpointer LangGraph
> - **RAG en production**: Implémentation d'une base documentaire retrieval-augmented avec ChromaDB + Mistral
> - **Crossplatform**: Frontend doit fonctionner sur 3 cas d'usage différents (assurance, banque, immo)"

---

### B. **QUESTIONS TECHNIQUES**

#### Q4: Expliquez l'architecture multi-agents et le flux de données
**Réponse modèle:**
> "L'architecture repose sur 4 agents séquencés qui communiquent via un état partagé (TyphoonState):
> 1. **Collector**: Collecte données en parallèle (BDNB, Géorisques, IGN, climatique, CATNAT) + lookups locaux
> 2. **Scoring**: Calcule scores de risque par aléa et zone du bâtiment
> 3. **RAG**: Retrieval base documentaire + génération recommandations Mistral
> 4. **Digital Twin**: Assemble la géométrie 3D + scores + recommandations → contrat JSON pour Three.js
> 
> Avantage: État partagé = bus de communication centralisé → audit trail + reprise sur interruption via Checkpointer LangGraph."

#### Q5: Comment gérez-vous la performance du Collector?
**Réponse modèle:**
> "Le Collector parallélise ses 5 appels externes via `asyncio.gather()` pour minimiser latence. Cela nous permet de garder un temps quasi instantané même avec des APIs externes lentes. Les lookups locaux (DVF, Copernicus) sont instantanés par cache local. L'orchestration LangGraph manage l'ordre de passage agent-par-agent, mais au sein du Collector, tout est parallélisé."

#### Q6: Comment intégrez-vous les données climatiques Copernicus?
**Réponse modèle:**
> "Copernicus fournit des projections climatiques en format NetCDF. Nous:
> - Téléchargeons les données via CDS API au démarrage (cache PACA)
> - Les traitons avec XArray/NetCDF4
> - Les intégrons au Collector sous forme de lookup local
> - Cela évite d'appeler l'API à chaque diagnostic → performance"

#### Q7: Pourquoi le Digital Twin n'est-il qu'une orchestration finale?
**Réponse modèle:**
> "Le Digital Twin reçoit:
> - Géométrie brute du bâti (du Collector)
> - Scores de risque (du Scoring)
> - Recommandations (du RAG)
> 
> Il n'a pas besoin de recalculer → il assemble simplement ces données dans le contrat JSON attendu par Three.js. C'est une séparation des responsabilités claire: chaque agent fait un job, le Digital Twin coordonne l'output final."

#### Q8: Comment gérez-vous la persistence et l'audit trail?
**Réponse modèle:**
> "Nous utilisons le Checkpointer LangGraph pour persister l'état du graphe après chaque diagnostic:
> - SQLite en local (développement)
> - Postgres en production
> Cela permet:
> - Audit trail complet (qui a demandé quel diagnostic quand)
> - Reprise sur interruption (rejouer un diagnostic incomplet)
> - Debugging (voir l'état à chaque étape du graphe)"

---

### C. **QUESTIONS SUR LE PRODUIT & BUSINESS**

#### Q9: Pourquoi 3 frontends différents?
**Réponse modèle:**
> "Le diagnostic (le graphe d'agents) est unique, mais chaque cas d'usage a des besoins différents:
> - **Assurance**: Focus sur score + devis → écran simple, scoring prominent
> - **Banque**: Focus sur risque d'un bien financé → analyse détaillée des zones
> - **Promoteurs**: Focus sur résilience climatique + argumentaire → met en avant recommandations
> 
> Le backend expose des routes différentes par cas d'usage, le frontend s'adapte."

#### Q10: Quel est l'avantage du jumeau numérique 3D?
**Réponse modèle:**
> "C'est le cœur de l'UX: au lieu de lire un rapport textuel, l'utilisateur **parcourt sa maison en 3D**. Chaque zone est colorée par niveau de risque (vert = faible, rouge = critique). En cliquant sur une zone, il voit le détail + les recommandations. C'est beaucoup plus intuitif et engageant qu'un rapport PDF."

#### Q11: Comment Typhoon se différencie des solutions existantes?
**Réponse modèle:**
> "Typhoon combine 3 éléments rares:
> 1. **Données intégrées**: Fusion BDNB + Géorisques + climatiques + CATNAT → vue holistique
> 2. **Intelligence (RAG)**: Recommandations basées sur base documentaire (MRN, BRGM, ADEME) → pas juste un score
> 3. **UX 3D**: Jumeau numérique interactif → communication plus efficace que rapports traditionnels
> 
> La plupart des concurrents offrent soit le scoring, soit les recommandations, rarement les trois + l'UX 3D."

---

### D. **QUESTIONS SUR LES DÉFIS & LEARNINGS**

#### Q12: Avez-vous rencontré des problèmes majeurs? Comment les avez-vous résolus?
**Réponse modèle:**
> "[À préparer avec exemples réels du projet] Par exemple:
> - **Problème**: Les appels API externes étaient séquentiels → trop lent
> - **Solution**: Implémentation parallélisation asyncio.gather()
> - **Résultat**: Performance multipliée par 4-5x
> 
> Autre exemple:
> - **Problème**: Persistance d'état complexe avec 4 agents
> - **Solution**: Utilisation Checkpointer LangGraph
> - **Résultat**: Audit trail + reprise automatique sur crash"

#### Q13: Quels learnings avez-vous tiré de ce projet?
**Réponse modèle:**
> "Plusieurs insights:
> - **LangGraph**: Framework excellent pour orchestration multi-agents; état partagé >> appels directs
> - **Parallélisation critique**: Quand chaque milliseconde compte, asyncio + gathering font la différence
> - **Data complexity**: Intégrer des sources hétérogènes demande beaucoup de data cleaning et validation
> - **Frontend <-> Backend contrat**: Définir un contrat JSON clair (ex: Digital Twin schema) = gain de temps énorme
> - **Testing**: Tester des pipelines de données complexes est challenge → besoin fixtures + mocks robustes"

#### Q14: Avez-vous dû apprendre de nouvelles technologies?
**Réponse modèle:**
> "Oui, plusieurs:
> - **LangGraph**: Nouveau framework pour moi → courbe d'apprentissage rapide, très bien documenté
> - **NetCDF/XArray**: Manipuler données climatiques en format NetCDF était nouveau
> - **ChromaDB**: RAG + embeddings vectoriels → domaine nouveau mais très puissant
> - **Three.js (si frontend)**: Rendu 3D interactif → compétence complètement nouvelle
> 
> J'ai apprécié la diversité des technos et la nécessité d'apprendre vite."

---

### E. **QUESTIONS COMPORTEMENTALES**

#### Q15: Comment travaillez-vous en équipe sur un projet complexe?
**Réponse modèle:**
> "Sur Typhoon:
> - **Communication**: Découpes claires par domaine (Backend API, Agents, Frontend, Data)
> - **Contrats**: Définition précise des schémas JSON échangés (ex: TyphoonState, Digital Twin output)
> - **Testing**: Chacun test son périmètre, intégration via tests d'intégration
> - **Review**: Code reviews régulières pour garder la qualité et les bonnes pratiques
> - **Documentation**: ReadMe clair par composant, docs/ pour les specs"

#### Q16: Comment gérez-vous l'ambiguïté et les changements?
**Réponse modèle:**
> "Typhoon est en phase MVP → beaucoup de changements specs:
> - Roadmap publique (ROADMAP_MVP_PACA.md) = clarté sur priorités
> - Discussions régulières avec product/métier sur priorités
> - Architecture = flexible (agents découplés) → changements impactent peu
> - Exemple: Si une source de données change, seul le Collector est impacté"

#### Q17: Comment assurez-vous la qualité du code?
**Réponse modèle:**
> "Plusieurs couches:
> - **Linting/typing**: Python strict (pydantic), TypeScript strict
> - **Tests**: Unittests + tests d'intégration pour pipelines complexes
> - **Fixtures**: Test data pour APIs (mocks des appels externes)
> - **PR reviews**: Feedback sur code quality, architecture, edge cases
> - **Documentation**: Code self-documenting + docstrings + typehints"

#### Q18: Exemple de moment où vous avez dû dire "non" ou faire un tradeoff?
**Réponse modèle:**
> "[À préparer avec exemple réel] Par exemple:
> - **Contexte**: Demand pour ajouter une 6ème source API au Collector
> - **Issue**: Ça aurait augmenté latence de 500ms → violation du requirement 'quasi-instantané'
> - **Decision**: Proposé à la place comme async background task post-diagnostic
> - **Résultat**: Specs satisfied, flexibilité pour feature future"

---

### F. **QUESTIONS SPÉCIFIQUES À LA POSITION**

#### Q19: Quelle était la plus grande contribution technique?
**Réponse modèle:**
> "[À personnaliser fortement] Par exemple:
> Si architecture backend: 'J'ai conçu la TyphoonState et le pattern d'orchestration multi-agents → cela a permis au projet de scalabilité et d'auditabilité'
> Si RAG: 'J'ai implémenté le pipeline RAG de retrieval + génération → première implémentation des recommandations dynamiques'
> Si frontend 3D: 'J'ai conçu la scène Three.js interactive → c'est maintenant le cœur de l'UX produit'"

#### Q20: Comment voyez-vous le futur du projet?
**Réponse modèle:**
> "Court terme (3-6 mois):
> - MVP PACA en production
> - Affinage RAG basé sur feedback utilisateurs
> - Scaling infrastructure (Postgres, monitoring)
> 
> Moyen terme (6-12 mois):
> - Expansion géographique (au-delà PACA)
> - Intégration nouveaux aléas (canicule, pollution)
> - Marketplace recommandations (artisans, matériaux)
> 
> Long terme (vision):
> - Devenir référence en diagnostic climatique bâti pour France
> - API publique pour autres players
> - Intégration solutions assurance/fintech"

---

## 6️⃣ QUESTIONS À PRÉPARER SPÉCIFIQUEMENT

### À compléter avant l'entretien:

**Mes 3-5 contributions majeures:**
1. [ ] **Contribution 1**: [Description + impact mesuré]
2. [ ] **Contribution 2**: [Description + impact mesuré]
3. [ ] **Contribution 3**: [Description + impact mesuré]
4. [ ] **Contribution 4** (optionnel): [Description + impact mesuré]
5. [ ] **Contribution 5** (optionnel): [Description + impact mesuré]

**Exemples de problèmes résolus:**
- [ ] Problème 1: [Quoi] → [Solution] → [Résultat]
- [ ] Problème 2: [Quoi] → [Solution] → [Résultat]
- [ ] Problème 3: [Quoi] → [Solution] → [Résultat]

**Questions personnelles à poser:**
- [ ] Q1: Où voyez-vous le projet dans 12 mois?
- [ ] Q2: Quels sont les 3 plus gros défis techniques restants?
- [ ] Q3: Comment évaluez-vous mon impact sur le projet?
- [ ] Q4: Quelles compétences aimeriez-vous que je développe davantage?

---

## 7️⃣ TALKING POINTS À MÉMORISER

### Phrases clés pour sonner expert:

- **"État partagé vs appels directs"** → montre compréhension architecture
- **"Checkpointer LangGraph pour auditabilité"** → montre pensée scalabilité
- **"Parallélisation asyncio du Collector"** → montre focus performance
- **"Contrat JSON clair entre agents"** → montre design rigoreux
- **"RAG avec base documentaire"** → montre compréhension intelligence artificielle
- **"3 cas d'usage, 1 graphe"** → montre flexibilité architecture
- **"Jumeau numérique 3D comme UX différenciatrice"** → montre pensée produit

### Points de vulnérabilité à bien gérer:

- **"C'est encore en MVP"** → POSITIF! = opportunité d'impact, apprentissage rapide
- **"Points techniques ouverts"** → POSITIF! = challenges intéressants, croissance
- **"Technos nouvelles pour moi"** → POSITIF! = capacité d'apprentissage, adaptabilité

---

## 8️⃣ STRUCTURE RÉPONSE PAR QUESTION (Template)

### Quand on vous pose une question:

**1. PAUSE (2-3s)** → montrer vous réfléchissez
**2. CONTEXTE** → situer dans le projet
**3. EXEMPLE** → donner un cas concret
**4. LEÇON** → ce que vous en avez tiré
**5. CONCLUSION** → résumé clair

Exemple:
> Q: "Décrivez un moment difficile du projet"
> 
> A: "[Pause] Un défi majeur a été la performance du Collector. [Contexte] Au départ, on faisait 5 appels API séquentiellement, ce qui prenait 5-8 secondes. Mais la spec requiert 'quasi-instantané' (<1s). [Exemple] J'ai implémenté asyncio.gather() pour paralléliser → résultat: 800ms au lieu de 6 secondes. [Leçon] Parfois la solution la plus simple (parallélisation) a l'impact le plus fort. [Conclusion] Maintenant le Collector respecte les SLAs."

---

## 9️⃣ RESSOURCES À CONSULTER AVANT L'ENTRETIEN

**À lire:**
- [ ] [README.md](README.md) — Vue d'ensemble complète
- [ ] [ROADMAP_MVP_PACA.md](docs/ROADMAP_MVP_PACA.md) — Vision produit
- [ ] [DETTE_TECHNIQUE.md](docs/DETTE_TECHNIQUE.md) — Challenges connus
- [ ] [GUIDE_ORCHESTRATEUR_API.md](docs/GUIDE_ORCHESTRATEUR_API.md) — Architecture backend

**À refamiliariser:**
- [ ] Architecture agents (graphe LangGraph)
- [ ] Contrats de données (TyphoonState, Digital Twin)
- [ ] Sources de données externes (APIs, lookups)
- [ ] Votre code spécifique (revisite commits, PRs)

---

## 🔟 CHECKLIST PRÉ-ENTRETIEN

- [ ] **J'ai lié mes contributions à des impacts mesurables** (performance, features, scalabilité)
- [ ] **J'ai 3-5 exemples concrets prêts** (pas juste "j'ai fait X", mais "j'ai fait X ce qui a permis Y")
- [ ] **J'ai révisé l'architecture multi-agents** (comprendre StateGraph + agents en détail)
- [ ] **J'ai une liste de questions à poser** (shows engagement)
- [ ] **J'ai pratiqué mes réponses à haute voix** (évite de bafouiller)
- [ ] **J'ai des chiffres/métriques prêts** (si possible: % perf gain, temps savings, etc.)
- [ ] **Je sais où sont les points ouverts** (ROADMAP.md) et comment je pourrais contribuer
- [ ] **J'ai revu ma propre code** (commits, PRs) pour expliquer mes décisions design
- [ ] **Je suis prêt à parler de ce que j'aimerais apprendre** (growth mindset)
- [ ] **Je suis prêt à dire "je ne sais pas, mais voilà comment j'apprendrais"** (humilité)

---

## 1️⃣1️⃣ NOTES PERSONNELLES

_À remplir avec contexte spécifique à votre rôle et contributions:_

### Mon rôle exact dans le projet:
```
[À compléter]
```

### Mes achievements spécifiques:
```
1. [Contribution 1 avec métrique]
2. [Contribution 2 avec métrique]
3. [Contribution 3 avec métrique]
```

### Domaines où je pourrais croître:
```
1. [Domaine 1]
2. [Domaine 2]
3. [Domaine 3]
```

### Questions que je veux poser:
```
1. [Question 1]
2. [Question 2]
3. [Question 3]
```

---

## 1️⃣2️⃣ BON COURAGE! 🚀

Vous avez travaillé sur un projet ambitieux avec stack moderne et enjeux réels. Soyez confiant, donnez des exemples précis, et montrez votre curiosité.

**Derniers tips:**
- ✅ Smile, langage corporel positif
- ✅ Parlez lentement, articulez
- ✅ Faites des pauses — pas besoin de répondre ultra-vite
- ✅ Si vous ne savez pas, dites "je ne sais pas, voilà comment je trouverais la réponse"
- ✅ Posez vos propres questions — shows engagement
- ✅ Focus sur l'impact, pas juste la technique
