# Système intelligent de prévision énergétique

## Présentation

Ce projet de fin d'études porte sur le développement d'un système intelligent de prévision à court terme de la production renouvelable et de la demande électrique


L'objectif est de prévoir, à un horizon d'une heure (**H+1**), trois variables énergétiques :

- la production photovoltaïque ;
- la production éolienne ;
- la demande électrique.

Le projet suit une démarche complète de Data Science appliquée aux séries temporelles : audit et préparation des données, analyse exploratoire, ingénierie des caractéristiques, modélisation, évaluation temporelle et restitution des résultats.

Une attention particulière est accordée à la **robustesse de l'évaluation**. Les performances ne sont pas étudiées uniquement à travers les métriques classiques : les modèles sont également comparés à une baseline, évalués sur un jeu de test chronologiquement isolé, soumis à une validation walk-forward et étudiés dans deux contextes externes, l'Allemagne et le Maroc.

Le projet comprend également une application interactive développée avec **Streamlit** ainsi qu'un tableau de bord **Power BI**.

---

## Objectifs

Les principaux objectifs du projet sont :

- analyser et contrôler la qualité des données énergétiques ;
- préparer des séries temporelles adaptées à la modélisation ;
- construire un problème supervisé de prévision à l'horizon H+1 ;
- créer des caractéristiques temporelles et historiques pertinentes ;
- comparer une approche linéaire à une approche non linéaire ;
- mesurer l'apport réel des modèles par rapport à une baseline ;
- respecter la chronologie des données lors de l'entraînement et de l'évaluation ;
- sélectionner les modèles sans utiliser le jeu de test final ;
- étudier la stabilité des performances dans le temps ;
- évaluer la transférabilité de la méthodologie sur des données externes ;
- développer une interface Streamlit pour l'exploration et la démonstration des résultats ;
- restituer les principaux indicateurs dans Power BI.

---

## Problématique

Les systèmes électriques doivent continuellement maintenir un équilibre entre production et consommation.

Cette problématique devient plus complexe avec l'intégration des énergies renouvelables. La production photovoltaïque dépend fortement du cycle jour/nuit et des conditions météorologiques, tandis que la production éolienne varie selon la dynamique du vent. La demande électrique possède également des cycles horaires, hebdomadaires et saisonniers.

La problématique étudiée peut être formulée ainsi :

> **Dans quelle mesure des modèles de Machine Learning peuvent-ils améliorer la prévision à une heure de la production photovoltaïque, de la production éolienne et de la demande électrique par rapport à une prévision naïve, tout en conservant des performances stables dans le temps et sur d'autres contextes énergétiques ?**

---

## Méthodologie

Le projet est organisé autour des étapes suivantes :

1. audit et contrôle de qualité des données ;
2. prétraitement et mise en cohérence temporelle ;
3. analyse exploratoire ;
4. ingénierie des caractéristiques ;
5. construction des cibles à H+1 ;
6. séparation chronologique en ensembles d'entraînement, de validation et de test ;
7. construction d'une baseline ;
8. entraînement et comparaison des modèles ;
9. sélection des modèles sur le jeu de validation ;
10. évaluation sur le jeu de test final ;
11. analyse des erreurs ;
12. validation temporelle walk-forward ;
13. validation externe sur l'Allemagne ;
14. étude complémentaire de transférabilité sur le Maroc ;
15. restitution avec Streamlit et Power BI.

Cette organisation permet de conserver la chronologie des séries et de limiter les risques de fuite d'information entre les différentes phases expérimentales.

---

# Jeux de données

## Jeu de données principal

Le fichier principal utilisé dans le pipeline est :

```text
data/raw/Database.csv
```

Il contient notamment les variables :

```text
Time
Season
Day_of_the_week
DHI
DNI
GHI
Wind_speed
Humidity
Temperature
PV_production
Wind_production
Electric_demand
```

Le dataset principal contient **315 648 observations à une fréquence de cinq minutes**, couvrant la période 2019–2021.

Une heure correspond donc à **12 pas de temps** lors de la construction des cibles H+1.

Ce dataset constitue la base des notebooks d'audit, de prétraitement, d'analyse exploratoire, d'ingénierie des caractéristiques, de modélisation et d'évaluation finale.

