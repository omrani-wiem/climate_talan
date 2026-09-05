# 📝 DESCRIPTION DÉTAILLÉE DU PROJET TYPHOON

## Version Ultra-Courte (15-30 secondes)
*Idéale si on vous pose la question rapidement, sans contexte*

> "Typhoon est un système d'intelligence artificielle qui évalue les risques climatiques d'une maison — inondation, sécheresse, tremblements de terre — et propose des travaux de résilience. Le diagnostic est présenté dans une maison 3D interactive où chaque pièce est colorée selon son niveau de risque. C'est destiné aux assurances, banques et agents immobiliers."

---

## Version Courte (30-60 secondes)
*Pour un entretien RH standard, réponse claire et concise*

> "Typhoon construit un diagnostic climatique d'une maison via une architecture d'**agents orchestrés avec LangGraph**. 
> 
> **Le concept:** Imaginez que vous vendez une maison — vous aimeriez savoir si elle risque une inondation, une sécheresse extrême ou un glissement de terrain. Typhoon répond à cette question en 3 étapes:
> 
> 1. **Collecte de données** — On récupère l'info du bâti, sa localisation exacte, et les projections climatiques (5 API en parallèle)
> 2. **Scoring de risque** — On calcule un score par aléa (inondation, sécheresse, etc.) et par partie de la maison
> 3. **Recommandations** — On propose des travaux de résilience basés sur une base documentaire (MRN, BRGM, etc.)
> 4. **Visualisation 3D** — Tout s'affiche dans une maison 3D interactive où chaque zone change de couleur selon le risque
> 
> On a trois clients: assurances (devis personnalisés), banques (évaluation du risque d'un prêt immobilier), et agents immobiliers (vente de biens résilients)."

---

## Version Moyenne (2-3 minutes)
*Pour une explication équilibrée avec détail technique*

> "Typhoon est un produit SaaS qui fait du diagnostic climatique de bien immobilier. 
> 
> **Le problème qu'on résout:** Aujourd'hui, une assurance immobilière ne sait pas vraiment évaluer le risque climatique futur d'un bien. Un bien à Marseille face à la mer, c'est risqué submersion marine et sécheresse — mais comment le chiffrer précisément? Une banque prête sur un bien sans vraiment savoir s'il sera submergé en 2050. Un promoteur vend des biens sans pouvoir prouver qu'ils sont résilients. Et des propriétaires ne savent pas quels travaux faire pour adapter leur maison.
> 
> **Notre solution:** Typhoon intègre les meilleures sources de données publiques et privées — cartes de risques Géorisques, données du bâti BDNB, projections climatiques Open-Meteo, données sur les prix immobiliers DVF, données de catastrophes naturelles (CATNAT) — et les fuse via une orchestration multi-agents.
> 
> **L'architecture technique:** 
> - **Collector agent**: Parallélise 5 appels API externes (BDNB, Géorisques, IGN, climatique, CATNAT) pour récupérer les données du bien et son environnement
> - **Scoring agent**: Calcule des scores de risque par aléa (inondation, sécheresse, mouvement de terrain, etc.) et par zone du bâtiment (fondations, murs, toiture, etc.)
> - **RAG agent**: Utilise une base documentaire (MRN, BRGM, CEPRI, ADEME) pour générer des recommandations de travaux spécifiques à chaque zone à risque
> - **Digital Twin agent**: Assemble tout ça dans un contrat JSON qui est rendu par Three.js en une maison 3D interactive
> 
> **La différenciation:** L'utilisateur ne lit pas un rapport PDF ennuyeux. Il parcourt sa maison en 3D, chaque zone est colorée par niveau de risque, et en cliquant il voit les détails et les travaux recommandés. C'est beaucoup plus intuitif et engageant.
> 
> **Trois cas d'usage:**
> - **Assurance**: Le client rentre son adresse → diagnostic → score de risque → devis avec prime ajustée
> - **Banque**: Évaluation du risque d'un bien financé pour arbitrer un dossier de prêt
> - **Agents immobiliers**: Recherche de biens résilients et argumentaires de vente
> 
> Le projet est actuellement en MVP pour la région PACA, cible à court terme est la couverture nationale. Stack technique: FastAPI backend, LangGraph pour l'orchestration, ChromaDB pour le RAG, React/TypeScript frontend, Three.js pour la 3D."

---

## Version Longue (5-7 minutes)
*Pour un recruteur très intéressé ou un technical discussion*

> "Typhoon est une plateforme de diagnostic climatique qui combine **collecte de données**, **scoring de risque**, **intelligence artificielle** (RAG), et **visualisation 3D**.
> 
> **Contexte et enjeux:**
> Le changement climatique crée une urgence pour le secteur immobilier: inondations de plus en plus fréquentes, sécheresses extrêmes, mouvements de terrain, canicules. Une maison construite il y a 30 ans sans considération pour le climat, c'est un risque énorme aujourd'hui. Mais:
> - Les assureurs ne savent pas bien évaluer ce risque → devis génériques ou refus arbitraires
> - Les banques financent des biens sans vraiment évaluer l'exposition → risque prêt
> - Les promoteurs ne peuvent pas différencier sur la résilience → perdu une opportunité de vente
> - Les propriétaires ne savent pas quels travaux faire → paralysie
> 
> **Ce que Typhoon fait:**
> On agrège les meilleures sources publiques et privées — données du bâti (BDNB), cartes de risques (Géorisques), projections climatiques (Open-Meteo), historique des catastrophes (CATNAT), données de prix (DVF), données climatiques haute résolution (Copernicus CDS) — et on les fusionne dans une **orchestration multi-agents** pour générer un diagnostic complet et une visualisation 3D du bien.
> 
> **Architecture détaillée:**
> 
> L'orchestration est basée sur **LangGraph**, un framework pour orchestrer des agents d'IA. Le flux est:
> 
> 1. **Collector Agent** (fan-out/fan-in interne):
>    - Prend une adresse en input
>    - Lance **5 appels API en parallèle** (via asyncio.gather) pour être quasi-instantané:
>      - BDNB: géocodage précis + données du bâti (année construction, énergie, étages, surface)
>      - Géorisques v1: cartes d'exposition aux aléas naturels (inondation, mouvement de terrain, remontée nappe, etc.)
>      - IGN Altitude: MNT pour connaître l'altitude du bien
>      - Open-Meteo: projections climatiques 2050/2100
>      - CATNAT: historique des catastrophes naturelles
>    - Lance **2 lookups locaux** (instantanés):
>      - DVF: contexte immobilier (prix local, tendance)
>      - Copernicus CDS: données climatiques pré-téléchargées en cache local (NetCDF)
>    - Output: `state.building_data` = fusion complète + géométrie brute du bien
> 
> 2. **Scoring Agent**:
>    - Prend `building_data`
>    - Applique des règles de scoring par aléa (inondation, sécheresse/RGA, mouvement de terrain, canicule, etc.)
>    - Calcule des scores de risque par zone physique du bâtiment (fondations, murs, toiture, cave, jardin, etc.)
>    - Output: `state.risk_scores` = scores structurés par aléa × zone
> 
> 3. **RAG Agent** (Retrieval-Augmented Generation):
>    - Prend `risk_scores`
>    - Pour chaque zone à risque, interroge une base documentaire vectorisée (ChromaDB):
>      - Normes MRN (construction résiliente)
>      - Guides BRGM (géotechnique, retrait-gonflement)
>      - Retours d'expérience CEPRI (inondation)
>      - Guides ADEME (efficacité énergétique + résilience)
>    - Génère des recommandations spécifiques (ex: "Pour votre sous-sol à risque inondation: surélever les installations élec + poser des cloisons amovibles")
>    - Output: `state.recommendations` = liste structurée des travaux par zone
> 
> 4. **Digital Twin Agent** (orchestration finale):
>    - Ne recalcule RIEN — assemble les trois précédentes outputs
>    - Prend:
>      - Géométrie du bâti (de Collector)
>      - Scores (de Scoring)
>      - Recommandations (de RAG)
>    - Assemble un contrat JSON unique:
>      ```json
>      {
>        \"geometry\": { forme: \"maison\", etages: 2, zones: [...] },
>        \"risk_scores\": { inondation: 0.7, secheresse: 0.4, ... },
>        \"recommendations\": [{ zone: \"fondations\", alea: \"inondation\", travaux: [...] }, ...],
>        \"projection_2050\": { inondation: 0.8, ... }
>      }
>      ```
>    - Cet output est exactement ce qu'attend Three.js côté frontend
> 
> **Points architecturaux clés:**
> - **État partagé (TyphoonState)**: Tous les agents lisent/écrivent dans un TypedDict versionné → bus de communication centralisé, pas d'appels directs agent-à-agent
> - **Checkpointer LangGraph**: Chaque diagnostic persiste en SQLite (local) / Postgres (prod) → audit trail complet + reprise sur interruption
> - **Parallélisation critique**: Le Collector parallélise ses 5 appels externes → atteindre <1s latence total
> - **Séparation des responsabilités**: Chaque agent a un job clair, pas de couplage
> 
> **Trois cas d'usage / trois frontends, un seul graphe:**
> 
> Le diagnostic (le StateGraph) est UNIQUE. Ce qui change:
> - Routes API exposées côté backend (ex: assurance expose `/devis`, banque expose `/score_pret`)
> - Écrans côté frontend (assurance: focus score + devis, banque: focus analyse détaillée, agents: focus recommandations + matching artisans)
> - Chemins de données (ex: assurance envoie aussi les années de contribution pour calculer la prime)
> 
> **Visualisation 3D — le cœur de l'UX:**
> 
> Au lieu de lire un rapport PDF de 20 pages, l'utilisateur parcourt sa maison en 3D avec sa souris/touch. Chaque zone est colorée:
> - Vert = risque faible
> - Orange = risque moyen
> - Rouge = risque critique
> 
> En cliquant sur une zone, il voit:
> - Les aléas qui menacent cette zone
> - L'évolution du risque 2030/2050/2100
> - Les travaux recommandés avec sources (\"BRGM: surélever de 1m minimum\")
> - Un estimé du coût des travaux
> 
> C'est beaucoup plus engageant qu'un rapport textuel, et ça communique le risque instantanément.
> 
> **Statut du projet:**
> 
> Actuellement en **MVP pour la région PACA** (10 jours de cadrage). Déploiement complet en cours avec:
> - Semaine 1: Collector + Scoring sur cas d'usage assurance
> - Semaine 2: RAG + Digital Twin + intégration frontend
> - Post-MVP: Expansion géographique, deux autres cas d'usage, nouveau aléas (canicule, pollution)
> 
> **Stack technique:**
> - Backend: FastAPI + Uvicorn, LangGraph pour orchestration, Mistral LLM pour recommandations
> - Data: Pandas + XArray + NetCDF4 pour traitement données climatiques
> - RAG: ChromaDB + embeddings vectoriels + LangChain
> - Frontend: React/TypeScript + Vite + Three.js pour la 3D
> - Persistance: SQLite (local) / Postgres (prod) + Checkpointer LangGraph
> - Déploiement: Docker-compose pour démo, Kubernetes cible long terme
> 
> **Enjeux techniques:**
> - Parallélisation critique du Collector pour respecter <1s latence
> - Fusion de sources de données hétérogènes (APIs, lookups, NetCDF)
> - Intégration RAG en production avec base documentaire fiable
> - Scalabilité: gestion concurrence de diagnostics multiples
> - Qualité de la géométrie 3D générée vs réalité du bâti"

---

## Version Focus Business (pour RH/Product)
*Si l'entretien est plutôt business-oriented*

> "Typhoon résout un problème **critiquement urgent** pour le secteur immobilier français:
> 
> **La problématique:** Aujourd'hui, le marché immobilier n'a pas d'outil standard pour évaluer l'exposition climatique d'un bien. Une assurance refuse une maison à Marseille au feeling, une banque finance un bien sans vraiment connaître les risques, un propriétaire achète une maison qu'il ignorer sera inondée en 2050.
> 
> **La solution:** Typhoon crée un **diagnostic climatique standardisé**, intégrant les meilleures données publiques (Géorisques, BDNB, etc.), et le restitue dans un **jumeau numérique 3D** que n'importe quel utilisateur peut comprendre.
> 
> **Les trois clients identifiés:**
> 
> 1. **Assurance immobilière** (~800M€ marché France)
>    - Aujourd'hui: Tarification au sentiment + refus arbitraire
>    - Avec Typhoon: Score de risque objectif → prime adaptée ou refus argumenté → meilleure rentabilité + moins de litiges
>    - ROI: Économies d'indemnisations + premium pricing pour biens résilients
> 
> 2. **Banque** (crédit immobilier)
>    - Aujourd'hui: Évaluation du bien = valeur d'échange uniquement, ignorer la volatilité climatique
>    - Avec Typhoon: Évaluation risque climatique → arbitrage dossier de prêt + taux adapté
>    - ROI: Réduction des défauts de paiement + premium sur prêts bas-risque
> 
> 3. **Agents/Promoteurs immobiliers** (~10k agences France)
>    - Aujourd'hui: \"Cette maison c'est l'investissement du siècle\" (sans preuve)
>    - Avec Typhoon: Argument béton = \"Cette maison a un score de résilience climatique 9/10\" + recommandations de travaux (donc crédibilité)
>    - ROI: Différenciation sur marché concurrentiel + vente plus rapide + prix moyen +5-10%
> 
> **Modèle économique cible:**
> - B2B SaaS: API/dashboard
> - Tarification par diagnostic (ex: 5-50€ / diagnostic selon client)
> - Ou SaaS mensuel si client corporate
> - Marché TAM = 800M€ (assurance) + 200M€ (banque) + 500M€ (agences) = ~1.5B€ potential
> 
> **Avantage concurrentiel:**
> - Intégration de données complète (pas juste scoring brut comme Géorisques)
> - Intelligence artificielle (recommandations) vs juste scorecards
> - UX 3D vs rapports PDF textuels
> - Données en France vs outils internationaux mal calibrés"

---

## Version Focus Technique (pour Dev/Arch)
*Si l'entretien est technique*

> "Typhoon est une orchestration multi-agents avec **LangGraph** qui résout le problème de fusion de données hétérogènes dans un pipeline déterministe.
> 
> **Architecture:**
> 
> StateGraph à 4 nœuds séquencés:
> - **Collector**: Fan-out/fan-in interne de 7 sources (5 APIs live + 2 lookups locaux), parallélisation asyncio.gather()
> - **Scoring**: Règles de scoring pondérées par aléa × zone architecturale
> - **RAG**: Retrieval documentaire (ChromaDB) + génération (Mistral)
> - **Digital Twin**: Assemblage orchestration finale
> 
> Communication: État partagé `TyphoonState` (TypedDict versionné) = bus centralisé
> 
> **Choix architecturaux motivés:**
> 
> 1. **Pas d'appels directs agent-à-agent** → état partagé
>    - Avantage: Découplage, testabilité, audit trail
>    - Checkpointer LangGraph peut persister/reprendre n'importe quel diagnostic
> 
> 2. **Parallélisation du Collector**
>    - Req spec: <1s latence total
>    - Solution: asyncio.gather() sur les 5 appels externes
>    - Mitigation latence API externe: mise en cache des réponses de démo
> 
> 3. **Digital Twin ≠ générateur paramétrique complet**
>    - Digital Twin reçoit géométrie brute du Collector
>    - Applique templates de rendering (au lieu de générer une géométrie 3D parfaite)
>    - Cela fait simplement un assemblage d'output
>    - Risque technique réduit, output déterministe
> 
> 4. **RAG avec base documentaire spécialisée**
>    - Pas de RAG généraliste (Wikipedia, web)
>    - Documentaire expertisée: MRN, BRGM, CEPRI, ADEME, AQC
>    - Embeddings vectoriels ChromaDB
>    - LLM: Mistral (80B) pour recommandations de qualité
> 
> **Challenges techniques:**
> 
> 1. **Fusion données hétérogènes**
>    - BDNB: JSON structuré
>    - Géorisques v1: API spatiale (WFS, GeoJSON)
>    - NetCDF Copernicus: Arrays multidimensionnels XArray
>    - DVF: CSV local
>    - Schéma unique `building_data`: validation Pydantic stricte
> 
> 2. **Persistance et audit trail**
>    - Checkpointer LangGraph + SQLite (local) / Postgres (prod)
>    - Permet rejeu complet d'un diagnostic (\\"what-if\\": changer une hypothèse de scoring)
>    - Audit qui a lancé quel diagnostic quand
> 
> 3. **Scalabilité**
>    - Chaque appel diagnostic = nœud LangGraph distinct
>    - Concurrent diagnostics gérés par le checkpointer
>    - Requiert pooling de connexions DB, rate limiting APIs externes
> 
> **Stack d'intérêt:**
> - **LangGraph**: Orchestration agents → état partagé >> direct RPC
> - **Pydantic**: Validation schémas stricts → zéro surprises en prod
> - **ChromaDB**: RAG vectoriel en pur Python → pas de dépendance externe
> - **XArray**: Manipulation NetCDF → multidim arrays de base scientifique
> - **Three.js**: Rendu 3D interactif navigable → UX engagement
> 
> **Patterns d'intérêt:**
> - TypedDict versionné = contrat inter-agents
> - Checkpointing = replay/debugging/audit
> - Parallélisation asyncio = performance sous contrainte latence
> - Templates vs paramétrie = réduction risque technique vs perfection"

---

## Phrases Clés à Retenir (pour vous aider à improviser)

Utilisez ces phrases clés si vous oubliez un détail:

### Cadre général
- *"Diagnostic climatique d'une maison par orchestration multi-agents"*
- *"Fusion de 7 sources de données (5 APIs + 2 lookups locaux)"*
- *"Restitution en jumeau numérique 3D interactif"*

### Problème / Solution
- *"Les assurances ne savent pas bien évaluer le risque climatique → Typhoon le fait"*
- *"Au lieu d'un rapport PDF, on affiche une maison 3D colorée par zone de risque"*
- *"Trois cas d'usage (assurance, banque, agents immobiliers) alimentés par un seul graphe d'agents"*

### Architecture
- *"LangGraph: 4 agents séquencés (Collector → Scoring → RAG → Digital Twin)"*
- *"État partagé TyphoonState = bus de communication inter-agents"*
- *"Collector parallélise 5 appels externes en <1s via asyncio.gather()"*
- *"Checkpointer LangGraph = persistence + audit trail + reprise sur crash"*

### RAG
- *"Recommandations générées par RAG sur base documentaire: MRN, BRGM, CEPRI, ADEME"*
- *"Pas juste un score, mais des travaux concrets recommandés"*

### Enjeux
- *"Performance: Collector doit être quasi-instantané"*
- *"Intégration: fusion de sources hétérogènes (JSON, WFS, NetCDF, CSV)"*
- *"Scalabilité: gestion de diagnostics multiples concurrents"*

---

## Conseil de Présentation

✅ **Commencez toujours par le problème** ("Les assurances ignorent le risque climatique futur")
✅ **Puis la solution** ("Typhoon évalue et affiche le risque dans une maison 3D")
✅ **Puis la technologie** (si on vous demande) ("On use LangGraph pour orchestrer 4 agents")
✅ **Finissez par l'impact** ("Trois segments de clients ciblés, TAM ~1.5B€")

❌ **Ne commencez PAS par la technique** (APIs, LangGraph, etc.) — cela perd les RH immédiatement
❌ **Ne vous perdez PAS dans les détails NetCDF** — mentionnez-les que si on creuse sur la data
❌ **Ne dites PAS "c'est compliqué"** — dites "c'est intégré mais chaque brique est simple"
