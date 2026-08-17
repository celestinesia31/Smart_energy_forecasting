# ============================================================
# APPLICATION STREAMLIT - PRÉVISION ÉNERGÉTIQUE H+1
# ============================================================

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# 1. CONFIGURATION DE LA PAGE
# ============================================================

st.set_page_config(
    page_title="Prévision énergétique",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 2. THÈME VISUEL PERSONNALISÉ
# ============================================================

st.markdown(
    """
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap'
);

html, body, [class*="css"] {
    font-family: "Inter", sans-serif;
}

.stApp {
    background:
        linear-gradient(
            135deg,
            #f4f8fb 0%,
            #edf7f5 55%,
            #fff9e8 100%
        );
    color: #132238;
}

.main .block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* ---------------- SIDEBAR ---------------- */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #102a43 0%,
            #164e63 100%
        );
    border-right: 1px solid rgba(255, 255, 255, 0.10);
}

section[data-testid="stSidebar"] * {
    color: #f8fafc;
}

section[data-testid="stSidebar"] hr {
    border-color: rgba(255, 255, 255, 0.20);
}

section[data-testid="stSidebar"]
div[data-testid="stRadio"] label {
    padding: 0.45rem 0.55rem;
    border-radius: 0.65rem;
    transition: 0.2s ease;
}

section[data-testid="stSidebar"]
div[data-testid="stRadio"] label:hover {
    background-color: rgba(255, 255, 255, 0.10);
}

/* ---------------- TITRES ---------------- */

h1, h2, h3 {
    color: #102a43;
    letter-spacing: -0.02em;
}

h1 {
    font-weight: 700;
}

/* ---------------- KPI ---------------- */

div[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.92);
    border: 1px solid rgba(15, 118, 110, 0.18);
    border-left: 5px solid #0f766e;
    border-radius: 1rem;
    padding: 1rem 1.1rem;
    box-shadow: 0 8px 24px rgba(16, 42, 67, 0.08);
    min-height: 125px;
}

div[data-testid="stMetricLabel"] {
    color: #486581;
    font-weight: 600;
}

div[data-testid="stMetricValue"] {
    color: #102a43;
    font-weight: 700;
    font-size: 1.75rem;
}

/* ---------------- TABLEAUX ---------------- */

div[data-testid="stDataFrame"] {
    background-color: white;
    border: 1px solid #d9e2ec;
    border-radius: 0.9rem;
    overflow: hidden;
    box-shadow: 0 6px 18px rgba(16, 42, 67, 0.06);
}

/* ---------------- INPUTS ---------------- */

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background-color: rgba(255, 255, 255, 0.96);
    border-radius: 0.75rem;
}

/* ---------------- BOUTONS ---------------- */

.stButton > button,
.stDownloadButton > button {
    background:
        linear-gradient(
            90deg,
            #0f766e,
            #0891b2
        );
    color: white;
    border: none;
    border-radius: 0.75rem;
    padding: 0.65rem 1rem;
    font-weight: 650;
    box-shadow: 0 6px 16px rgba(15, 118, 110, 0.20);
    transition: 0.2s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 8px 20px rgba(15, 118, 110, 0.30);
    color: white;
}

/* ---------------- HERO ACCUEIL ---------------- */

.hero {
    background:
        linear-gradient(
            120deg,
            #102a43 0%,
            #0f766e 65%,
            #0891b2 100%
        );
    padding: 2.2rem 2.3rem;
    border-radius: 1.3rem;
    color: white;
    box-shadow: 0 16px 40px rgba(16, 42, 67, 0.20);
    margin-bottom: 1.6rem;
}

.hero h1 {
    color: white;
    margin: 0;
    font-size: 2.7rem;
}

.hero p {
    color: #e0f2fe;
    font-size: 1.08rem;
    margin-top: 0.7rem;
    margin-bottom: 0;
    max-width: 900px;
}

.hero-badge {
    display: inline-block;
    background: rgba(255, 255, 255, 0.14);
    border: 1px solid rgba(255, 255, 255, 0.24);
    padding: 0.35rem 0.75rem;
    border-radius: 999px;
    margin-bottom: 0.9rem;
    font-size: 0.9rem;
    font-weight: 600;
    color: #fef3c7;
}

/* ---------------- CARTES ---------------- */

.info-card {
    background: rgba(255, 255, 255, 0.92);
    border: 1px solid #d9e2ec;
    border-radius: 1rem;
    padding: 1.15rem;
    min-height: 165px;
    box-shadow: 0 8px 22px rgba(16, 42, 67, 0.07);
}

.info-card h3 {
    margin-top: 0;
    color: #0f766e;
}

.section-title {
    margin-top: 1.8rem;
    margin-bottom: 0.8rem;
    padding-left: 0.8rem;
    border-left: 5px solid #f59e0b;
}

.forecast-box {
    background: rgba(255, 255, 255, 0.95);
    border: 1px solid #d9e2ec;
    border-radius: 1rem;
    padding: 1.2rem 1.4rem;
    box-shadow: 0 8px 22px rgba(16, 42, 67, 0.07);
    margin-bottom: 1rem;
}

.forecast-box h3 {
    margin-top: 0;
}

footer {
    visibility: hidden;
}

</style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 3. DÉFINITION DES CHEMINS
# ============================================================

APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent

DATA_DIR = PROJECT_DIR / "data" / "processed"
RESULTS_DIR = PROJECT_DIR / "results"
FIGURES_DIR = PROJECT_DIR / "figures"

DASHBOARD_DATA_FILE = DATA_DIR / "dashboard_data.csv"
FINAL_RESULTS_FILE = RESULTS_DIR / "final_test_results.csv"
POWERBI_PREDICTIONS_FILE = RESULTS_DIR / "powerbi_predictions.csv"
WALK_FORWARD_SUMMARY_FILE = RESULTS_DIR / "walk_forward_summary.csv"
EXTERNAL_VALIDATION_FILE = RESULTS_DIR / "external_validation_germany.csv"


# ============================================================
# 4. CHARGEMENT DES DONNÉES
# ============================================================

@st.cache_data
def load_dashboard_data() -> pd.DataFrame:

    if not DASHBOARD_DATA_FILE.exists():
        raise FileNotFoundError(
            f"Fichier introuvable : {DASHBOARD_DATA_FILE}"
        )

    dataframe = pd.read_csv(
        DASHBOARD_DATA_FILE,
        parse_dates=["Time"]
    )

    return (
        dataframe
        .sort_values("Time")
        .reset_index(drop=True)
    )


@st.cache_data
def load_final_results() -> pd.DataFrame:

    if not FINAL_RESULTS_FILE.exists():
        raise FileNotFoundError(
            f"Fichier introuvable : {FINAL_RESULTS_FILE}"
        )

    return pd.read_csv(FINAL_RESULTS_FILE)


@st.cache_data
def load_test_predictions() -> pd.DataFrame:
    """
    Charge les prédictions finales réalisées sur le jeu de test.

    Pour chaque instant t, les colonnes de prédiction correspondent
    à une prévision à l'horizon H+1.
    """

    if not POWERBI_PREDICTIONS_FILE.exists():
        raise FileNotFoundError(
            f"Fichier introuvable : {POWERBI_PREDICTIONS_FILE}"
        )

    dataframe = pd.read_csv(
        POWERBI_PREDICTIONS_FILE,
        parse_dates=["Time"]
    )

    return (
        dataframe
        .sort_values("Time")
        .reset_index(drop=True)
    )


@st.cache_data
def load_walk_forward_summary() -> pd.DataFrame:
    """
    Charge la synthèse de la validation temporelle walk-forward.
    """

    if not WALK_FORWARD_SUMMARY_FILE.exists():
        raise FileNotFoundError(
            f"Fichier introuvable : {WALK_FORWARD_SUMMARY_FILE}"
        )

    return pd.read_csv(WALK_FORWARD_SUMMARY_FILE)


@st.cache_data
def load_external_validation() -> pd.DataFrame:
    """
    Charge les résultats de la validation externe sur les données allemandes.
    """

    if not EXTERNAL_VALIDATION_FILE.exists():
        raise FileNotFoundError(
            f"Fichier introuvable : {EXTERNAL_VALIDATION_FILE}"
        )

    return pd.read_csv(EXTERNAL_VALIDATION_FILE)


try:

    energy_df = load_dashboard_data()
    results_df = load_final_results()
    predictions_df = load_test_predictions()
    walk_forward_df = load_walk_forward_summary()
    external_validation_df = load_external_validation()

except FileNotFoundError as error:

    st.error(str(error))

    st.info(
        "Exécute d'abord les notebooks nécessaires afin de créer "
        "les fichiers de données et de résultats."
    )

    st.stop()


# ============================================================
# 5. FONCTIONS UTILITAIRES
# ============================================================

def apply_energy_theme(
    figure,
    height: int = 500
):

    figure.update_layout(
        height=height,
        template="plotly_white",
        font={
            "family": "Inter, sans-serif",
            "color": "#243b53"
        },
        title={
            "font": {
                "size": 22,
                "color": "#102a43"
            },
            "x": 0.02
        },
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(255, 255, 255, 0.78)",
        hovermode="x unified",
        margin={
            "l": 40,
            "r": 25,
            "t": 75,
            "b": 45
        },
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "right",
            "x": 1
        }
    )

    figure.update_xaxes(
        showgrid=True,
        gridcolor="rgba(72, 101, 129, 0.12)",
        zeroline=False
    )

    figure.update_yaxes(
        showgrid=True,
        gridcolor="rgba(72, 101, 129, 0.12)",
        zeroline=False
    )

    return figure


def display_time_series(
    dataframe: pd.DataFrame,
    column: str,
    title: str,
    y_label: str,
    color: str = "#0891b2"
) -> None:

    figure = px.line(
        dataframe,
        x="Time",
        y=column,
        title=title,
        labels={
            "Time": "Temps",
            column: y_label
        }
    )

    figure.update_traces(
        line={
            "color": color,
            "width": 1.4
        }
    )

    figure = apply_energy_theme(
        figure,
        height=500
    )

    st.plotly_chart(
        figure,
        use_container_width=True
    )


def display_real_vs_target(
    dataframe: pd.DataFrame,
    real_column: str,
    target_column: str,
    title: str,
    y_label: str
) -> None:

    chart_data = dataframe[
        ["Time", real_column, target_column]
    ].copy()

    chart_data = chart_data.rename(
        columns={
            real_column: "Valeur actuelle",
            target_column: "Valeur observée à +1 h"
        }
    )

    figure = px.line(
        chart_data,
        x="Time",
        y=[
            "Valeur actuelle",
            "Valeur observée à +1 h"
        ],
        title=title,
        labels={
            "Time": "Temps",
            "value": y_label,
            "variable": "Série"
        }
    )

    colors = [
        "#0f766e",
        "#f59e0b"
    ]

    for trace, color in zip(
        figure.data,
        colors
    ):
        trace.update(
            line={
                "color": color,
                "width": 1.6
            }
        )

    figure = apply_energy_theme(
        figure,
        height=500
    )

    st.plotly_chart(
        figure,
        use_container_width=True
    )


def show_saved_figure(
    filename: str,
    caption: str
) -> None:

    figure_path = FIGURES_DIR / filename

    if figure_path.exists():

        st.image(
            str(figure_path),
            caption=caption,
            use_container_width=True
        )

    else:

        st.warning(
            f"Figure non trouvée : {filename}"
        )


def format_value(value) -> str:

    if pd.isna(value):
        return "N/A"

    return f"{float(value):,.2f}".replace(",", " ")


# ============================================================
# 6. PRÉPARATION DES DONNÉES POUR LA DÉMONSTRATION H+1
# ============================================================

current_values = (
    energy_df[
        [
            "Time",
            "PV_production",
            "Wind_production",
            "Electric_demand"
        ]
    ]
    .drop_duplicates(subset=["Time"])
    .copy()
)

demo_df = predictions_df.merge(
    current_values,
    on="Time",
    how="left"
)

demo_df = (
    demo_df
    .sort_values("Time")
    .reset_index(drop=True)
)


# ============================================================
# 7. BARRE LATÉRALE
# ============================================================

st.sidebar.title("⚡ Navigation")

NAVIGATION_OPTIONS = [
    "🏠 Accueil",
    "🎯 Démonstration H+1",
    "📊 Exploration des données",
    "☀️ Production photovoltaïque",
    "🌬️ Production éolienne",
    "⚡ Demande électrique",
    "📈 Performances des modèles",
    "ℹ️ À propos"
]

page = st.sidebar.radio(
    "Sélectionner une page",
    NAVIGATION_OPTIONS,
    key="main_navigation"
)

st.sidebar.divider()

st.sidebar.write("**Période disponible**")

st.sidebar.write(
    f"{energy_df['Time'].min():%d/%m/%Y}"
    f" — "
    f"{energy_df['Time'].max():%d/%m/%Y}"
)

st.sidebar.write(
    f"**Observations :** "
    f"{len(energy_df):,}".replace(",", " ")
)


# ============================================================
# 8. FILTRE TEMPOREL GLOBAL
# ============================================================

minimum_date = energy_df["Time"].min().date()
maximum_date = energy_df["Time"].max().date()

selected_dates = st.sidebar.date_input(
    "Filtrer la période",
    value=(minimum_date, maximum_date),
    min_value=minimum_date,
    max_value=maximum_date
)

if (
    isinstance(selected_dates, tuple)
    and len(selected_dates) == 2
):

    start_date, end_date = selected_dates

    filtered_df = energy_df[
        (energy_df["Time"].dt.date >= start_date)
        & (energy_df["Time"].dt.date <= end_date)
    ].copy()

else:

    filtered_df = energy_df.copy()


if filtered_df.empty:

    st.warning(
        "Aucune observation n'est disponible pour cette période."
    )

    st.stop()


# ============================================================
# 9. TITRE DES PAGES
# ============================================================

if page != "🏠 Accueil":
    st.title(page)


# ============================================================
# 10. PAGE ACCUEIL
# ============================================================

if page == "🏠 Accueil":

    st.markdown(
        """
<div class="hero">
<div class="hero-badge">⚡ Intelligence artificielle & énergies renouvelables</div>
<h1>Système intelligent de prévision énergétique</h1>
<p>Application interactive de prévision à un horizon d'une heure pour la production photovoltaïque, la production éolienne et la demande électrique.</p>
</div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Observations",
        f"{len(energy_df):,}".replace(",", " ")
    )

    col2.metric(
        "Période étudiée",
        f"{energy_df['Time'].dt.year.nunique()} ans"
    )

    col3.metric(
        "Variables prédites",
        "3"
    )

    col4.metric(
        "Horizon de prévision",
        "+1 heure"
    )

    st.markdown(
        '<h2 class="section-title">Domaines de prévision</h2>',
        unsafe_allow_html=True
    )

    card1, card2, card3 = st.columns(3)

    with card1:

        st.markdown(
            """
<div class="info-card">
<h3>☀️ Photovoltaïque</h3>
<p>
Prévision de la production solaire à partir du rayonnement,
de la température et des caractéristiques temporelles.
</p>
</div>
            """,
            unsafe_allow_html=True
        )

    with card2:

        st.markdown(
            """
<div class="info-card">
<h3>🌬️ Éolien</h3>
<p>
Estimation de la production éolienne en exploitant la vitesse
du vent et l'historique énergétique récent.
</p>
</div>
            """,
            unsafe_allow_html=True
        )

    with card3:

        st.markdown(
            """
<div class="info-card">
<h3>⚡ Demande électrique</h3>
<p>
Anticipation de la consommation à partir des cycles temporels,
des conditions météorologiques et des valeurs retardées.
</p>
</div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        '<h2 class="section-title">Aperçu des données</h2>',
        unsafe_allow_html=True
    )

    st.dataframe(
        filtered_df.head(100),
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        '<h2 class="section-title">Architecture du projet</h2>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
1. Audit et contrôle de qualité des données  
2. Prétraitement  
3. Analyse exploratoire  
4. Ingénierie des caractéristiques  
5. Modélisation prédictive  
6. Validation temporelle et évaluation finale  
7. Visualisation et démonstration interactive
        """
    )


# ============================================================
# 11. PAGE DÉMONSTRATION H+1
# ============================================================

elif page == "🎯 Démonstration H+1":

    st.markdown(
        """
Cette page illustre concrètement le fonctionnement du système.

Pour un instant **t** appartenant au jeu de test, le modèle utilise les
informations disponibles à cet instant afin d'estimer la valeur qui sera
observée **une heure plus tard**.

Les prédictions sont ensuite comparées aux valeurs réellement enregistrées
à **t + 1 heure**.
        """
    )

    st.markdown(
        '<h2 class="section-title">'
        'Choisir un instant du jeu de test'
        '</h2>',
        unsafe_allow_html=True
    )

    demo_min_date = demo_df["Time"].min().date()
    demo_max_date = demo_df["Time"].max().date()

    selected_demo_date = st.date_input(
        "Date",
        value=demo_min_date,
        min_value=demo_min_date,
        max_value=demo_max_date,
        key="demo_date"
    )

    available_times_df = demo_df[
        demo_df["Time"].dt.date == selected_demo_date
    ].copy()

    if available_times_df.empty:

        st.warning(
            "Aucune observation du jeu de test n'est disponible "
            "pour cette date."
        )

    else:

        available_times = (
            available_times_df["Time"]
            .dt.strftime("%H:%M")
            .tolist()
        )

        selected_demo_time = st.selectbox(
            "Heure de référence",
            available_times,
            key="demo_time"
        )

        selected_timestamp = pd.Timestamp(
            f"{selected_demo_date} {selected_demo_time}"
        )

        selected_rows = demo_df[
            demo_df["Time"] == selected_timestamp
        ]

        if selected_rows.empty:

            st.warning(
                "Impossible de retrouver cette observation."
            )

        else:

            row = selected_rows.iloc[0]

            forecast_timestamp = (
                selected_timestamp
                + pd.Timedelta(hours=1)
            )

            st.success(
                "Prévision effectuée à "
                f"{selected_timestamp:%d/%m/%Y %H:%M} "
                "pour l'horizon "
                f"{forecast_timestamp:%d/%m/%Y %H:%M}."
            )

            # ------------------------------------------------
            # PHOTOVOLTAÏQUE
            # ------------------------------------------------

            st.markdown(
                '<h2 class="section-title">'
                '☀️ Production photovoltaïque'
                '</h2>',
                unsafe_allow_html=True
            )

            pv1, pv2, pv3, pv4 = st.columns(4)

            pv1.metric(
                "Valeur actuelle",
                format_value(row["PV_production"])
            )

            pv2.metric(
                "Prévision à +1 h",
                format_value(row["PV_predit"])
            )

            pv3.metric(
                "Valeur réelle à +1 h",
                format_value(row["PV_reel"])
            )

            pv4.metric(
                "Erreur absolue",
                format_value(abs(row["PV_erreur"]))
            )

            # ------------------------------------------------
            # ÉOLIEN
            # ------------------------------------------------

            st.markdown(
                '<h2 class="section-title">'
                '🌬️ Production éolienne'
                '</h2>',
                unsafe_allow_html=True
            )

            wind1, wind2, wind3, wind4 = st.columns(4)

            wind1.metric(
                "Valeur actuelle",
                format_value(row["Wind_production"])
            )

            wind2.metric(
                "Prévision à +1 h",
                format_value(row["Wind_predit"])
            )

            wind3.metric(
                "Valeur réelle à +1 h",
                format_value(row["Wind_reel"])
            )

            wind4.metric(
                "Erreur absolue",
                format_value(abs(row["Wind_erreur"]))
            )

            # ------------------------------------------------
            # DEMANDE
            # ------------------------------------------------

            st.markdown(
                '<h2 class="section-title">'
                '⚡ Demande électrique'
                '</h2>',
                unsafe_allow_html=True
            )

            demand1, demand2, demand3, demand4 = st.columns(4)

            demand1.metric(
                "Valeur actuelle",
                format_value(row["Electric_demand"])
            )

            demand2.metric(
                "Prévision à +1 h",
                format_value(row["Demand_predit"])
            )

            demand3.metric(
                "Valeur réelle à +1 h",
                format_value(row["Demand_reel"])
            )

            demand4.metric(
                "Erreur absolue",
                format_value(abs(row["Demand_erreur"]))
            )

            # ------------------------------------------------
            # TABLEAU SYNTHÈSE
            # ------------------------------------------------

            st.markdown(
                '<h2 class="section-title">'
                'Synthèse de la prévision'
                '</h2>',
                unsafe_allow_html=True
            )

            comparison_table = pd.DataFrame(
                {
                    "Cible": [
                        "Production photovoltaïque",
                        "Production éolienne",
                        "Demande électrique"
                    ],
                    "Valeur actuelle": [
                        row["PV_production"],
                        row["Wind_production"],
                        row["Electric_demand"]
                    ],
                    "Prévision H+1": [
                        row["PV_predit"],
                        row["Wind_predit"],
                        row["Demand_predit"]
                    ],
                    "Réel H+1": [
                        row["PV_reel"],
                        row["Wind_reel"],
                        row["Demand_reel"]
                    ],
                    "Erreur signée": [
                        row["PV_erreur"],
                        row["Wind_erreur"],
                        row["Demand_erreur"]
                    ],
                    "Erreur absolue": [
                        abs(row["PV_erreur"]),
                        abs(row["Wind_erreur"]),
                        abs(row["Demand_erreur"])
                    ]
                }
            )

            numeric_demo_columns = [
                "Valeur actuelle",
                "Prévision H+1",
                "Réel H+1",
                "Erreur signée",
                "Erreur absolue"
            ]

            comparison_table[numeric_demo_columns] = (
                comparison_table[numeric_demo_columns]
                .round(2)
            )

            st.dataframe(
                comparison_table,
                use_container_width=True,
                hide_index=True
            )

            # ------------------------------------------------
            # GRAPHIQUE PRÉDIT VS RÉEL
            # ------------------------------------------------

            chart_table = comparison_table[
                [
                    "Cible",
                    "Prévision H+1",
                    "Réel H+1"
                ]
            ].copy()

            comparison_figure = px.bar(
                chart_table,
                x="Cible",
                y=[
                    "Prévision H+1",
                    "Réel H+1"
                ],
                barmode="group",
                title=(
                    "Prévisions et valeurs réellement "
                    "observées à +1 heure"
                ),
                labels={
                    "value": "Valeur",
                    "variable": "Série"
                },
                color_discrete_map={
                    "Prévision H+1": "#0891b2",
                    "Réel H+1": "#102a43"
                }
            )

            comparison_figure = apply_energy_theme(
                comparison_figure,
                height=480
            )

            st.plotly_chart(
                comparison_figure,
                use_container_width=True
            )

            # ------------------------------------------------
            # BASELINE NAÏVE
            # ------------------------------------------------

            with st.expander(
                "Comparer également avec la baseline naïve"
            ):

                baseline_columns = [
                    "PV_naif",
                    "Wind_naif",
                    "Demand_naif"
                ]

                if all(
                    column in row.index
                    for column in baseline_columns
                ):

                    baseline_table = pd.DataFrame(
                        {
                            "Cible": [
                                "Production photovoltaïque",
                                "Production éolienne",
                                "Demande électrique"
                            ],
                            "Modèle ML": [
                                row["PV_predit"],
                                row["Wind_predit"],
                                row["Demand_predit"]
                            ],
                            "Baseline naïve": [
                                row["PV_naif"],
                                row["Wind_naif"],
                                row["Demand_naif"]
                            ],
                            "Réel H+1": [
                                row["PV_reel"],
                                row["Wind_reel"],
                                row["Demand_reel"]
                            ]
                        }
                    )

                    baseline_table[
                        [
                            "Modèle ML",
                            "Baseline naïve",
                            "Réel H+1"
                        ]
                    ] = (
                        baseline_table[
                            [
                                "Modèle ML",
                                "Baseline naïve",
                                "Réel H+1"
                            ]
                        ]
                        .round(2)
                    )

                    st.dataframe(
                        baseline_table,
                        use_container_width=True,
                        hide_index=True
                    )

                else:

                    st.info(
                        "Les colonnes de la baseline naïve ne sont "
                        "pas disponibles dans ce fichier."
                    )


# ============================================================
# 12. PAGE EXPLORATION
# ============================================================

elif page == "📊 Exploration des données":

    variable_options = {
        "Température": "Temperature",
        "Humidité": "Humidity",
        "Vitesse du vent": "Wind_speed",
        "Rayonnement solaire GHI": "GHI",
        "Production photovoltaïque": "PV_production",
        "Production éolienne": "Wind_production",
        "Demande électrique": "Electric_demand"
    }

    selected_label = st.selectbox(
        "Variable à visualiser",
        list(variable_options.keys())
    )

    selected_column = variable_options[selected_label]

    display_time_series(
        filtered_df,
        selected_column,
        f"Évolution de la variable : {selected_label}",
        selected_label,
        color="#0f766e"
    )

    st.markdown(
        '<h2 class="section-title">'
        'Statistiques descriptives'
        '</h2>',
        unsafe_allow_html=True
    )

    statistics = (
        filtered_df[selected_column]
        .describe()
        .to_frame(name="Valeur")
    )

    st.dataframe(
        statistics,
        use_container_width=True
    )

    histogram = px.histogram(
        filtered_df,
        x=selected_column,
        nbins=50,
        title=f"Distribution : {selected_label}",
        color_discrete_sequence=["#0f766e"]
    )

    histogram = apply_energy_theme(
        histogram,
        height=450
    )

    st.plotly_chart(
        histogram,
        use_container_width=True
    )


# ============================================================
# 13. PAGE PHOTOVOLTAÏQUE
# ============================================================

elif page == "☀️ Production photovoltaïque":

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Production moyenne",
        f"{filtered_df['PV_production'].mean():.2f}"
    )

    col2.metric(
        "Production maximale",
        f"{filtered_df['PV_production'].max():.2f}"
    )

    col3.metric(
        "GHI moyen",
        f"{filtered_df['GHI'].mean():.2f}"
    )

    display_time_series(
        filtered_df,
        "PV_production",
        "Évolution de la production photovoltaïque",
        "Production photovoltaïque",
        color="#16A085"
    )

    display_real_vs_target(
        filtered_df,
        "PV_production",
        "target_PV_production_1h",
        (
            "Production actuelle et production observée "
            "une heure plus tard"
        ),
        "Production photovoltaïque"
    )

    st.markdown(
        '<h2 class="section-title">'
        'Évaluation finale du modèle'
        '</h2>',
        unsafe_allow_html=True
    )

    show_saved_figure(
        "pv_prediction_vs_real.png",
        "Valeurs réelles et prédictions photovoltaïques"
    )

    show_saved_figure(
        "pv_residuals.png",
        "Distribution des résidus photovoltaïques"
    )


