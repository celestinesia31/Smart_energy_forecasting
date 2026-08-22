# APPLICATION STREAMLIT
# SYSTÈME INTELLIGENT DE PRÉVISION ÉNERGÉTIQUE
# ET D'AIDE À LA DÉCISION FACE AUX ÉVOLUTIONS CLIMATIQUES

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# ---------------------------------------------------------------------
# 1. CONFIGURATION DE LA PAGE
# ---------------------------------------------------------------------

st.set_page_config(
    page_title="IA, climat et énergie",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------------------
# 2. THÈME VISUEL
# ---------------------------------------------------------------------

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

/* SIDEBAR */

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

/* TITRES */

h1, h2, h3 {
    color: #102a43;
    letter-spacing: -0.02em;
}

h1 {
    font-weight: 700;
}

/* KPI */

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

/* TABLEAUX */

div[data-testid="stDataFrame"] {
    background-color: white;
    border: 1px solid #d9e2ec;
    border-radius: 0.9rem;
    overflow: hidden;
    box-shadow: 0 6px 18px rgba(16, 42, 67, 0.06);
}

/* INPUTS */

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background-color: rgba(255, 255, 255, 0.96);
    border-radius: 0.75rem;
}

/* BOUTONS */

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

/* HERO */

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
    font-size: 2.55rem;
}