> **Remarque sur la provenance :** le fichier `Database.csv` est le jeu de données principal fourni et utilisé dans le cadre du projet. Sa référence publique d'origine n'est pas explicitement documentée dans les notebooks actuels. Elle devra être ajoutée ici si une référence officielle, DOI ou page de téléchargement est confirmée.

---

## Données de validation externe / Allemagne

La validation externe allemande repose sur deux jeux de données d'**Open Power System Data (OPSD)** :

```text
data/raw/time_series_60min_singleindex.csv
data/raw/weather_data.csv
```

Le premier contient des séries électriques européennes à résolution horaire, notamment la charge, la production solaire et la production éolienne. La version utilisée correspond au package **Time series — 2020-10-06**, dont les données proviennent principalement de la plateforme **ENTSO-E Transparency**.

Le second contient des données météorologiques horaires agrégées par pays, notamment la température ainsi que le rayonnement direct et diffus. La version utilisée correspond au package **Weather Data — 2020-09-16**.

Pour l'Allemagne, les variables utilisées sont notamment :

```text
DE_load_actual_entsoe_transparency
DE_solar_generation_actual
DE_wind_generation_actual
DE_temperature
DE_radiation_direct_horizontal
DE_radiation_diffuse_horizontal
```

Les modèles sont réentraînés sur ce nouveau contexte tout en conservant le même protocole de prévision H+1.

Cette expérimentation évalue donc la **transférabilité de la méthodologie**, et non le transfert direct des modèles entraînés sur le dataset principal.

### Références

- Open Power System Data. *Data Package Time series*, version 2020-10-06. DOI : https://doi.org/10.25832/time_series/2020-10-06
- Open Power System Data. *Data Package Weather Data*, version 2020-09-16. DOI : https://doi.org/10.25832/weather_data/2020-09-16
- ENTSO-E Transparency Platform : https://transparency.entsoe.eu/

---

## Données utilisées pour l'étude du Maroc

Le dataset marocain utilisé dans le projet est stocké localement sous le nom :

```text
data/raw/morocco_data.csv
```

Il provient du jeu de données :

**Hourly wind and solar capacity factors and electricity demand profiles for 164 countries**, publié sur Zenodo.

Le dataset fournit, pour 164 pays, des profils horaires nationaux de :

- facteur de capacité éolien ;
- facteur de capacité solaire ;
- demande électrique.

Pour le Maroc, les données couvrent une année représentative, **2015**, avec une résolution horaire.

Le fichier contient **8 760 observations**, soit 365 jours × 24 heures.

Les variables principales sont notamment :

```text
time
demand_GW
baseload_GW
heating_GW
cooling_GW
wind_onshore_CF
wind_offshore_CF
solar_CF
```

Les trois séries retenues dans l'étude sont :

- `demand_GW` pour la demande électrique ;
- `solar_CF` pour le solaire ;
- `wind_onshore_CF` pour l'éolien terrestre.

Les profils solaire et éolien sont issus de **Renewables.ninja** et la demande de **Demand.ninja**. Ils correspondent à des profils modélisés à l'échelle nationale.

Les séries `solar_CF` et `wind_onshore_CF` sont des **facteurs de capacité**. Elles ne représentent donc pas directement des productions électriques mesurées en GW.

Cette expérimentation doit ainsi être interprétée comme une **étude de transférabilité méthodologique** dans un contexte marocain et non comme une validation opérationnelle du réseau électrique marocain.

### Référence

- Nathan Johnson. *Hourly wind and solar capacity factors and electricity demand profiles for 164 countries*. Zenodo : https://zenodo.org/records/17853401

---

# Préparation et contrôle de qualité

Plusieurs contrôles sont réalisés avant la modélisation :

- conversion et contrôle des timestamps ;
- détection des doublons ;
- analyse des valeurs manquantes ;
- vérification de la fréquence des observations ;
- contrôle de la continuité temporelle ;
- analyse des valeurs extrêmes ;
- contrôle de la cohérence physique des variables.

L'ordre chronologique des observations est conservé pendant toute la préparation.

---

## Construction de la prévision H+1

Pour chaque variable énergétique, l'objectif est de prédire la valeur observée une heure plus tard.