# ============================================================
# 14. PAGE ÉOLIENNE
# ============================================================

elif page == "🌬️ Production éolienne":

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Production moyenne",
        f"{filtered_df['Wind_production'].mean():.2f}"
    )

    col2.metric(
        "Production maximale",
        f"{filtered_df['Wind_production'].max():.2f}"
    )

    col3.metric(
        "Vitesse moyenne du vent",
        f"{filtered_df['Wind_speed'].mean():.2f}"
    )

    display_time_series(
        filtered_df,
        "Wind_production",
        "Évolution de la production éolienne",
        "Production éolienne",
        color="#2F80ED"
    )

    display_real_vs_target(
        filtered_df,
        "Wind_production",
        "target_Wind_production_1h",
        (
            "Production actuelle et production observée "
            "une heure plus tard"
        ),
        "Production éolienne"
    )

    st.markdown(
        '<h2 class="section-title">'
        'Évaluation finale du modèle'
        '</h2>',
        unsafe_allow_html=True
    )

    show_saved_figure(
        "wind_prediction_vs_real.png",
        "Valeurs réelles et prédictions éoliennes"
    )

    show_saved_figure(
        "wind_residuals.png",
        "Distribution des résidus éoliens"
    )


# ============================================================
# 15. PAGE DEMANDE ÉLECTRIQUE
# ============================================================