.hero p {
    color: #e0f2fe;
    font-size: 1.08rem;
    margin-top: 0.7rem;
    margin-bottom: 0;
    max-width: 1050px;
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

/* CARTES */

.info-card {
    background: rgba(255, 255, 255, 0.92);
    border: 1px solid #d9e2ec;
    border-radius: 1rem;
    padding: 1.15rem;
    min-height: 170px;
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

/* AVERTISSEMENT SCIENTIFIQUE */

.science-note {
    background: rgba(255, 255, 255, 0.92);
    border-left: 5px solid #0891b2;
    border-radius: 0.8rem;
    padding: 1rem 1.2rem;
    margin: 1rem 0;
    box-shadow: 0 5px 16px rgba(16, 42, 67, 0.06);
}

/* BOÎTES DE RISQUE */

.risk-favorable {
    background: #ecfdf5;
    border-left: 6px solid #059669;
    padding: 1rem 1.2rem;
    border-radius: 0.8rem;
}

.risk-vigilance {
    background: #fffbeb;
    border-left: 6px solid #f59e0b;
    padding: 1rem 1.2rem;
    border-radius: 0.8rem;
}

.risk-moderate {
    background: #fff7ed;
    border-left: 6px solid #ea580c;
    padding: 1rem 1.2rem;
    border-radius: 0.8rem;
}

.risk-high {
    background: #fef2f2;
    border-left: 6px solid #dc2626;
    padding: 1rem 1.2rem;
    border-radius: 0.8rem;
}

footer {
    visibility: hidden;
}

</style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------
# 3. CHEMINS
# ---------------------------------------------------------------------

APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent

DATA_DIR = PROJECT_DIR / "data" / "processed"
RESULTS_DIR = PROJECT_DIR / "results"
FIGURES_DIR = PROJECT_DIR / "figures"

DASHBOARD_DATA_FILE = DATA_DIR / "dashboard_data.csv"

FINAL_RESULTS_FILE = (
    RESULTS_DIR
    / "final_test_results.csv"
)

POWERBI_PREDICTIONS_FILE = (
    RESULTS_DIR
    / "powerbi_predictions.csv"
)

WALK_FORWARD_SUMMARY_FILE = (
    RESULTS_DIR
    / "walk_forward_summary.csv"
)

EXTERNAL_VALIDATION_FILE = (
    RESULTS_DIR
    / "external_validation_germany.csv"
)

MOROCCO_TRANSFERABILITY_FILE = (
    RESULTS_DIR
    / "morocco_transferability_results.csv"
)


# Résultats du Notebook 10

CLIMATE_TRENDS_FILE = (
    RESULTS_DIR
    / "climate_trends_fes_1990_2025.csv"
)

CLIMATE_PERIOD_COMPARISON_FILE = (
    RESULTS_DIR
    / "climate_period_comparison_fes.csv"
)

CLIMATE_ENERGY_SUMMARY_FILE = (
    RESULTS_DIR
    / "climate_energy_summary.csv"
)

CLIMATE_SCENARIOS_FILE = (
    RESULTS_DIR
    / "climate_energy_scenarios.csv"
)

CLIMATE_DECISION_FILE = (
    RESULTS_DIR
    / "climate_energy_decision_support.csv"
)

CLIMATE_ADAPTATION_FILE = (
    RESULTS_DIR
    / "climate_energy_adaptation.csv"
)


# ---------------------------------------------------------------------
# 4. CHARGEMENT DES DONNÉES
# ---------------------------------------------------------------------

@st.cache_data
def load_dashboard_data() -> pd.DataFrame:

    if not DASHBOARD_DATA_FILE.exists():
        raise FileNotFoundError(
            f"Fichier introuvable : {DASHBOARD_DATA_FILE}"
        )

    dataframe = pd.read_csv(
        DASHBOARD_DATA_FILE,
        parse_dates=["Time"],
    )

    return (
        dataframe
        .sort_values("Time")
        .reset_index(drop=True)
    )


@st.cache_data
def load_csv_required(
    filepath: Path
) -> pd.DataFrame:

    if not filepath.exists():
        raise FileNotFoundError(
            f"Fichier introuvable : {filepath}"
        )

    return pd.read_csv(filepath)


@st.cache_data
def load_csv_optional(
    filepath: Path
) -> pd.DataFrame:

    if not filepath.exists():
        return pd.DataFrame()

    return pd.read_csv(filepath)


@st.cache_data
def load_test_predictions() -> pd.DataFrame:

    if not POWERBI_PREDICTIONS_FILE.exists():
        raise FileNotFoundError(
            f"Fichier introuvable : {POWERBI_PREDICTIONS_FILE}"
        )

    dataframe = pd.read_csv(
        POWERBI_PREDICTIONS_FILE,
        parse_dates=["Time"],
    )

    return (
        dataframe
        .sort_values("Time")
        .reset_index(drop=True)
    )


try:

    energy_df = load_dashboard_data()

    results_df = load_csv_required(
        FINAL_RESULTS_FILE
    )

    predictions_df = load_test_predictions()

    walk_forward_df = load_csv_required(
        WALK_FORWARD_SUMMARY_FILE
    )

    external_validation_df = load_csv_required(
        EXTERNAL_VALIDATION_FILE
    )

    morocco_transferability_df = load_csv_required(
        MOROCCO_TRANSFERABILITY_FILE
    )

except FileNotFoundError as error:

    st.error(str(error))

    st.info(
        "Exécute d'abord les notebooks nécessaires afin "
        "de générer les fichiers de données et de résultats."
    )

    st.stop()


# Fichiers climatiques :
# chargement optionnel afin de conserver l'application utilisable
# même si une sortie secondaire du Notebook 10 manque.

climate_trends_df = load_csv_optional(
    CLIMATE_TRENDS_FILE
)

climate_period_df = load_csv_optional(
    CLIMATE_PERIOD_COMPARISON_FILE
)

climate_summary_df = load_csv_optional(
    CLIMATE_ENERGY_SUMMARY_FILE
)

climate_scenarios_df = load_csv_optional(
    CLIMATE_SCENARIOS_FILE
)

climate_decision_df = load_csv_optional(
    CLIMATE_DECISION_FILE
)

climate_adaptation_df = load_csv_optional(
    CLIMATE_ADAPTATION_FILE
)


# ---------------------------------------------------------------------
# 5. FONCTIONS UTILITAIRES
# ---------------------------------------------------------------------

def apply_energy_theme(
    figure,
    height: int = 500,
):

    figure.update_layout(
        height=height,
        template="plotly_white",
        font={
            "family": "Inter, sans-serif",
            "color": "#243b53",
        },
        title={
            "font": {
                "size": 22,
                "color": "#102a43",
            },
            "x": 0.02,
        },
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(255, 255, 255, 0.78)",
        margin={
            "l": 40,
            "r": 25,
            "t": 75,
            "b": 45,
        },
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "right",
            "x": 1,
        },
    )

    figure.update_xaxes(
        showgrid=True,
        gridcolor="rgba(72, 101, 129, 0.12)",
        zeroline=False,
    )

    figure.update_yaxes(
        showgrid=True,
        gridcolor="rgba(72, 101, 129, 0.12)",
        zeroline=False,
    )

    return figure


def display_time_series(
    dataframe: pd.DataFrame,
    column: str,
    title: str,
    y_label: str,
    color: str = "#0891b2",
) -> None:

    figure = px.line(
        dataframe,
        x="Time",
        y=column,
        title=title,
        labels={
            "Time": "Temps",
            column: y_label,
        },
    )

    figure.update_traces(
        line={
            "color": color,
            "width": 1.4,
        }
    )

    st.plotly_chart(
        apply_energy_theme(
            figure,
            height=500,
        ),
        use_container_width=True,
    )


def display_real_vs_target(
    dataframe: pd.DataFrame,
    real_column: str,
    target_column: str,
    title: str,
    y_label: str,
) -> None:

    chart_data = dataframe[
        [
            "Time",
            real_column,
            target_column,
        ]
    ].copy()

    chart_data = chart_data.rename(
        columns={
            real_column: "Valeur actuelle",
            target_column: "Valeur observée à +1 h",
        }
    )

    figure = px.line(
        chart_data,
        x="Time",
        y=[
            "Valeur actuelle",
            "Valeur observée à +1 h",
        ],
        title=title,
        labels={
            "Time": "Temps",
            "value": y_label,
            "variable": "Série",
        },
    )

    colors = [
        "#0f766e",
        "#f59e0b",
    ]

    for trace, color in zip(
        figure.data,
        colors,
    ):

        trace.update(
            line={
                "color": color,
                "width": 1.6,
            }
        )

    st.plotly_chart(
        apply_energy_theme(
            figure,
            height=500,
        ),
        use_container_width=True,
    )


def show_saved_figure(
    filename: str,
    caption: str,
) -> None:

    figure_path = FIGURES_DIR / filename

    if figure_path.exists():

        st.image(
            str(figure_path),
            caption=caption,
            use_container_width=True,
        )

    else:

        st.info(
            f"Figure non disponible : {filename}"
        )


def format_value(
    value,
    decimals: int = 2,
) -> str:

    if pd.isna(value):
        return "N/A"

    try:

        return (
            f"{float(value):,.{decimals}f}"
            .replace(",", " ")
        )

    except (ValueError, TypeError):

        return str(value)


def section_title(
    text: str
) -> None:

    st.markdown(
        (
            '<h2 class="section-title">'
            f'{text}'
            '</h2>'
        ),
        unsafe_allow_html=True,
    )


def find_value(
    dataframe: pd.DataFrame,
    indicator_text: str,
) -> str:

    if dataframe.empty:
        return "N/A"

    if not {
        "Indicateur",
        "Résultat",
    }.issubset(dataframe.columns):

        return "N/A"

    mask = (
        dataframe["Indicateur"]
        .astype(str)
        .str.contains(
            indicator_text,
            case=False,
            regex=False,
            na=False,
        )
    )

    if not mask.any():
        return "N/A"

    return str(
        dataframe.loc[
            mask,
            "Résultat",
        ].iloc[0]
    )


def render_risk_box(
    risk_level: str,
    recommendation: str,
) -> None:

    level = str(risk_level)

    if level == "Situation favorable":

        css_class = "risk-favorable"
        icon = "✅"

    elif level == "Vigilance":

        css_class = "risk-vigilance"
        icon = "🟡"

    elif level == "Risque modéré":

        css_class = "risk-moderate"
        icon = "🟠"

    else:

        css_class = "risk-high"
        icon = "🔴"

    st.markdown(
        f"""
<div class="{css_class}">
<h3>{icon} {level}</h3>
<p>{recommendation}</p>
</div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------
# 6. DONNÉES DE DÉMONSTRATION H+1
# ---------------------------------------------------------------------

current_values = (
    energy_df[
        [
            "Time",
            "PV_production",
            "Wind_production",
            "Electric_demand",
        ]
    ]
    .drop_duplicates(subset=["Time"])
    .copy()
)

demo_df = predictions_df.merge(
    current_values,
    on="Time",
    how="left",
)

demo_df = (
    demo_df
    .sort_values("Time")
    .reset_index(drop=True)
)


# ---------------------------------------------------------------------
# 7. NAVIGATION
# ---------------------------------------------------------------------

st.sidebar.title("⚡ Navigation")

NAVIGATION_OPTIONS = [
    "🏠 Accueil",
    "🎯 Démonstration H+1",
    "📊 Exploration des données",
    "☀️ Production photovoltaïque",
    "🌬️ Production éolienne",
    "⚡ Demande électrique",
    "📈 Performances des modèles",
    "🌍 Climat & tendances",
    "🔗 Climat & système énergétique",
    "🧭 Scénarios & aide à la décision",
    "ℹ️ À propos",
]

page = st.sidebar.radio(
    "Sélectionner une page",
    NAVIGATION_OPTIONS,
    key="main_navigation",
)

st.sidebar.divider()

st.sidebar.write(
    "**Données énergétiques principales**"
)

st.sidebar.write(
    f"{energy_df['Time'].min():%d/%m/%Y}"
    " - "
    f"{energy_df['Time'].max():%d/%m/%Y}"
)

st.sidebar.write(
    "**Observations :** "
    f"{len(energy_df):,}".replace(",", " ")
)

st.sidebar.divider()

st.sidebar.caption(
    "Les scénarios climatiques présentés dans "
    "l'application sont des tests de sensibilité "
    "et non des projections climatiques officielles."
)


# ---------------------------------------------------------------------
# 8. FILTRE TEMPOREL
# ---------------------------------------------------------------------

minimum_date = energy_df["Time"].min().date()
maximum_date = energy_df["Time"].max().date()

selected_dates = st.sidebar.date_input(
    "Filtrer les données énergétiques",
    value=(
        minimum_date,
        maximum_date,
    ),
    min_value=minimum_date,
    max_value=maximum_date,
)

if (
    isinstance(selected_dates, tuple)
    and len(selected_dates) == 2
):

    start_date, end_date = selected_dates

    filtered_df = energy_df[
        (
            energy_df["Time"].dt.date
            >= start_date
        )
        &
        (
            energy_df["Time"].dt.date
            <= end_date
        )
    ].copy()

else:

    filtered_df = energy_df.copy()


if filtered_df.empty:

    st.warning(
        "Aucune observation disponible "
        "pour la période sélectionnée."
    )

    st.stop()


# ---------------------------------------------------------------------
# 9. TITRE DES PAGES
# ---------------------------------------------------------------------

if page != "🏠 Accueil":
    st.title(page)


# =====================================================================
# PAGE ACCUEIL
# =====================================================================

if page == "🏠 Accueil":

    st.markdown(
        """
<div class="hero">
<div class="hero-badge">
⚡ Intelligence artificielle · énergie · climat
</div>

<h1>
Système intelligent de prévision et d'aide à la décision énergétique
</h1>

<p>
Le projet combine la prévision à court terme de la production
photovoltaïque, de la production éolienne et de la demande électrique
avec une analyse des évolutions climatiques et de leurs conséquences
potentielles sur l'équilibre énergétique.
</p>
</div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Observations énergétiques",
        f"{len(energy_df):,}".replace(
            ",",
            " ",
        ),
    )

    col2.metric(
        "Variables prédites",
        "3",
    )

    col3.metric(
        "Horizon IA",
        "+1 heure",
    )

    col4.metric(
        "Analyse climatique",
        "1990-2025",
    )

    section_title(
        "Les quatre dimensions du projet"
    )

    card1, card2, card3, card4 = st.columns(4)

    with card1:

        st.markdown(
            """
<div class="info-card">
<h3>🤖 Prévision IA</h3>
<p>
Prévision H+1 de la production photovoltaïque,
de la production éolienne et de la demande électrique.
</p>
</div>
            """,
            unsafe_allow_html=True,
        )

    with card2:

        st.markdown(
            """
<div class="info-card">
<h3>🌍 Analyse climatique</h3>
<p>
Analyse des évolutions de température, rayonnement solaire,
vent et humidité sur la période 1990–2025.
</p>
</div>
            """,
            unsafe_allow_html=True,
        )

    with card3:

        st.markdown(
            """
<div class="info-card">
<h3>⚖️ Équilibre énergétique</h3>
<p>
Estimation de la couverture renouvelable et du déficit
entre productions photovoltaïque et éolienne et demande.
</p>
</div>
            """,
            unsafe_allow_html=True,
        )

    with card4:

        st.markdown(
            """
<div class="info-card">
<h3>🧭 Aide à la décision</h3>
<p>
Transformation des scénarios climatiques en niveaux
de vigilance, recommandations et besoins d'adaptation.
</p>
</div>
            """,
            unsafe_allow_html=True,
        )

    section_title(
        "Résultats clés"
    )

    k1, k2, k3, k4 = st.columns(4)

    k1.metric(
        "Tendance température",
        find_value(
            climate_summary_df,
            "Tendance température",
        ),
    )

    k2.metric(
        "MAE couverture",
        find_value(
            climate_summary_df,
            "MAE taux de couverture",
        ),
    )

    k3.metric(
        "Concordance décisionnelle",
        find_value(
            climate_summary_df,
            "Concordance",
        ),
    )

    k4.metric(
        "Adaptation maximale",
        find_value(
            climate_summary_df,
            "Besoin supplémentaire maximal",
        ),
    )

    section_title(
        "Architecture du projet"
    )

    st.markdown(
        """
1. Audit et contrôle de qualité des données  
2. Prétraitement des données  
3. Analyse exploratoire  
4. Ingénierie des caractéristiques  
5. Modélisation prédictive  
6. Évaluation finale et comparaison à une baseline  
7. Dashboard interactif  
8. Validation externe sur l'Allemagne  
9. Étude de transférabilité au Maroc  
10. Analyse climatique et aide à la décision énergétique  
        """
    )


# =====================================================================
# PAGE DÉMONSTRATION H+1
# =====================================================================

elif page == "🎯 Démonstration H+1":

    st.markdown(
        """
Pour un instant **t** du jeu de test, cette page présente la prévision
réalisée pour **t + 1 heure** ainsi que la valeur réellement observée.

Il s'agit d'une relecture historique du fonctionnement du modèle,
et non d'une prévision temps réel sur une donnée future inconnue.
        """
    )

    section_title(
        "Choisir un instant du jeu de test"
    )

    demo_min_date = demo_df["Time"].min().date()
    demo_max_date = demo_df["Time"].max().date()

    selected_demo_date = st.date_input(
        "Date",
        value=demo_min_date,
        min_value=demo_min_date,
        max_value=demo_max_date,
        key="demo_date",
    )

    available_times_df = demo_df[
        (
            demo_df["Time"].dt.date
            == selected_demo_date
        )
    ].copy()

    if available_times_df.empty:

        st.warning(
            "Aucune observation du jeu de test "
            "n'est disponible pour cette date."
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
            key="demo_time",
        )

        selected_timestamp = pd.Timestamp(
            f"{selected_demo_date} "
            f"{selected_demo_time}"
        )

        selected_rows = demo_df[
            demo_df["Time"]
            == selected_timestamp
        ]

        if selected_rows.empty:

            st.warning(
                "Observation introuvable."
            )

        else:

            row = selected_rows.iloc[0]

            forecast_timestamp = (
                selected_timestamp
                + pd.Timedelta(hours=1)
            )

            st.success(
                "Prévision à "
                f"{selected_timestamp:%d/%m/%Y %H:%M} "
                "pour "
                f"{forecast_timestamp:%d/%m/%Y %H:%M}."
            )

            section_title(
                "☀️ Production photovoltaïque"
            )

            pv1, pv2, pv3, pv4 = st.columns(4)

            pv1.metric(
                "Valeur actuelle",
                format_value(
                    row["PV_production"]
                ),
            )

            pv2.metric(
                "Prévision H+1",
                format_value(
                    row["PV_predit"]
                ),
            )

            pv3.metric(
                "Réel H+1",
                format_value(
                    row["PV_reel"]
                ),
            )

            pv4.metric(
                "Erreur absolue",
                format_value(
                    abs(row["PV_erreur"])
                ),
            )

            section_title(
                "🌬️ Production éolienne"
            )

            w1, w2, w3, w4 = st.columns(4)

            w1.metric(
                "Valeur actuelle",
                format_value(
                    row["Wind_production"]
                ),
            )

            w2.metric(
                "Prévision H+1",
                format_value(
                    row["Wind_predit"]
                ),
            )

            w3.metric(
                "Réel H+1",
                format_value(
                    row["Wind_reel"]
                ),
            )

            w4.metric(
                "Erreur absolue",
                format_value(
                    abs(row["Wind_erreur"])
                ),
            )

            section_title(
                "⚡ Demande électrique"
            )

            d1, d2, d3, d4 = st.columns(4)

            d1.metric(
                "Valeur actuelle",
                format_value(
                    row["Electric_demand"]
                ),
            )

            d2.metric(
                "Prévision H+1",
                format_value(
                    row["Demand_predit"]
                ),
            )

            d3.metric(
                "Réel H+1",
                format_value(
                    row["Demand_reel"]
                ),
            )

            d4.metric(
                "Erreur absolue",
                format_value(
                    abs(row["Demand_erreur"])
                ),
            )

            comparison_table = pd.DataFrame(
                {
                    "Cible": [
                        "Photovoltaïque",
                        "Éolien",
                        "Demande",
                    ],
                    "Valeur actuelle": [
                        row["PV_production"],
                        row["Wind_production"],
                        row["Electric_demand"],
                    ],
                    "Prévision H+1": [
                        row["PV_predit"],
                        row["Wind_predit"],
                        row["Demand_predit"],
                    ],
                    "Réel H+1": [
                        row["PV_reel"],
                        row["Wind_reel"],
                        row["Demand_reel"],
                    ],
                }
            ).round(2)

            section_title(
                "Synthèse de la prévision"
            )

            st.dataframe(
                comparison_table,
                use_container_width=True,
                hide_index=True,
            )

            comparison_figure = px.bar(
                comparison_table,
                x="Cible",
                y=[
                    "Prévision H+1",
                    "Réel H+1",
                ],
                barmode="group",
                title=(
                    "Prévision et observation "
                    "à l'horizon H+1"
                ),
                labels={
                    "value": "Valeur",
                    "variable": "Série",
                },
                color_discrete_map={
                    "Prévision H+1": "#0891b2",
                    "Réel H+1": "#102a43",
                },
            )

            st.plotly_chart(
                apply_energy_theme(
                    comparison_figure,
                    480,
                ),
                use_container_width=True,
            )


# =====================================================================
# PAGE EXPLORATION
# =====================================================================

elif page == "📊 Exploration des données":

    variable_options = {
        "Température": "Temperature",
        "Humidité": "Humidity",
        "Vitesse du vent": "Wind_speed",
        "Rayonnement solaire GHI": "GHI",
        "Production photovoltaïque": "PV_production",
        "Production éolienne": "Wind_production",
        "Demande électrique": "Electric_demand",
    }

    selected_label = st.selectbox(
        "Variable à visualiser",
        list(variable_options.keys()),
    )

    selected_column = (
        variable_options[selected_label]
    )

    display_time_series(
        filtered_df,
        selected_column,
        f"Évolution : {selected_label}",
        selected_label,
        "#0f766e",
    )

    section_title(
        "Statistiques descriptives"
    )

    st.dataframe(
        (
            filtered_df[selected_column]
            .describe()
            .to_frame(name="Valeur")
        ),
        use_container_width=True,
    )

    histogram = px.histogram(
        filtered_df,
        x=selected_column,
        nbins=50,
        title=f"Distribution : {selected_label}",
        color_discrete_sequence=[
            "#0f766e"
        ],
    )

    st.plotly_chart(
        apply_energy_theme(
            histogram,
            450,
        ),
        use_container_width=True,
    )


# =====================================================================
# PAGE PHOTOVOLTAÏQUE
# =====================================================================

elif page == "☀️ Production photovoltaïque":

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Production moyenne",
        f"{filtered_df['PV_production'].mean():.2f}",
    )

    col2.metric(
        "Production maximale",
        f"{filtered_df['PV_production'].max():.2f}",
    )

    col3.metric(
        "GHI moyen",
        f"{filtered_df['GHI'].mean():.2f}",
    )

    display_time_series(
        filtered_df,
        "PV_production",
        "Évolution de la production photovoltaïque",
        "Production photovoltaïque",
        "#16A085",
    )

    display_real_vs_target(
        filtered_df,
        "PV_production",
        "target_PV_production_1h",
        (
            "Production actuelle et production "
            "observée une heure plus tard"
        ),
        "Production photovoltaïque",
    )

    section_title(
        "Évaluation finale du modèle"
    )

    show_saved_figure(
        "pv_prediction_vs_real.png",
        "Photovoltaïque - réel vs prédit",
    )

    show_saved_figure(
        "pv_residuals.png",
        "Distribution des résidus photovoltaïques",
    )