Le principe est simple :

```text
Informations disponibles à l'instant t
---------------------------------------
Prévision de la valeur à t + 1 heure
```

Dans le dataset principal, la fréquence est de cinq minutes. Une prévision à H+1 correspond donc à **12 pas de temps** :

```python
target_H1 = target.shift(-12)
```

Dans les datasets externes horaires Allemagne et Maroc, H+1 correspond à un seul pas :

```python
target_H1 = target.shift(-1)
```

La continuité temporelle est contrôlée afin de vérifier que les observations utilisées correspondent réellement à l'horizon prévu.

---

# Ingénierie des caractéristiques

Le feature engineering vise à fournir aux modèles des variables représentant :

- les cycles horaires, hebdomadaires et saisonniers ;
- les valeurs historiques des séries énergétiques ;
- les dynamiques récentes à travers des statistiques glissantes ;
- les conditions météorologiques disponibles.

Des variables cycliques sont notamment créées pour l'heure, le jour de la semaine et le mois.

Exemple pour l'heure :

```python
Hour_sin = np.sin(2 * np.pi * Hour / 24)
Hour_cos = np.cos(2 * np.pi * Hour / 24)
```

Les variables retardées et les statistiques mobiles sont construites uniquement à partir d'informations disponibles dans le passé afin d'éviter les fuites temporelles.

---

# Protocole expérimental

## Découpage chronologique

Les observations ne sont pas mélangées aléatoirement.

Le découpage principal respecte l'ordre temporel :

```text
Entraînement : 70 %
Validation    : 15 %
Test final    : 15 %
```

Le jeu de validation sert à comparer et sélectionner les modèles.

Le jeu de test final reste isolé pendant l'entraînement et la sélection. Il n'est utilisé qu'après le choix définitif des modèles.

---

## Baseline de référence

Dans le pipeline principal, les modèles de Machine Learning sont comparés à une **baseline naïve saisonnière journalière**.

Le dataset principal étant échantillonné toutes les cinq minutes, une journée représente :

```text
24 × 60 / 5 = 288 pas de temps
```

La baseline utilise donc comme référence la valeur observée au même instant de la journée précédente.

Dans les expérimentations externes Allemagne et Maroc, une baseline de persistance à court terme est également utilisée pour mesurer l'apport réel du modèle à H+1.

Le gain relatif en RMSE est calculé selon :

```text
Gain (%) = (RMSE baseline - RMSE modèle) / RMSE baseline × 100
```

Un gain positif indique que le modèle améliore la baseline.

---

# Modèles étudiés

L'étude se concentre volontairement sur deux familles de modèles.

## Régression linéaire

La régression linéaire constitue une approche simple, interprétable et peu complexe.

Elle permet de déterminer si les relations présentes dans les données peuvent être suffisamment représentées par un modèle linéaire.

## HistGradientBoostingRegressor

`HistGradientBoostingRegressor`, disponible dans scikit-learn, permet de modéliser des relations non linéaires et des interactions plus complexes entre les variables.

Il constitue ainsi un contraste pertinent avec la régression linéaire pour des données énergétiques tabulaires.

## Justification du choix des modèles

L'objectif du projet n'est pas de multiplier les algorithmes afin de rechercher uniquement le meilleur score possible.

Le protocole repose sur trois niveaux de comparaison :

```text
Baseline
--------
Modèle linéaire
--------
Modèle non linéaire
```

Cette approche permet de répondre successivement à trois questions :

1. le Machine Learning apporte-t-il une amélioration par rapport à une stratégie naïve ?
2. une relation linéaire est-elle suffisante ?
3. la modélisation de relations non linéaires apporte-t-elle un gain supplémentaire ?

L'effort expérimental est ensuite consacré à la robustesse de l'évaluation : séparation chronologique, test final isolé, analyse des erreurs, validation walk-forward et expérimentations sur des jeux de données externes.

Le projet privilégie ainsi **la profondeur de validation à la multiplication des algorithmes**.

---

# Métriques d'évaluation

Trois métriques principales sont utilisées :

- **MAE - Mean Absolute Error** ;
- **RMSE - Root Mean Squared Error** ;
- **R² - coefficient de détermination**.

