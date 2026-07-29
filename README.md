# Système Intelligent de Prévision Énergétique

## Présentation

Ce projet de fin d'études a pour objectif de développer un système intelligent capable de prévoir, à un horizon d'une heure :

-  la production photovoltaïque ;
-  la production éolienne ;
-  la demande électrique.

L'ensemble du projet suit un pipeline complet de Data Science, depuis l'audit des données jusqu'au développement d'une application interactive.

---

# Objectifs

Le projet vise à :

- analyser les données énergétiques ;
- préparer les données pour la modélisation ;
- créer de nouvelles caractéristiques temporelles ;
- entraîner plusieurs modèles de Machine Learning ;
- sélectionner les meilleurs modèles ;
- développer une application Streamlit ;
- créer un tableau de bord Power BI.

---

# Technologies utilisées

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Streamlit
- Plotly
- Power BI

---

# Notebooks

- Notebook 01_Audit des données
- Notebook 02_Prétraitement des données
- Notebook 03_Analyse exploratoire
- Notebook 04_Ingénierie des caractéristiques
- Notebook 05_Modélisation prédictive
- Notebook 06_Évaluation des modèles
- Notebook 07_Dashboard interactif

---

# Résultats

| Variable | Modèle retenu | R² |
|-----------|---------------|------|
| Production photovoltaïque | HistGradientBoosting | 0.9895 |
| Production éolienne | Régression linéaire | 0.9517 |
| Demande électrique | HistGradientBoosting | 0.9971 |

---

# Auteur

Projet réalisé dans le cadre d'un Projet de Fin d'Études (PFE) M2.