# =====================================================================
# PAGE ÉOLIEN
# =====================================================================

elif page == "🌬️ Production éolienne":

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Production moyenne",
        f"{filtered_df['Wind_production'].mean():.2f}",
    )

    col2.metric(
        "Production maximale",
        f"{filtered_df['Wind_production'].max():.2f}",
    )

    col3.metric(
        "Vent moyen",
        f"{filtered_df['Wind_speed'].mean():.2f}",
    )

    display_time_series(
        filtered_df,
        "Wind_production",
        "Évolution de la production éolienne",
        "Production éolienne",
        "#2F80ED",
    )

    display_real_vs_target(
        filtered_df,
        "Wind_production",
        "target_Wind_production_1h",
        (
            "Production actuelle et production "
            "observée une heure plus tard"
        ),
        "Production éolienne",
    )

    section_title(
        "Évaluation finale du modèle"
    )

    show_saved_figure(
        "wind_prediction_vs_real.png",
        "Éolien - réel vs prédit",
    )

    show_saved_figure(
        "wind_residuals.png",
        "Distribution des résidus éoliens",
    )


# =====================================================================
# PAGE DEMANDE
# =====================================================================

elif page == "⚡ Demande électrique":

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Demande moyenne",
        f"{filtered_df['Electric_demand'].mean():.2f}",
    )

    col2.metric(
        "Demande maximale",
        f"{filtered_df['Electric_demand'].max():.2f}",
    )

    col3.metric(
        "Température moyenne",
        (
            f"{filtered_df['Temperature'].mean():.2f} °C"
        ),
    )

    display_time_series(
        filtered_df,
        "Electric_demand",
        "Évolution de la demande électrique",
        "Demande électrique",
        "#E66B32",
    )

    display_real_vs_target(
        filtered_df,
        "Electric_demand",
        "target_Electric_demand_1h",
        (
            "Demande actuelle et demande "
            "observée une heure plus tard"
        ),
        "Demande électrique",
    )

    section_title(
        "Évaluation finale du modèle"
    )

    show_saved_figure(
        "demand_prediction_vs_real.png",
        "Demande - réel vs prédit",
    )

    show_saved_figure(
        "demand_residuals.png",
        "Distribution des résidus de la demande",
    )