Un R² élevé n'est pas considéré comme une preuve suffisante de performance. Il est interprété conjointement avec les erreurs MAE/RMSE et la comparaison à la baseline.

---

# Résultats du pipeline principal

La sélection réalisée sur le jeu de validation conduit aux modèles suivants :

| Cible | Modèle retenu | MAE test | RMSE test | R² test | Gain RMSE vs baseline |
|---|---|---:|---:|---:|---:|
| Production photovoltaïque | HistGradientBoosting | ≈ 269,95 | ≈ 470,21 | ≈ 0,9895 | ≈ 51,67 % |
| Production éolienne | Régression linéaire | ≈ 169,93 | ≈ 264,16 | ≈ 0,9517 | ≈ 78,05 % |
| Demande électrique | HistGradientBoosting | ≈ 200,83 | ≈ 271,56 | ≈ 0,9971 | ≈ 85,46 % |

Les trois cibles ne conduisent donc pas au même modèle.

HistGradientBoosting est retenu pour le photovoltaïque et la demande, tandis que la régression linéaire reste préférable pour l'éolien.

---

# Analyse des erreurs

L'évaluation ne se limite pas aux métriques globales.

Une analyse temporelle des erreurs est également réalisée afin d'étudier les périodes pendant lesquelles les prévisions sont les plus difficiles.

L'erreur absolue moyenne est notamment étudiée selon l'heure de la journée.

La figure correspondante est générée dans :

```text
figures/mean_absolute_error_by_hour.png
```

---

# Validation temporelle walk-forward

Une validation de type **walk-forward** est réalisée sur trois fenêtres temporelles successives, uniquement à partir des ensembles d'entraînement et de validation.

Cette approche permet d'étudier la stabilité temporelle des performances sans utiliser le jeu de test final pendant la sélection.

Les résultats sont enregistrés dans :

```text
results/walk_forward_results.csv
results/walk_forward_summary.csv
```

et une figure est générée dans :

```text
figures/walk_forward_rmse.png
```

Les performances moyennes observées sont notamment :

| Cible | RMSE moyen | R² moyen |
|---|---:|---:|
| Production photovoltaïque | ≈ 440,94 | ≈ 0,9897 |
| Production éolienne | ≈ 240,60 | ≈ 0,9617 |
| Demande électrique | ≈ 318,06 | ≈ 0,9942 |

---

# Validation externe / Allemagne

La méthodologie H+1 est évaluée sur un jeu de données allemand indépendant.

Les résultats finaux obtenus sont :

| Cible | Modèle retenu | RMSE modèle | R² | RMSE baseline | Gain RMSE |
|---|---|---:|---:|---:|---:|
| Production photovoltaïque | HistGradientBoosting | ≈ 474,68 | ≈ 0,996 | ≈ 2 264,06 | ≈ 79,03 % |
| Production éolienne | Régression linéaire | ≈ 1 037,59 | ≈ 0,985 | ≈ 1 051,12 | ≈ 1,29 % |
| Demande électrique | HistGradientBoosting | ≈ 604,03 | ≈ 0,996 | ≈ 2 489,68 | ≈ 75,74 % |

Le photovoltaïque et la demande montrent une forte amélioration par rapport à la baseline.

Pour l'éolien, le gain reste faible malgré un R² élevé. Ce résultat illustre l'importance de comparer les modèles à une référence simple plutôt que de s'appuyer uniquement sur le coefficient de détermination.

Les résultats sont enregistrés dans :

```text
results/external_validation_germany.csv
```

---

# Étude de transférabilité / Maroc

Après contrôle temporel et construction des cibles H+1, **8 759 couples horaires valides** sont obtenus.

Le découpage chronologique comprend :

```text
Entraînement : 6 131 observations
Validation    : 1 314 observations
Test final    : 1 314 observations
```

Sur le test final :

| Cible | Modèle retenu | RMSE test | R² test | Gain RMSE vs baseline |
|---|---|---:|---:|---:|
| Production photovoltaïque | HistGradientBoosting | ≈ 0,02025 | ≈ 0,9922 | ≈ 75,97 % |
| Production éolienne | Régression linéaire | ≈ 0,02888 | ≈ 0,9478 | ≈ -3,33 % |
| Demande électrique | HistGradientBoosting | ≈ 0,03357 | ≈ 0,9961 | ≈ 79,71 % |

