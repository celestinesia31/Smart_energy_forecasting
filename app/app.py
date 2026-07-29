# APPLICATION STREAMLIT PRÉVISION ÉNERGÉTIQUE

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# 1. CONFIGURATION DE LA PAGE


st.set_page_config(
    page_title="Prévision énergétique",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# 2. THÈME VISUEL PERSONNALISÉ

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

    h1, h2, h3 {
        color: #102a43;
        letter-spacing: -0.02em;
    }

    h1 {
        font-weight: 700;
    }

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
    }

    div[data-testid="stDataFrame"] {
        background-color: white;
        border: 1px solid #d9e2ec;
        border-radius: 0.9rem;
        overflow: hidden;
        box-shadow: 0 6px 18px rgba(16, 42, 67, 0.06);
    }

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        background-color: rgba(255, 255, 255, 0.96);
        border-radius: 0.75rem;
    }

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

    footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# 3. DÉFINITION DES CHEMINS

APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent

DATA_DIR = PROJECT_DIR / "data" / "processed"
RESULTS_DIR = PROJECT_DIR / "results"
FIGURES_DIR = PROJECT_DIR / "figures"

DASHBOARD_DATA_FILE = DATA_DIR / "dashboard_data.csv"
FINAL_RESULTS_FILE = RESULTS_DIR / "final_test_results.csv"


# 4. CHARGEMENT DES DONNÉES

@st.cache_data
def load_dashboard_data() -> pd.DataFrame:
    """
    Charge le dataset léger utilisé par le dashboard.
    """

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
    """
    Charge les résultats finaux obtenus sur le jeu de test.
    """

    if not FINAL_RESULTS_FILE.exists():
        raise FileNotFoundError(
            f"Fichier introuvable : {FINAL_RESULTS_FILE}"
        )

    return pd.read_csv(FINAL_RESULTS_FILE)


try:
    energy_df = load_dashboard_data()
    results_df = load_final_results()

except FileNotFoundError as error:
    st.error(str(error))
    st.info(
        "Exécute d’abord le Notebook 07 afin de créer "
        "`dashboard_data.csv`."
    )
    st.stop()


# 5. FONCTIONS UTILITAIRES