# =====================================================================
# PAGE PERFORMANCES
# =====================================================================

elif page == "📈 Performances des modèles":

    st.markdown(
        """
Les performances sont calculées sur le jeu de test final,
qui n'a été utilisé ni pour l'entraînement ni pour la sélection
des modèles.

Les modèles sont comparés à une baseline naïve saisonnière
journalière.
        """
    )

    display_results = results_df.copy()

    numeric_columns = [
        column
        for column in [
            "MAE_test",
            "RMSE_test",
            "R2_test",
            "Gain_RMSE_vs_naif_%",
        ]
        if column in display_results.columns
    ]

    if numeric_columns:

        display_results[
            numeric_columns
        ] = (
            display_results[
                numeric_columns
            ]
            .round(3)
        )

    st.dataframe(
        display_results,
        use_container_width=True,
        hide_index=True,
    )

    if {
        "Cible",
        "RMSE_test",
        "Modèle",
    }.issubset(results_df.columns):

        rmse_figure = px.bar(
            results_df,
            x="Cible",
            y="RMSE_test",
            color="Modèle",
            barmode="group",
            title=(
                "RMSE - modèles et baseline"
            ),
            text_auto=".1f",
        )

        st.plotly_chart(
            apply_energy_theme(
                rmse_figure,
                500,
            ),
            use_container_width=True,
        )

    if {
        "Cible",
        "R2_test",
        "Modèle",
    }.issubset(results_df.columns):

        r2_figure = px.bar(
            results_df,
            x="Cible",
            y="R2_test",
            color="Modèle",
            barmode="group",
            title=(
                "Coefficient de détermination "
                "sur le jeu de test"
            ),
            text_auto=".3f",
        )

        st.plotly_chart(
            apply_energy_theme(
                r2_figure,
                500,
            ),
            use_container_width=True,
        )

    section_title(
        "Validation temporelle walk-forward"
    )

    st.dataframe(
        walk_forward_df.round(3),
        use_container_width=True,
        hide_index=True,
    )

    section_title(
        "Validation externe - Allemagne"
    )

    st.markdown(
        """
Les modèles sont réentraînés sur le jeu de données allemand.
Cette expérimentation teste donc la **transférabilité de la
méthodologie**, et non le transfert direct des modèles entraînés
sur le dataset principal.
        """
    )

    st.dataframe(
        external_validation_df.round(3),
        use_container_width=True,
        hide_index=True,
    )

    show_saved_figure(
        "external_validation_germany_rmse_vs_baseline.png",
        (
            "Allemagne — comparaison du RMSE "
            "avec la baseline"
        ),
    )

    section_title(
        "Étude de transférabilité - Maroc 🇲🇦"
    )

    st.markdown(
        """
Le cas marocain repose sur des profils horaires nationaux
modélisés. Les variables solaire et éolienne sont des facteurs
de capacité et ne représentent pas directement des productions
électriques mesurées.
        """
    )

    st.dataframe(
        morocco_transferability_df.round(4),
        use_container_width=True,
        hide_index=True,
    )

    show_saved_figure(
        "morocco_rmse_vs_baseline.png",
        (
            "Maroc - comparaison avec "
            "la baseline naïve"
        ),
    )

    with st.expander(
        "Voir les courbes du cas marocain"
    ):

        show_saved_figure(
            "morocco_pv_real_vs_pred.png",
            "Maroc - photovoltaïque",
        )

        show_saved_figure(
            "morocco_wind_real_vs_pred.png",
            "Maroc - éolien",
        )

        show_saved_figure(
            "morocco_demand_real_vs_pred.png",
            "Maroc - demande",
        )

    section_title(
        "Analyse temporelle des erreurs"
    )

    show_saved_figure(
        "mean_absolute_error_by_hour.png",
        (
            "Erreur absolue moyenne "
            "selon l'heure"
        ),
    )

    csv_data = (
        results_df
        .to_csv(index=False)
        .encode("utf-8")
    )

    st.download_button(
        "Télécharger les résultats finaux",
        data=csv_data,
        file_name="final_test_results.csv",
        mime="text/csv",
    )