Pour l'éolien, le modèle sélectionné sur validation devient légèrement moins performant que la baseline sur le test final.

Ce résultat est volontairement conservé : aucun nouveau modèle n'est sélectionné après observation du test. Cette décision préserve l'indépendance de l'évaluation finale et met en évidence une limite réelle de la méthodologie.

Les résultats sont enregistrés dans :

```text
results/morocco_transferability_results.csv
```

---

# Application Streamlit

Une application interactive a été développée avec **Streamlit**.

Le fichier principal est :

```text
app/app.py
```

L'application comprend notamment :

- une page d'accueil présentant le projet ;
- une démonstration historique de prévision H+1 ;
- l'exploration des données ;
- des pages consacrées au photovoltaïque, à l'éolien et à la demande ;
- les performances finales des modèles ;
- la comparaison avec la baseline ;
- la validation walk-forward ;
- la validation externe allemande ;
- l'étude de transférabilité marocaine ;
- l'analyse temporelle des erreurs.

La démonstration H+1 permet de sélectionner un instant du jeu de test puis d'afficher :

- la valeur disponible à l'instant `t` ;
- la prévision du modèle pour `t + 1 heure` ;
- la valeur réellement observée à `t + 1 heure` ;
- l'erreur correspondante.

L'application constitue actuellement un prototype utilisant des données historiques. Elle ne prétend pas réaliser une prévision temps réel sur des données futures inconnues.

---

# Dashboard Power BI

Un tableau de bord complémentaire a été développé avec **Microsoft Power BI**.

Il permet de synthétiser notamment :

- les KPI de production et de demande ;
- les performances des modèles ;
- les valeurs réelles et prédites ;
- les gains par rapport à la baseline ;
- les évolutions temporelles des trois cibles.

Les fichiers correspondants sont conservés dans :

```text
powerbi/
```

Power BI joue ici un rôle de restitution décisionnelle, tandis que Streamlit permet une exploration plus interactive du pipeline et des expérimentations.

---

# Organisation des notebooks

Le projet est organisé en neuf notebooks :

| Notebook | Rôle |
|---|---|
| `01_data_audit.ipynb` | Audit et contrôle de qualité des données |
| `02_data_preprocessing.ipynb` | Prétraitement et nettoyage |
| `03_exploratory_data_analysis.ipynb` | Analyse exploratoire des données |
| `04_feature_engineering.ipynb` | Construction des cibles H+1 et ingénierie des caractéristiques |
| `05_predictive_modeling.ipynb` | Entraînement, validation et sélection des modèles |
| `06_model_evaluation.ipynb` | Évaluation finale, baseline et analyse des erreurs |
| `07_dashboard_streamlit.ipynb` | Préparation des données et ressources nécessaires à Streamlit |
| `08_external_validation.ipynb` | Validation externe de la méthodologie sur l'Allemagne |
| `09_morocco_transferability.ipynb` | Étude complémentaire de transférabilité au Maroc |

Les notebooks doivent être lus dans cet ordre pour suivre la logique complète du projet.

---

# Structure du dépôt

```text
PFE/
├── app/
│   └── app.py
├── data/
│   ├── raw/
│   └── processed/
│ 
├── figures/
├── models/
├── notebooks/
│   ├── 01_data_audit.ipynb
│   ├── 02_data_preprocessing.ipynb
│   ├── 03_exploratory_data_analysis.ipynb
│   ├── 04_feature_engineering.ipynb
│   ├── 05_predictive_modeling.ipynb
│   ├── 06_model_evaluation.ipynb
│   ├── 07_dashboard_streamlit.ipynb
│   ├── 08_external_validation.ipynb
│   └── 09_morocco_transferability.ipynb
├── powerbi/
├── results/
├── .gitignore
├── README.md
└── requirements.txt
```

Les données brutes volumineuses sont conservées localement et exclues du suivi Git lorsque nécessaire.

---

# Environnement logiciel

Le projet utilise principalement :

- Python ;
- Jupyter Notebook / ipykernel ;
- Pandas ;
- NumPy ;
- Matplotlib ;
- scikit-learn ;
- Streamlit ;
- Plotly ;
- Microsoft Power BI ;
- Git et GitHub.