def apply_energy_theme(
    figure,
    height: int = 500
):
    """
    Applique un thème graphique cohérent avec le dashboard.
    """

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
    """
    Affiche une série temporelle interactive.
    """

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
    """
    Compare la valeur actuelle avec la valeur observée une heure plus tard.
    """

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

    line_colors = [
        "#0f766e",
        "#f59e0b"
    ]

    for trace, color in zip(
        figure.data,
        line_colors
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
    """
    Affiche une figure enregistrée si elle existe.
    """

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


# 6. BARRE LATÉRALE

st.sidebar.title("⚡ Navigation")

NAVIGATION_OPTIONS = [
    "🏠 Accueil",
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


# 7. FILTRE TEMPOREL GLOBAL

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
        "Aucune observation n’est disponible pour cette période."
    )
    st.stop()


# 8. TITRE DYNAMIQUE UNIQUE

if page != "🏠 Accueil":
    st.title(page)


# 9. PAGE ACCUEIL


if page == "🏠 Accueil":

    st.markdown(
    """<div class="hero">
<div class="hero-badge">⚡ Intelligence artificielle & énergies renouvelables</div>
<h1>Système intelligent de prévision énergétique</h1>
<p>Application interactive de prévision à un horizon d’une heure pour la production photovoltaïque, la production éolienne et la demande électrique.</p>
</div>""",
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
                    Prévision de la production solaire à partir du
                    rayonnement, de la température et des caractéristiques
                    temporelles.
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
                    Estimation de la production éolienne en exploitant
                    la vitesse du vent et l’historique énergétique récent.
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
                    Anticipation de la consommation à partir des cycles
                    temporels, des conditions météo et des valeurs retardées.
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
        6. Évaluation finale  
        7. Application interactive
        """
    )


# 10. PAGE EXPLORATION

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
        '<h2 class="section-title">Statistiques descriptives</h2>',
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


# 11. PAGE PHOTOVOLTAÏQUE

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
        color="#f59e0b"
    )

    display_real_vs_target(
        filtered_df,
        "PV_production",
        "target_PV_production_1h",
        "Production actuelle et production observée une heure plus tard",
        "Production photovoltaïque"
    )

    st.markdown(
        '<h2 class="section-title">Évaluation finale du modèle</h2>',
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


# 12. PAGE ÉOLIENNE

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
        color="#0891b2"
    )

    display_real_vs_target(
        filtered_df,
        "Wind_production",
        "target_Wind_production_1h",
        "Production actuelle et production observée une heure plus tard",
        "Production éolienne"
    )

    st.markdown(
        '<h2 class="section-title">Évaluation finale du modèle</h2>',
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


# 13. PAGE DEMANDE ÉLECTRIQUE

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
        color="#7c3aed"
    )

    display_real_vs_target(
        filtered_df,
        "Electric_demand",
        "target_Electric_demand_1h",
        "Demande actuelle et demande observée une heure plus tard",
        "Demande électrique"
    )

    st.markdown(
        '<h2 class="section-title">Évaluation finale du modèle</h2>',
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


# 14. PAGE PERFORMANCES

elif page == "📈 Performances des modèles":


    st.markdown(
        """
        Les performances présentées ci-dessous ont été calculées sur
        l’ensemble de test, jamais utilisé lors de l’entraînement ni lors
        de la sélection des modèles.
        """
    )

    st.dataframe(
        results_df,
        use_container_width=True,
        hide_index=True
    )

    if "R2_test" in results_df.columns:

        r2_figure = px.bar(
            results_df,
            x="Cible",
            y="R2_test",
            color="Modèle retenu",
            title="Coefficient de détermination par cible",
            text_auto=".3f",
            color_discrete_map={
                "HistGradientBoosting": "#0f766e",
                "Régression linéaire": "#f59e0b"
            }
        )

        r2_figure.update_traces(
            textposition="outside"
        )

        r2_figure.update_yaxes(
            range=[
                max(
                    0,
                    results_df["R2_test"].min() - 0.05
                ),
                1.01
            ]
        )

        r2_figure = apply_energy_theme(
            r2_figure,
            height=450
        )

        st.plotly_chart(
            r2_figure,
            use_container_width=True
        )

    if "RMSE_test" in results_df.columns:

        rmse_figure = px.bar(
            results_df,
            x="Cible",
            y="RMSE_test",
            color="Modèle retenu",
            title="Erreur RMSE par cible",
            text_auto=".1f",
            color_discrete_map={
                "HistGradientBoosting": "#0f766e",
                "Régression linéaire": "#f59e0b"
            }
        )

        rmse_figure.update_traces(
            textposition="outside"
        )

        rmse_figure = apply_energy_theme(
            rmse_figure,
            height=450
        )

        st.plotly_chart(
            rmse_figure,
            use_container_width=True
        )

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


# 15. PAGE À PROPOS

elif page == "ℹ️ À propos":


    st.markdown(
        """
        ## Objectif

        Développer un système de prévision à court terme permettant
        d’estimer une heure à l’avance :

        - la production photovoltaïque ;
        - la production éolienne ;
        - la demande électrique.

        ## Méthodologie

        Le projet repose sur un pipeline complet comprenant :

        - l’audit et le contrôle de qualité des données ;
        - le prétraitement ;
        - l’analyse exploratoire ;
        - l’ingénierie des caractéristiques ;
        - la modélisation prédictive ;
        - la validation et l’évaluation finale ;
        - la création d’une application interactive.

        ## Modèles retenus

        - **Photovoltaïque :** HistGradientBoosting  
        - **Éolien :** Régression linéaire  
        - **Demande électrique :** HistGradientBoosting

        ## Technologies

        Python, Pandas, NumPy, scikit-learn, Plotly et Streamlit.
        """
    )