# =====================================================================
# PAGE CLIMAT & TENDANCES
# =====================================================================

elif page == "🌍 Climat & tendances":

    st.markdown(
        """
Cette partie présente l'analyse climatique de long terme réalisée
à partir des données **NASA POWER** pour la région étudiée autour
de Fès sur la période **1990-2025**.

Les tendances historiques observées ne constituent pas à elles
seules une attribution causale au changement climatique
anthropique.
        """
    )

    section_title(
        "Principaux résultats climatiques"
    )

    c1, c2 = st.columns(2)

    c1.metric(
        "Tendance température",
        find_value(
            climate_summary_df,
            "Tendance température",
        ),
    )

    c2.metric(
        "Tendance rayonnement solaire",
        find_value(
            climate_summary_df,
            "Tendance rayonnement solaire",
        ),
    )

    if not climate_trends_df.empty:

        with st.expander(
            "Voir le tableau complet des tendances"
        ):

            st.dataframe(
                climate_trends_df,
                use_container_width=True,
                hide_index=True,
            )

    section_title(
        "Température"
    )

    show_saved_figure(
        "climate_temperature_annual_1990_2025.png",
        (
            "Évolution annuelle de la température "
            "sur la période 1990-2025"
        ),
    )

    section_title(
        "Rayonnement solaire"
    )

    show_saved_figure(
        "climate_solar_radiation_annual_1990_2025.png",
        (
            "Évolution annuelle du rayonnement solaire"
        ),
    )

    section_title(
        "Vitesse du vent"
    )

    show_saved_figure(
        "climate_wind_speed_annual_1990_2025.png",
        (
            "Évolution annuelle de la vitesse du vent"
        ),
    )

    section_title(
        "Humidité relative"
    )

    show_saved_figure(
        "climate_humidity_annual_1990_2025.png",
        (
            "Évolution annuelle de l'humidité relative"
        ),
    )

    section_title(
        "Anomalies de température"
    )

    show_saved_figure(
        "climate_temperature_anomalies_1990_2025.png",
        (
            "Anomalies annuelles de température"
        ),
    )

    if not climate_period_df.empty:

        section_title(
            "Comparaison entre périodes"
        )

        st.dataframe(
            climate_period_df,
            use_container_width=True,
            hide_index=True,
        )

    st.markdown(
        """
<div class="science-note">
<b>Interprétation :</b>
la température présente la tendance de long terme la plus nette
parmi les variables étudiées. Les évolutions du rayonnement,
du vent et de l'humidité doivent être interprétées selon leur
significativité statistique et leur variabilité interannuelle.
</div>
        """,
        unsafe_allow_html=True,
    )