elif page == "⚡ Demande électrique":

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Demande moyenne",
        f"{filtered_df['Electric_demand'].mean():.2f}"
    )

    col2.metric(
        "Demande maximale",
        f"{filtered_df['Electric_demand'].max():.2f}"
    )

    col3.metric(
        "Température moyenne",
        f"{filtered_df['Temperature'].mean():.2f} °C"
    )

    display_time_series(
        filtered_df,
        "Electric_demand",
        "Évolution de la demande électrique",
        "Demande électrique",
        color="#E66B32"
    )

    display_real_vs_target(
        filtered_df,
        "Electric_demand",
        "target_Electric_demand_1h",
        (
            "Demande actuelle et demande observée "
            "une heure plus tard"
        ),
        "Demande électrique"
    )

    st.markdown(
        '<h2 class="section-title">'
        'Évaluation finale du modèle'
        '</h2>',
        unsafe_allow_html=True
    )

    show_saved_figure(
        "demand_prediction_vs_real.png",
        "Valeurs réelles et prédictions de la demande"
    )

    show_saved_figure(
        "demand_residuals.png",
        "Distribution des résidus de la demande"
    )


# ============================================================
# 16. PAGE PERFORMANCES
# ============================================================

elif page == "📈 Performances des modèles":

    st.markdown(
        """
Les performances présentées ci-dessous ont été calculées sur
l'ensemble de test, jamais utilisé lors de l'entraînement ni lors
de la sélection des modèles.

Les modèles retenus sont également comparés à une baseline
naïve saisonnière journalière.
        """
    )

    required_columns = {
        "Cible",
        "Modèle",
        "MAE_test",
        "RMSE_test",
        "R2_test",
        "Gain_RMSE_vs_naif_%"
    }

    missing_columns = required_columns.difference(
        results_df.columns
    )

    if missing_columns:

        st.error(
            "Le fichier final_test_results.csv ne contient pas "
            "toutes les colonnes attendues : "
            + ", ".join(sorted(missing_columns))
        )

        st.stop()

    display_results = results_df.copy()

    numeric_columns = [
        "MAE_test",
        "RMSE_test",
        "R2_test",
        "Gain_RMSE_vs_naif_%"
    ]

    display_results[numeric_columns] = (
        display_results[numeric_columns]
        .round(3)
    )

    st.dataframe(
        display_results,
        use_container_width=True,
        hide_index=True
    )

    model_results = results_df[
        results_df["Modèle"]
        != "Naïf saisonnier journalier"
    ].copy()

    st.markdown(
        '<h2 class="section-title">'
        'Gains par rapport à la baseline'
        '</h2>',
        unsafe_allow_html=True
    )

    metric_columns = st.columns(
        max(1, len(model_results))
    )

    for column, (_, result_row) in zip(
        metric_columns,
        model_results.iterrows()
    ):

        column.metric(
            label=result_row["Cible"],
            value=(
                f'{result_row["Gain_RMSE_vs_naif_%"]:.1f} %'
            ),
            delta="Réduction du RMSE"
        )

    comparison_results = results_df.copy()

    # --------------------------------------------------------
    # RMSE TEST
    # --------------------------------------------------------

    rmse_figure = px.bar(
        comparison_results,
        x="Cible",
        y="RMSE_test",
        color="Modèle",
        barmode="group",
        title="RMSE : modèles retenus et baseline saisonnière",
        text_auto=".1f",
        color_discrete_map={
            "HistGradientBoosting": "#16A085",
            "Régression linéaire": "#F59E0B",
            "Naïf saisonnier journalier": "#2F80ED"
        }
    )

    rmse_figure.update_traces(
        textposition="outside"
    )

    rmse_figure = apply_energy_theme(
        rmse_figure,
        height=500
    )

    st.plotly_chart(
        rmse_figure,
        use_container_width=True
    )

    # --------------------------------------------------------
    # R² TEST
    # --------------------------------------------------------

    r2_figure = px.bar(
        comparison_results,
        x="Cible",
        y="R2_test",
        color="Modèle",
        barmode="group",
        title="Coefficient de détermination sur le jeu de test",
        text_auto=".3f",
        color_discrete_map={
            "HistGradientBoosting": "#16A085",
            "Régression linéaire": "#F59E0B",
            "Naïf saisonnier journalier": "#2F80ED"
        }
    )

    r2_figure.update_traces(
        textposition="outside"
    )

    r2_figure = apply_energy_theme(
        r2_figure,
        height=500
    )

    st.plotly_chart(
        r2_figure,
        use_container_width=True
    )

    # --------------------------------------------------------
    # WALK-FORWARD
    # --------------------------------------------------------

    st.markdown(
        '<h2 class="section-title">'
        'Validation temporelle walk-forward'
        '</h2>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
La validation walk-forward a été réalisée sur **trois fenêtres
temporelles successives**, uniquement à partir des ensembles
d'entraînement et de validation.

Le jeu de test final n'a jamais été utilisé pendant cette étape.

Cette analyse permet de vérifier que les performances des modèles
ne dépendent pas uniquement d'une seule période de validation.
        """
    )

    walk_forward_display = walk_forward_df.copy()

    walk_numeric_columns = [
        column
        for column in [
            "RMSE_moyen",
            "RMSE_ecart_type",
            "MAE_moyenne",
            "R2_moyen",
            "R2_ecart_type"
        ]
        if column in walk_forward_display.columns
    ]

    if walk_numeric_columns:

        walk_forward_display[
            walk_numeric_columns
        ] = (
            walk_forward_display[
                walk_numeric_columns
            ]
            .round(3)
        )

    st.dataframe(
        walk_forward_display,
        use_container_width=True,
        hide_index=True
    )

    if {
        "Cible",
        "RMSE_moyen"
    }.issubset(walk_forward_df.columns):

        walk_rmse_figure = px.bar(
            walk_forward_df,
            x="Cible",
            y="RMSE_moyen",
            title=(
                "RMSE moyen lors de la validation "
                "temporelle walk-forward"
            ),
            text_auto=".1f",
            color="Cible",
            color_discrete_map={
                "Production photovoltaïque": "#16A085",
                "Production éolienne": "#2F80ED",
                "Demande électrique": "#E66B32"
            }
        )

        walk_rmse_figure.update_traces(
            textposition="outside"
        )

        walk_rmse_figure.update_layout(
            showlegend=False
        )

        walk_rmse_figure = apply_energy_theme(
            walk_rmse_figure,
            height=470
        )

        st.plotly_chart(
            walk_rmse_figure,
            use_container_width=True
        )

    # --------------------------------------------------------
    # VALIDATION EXTERNE ALLEMAGNE
    # --------------------------------------------------------

    st.markdown(
        '<h2 class="section-title">'
        'Validation externe — Allemagne'
        '</h2>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
Afin d'évaluer la **transférabilité de la méthodologie H+1**, le même
protocole général a été appliqué à un jeu de données énergétique externe
indépendant relatif au système électrique allemand (OPSD / ENTSO-E).

Les modèles ont été **réentraînés sur les données allemandes** : cette
expérience évalue donc la transférabilité de la démarche méthodologique,
et non le transfert direct des modèles entraînés sur le dataset principal.
        """
    )

    external_display = external_validation_df.copy()

    external_numeric_columns = [
        column
        for column in [
            "MAE modèle",
            "RMSE modèle",
            "R2 modèle",
            "RMSE baseline",
            "Gain RMSE vs baseline (%)",
        ]
        if column in external_display.columns
    ]

    if external_numeric_columns:
        external_display[external_numeric_columns] = (
            external_display[external_numeric_columns]
            .round(3)
        )

    st.dataframe(
        external_display,
        use_container_width=True,
        hide_index=True
    )

    required_external_columns = {
        "Cible",
        "Gain RMSE vs baseline (%)"
    }

    if required_external_columns.issubset(
        external_validation_df.columns
    ):

        external_gain_columns = st.columns(
            len(external_validation_df)
        )

        for column, (_, result_row) in zip(
            external_gain_columns,
            external_validation_df.iterrows()
        ):

            column.metric(
                label=result_row["Cible"],
                value=(
                    f'{result_row["Gain RMSE vs baseline (%)"]:.1f} %'
                ),
                delta="Gain RMSE externe"
            )

    show_saved_figure(
        "external_validation_germany_rmse_vs_baseline.png",
        (
            "Validation externe Allemagne — RMSE du modèle retenu "
            "comparé à la baseline naïve"
        )
    )

    st.markdown(
        """
**Lecture des résultats externes :** la méthodologie conserve une forte
valeur ajoutée pour la production photovoltaïque et la demande électrique.
Pour l'éolien, le coefficient R² reste élevé mais le gain par rapport à la
persistance est faible, ce qui montre l'importance de disposer de variables
météorologiques directement liées au vent.
        """
    )

    # --------------------------------------------------------
    # ANALYSE TEMPORELLE DES ERREURS
    # --------------------------------------------------------

    st.markdown(
        '<h2 class="section-title">'
        'Analyse temporelle des erreurs'
        '</h2>',
        unsafe_allow_html=True
    )

    show_saved_figure(
        "mean_absolute_error_by_hour.png",
        "Erreur absolue moyenne selon l'heure de la journée"
    )

    # --------------------------------------------------------
    # TÉLÉCHARGEMENT
    # --------------------------------------------------------

    csv_data = (
        results_df
        .to_csv(index=False)
        .encode("utf-8")
    )

    st.download_button(
        label="Télécharger les résultats",
        data=csv_data,
        file_name="final_test_results.csv",
        mime="text/csv"
    )