Les versions utilisées sont définies dans :

```text
requirements.txt
```

---

# Reproductibilité

## 1. Cloner le dépôt

```bash
git clone <URL_DU_DEPOT>
cd PFE
```

## 2. Créer un environnement virtuel

Sous Windows :

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Sous Linux ou macOS :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Installer les dépendances

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Préparer les données

Les fichiers sources nécessaires doivent être placés dans :

```text
data/raw/
```

Les gros fichiers bruts ne sont pas nécessairement inclus dans GitHub.

## 5. Exécuter les notebooks

Exécuter les notebooks dans l'ordre :

```text
01_data_audit.ipynb
02_data_preprocessing.ipynb
03_exploratory_data_analysis.ipynb
04_feature_engineering.ipynb
05_predictive_modeling.ipynb
06_model_evaluation.ipynb
07_dashboard_streamlit.ipynb
08_external_validation.ipynb
09_morocco_transferability.ipynb
```

## 6. Lancer Streamlit

Depuis la racine du projet :

```bash
streamlit run app/app.py
```

---

# Limites

### Horizon de prévision

Les expérimentations sont centrées sur H+1. Les performances observées ne peuvent pas être directement extrapolées à des horizons plus longs.

### Périmètre de comparaison des modèles

L'étude se concentre volontairement sur deux familles de modèles : une régression linéaire simple et interprétable, et HistGradientBoosting pour représenter des relations non linéaires plus complexes.

L'objectif n'est pas de constituer un catalogue d'algorithmes, mais d'évaluer rigoureusement les modèles retenus grâce à une baseline, un découpage chronologique, un test indépendant, une validation walk-forward et des expérimentations sur des données externes.

### Validation externe

La validation allemande évalue principalement la transférabilité de la méthodologie puisque les modèles y sont réentraînés.

### Étude marocaine

Les séries solaire et éolienne utilisées pour le Maroc correspondent à des facteurs de capacité modélisés. Cette expérimentation ne constitue donc pas une validation opérationnelle sur des mesures réelles de production marocaines.

### Déploiement

L'application Streamlit constitue actuellement un prototype utilisant des données historiques et n'est pas connectée à des flux énergétiques ou météorologiques temps réel.

---

# Perspectives

Plusieurs prolongements peuvent être envisagés :

- étudier des horizons de prévision plus longs tels que H+3, H+6 ou H+24 ;
- intégrer de véritables prévisions météorologiques futures ;
- étendre les validations externes à d'autres périodes ou zones géographiques ;
- étudier d'autres familles de modèles lorsque la problématique le justifie ;
- quantifier l'incertitude associée aux prédictions ;
- connecter l'application à des flux de données temps réel ;
- automatiser le réentraînement périodique des modèles ;
- mettre en place une surveillance de la dérive des données et des performances.

---

# Conclusion

Ce projet met en œuvre une chaîne complète de prévision énergétique à court terme, depuis la préparation des données jusqu'à la restitution interactive des résultats.

Au-delà de la recherche de bonnes performances prédictives, le travail accorde une place importante à la qualité du protocole expérimental.

La comparaison avec une baseline, la séparation chronologique des données, l'isolation du jeu de test, l'analyse des erreurs, la validation walk-forward et les expérimentations sur l'Allemagne et le Maroc permettent d'étudier les modèles de manière plus rigoureuse qu'une simple comparaison de scores.

Les résultats montrent également que la complexité n'est pas systématiquement synonyme de meilleure performance : HistGradientBoosting est particulièrement efficace pour certaines cibles, tandis que la régression linéaire reste pertinente pour l'éolien.

Le projet aboutit ainsi à un prototype combinant **Machine Learning, séries temporelles, validation expérimentale, visualisation interactive et Business Intelligence**.

---

# Contexte académique

Ce projet a été réalisé dans le cadre d'un **Projet de Fin d'Études de Master 2 - Exploration Informatique des Données et Décisionnel (EI2D)**.

Le sujet de stage porte sur **l'utilisation des techniques d'intelligence artificielle pour l'amélioration de la production énergétique en tenant compte des changements climatiques.**