# =====================================================================
# PAGE CLIMAT & SYSTÈME ÉNERGÉTIQUE
# =====================================================================

elif page == "🔗 Climat & système énergétique":

    st.markdown(
        """
Les données climatiques et énergétiques ont été mises à une
résolution quotidienne commune sur **164 jours en 2021**.

L'objectif est d'étudier des associations empiriques entre
conditions météorologiques et comportement énergétique.

Ces corrélations ne démontrent pas à elles seules une causalité.
        """
    )

    section_title(
        "Rayonnement solaire et photovoltaïque"
    )

    show_saved_figure(
        "climate_solar_vs_pv.png",
        (
            "Relation entre rayonnement solaire "
            "et production photovoltaïque"
        ),
    )

    st.info(
        "Pearson r ≈ 0,7415 : une forte association "
        "positive est observée sur la période commune."
    )

    section_title(
        "Température et demande électrique"
    )

    show_saved_figure(
        "climate_temperature_vs_demand.png",
        (
            "Relation entre température "
            "et demande électrique"
        ),
    )

    st.info(
        "Pearson r ≈ 0,7080 : les températures "
        "plus élevées sont associées à une demande "
        "électrique plus importante sur la période étudiée."
    )

    section_title(
        "Vent et production éolienne"
    )

    show_saved_figure(
        "climate_wind_vs_wind_generation.png",
        (
            "Relation entre vitesse du vent à 10 m "
            "et production éolienne"
        ),
    )

    st.warning(
        "La relation est faible. Le vent NASA POWER est "
        "disponible à 10 m, alors que les turbines exploitent "
        "le vent à des hauteurs nettement supérieures. "
        "Cette variable ne permet donc pas de construire "
        "une sensibilité éolienne robuste."
    )

    section_title(
        "Couverture renouvelable"
    )

    st.markdown(
        """
Le taux de couverture correspond ici à la part de la demande
représentée par la somme des productions photovoltaïque et
éolienne considérées.

Il ne représente pas la couverture totale du réseau électrique :
les autres moyens de production, le stockage et les échanges ne
sont pas inclus dans cet indicateur.
        """
    )

    show_saved_figure(
        "renewable_coverage_confusion_matrix.png",
        (
            "Classification des niveaux "
            "de couverture renouvelable"
        ),
    )

    m1, m2 = st.columns(2)

    m1.metric(
        "MAE du taux de couverture",
        find_value(
            climate_summary_df,
            "MAE taux de couverture",
        ),
    )

    m2.metric(
        "Concordance des niveaux",
        find_value(
            climate_summary_df,
            "Concordance",
        ),
    )