# ============================================================
# 17. PAGE À PROPOS
# ============================================================

elif page == "ℹ️ À propos":

    st.markdown(
        """
## Objectif

Développer un système de prévision à court terme permettant
d'estimer une heure à l'avance :

- la production photovoltaïque ;
- la production éolienne ;
- la demande électrique.

## Méthodologie

Le projet repose sur un pipeline complet comprenant :

- l'audit et le contrôle de qualité des données ;
- le prétraitement ;
- l'analyse exploratoire ;
- l'ingénierie des caractéristiques ;
- la création des cibles de prévision à H+1 ;
- la modélisation prédictive ;
- la sélection des modèles sur validation ;
- la validation temporelle walk-forward ;
- une validation externe sur un jeu de données allemand indépendant ;
- l'évaluation finale sur un jeu de test indépendant ;
- la comparaison avec une baseline saisonnière ;
- l'analyse des erreurs ;
- la restitution dans Power BI et Streamlit.

## Modèles retenus

- **Photovoltaïque :** HistGradientBoosting
- **Éolien :** Régression linéaire
- **Demande électrique :** HistGradientBoosting

## Validation

Les données sont séparées chronologiquement afin de respecter
la structure temporelle du problème.

La stratégie utilisée repose sur :

- **70 %** des observations pour l'entraînement ;
- **15 %** pour la validation ;
- **15 %** pour le test final.

Le jeu de test final est constitué des observations les plus
récentes et n'est pas utilisé pour entraîner ou sélectionner
les modèles.

Une validation temporelle de type **walk-forward** a également
été réalisée sur **trois fenêtres successives**, uniquement à partir
des données d'entraînement et de validation.

Cette approche permet d'étudier la stabilité des performances
dans le temps tout en préservant totalement le jeu de test final.

Une **validation externe** a également été réalisée sur des séries horaires
allemandes issues d'Open Power System Data / ENTSO-E. Les modèles ont été
réentraînés sur ce second jeu de données afin de tester la transférabilité
de la méthodologie H+1 dans un contexte énergétique indépendant. Les gains
de RMSE par rapport à la baseline atteignent environ **79,0 %** pour le
photovoltaïque, **75,7 %** pour la demande électrique et **1,3 %** pour
l'éolien.

## Baseline de référence

Les modèles de Machine Learning sont comparés à une baseline
naïve saisonnière journalière.

Cette baseline utilise comme référence la valeur observée au même
instant de la journée précédente.

Cette comparaison permet de vérifier que les modèles apportent
une amélioration réelle par rapport à une stratégie simple.

## Démonstration H+1

L'application permet de sélectionner un instant du jeu de test et
de rejouer une situation de prévision historique.

Pour chaque cible, elle présente :

- la valeur disponible à l'instant **t** ;
- la prévision du modèle pour **t + 1 heure** ;
- la valeur réellement observée à **t + 1 heure** ;
- l'erreur de prédiction correspondante.

Cette démonstration permet d'illustrer concrètement le
fonctionnement du système sans prétendre réaliser une prévision
temps réel sur des données futures inconnues.

## Limites

Malgré les bonnes performances obtenues, plusieurs limites doivent
être prises en compte :

- les résultats ont été obtenus sur un jeu de données et une période
  historique déterminés ;
- une validation externe a été réalisée sur l'Allemagne, mais la
  généralisation à d'autres pays, sites et contextes énergétiques reste
  à approfondir ;
- l'horizon de prévision est actuellement limité à +1 heure ;
- certaines périodes présentent des erreurs plus importantes,
  notamment pour la production photovoltaïque ;
- l'application constitue un prototype et n'est pas encore connectée
  à des flux de données temps réel.

## Perspectives

Plusieurs prolongements sont envisageables :

- étendre la validation externe à d'autres pays, périodes et sites ;
- extension à plusieurs horizons de prévision, par exemple +2 h,
  +6 h ou +24 h ;
- intégration de véritables prévisions météorologiques disponibles
  au moment de la prédiction ;
- connexion à des flux de données énergétiques en temps réel ;
- mise en place d'un mécanisme de réentraînement périodique ;
- surveillance de la dérive des données et des performances ;
- étude de modèles temporels plus avancés lorsque cela est justifié.

## Technologies

Python, Pandas, NumPy, scikit-learn, Plotly, Streamlit et Power BI.
        """
    )