# =====================================================================
# PAGE SCÉNARIOS & AIDE À LA DÉCISION
# =====================================================================

elif page == "🧭 Scénarios & aide à la décision":

    st.markdown(
        """
<div class="science-note">
<b>Important :</b>
les scénarios présentés ici sont des
<b>tests de sensibilité</b>.
Ils ne constituent ni des projections climatiques officielles,
ni des scénarios SSP/RCP du GIEC.
</div>
        """,
        unsafe_allow_html=True,
    )

    if climate_scenarios_df.empty:

        st.error(
            "Le fichier climate_energy_scenarios.csv "
            "n'est pas disponible."
        )

        st.stop()

    scenario_names = (
        climate_scenarios_df["Scenario"]
        .dropna()
        .astype(str)
        .tolist()
    )

    selected_scenario = st.selectbox(
        "Choisir un scénario",
        scenario_names,
    )

    scenario_row = (
        climate_scenarios_df[
            climate_scenarios_df["Scenario"]
            == selected_scenario
        ]
        .iloc[0]
    )

    decision_row = None
    adaptation_row = None

    if (
        not climate_decision_df.empty
        and "Scenario"
        in climate_decision_df.columns
    ):

        selected_decision = (
            climate_decision_df[
                climate_decision_df["Scenario"]
                == selected_scenario
            ]
        )

        if not selected_decision.empty:
            decision_row = (
                selected_decision.iloc[0]
            )

    if (
        not climate_adaptation_df.empty
        and "Scenario"
        in climate_adaptation_df.columns
    ):

        selected_adaptation = (
            climate_adaptation_df[
                climate_adaptation_df["Scenario"]
                == selected_scenario
            ]
        )

        if not selected_adaptation.empty:
            adaptation_row = (
                selected_adaptation.iloc[0]
            )

    section_title(
        "Conditions et conséquences du scénario"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Température",
        (
            f"{scenario_row['Temperature_C']:.2f} °C"
            if "Temperature_C" in scenario_row
            else "N/A"
        ),
    )

    col2.metric(
        "Rayonnement",
        format_value(
            scenario_row.get(
                "Solar_radiation"
            )
        ),
    )

    col3.metric(
        "Production PV estimée",
        format_value(
            scenario_row.get(
                "PV_estimated"
            )
        ),
    )

    col4.metric(
        "Demande estimée",
        format_value(
            scenario_row.get(
                "Demand_estimated"
            )
        ),
    )

    col5, col6, col7 = st.columns(3)

    col5.metric(
        "Production renouvelable",
        format_value(
            scenario_row.get(
                "Renewable_estimated"
            )
        ),
    )

    col6.metric(
        "Couverture renouvelable",
        (
            f"{scenario_row['Coverage_pct']:.2f} %"
            if "Coverage_pct" in scenario_row
            else "N/A"
        ),
    )

    col7.metric(
        "Déficit relatif",
        (
            f"{scenario_row['Deficit_pct']:.2f} %"
            if "Deficit_pct" in scenario_row
            else "N/A"
        ),
    )

    if decision_row is not None:

        section_title(
            "Diagnostic énergétique"
        )

        risk_level = decision_row.get(
            "Niveau_vigilance",
            "Non déterminé",
        )

        recommendation = decision_row.get(
            "Recommandation",
            "Aucune recommandation disponible.",
        )

        render_risk_box(
            risk_level,
            recommendation,
        )

        r1, r2 = st.columns(2)

        if (
            "Variation_coverage_points"
            in decision_row.index
        ):

            r1.metric(
                "Variation de couverture",
                (
                    f"{decision_row['Variation_coverage_points']:+.2f} "
                    "point(s)"
                ),
            )

        if (
            "Variation_deficit_pct"
            in decision_row.index
        ):

            r2.metric(
                "Variation du déficit",
                (
                    f"{decision_row['Variation_deficit_pct']:+.2f} %"
                ),
            )

    if adaptation_row is not None:

        section_title(
            "Effort d'adaptation estimé"
        )

        a1, a2, a3 = st.columns(3)

        a1.metric(
            "Renouvelable estimé",
            format_value(
                adaptation_row.get(
                    "Renewable_estimated"
                )
            ),
        )

        a2.metric(
            "Renouvelable requis",
            format_value(
                adaptation_row.get(
                    "Renewable_required"
                )
            ),
        )

        additional_pct = (
            adaptation_row.get(
                "Additional_renewable_pct",
                0,
            )
        )

        a3.metric(
            "Besoin supplémentaire",
            f"{float(additional_pct):.2f} %",
        )

        st.caption(
            "Ce besoin représente un indicateur théorique "
            "d'adaptation. Il ne constitue pas un dimensionnement "
            "d'infrastructure photovoltaïque, éolienne ou de stockage."
        )

    section_title(
        "Comparaison de tous les scénarios"
    )

    scenario_chart = px.bar(
        climate_scenarios_df,
        x="Scenario",
        y="Coverage_pct",
        title=(
            "Impact des scénarios sur "
            "la couverture renouvelable"
        ),
        text_auto=".2f",
    )

    scenario_chart.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        apply_energy_theme(
            scenario_chart,
            520,
        ),
        use_container_width=True,
    )

    if (
        not climate_decision_df.empty
        and {
            "Scenario",
            "Variation_deficit_pct",
        }.issubset(
            climate_decision_df.columns
        )
    ):

        deficit_chart = px.bar(
            climate_decision_df,
            x="Scenario",
            y="Variation_deficit_pct",
            title=(
                "Variation du déficit énergétique "
                "par rapport à la référence"
            ),
            text_auto=".2f",
        )

        deficit_chart.update_traces(
            textposition="outside"
        )

        st.plotly_chart(
            apply_energy_theme(
                deficit_chart,
                520,
            ),
            use_container_width=True,
        )

    if (
        not climate_adaptation_df.empty
        and {
            "Scenario",
            "Additional_renewable_pct",
        }.issubset(
            climate_adaptation_df.columns
        )
    ):

        adaptation_chart = px.bar(
            climate_adaptation_df,
            x="Scenario",
            y="Additional_renewable_pct",
            title=(
                "Effort d'adaptation pour maintenir "
                "la couverture de référence"
            ),
            text_auto=".2f",
        )

        adaptation_chart.update_traces(
            textposition="outside"
        )

        st.plotly_chart(
            apply_energy_theme(
                adaptation_chart,
                520,
            ),
            use_container_width=True,
        )

    with st.expander(
        "Voir les données détaillées des scénarios"
    ):

        st.dataframe(
            climate_scenarios_df.round(3),
            use_container_width=True,
            hide_index=True,
        )

        if not climate_decision_df.empty:

            st.dataframe(
                climate_decision_df,
                use_container_width=True,
                hide_index=True,
            )


# =====================================================================
# PAGE À PROPOS
# =====================================================================

elif page == "ℹ️ À propos":

    st.markdown(
        """
## Objectif du projet

Le projet étudie l'utilisation de techniques d'intelligence artificielle
pour contribuer à une meilleure anticipation et adaptation de la production
énergétique face à l'évolution des conditions climatiques.

La démarche repose sur deux horizons complémentaires.

### Court terme

Des modèles de Machine Learning prévoient à **H+1 heure** :

- la production photovoltaïque ;
- la production éolienne ;
- la demande électrique.

### Long terme

Les données climatiques NASA POWER sur la période **1990-2025** permettent
d'étudier les évolutions de :

- la température ;
- le rayonnement solaire ;
- la vitesse du vent ;
- l'humidité relative.

## Pipeline méthodologique

Le projet comprend :

1. audit et contrôle des données ;
2. prétraitement ;
3. analyse exploratoire ;
4. ingénierie des caractéristiques ;
5. modélisation prédictive ;
6. validation temporelle et évaluation finale ;
7. restitution Streamlit et Power BI ;
8. validation externe sur l'Allemagne ;
9. transférabilité méthodologique au Maroc ;
10. analyse climatique et aide à la décision énergétique.

## Modèles retenus

- **Photovoltaïque :** HistGradientBoosting
- **Éolien :** Régression linéaire
- **Demande électrique :** HistGradientBoosting

## Validation

Les données principales sont séparées chronologiquement :

- 70 % entraînement ;
- 15 % validation ;
- 15 % test final.

Le jeu de test n'est jamais utilisé pour sélectionner les modèles.

Une validation temporelle **walk-forward** complète également cette
évaluation.

## Validation externe

La méthodologie H+1 a également été appliquée à un jeu de données
indépendant relatif à l'Allemagne. Les modèles ont été réentraînés
dans ce nouveau contexte afin d'étudier la transférabilité de la méthode.

## Maroc

Une expérimentation complémentaire a été conduite sur des profils horaires
nationaux modélisés pour le Maroc.

Cette analyse constitue une étude de transférabilité méthodologique et non
une validation opérationnelle du réseau électrique marocain.

## Climat et énergie

L'analyse climat-énergie met notamment en évidence :

- une association forte entre rayonnement solaire et production PV ;
- une association importante entre température et demande électrique ;
- une faible représentativité du vent NASA POWER à 10 m pour expliquer
  directement la production éolienne du système étudié.

## Scénarios climatiques

Les scénarios de température et de rayonnement servent à étudier la
**sensibilité énergétique** du système.

Ils ne constituent pas des projections SSP/RCP ou des prévisions climatiques
officielles.

Le scénario combinant une température plus élevée et un rayonnement plus
faible est le plus défavorable parmi les situations testées.

## Aide à la décision

Les scénarios sont transformés en :

- taux de couverture renouvelable ;
- déficit énergétique ;
- niveau de vigilance ;
- recommandation ;
- besoin théorique d'adaptation.

Cette couche constitue un prototype d'aide à la décision.

Elle ne représente pas une optimisation complète d'un réseau électrique.

## Limites

Plusieurs limites doivent être prises en compte :

- l'analyse climatique NASA POWER est locale ;
- la période climat-énergie commune est limitée à 164 jours ;
- la vitesse du vent à 10 m est insuffisante pour représenter précisément
  les conditions à hauteur de turbine ;
- les scénarios sont des tests de sensibilité ;
- aucune capacité réelle de stockage ou de réseau n'est modélisée ;
- le projet ne réalise pas un dimensionnement d'infrastructure ;
- l'application n'est pas connectée à des flux temps réel.

## Technologies

Python, Pandas, NumPy, scikit-learn, Plotly, Streamlit,
Matplotlib et Power BI.
        """
    )