import os
import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import poisson

# ==============================================================================
# 0. CONFIGURACIÓN DE PÁGINA Y AUTO-BOOTSTRAP DE DATOS
# ==============================================================================
st.set_page_config(
    page_title="TERMINAL SHARP: UCL QUANT SCANNER",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

CSV_PATH = "ucl_stats_completo.csv"

def ensure_ucl_csv():
    if not os.path.exists(CSV_PATH):
        default_csv = """Equipo,xG_favor,xGA_contra,Forma,UEFA_Coef,Corners_Favor,Corners_Contra
Manchester City,2.45,0.75,0.88,148.0,7.8,2.9
Real Madrid,2.30,0.88,0.85,136.0,6.5,3.8
Bayern Munich,2.40,0.95,0.82,134.0,7.4,3.4
PSG,2.15,1.02,0.78,116.0,6.8,4.0
Inter Milan,2.05,0.78,0.84,108.0,6.1,3.9
Arsenal,2.18,0.72,0.86,98.0,7.2,3.1
Barcelona,2.25,1.05,0.83,96.0,6.6,4.1
Bayer Leverkusen,2.12,0.92,0.85,90.0,6.4,3.8
Atlético Madrid,1.80,0.85,0.76,89.0,5.4,4.4
Borussia Dortmund,1.95,1.18,0.74,88.0,5.9,4.7
Atalanta,1.92,1.15,0.77,81.0,5.8,4.5
Sporting CP,2.05,0.95,0.82,68.0,6.3,3.7
Benfica,1.88,1.10,0.75,69.0,6.2,4.3
Juventus,1.72,0.82,0.76,72.0,5.3,4.2
AC Milan,1.85,1.15,0.73,74.0,5.7,4.5
Aston Villa,1.78,1.08,0.79,52.0,5.8,4.6
AS Monaco,1.82,1.18,0.77,48.0,5.5,4.7
Feyenoord,1.75,1.25,0.70,54.0,5.9,4.8
PSV Eindhoven,1.90,1.22,0.78,56.0,6.1,4.5
Celtic,1.65,1.45,0.72,38.0,5.6,5.4
Club Brugge,1.55,1.40,0.68,44.0,5.1,5.3
Shakhtar Donetsk,1.35,1.65,0.60,41.0,4.4,6.1
Dinamo Zagreb,1.28,1.75,0.58,35.0,4.1,6.5
Red Star Belgrade,1.22,1.85,0.55,28.0,3.9,6.8
Sturm Graz,1.18,1.88,0.54,22.0,3.8,6.7
Young Boys,1.20,1.92,0.50,26.0,4.0,7.0
Slovan Bratislava,0.95,2.25,0.45,14.0,3.1,7.8
Sabah FK,0.85,2.40,0.42,9.5,2.8,8.2"""
        with open(CSV_PATH, "w", encoding="utf-8") as f:
            f.write(default_csv)

ensure_ucl_csv()

@st.cache_data
def load_data():
    df = pd.read_csv(CSV_PATH)
    df.set_index("Equipo", inplace=True)
    return df

df_stats = load_data()
TEAMS = list(df_stats.index)

# ==============================================================================
# 1. CYBER-QUANT UI CSS (CLON EXACTO: ORBITRON + JETBRAINS MONO + INTER)
# ==============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600;700;800&family=Orbitron:wght@600;700;800;900&display=swap');

:root {
    --bg-dark: #07090e;
    --glass-bg: rgba(15, 22, 36, 0.72);
    --glass-border: rgba(0, 240, 255, 0.18);
    --neon-green: #00ff9d;
    --neon-cyan: #00f0ff;
    --neon-gold: #ffb800;
    --neon-red: #ff3366;
    --text-main: #f0f6fc;
    --text-muted: #8b949e;
}

.stApp {
    background: radial-gradient(circle at 50% 0%, #0f1c3f 0%, #07090e 55%, #040609 100%);
    color: var(--text-main);
    font-family: 'Inter', sans-serif;
}

/* Header Principal Terminal */
.terminal-header {
    background: linear-gradient(135deg, rgba(12, 20, 38, 0.9) 0%, rgba(7, 11, 20, 0.95) 100%);
    border: 1px solid rgba(0, 240, 255, 0.3);
    border-left: 5px solid var(--neon-cyan);
    border-radius: 12px;
    padding: 20px 26px;
    margin-bottom: 22px;
    box-shadow: 0 0 30px rgba(0, 240, 255, 0.12);
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.terminal-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.75rem;
    font-weight: 900;
    letter-spacing: 2px;
    background: linear-gradient(90deg, #00f0ff, #00ff9d);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}
.terminal-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: var(--text-muted);
    margin-top: 4px;
}
.terminal-badge {
    font-family: 'JetBrains Mono', monospace;
    background: rgba(0, 255, 157, 0.1);
    border: 1px solid var(--neon-green);
    color: var(--neon-green);
    padding: 6px 14px;
    border-radius: 6px;
    font-size: 0.78rem;
    font-weight: 700;
    text-shadow: 0 0 8px rgba(0, 255, 157, 0.4);
}

/* Radar Ejecutivo (4 Tarjetas Top) */
.radar-section-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.05rem;
    color: var(--neon-cyan);
    letter-spacing: 1.5px;
    margin-bottom: 12px;
    text-transform: uppercase;
}
.radar-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 28px;
}
.radar-card {
    background: var(--glass-bg);
    backdrop-filter: blur(12px);
    border: 1px solid var(--glass-border);
    border-top: 3px solid var(--neon-cyan);
    border-radius: 12px;
    padding: 16px;
    transition: all 0.25s ease;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.45);
}
.radar-card:hover {
    transform: translateY(-4px);
    border-color: var(--neon-green);
    box-shadow: 0 0 22px rgba(0, 255, 157, 0.25);
}
.radar-tag {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.75rem;
    font-weight: 800;
    color: var(--neon-cyan);
    letter-spacing: 1px;
    margin-bottom: 6px;
}
.radar-match {
    font-family: 'Inter', sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 4px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.radar-pick {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.05rem;
    font-weight: 800;
    color: var(--neon-green);
    margin-bottom: 8px;
}
.radar-meta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: var(--text-muted);
    display: flex;
    justify-content: space-between;
    border-top: 1px solid rgba(255,255,255,0.08);
    padding-top: 8px;
}

/* Scoreboard TV Header */
.match-container {
    background: rgba(10, 15, 26, 0.78);
    border: 1px solid rgba(0, 240, 255, 0.22);
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 32px;
    box-shadow: 0 12px 36px rgba(0, 0, 0, 0.65);
}
.tv-scoreboard {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: center;
    background: linear-gradient(90deg, rgba(0, 255, 157, 0.08) 0%, rgba(12, 18, 32, 0.95) 50%, rgba(255, 184, 0, 0.08) 100%);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 12px;
    padding: 16px 24px;
    margin-bottom: 16px;
}
.team-side {
    display: flex;
    align-items: center;
    gap: 14px;
}
.team-side.away {
    justify-content: flex-end;
    text-align: right;
}
.team-badge-circle {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: rgba(0, 240, 255, 0.12);
    border: 2px solid var(--neon-cyan);
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Orbitron', sans-serif;
    font-weight: 900;
    font-size: 0.95rem;
    color: #fff;
    box-shadow: 0 0 14px rgba(0, 240, 255, 0.35);
}
.team-side.away .team-badge-circle {
    border-color: var(--neon-gold);
    background: rgba(255, 184, 0, 0.12);
    box-shadow: 0 0 14px rgba(255, 184, 0, 0.35);
}
.team-name {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.2rem;
    font-weight: 800;
    color: #ffffff;
}
.team-submeta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.74rem;
    color: var(--text-muted);
}
.tv-center {
    text-align: center;
    padding: 0 24px;
}
.xg-display {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.55rem;
    font-weight: 800;
    color: var(--neon-cyan);
    letter-spacing: 1px;
}
.xg-label {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.65rem;
    color: var(--text-muted);
    letter-spacing: 2px;
    margin-top: 2px;
}
.edge-pill {
    display: inline-block;
    margin-top: 5px;
    padding: 3px 10px;
    border-radius: 99px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    font-weight: 700;
    background: rgba(0, 240, 255, 0.12);
    border: 1px solid rgba(0, 240, 255, 0.35);
    color: var(--neon-cyan);
}

/* Barra Tricolor 1X2 (Tug-of-War) */
.tug-wrapper {
    margin: 14px 0 18px 0;
}
.tug-labels {
    display: flex;
    justify-content: space-between;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    font-weight: 700;
    margin-bottom: 6px;
}
.tug-bar {
    width: 100%;
    height: 14px;
    border-radius: 99px;
    overflow: hidden;
    display: flex;
    background: #121824;
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: inset 0 2px 5px rgba(0,0,0,0.6);
}
.tug-seg-home {
    background: linear-gradient(90deg, #00b871, #00ff9d);
    box-shadow: 0 0 12px rgba(0, 255, 157, 0.5);
}
.tug-seg-draw {
    background: linear-gradient(90deg, #525c6e, #7b869c);
}
.tug-seg-away {
    background: linear-gradient(90deg, #ff9900, #ffd000);
    box-shadow: 0 0 12px rgba(255, 184, 0, 0.5);
}

/* Banner de Pick Sugerido */
.sharp-banner {
    background: linear-gradient(90deg, rgba(0, 255, 157, 0.14) 0%, rgba(0, 240, 255, 0.08) 100%);
    border: 1px solid var(--neon-green);
    border-left: 5px solid var(--neon-green);
    border-radius: 10px;
    padding: 12px 18px;
    margin-bottom: 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.sharp-banner-left {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.92rem;
    font-weight: 800;
    color: #fff;
}
.sharp-banner-right {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.88rem;
    color: var(--neon-green);
    font-weight: 700;
}

/* Tarjetas de Cuotas (1X2, Protección, Goles) */
.section-sub {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.78rem;
    color: var(--neon-cyan);
    letter-spacing: 1.4px;
    margin: 12px 0 8px 0;
    text-transform: uppercase;
}
.market-row-3 {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-bottom: 12px;
}
.market-row-4 {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 16px;
}
.market-row-2 {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
    margin-bottom: 12px;
}
.quant-card {
    background: rgba(16, 23, 38, 0.78);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    padding: 12px 14px;
    transition: all 0.2s ease;
}
.quant-card:hover {
    border-color: var(--neon-cyan);
    box-shadow: 0 0 15px rgba(0, 240, 255, 0.2);
    transform: translateY(-2px);
}
.qc-title {
    font-family: 'Inter', sans-serif;
    font-size: 0.76rem;
    color: var(--text-muted);
    font-weight: 600;
    margin-bottom: 4px;
}
.qc-prob {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.25rem;
    font-weight: 800;
    color: #ffffff;
}
.qc-odds {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: var(--neon-cyan);
    margin-top: 4px;
}

/* Podio de Marcadores Exactos */
.podium-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-bottom: 14px;
}
.podium-card {
    background: rgba(18, 26, 44, 0.85);
    border-radius: 10px;
    padding: 12px 10px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.12);
    transition: all 0.2s ease;
}
.podium-card.gold {
    border-top: 3px solid #ffd700;
    box-shadow: 0 0 16px rgba(255, 215, 0, 0.15);
}
.podium-card.silver {
    border-top: 3px solid #c0c0c0;
}
.podium-card.bronze {
    border-top: 3px solid #cd7f32;
}
.podium-medal {
    font-size: 1.2rem;
    margin-bottom: 2px;
}
.podium-score {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.25rem;
    font-weight: 900;
    color: #fff;
}
.podium-prob {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: var(--neon-green);
    font-weight: 700;
}
.podium-odd {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: var(--text-muted);
}

@media (max-width: 900px) {
    .radar-grid, .market-row-4 { grid-template-columns: repeat(2, 1fr); }
    .tv-scoreboard { grid-template-columns: 1fr; text-align: center; gap: 10px; }
    .team-side, .team-side.away { justify-content: center; }
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. MOTOR CUANTITATIVO BIVARIADO (POISSON + DIXON-COLES + UEFA COEF MISMATCH)
# ==============================================================================
def prob_to_fair_odds(prob: float):
    """Convierte probabilidad (0 a 1) en Momio Justo Decimal y Americano (+EV)."""
    p = float(np.clip(prob, 0.001, 0.995))
    dec = 1.0 / p
    if p >= 0.5:
        amer = -int(round((p / (1.0 - p)) * 100))
        amer_str = f"{amer}"
    else:
        amer = int(round(((1.0 - p) / p) * 100))
        amer_str = f"+{amer}"
    return round(dec, 2), amer_str

def format_odds_line(prob: float):
    dec, amer = prob_to_fair_odds(prob)
    return f"Fair: {dec:.2f} ({amer})"

def dixon_coles_tau(x, y, lam_x, lam_y, rho=-0.09):
    """Factor de corrección de dependencia en marcadores bajos (Dixon-Coles 1997)."""
    if x == 0 and y == 0:
        return 1.0 - (lam_x * lam_y * rho)
    elif x == 0 and y == 1:
        return 1.0 + (lam_x * rho)
    elif x == 1 and y == 0:
        return 1.0 + (lam_y * rho)
    elif x == 1 and y == 1:
        return 1.0 - rho
    return 1.0

def simulate_ucl_match(home_team: str, away_team: str, df: pd.DataFrame):
    h = df.loc[home_team]
    a = df.loc[away_team]

    # Promedios base europeos
    avg_xg = df["xG_favor"].mean()
    avg_xga = df["xGA_contra"].mean()

    # Fuerza de ataque y defensa base
    h_att = h["xG_favor"] / avg_xg
    h_def = h["xGA_contra"] / avg_xga
    a_att = a["xG_favor"] / avg_xg
    a_def = a["xGA_contra"] / avg_xga

    # Ajuste por Forma reciente (0.0 a 1.0)
    h_form_mod = 0.88 + 0.24 * float(h["Forma"])
    a_form_mod = 0.88 + 0.24 * float(a["Forma"])

    # PONDERACIÓN FUERTE DE COEFICIENTE UEFA (Brechas Masivas en Europa)
    # Permite proyecciones de goleadas (xG > 3.5) en choques tipo Man City vs Sabah
    coef_diff = (float(h["UEFA_Coef"]) - float(a["UEFA_Coef"])) / 100.0
    mismatch_home = np.exp(0.58 * coef_diff)
    mismatch_away = np.exp(-0.52 * coef_diff)

    # Ventaja de localía en noches de Champions (~8%)
    home_adv = 1.08

    # Cálculo de xG Esperado (con techo alto para goleadas europeas)
    xg_home = float(np.clip(avg_xg * h_att * a_def * h_form_mod * mismatch_home * home_adv, 0.20, 5.20))
    xg_away = float(np.clip(avg_xg * a_att * h_def * a_form_mod * mismatch_away * 0.94, 0.15, 4.80))

    # Matriz Bivariada 11x11 (0 a 10 goles)
    max_goals = 10
    matrix = np.zeros((max_goals + 1, max_goals + 1))
    for i in range(max_goals + 1):
        for j in range(max_goals + 1):
            p_ind = poisson.pmf(i, xg_home) * poisson.pmf(j, xg_away)
            tau = max(0.0, dixon_coles_tau(i, j, xg_home, xg_away, rho=-0.08))
            matrix[i, j] = p_ind * tau

    # Normalización estricta
    matrix /= matrix.sum()

    # Mercados 1X2
    p_home = float(np.sum(np.tril(matrix, -1)))
    p_draw = float(np.sum(np.diag(matrix)))
    p_away = float(np.sum(np.triu(matrix, 1)))

    # Doble Oportunidad y Draw No Bet (DNB)
    p_1x = p_home + p_draw
    p_x2 = p_away + p_draw
    p_12 = p_home + p_away
    p_dnb_home = p_home / (p_home + p_away) if (p_home + p_away) > 0 else 0.5
    p_dnb_away = p_away / (p_home + p_away) if (p_home + p_away) > 0 else 0.5

    # Mercados de Goles (Over/Under 2.5 y 3.5, BTTS, Portería a Cero)
    p_over25 = 0.0
    p_over35 = 0.0
    p_btts_yes = 0.0
    p_ah_home_15 = 0.0
    p_ah_home_25 = 0.0
    p_ah_away_15 = 0.0
    p_ah_away_25 = 0.0

    for i in range(max_goals + 1):
        for j in range(max_goals + 1):
            prob_ij = matrix[i, j]
            if (i + j) > 2.5:
                p_over25 += prob_ij
            if (i + j) > 3.5:
                p_over35 += prob_ij
            if i >= 1 and j >= 1:
                p_btts_yes += prob_ij
            if (i - j) >= 2:
                p_ah_home_15 += prob_ij
            if (i - j) >= 3:
                p_ah_home_25 += prob_ij
            if (j - i) >= 2:
                p_ah_away_15 += prob_ij
            if (j - i) >= 3:
                p_ah_away_25 += prob_ij

    p_under25 = 1.0 - p_over25
    p_under35 = 1.0 - p_over35
    p_btts_no = 1.0 - p_btts_yes

    # Clean Sheets (Portería a cero)
    p_cs_home = float(np.sum(matrix[:, 0]))  # Visita anota 0
    p_cs_away = float(np.sum(matrix[0, :]))  # Local anota 0

    # Hándicap Asiático inteligente orientado al Favorito del partido
    if p_home >= p_away:
        fav_name = home_team
        p_fav_ah15 = p_ah_home_15
        p_fav_ah25 = p_ah_home_25
    else:
        fav_name = away_team
        p_fav_ah15 = p_ah_away_15
        p_fav_ah25 = p_ah_away_25

    # Marcadores Exactos (Mostrados visualmente hasta 6x6 goles para el Podio)
    exact_scores = []
    for i in range(7):
        for j in range(7):
            exact_scores.append(((i, j), float(matrix[i, j])))
    exact_scores.sort(key=lambda x: x[1], reverse=True)
    top_3_scores = exact_scores[:3]

    # Motor de Córners (Poisson sobre línea proyectada dinámica)
    exp_corners_home = ((h["Corners_Favor"] + a["Corners_Contra"]) / 2.0) * (1.0 + 0.08 * coef_diff)
    exp_corners_away = ((a["Corners_Favor"] + h["Corners_Contra"]) / 2.0) * (1.0 - 0.06 * coef_diff)
    exp_corners_home = float(np.clip(exp_corners_home, 2.0, 10.5))
    exp_corners_away = float(np.clip(exp_corners_away, 1.5, 9.5))
    total_corners = exp_corners_home + exp_corners_away

    # Línea dinámica estándar (.5) cercana a la expectativa o 9.5
    corner_line = round(total_corners) - 0.5
    corner_line = float(np.clip(corner_line, 8.5, 11.5))
    p_corners_over = float(1.0 - poisson.cdf(int(corner_line), total_corners))
    p_corners_under = 1.0 - p_corners_over

    # Pick Sugerido Algorítmico (Sharp Syndicate Selection)
    candidates = [
        (f"{home_team} ML (1)", p_home),
        (f"{away_team} ML (2)", p_away),
        (f"{fav_name} HA -1.5", p_fav_ah15),
        (f"{fav_name} HA -2.5", p_fav_ah25),
        ("Over 2.5 Goles", p_over25),
        ("Over 3.5 Goles", p_over35),
        ("Ambos Anotan (Sí)", p_btts_yes),
    ]
    # Filtra el pick con mejor balance de alta probabilidad (Sweet Spot Sharp >= 58%)
    best_pick_name, best_pick_prob = max(candidates, key=lambda item: item[1])

    return {
        "home": home_team,
        "away": away_team,
        "coef_home": float(h["UEFA_Coef"]),
        "coef_away": float(a["UEFA_Coef"]),
        "coef_diff": coef_diff * 100.0,
        "xg_home": xg_home,
        "xg_away": xg_away,
        "xg_total": xg_home + xg_away,
        "p_home": p_home,
        "p_draw": p_draw,
        "p_away": p_away,
        "p_1x": p_1x,
        "p_x2": p_x2,
        "p_12": p_12,
        "p_dnb_home": p_dnb_home,
        "p_dnb_away": p_dnb_away,
        "fav_name": fav_name,
        "p_fav_ah15": p_fav_ah15,
        "p_fav_ah25": p_fav_ah25,
        "p_over25": p_over25,
        "p_under25": p_under25,
        "p_over35": p_over35,
        "p_under35": p_under35,
        "p_btts_yes": p_btts_yes,
        "p_btts_no": p_btts_no,
        "p_cs_home": p_cs_home,
        "p_cs_away": p_cs_away,
        "top_3_scores": top_3_scores,
        "exp_corners_home": exp_corners_home,
        "exp_corners_away": exp_corners_away,
        "total_corners": total_corners,
        "corner_line": corner_line,
        "p_corners_over": p_corners_over,
        "p_corners_under": p_corners_under,
        "best_pick_name": best_pick_name,
        "best_pick_prob": best_pick_prob,
    }

def team_initials(name: str) -> str:
    parts = name.split()
    if len(parts) == 1:
        return name[:3].upper()
    return (parts[0][0] + parts[1][:2]).upper()

# ==============================================================================
# 3. HEADER PRINCIPAL & ESTADO DE SESIÓN
# ==============================================================================
st.markdown("""
<div class="terminal-header">
    <div>
        <div class="terminal-title">⚡ TERMINAL SHARP: UCL QUANT SCANNER</div>
        <div class="terminal-sub">BIVARIATE POISSON + DIXON-COLES // UEFA COEFFICIENT ASYMMETRY ENGINE // 90-MIN MATCH ODDS ONLY</div>
    </div>
    <div class="terminal-badge">SHARP SYNDICATE v4.2 // CYBER-QUANT UI</div>
</div>
""", unsafe_allow_html=True)

DEFAULT_FIXTURES = [
    ("Manchester City", "Sabah FK"),
    ("Real Madrid", "Borussia Dortmund"),
    ("Bayern Munich", "Slovan Bratislava"),
    ("Barcelona", "Bayern Munich"),
    ("Arsenal", "PSG"),
    ("Inter Milan", "RB Leipzig" if "RB Leipzig" in TEAMS else "Atalanta"),
    ("Bayer Leverkusen", "AC Milan"),
    ("Liverpool" if "Liverpool" in TEAMS else "Sporting CP", "Sturm Graz"),
    ("Atlético Madrid", "Benfica")
]

if "scanned" not in st.session_state:
    st.session_state.scanned = False
if "fixtures" not in st.session_state:
    st.session_state.fixtures = DEFAULT_FIXTURES

# ==============================================================================
# 4. FORMULARIO DE 9 CRUCES CON COLAPSO AUTOMÁTICO (st.expander + st.form)
# ==============================================================================
with st.expander("📡 CONFIGURADOR DE LA JORNADA EUROPEA (9 CRUCES UCL - 90 MIN)", expanded=not st.session_state.scanned):
    with st.form("ucl_scanner_form"):
        st.caption("Selecciona los 9 enfrentamientos de la jornada europea. Al ejecutar el escáner, este panel se colapsará automáticamente y desplegará el Radar Ejecutivo.")
        selected_pairs = []
        for idx in range(9):
            c1, c2, c3 = st.columns([5, 1, 5])
            def_h, def_a = st.session_state.fixtures[idx]
            h_idx = TEAMS.index(def_h) if def_h in TEAMS else (idx * 2) % len(TEAMS)
            a_idx = TEAMS.index(def_a) if def_a in TEAMS else (idx * 2 + 1) % len(TEAMS)
            with c1:
                h_team = st.selectbox(f"Local #{idx+1}", TEAMS, index=h_idx, key=f"h_{idx}")
            with c2:
                st.markdown("<div style='text-align:center; padding-top:28px; font-family:Orbitron; color:#00f0ff; font-weight:800;'>VS</div>", unsafe_allow_html=True)
            with c3:
                a_team = st.selectbox(f"Visita #{idx+1}", TEAMS, index=a_idx, key=f"a_{idx}")
            selected_pairs.append((h_team, a_team))

        submitted = st.form_submit_button("⚡ EJECUTAR ESCÁNER CUANTITATIVO UCL (9 PARTIDOS)", use_container_width=True)
        if submitted:
            st.session_state.fixtures = selected_pairs
            st.session_state.scanned = True
            st.rerun()

# ==============================================================================
# 5. PROCESAMIENTO DEL RADAR EJECUTIVO Y DESGLOSE POR PARTIDO
# ==============================================================================
if st.session_state.scanned:
    results = []
    for (h_team, a_team) in st.session_state.fixtures:
        if h_team != a_team:
            results.append(simulate_ucl_match(h_team, a_team, df_stats))

    if not results:
        st.warning("Selecciona equipos distintos entre Local y Visita.")
        st.stop()

    # --- CÁLCULO DE LAS 4 TARJETAS DEL RADAR EJECUTIVO ---
    # 1. EL LOCK (1X2)
    lock_match = max(results, key=lambda r: max(r["p_home"], r["p_away"]))
    lock_is_home = lock_match["p_home"] >= lock_match["p_away"]
    lock_team = lock_match["home"] if lock_is_home else lock_match["away"]
    lock_prob = lock_match["p_home"] if lock_is_home else lock_match["p_away"]
    lock_dec, lock_amer = prob_to_fair_odds(lock_prob)

    # 2. FIJA DE GOLES (Over 2.5 / 3.5)
    goals_match = max(results, key=lambda r: r["p_over25"])
    use_35 = goals_match["p_over35"] >= 0.58
    goals_label = "OVER 3.5 GOLES" if use_35 else "OVER 2.5 GOLES"
    goals_prob = goals_match["p_over35"] if use_35 else goals_match["p_over25"]
    goals_dec, goals_amer = prob_to_fair_odds(goals_prob)

    # 3. AMBOS ANOTAN (BTTS)
    btts_match = max(results, key=lambda r: r["p_btts_yes"])
    btts_prob = btts_match["p_btts_yes"]
    btts_dec, btts_amer = prob_to_fair_odds(btts_prob)

    # 4. REY DEL CÓRNER
    corner_match = max(results, key=lambda r: r["total_corners"])
    corner_prob = corner_match["p_corners_over"]
    corner_dec, corner_amer = prob_to_fair_odds(corner_prob)

    st.markdown('<div class="radar-section-title">📡 RADAR EJECUTIVO DE LA JORNADA EUROPEA // TOP PICKS +EV</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="radar-grid">
        <div class="radar-card">
            <div class="radar-tag">🔒 EL LOCK (1X2)</div>
            <div class="radar-match">{lock_match['home']} vs {lock_match['away']}</div>
            <div class="radar-pick">{lock_team} ML ({lock_prob*100:.1f}%)</div>
            <div class="radar-meta">
                <span>Fair: {lock_dec:.2f} ({lock_amer})</span>
                <span>Δ Coef: {abs(lock_match['coef_diff']):.0f} pts</span>
            </div>
        </div>
        <div class="radar-card">
            <div class="radar-tag">⚡ FIJA DE GOLES</div>
            <div class="radar-match">{goals_match['home']} vs {goals_match['away']}</div>
            <div class="radar-pick">{goals_label} ({goals_prob*100:.1f}%)</div>
            <div class="radar-meta">
                <span>Fair: {goals_dec:.2f} ({goals_amer})</span>
                <span>xG Total: {goals_match['xg_total']:.2f}</span>
            </div>
        </div>
        <div class="radar-card">
            <div class="radar-tag">🤝 AMBOS ANOTAN (BTTS)</div>
            <div class="radar-match">{btts_match['home']} vs {btts_match['away']}</div>
            <div class="radar-pick">BTTS: SÍ ({btts_prob*100:.1f}%)</div>
            <div class="radar-meta">
                <span>Fair: {btts_dec:.2f} ({btts_amer})</span>
                <span>xG: {btts_match['xg_home']:.2f} - {btts_match['xg_away']:.2f}</span>
            </div>
        </div>
        <div class="radar-card">
            <div class="radar-tag">🚩 REY DEL CÓRNER</div>
            <div class="radar-match">{corner_match['home']} vs {corner_match['away']}</div>
            <div class="radar-pick">OVER {corner_match['corner_line']} ({corner_prob*100:.1f}%)</div>
            <div class="radar-meta">
                <span>Fair: {corner_dec:.2f} ({corner_amer})</span>
                <span>Proy: {corner_match['total_corners']:.1f} Crn</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ==============================================================================
    # 6. DESGLOSE INDIVIDUAL POR PARTIDO (CYBER-QUANT SCOREBOARD & MARKETS)
    # ==============================================================================
    for idx, r in enumerate(results, start=1):
        h_ini = team_initials(r["home"])
        a_ini = team_initials(r["away"])
        best_dec, best_amer = prob_to_fair_odds(r["best_pick_prob"])

        # Porcentajes Barra Tricolor 1X2
        w_home = r["p_home"] * 100
        w_draw = r["p_draw"] * 100
        w_away = r["p_away"] * 100

        st.markdown(f"""
        <div class="match-container">
            <!-- SCOREBOARD TV HEADER -->
            <div class="tv-scoreboard">
                <div class="team-side home">
                    <div class="team-badge-circle">{h_ini}</div>
                    <div>
                        <div class="team-name">{r['home']}</div>
                        <div class="team-submeta">UEFA Coef: {r['coef_home']:.1f} // Córners Proy: {r['exp_corners_home']:.1f}</div>
                    </div>
                </div>
                <div class="tv-center">
                    <div class="xg-display">{r['xg_home']:.2f} &nbsp;—&nbsp; {r['xg_away']:.2f}</div>
                    <div class="xg-label">xG PROYECTADO (xG TOTAL: {r['xg_total']:.2f})</div>
                    <div class="edge-pill">Δ UEFA COEF: {r['coef_diff']:+.1f} PTS</div>
                </div>
                <div class="team-side away">
                    <div>
                        <div class="team-name">{r['away']}</div>
                        <div class="team-submeta">UEFA Coef: {r['coef_away']:.1f} // Córners Proy: {r['exp_corners_away']:.1f}</div>
                    </div>
                    <div class="team-badge-circle">{a_ini}</div>
                </div>
            </div>

            <!-- BARRA TRICOLOR 1X2 (TUG-OF-WAR) -->
            <div class="tug-wrapper">
                <div class="tug-labels">
                    <span style="color:#00ff9d;">1 LOCAL ({w_home:.1f}%)</span>
                    <span style="color:#b0b8c8;">X EMPATE ({w_draw:.1f}%)</span>
                    <span style="color:#ffb800;">2 VISITA ({w_away:.1f}%)</span>
                </div>
                <div class="tug-bar">
                    <div class="tug-seg-home" style="width:{w_home:.2f}%;"></div>
                    <div class="tug-seg-draw" style="width:{w_draw:.2f}%;"></div>
                    <div class="tug-seg-away" style="width:{w_away:.2f}%;"></div>
                </div>
            </div>

            <!-- BANNER DE PICK SUGERIDO -->
            <div class="sharp-banner">
                <div class="sharp-banner-left">🎯 PICK SUGERIDO SHARP: <span style="color:#00ff9d;">{r['best_pick_name']}</span></div>
                <div class="sharp-banner-right">PROB: {r['best_pick_prob']*100:.1f}% &nbsp;|&nbsp; FAIR ODD: {best_dec:.2f} ({best_amer})</div>
            </div>

            <!-- FILA 1X2 -->
            <div class="section-sub">⚡ MERCADO PRINCIPAL 1X2 (90 MINUTOS)</div>
            <div class="market-row-3">
                <div class="quant-card">
                    <div class="qc-title">1 // {r['home']}</div>
                    <div class="qc-prob" style="color:#00ff9d;">{r['p_home']*100:.1f}%</div>
                    <div class="qc-odds">{format_odds_line(r['p_home'])}</div>
                </div>
                <div class="quant-card">
                    <div class="qc-title">X // EMPATE</div>
                    <div class="qc-prob" style="color:#c9d1d9;">{r['p_draw']*100:.1f}%</div>
                    <div class="qc-odds">{format_odds_line(r['p_draw'])}</div>
                </div>
                <div class="quant-card">
                    <div class="qc-title">2 // {r['away']}</div>
                    <div class="qc-prob" style="color:#ffb800;">{r['p_away']*100:.1f}%</div>
                    <div class="qc-odds">{format_odds_line(r['p_away'])}</div>
                </div>
            </div>

            <!-- FILA DE PROTECCIÓN Y HÁNDICAPS ASIÁTICOS (-1.5 / -2.5) -->
            <div class="section-sub">🛡️ LÍNEAS DE PROTECCIÓN & HÁNDICAPS ASIÁTICOS DE GOLEADA</div>
            <div class="market-row-4">
                <div class="quant-card">
                    <div class="qc-title">DNB // {r['home']} / {r['away']}</div>
                    <div class="qc-prob">{r['p_dnb_home']*100:.1f}% <span style="font-size:0.85rem; color:#8b949e;">/ {r['p_dnb_away']*100:.1f}%</span></div>
                    <div class="qc-odds">1: {prob_to_fair_odds(r['p_dnb_home'])[0]:.2f} | 2: {prob_to_fair_odds(r['p_dnb_away'])[0]:.2f}</div>
                </div>
                <div class="quant-card">
                    <div class="qc-title">DOBLE OPORTUNIDAD (1X / X2)</div>
                    <div class="qc-prob">{r['p_1x']*100:.1f}% <span style="font-size:0.85rem; color:#8b949e;">/ {r['p_x2']*100:.1f}%</span></div>
                    <div class="qc-odds">1X: {prob_to_fair_odds(r['p_1x'])[0]:.2f} | X2: {prob_to_fair_odds(r['p_x2'])[0]:.2f}</div>
                </div>
                <div class="quant-card">
                    <div class="qc-title">HÁNDICAP ASIÁTICO -1.5 ({r['fav_name']})</div>
                    <div class="qc-prob" style="color:#00f0ff;">{r['p_fav_ah15']*100:.1f}%</div>
                    <div class="qc-odds">{format_odds_line(r['p_fav_ah15'])}</div>
                </div>
                <div class="quant-card">
                    <div class="qc-title">HÁNDICAP ASIÁTICO -2.5 ({r['fav_name']})</div>
                    <div class="qc-prob" style="color:#00f0ff;">{r['p_fav_ah25']*100:.1f}%</div>
                    <div class="qc-odds">{format_odds_line(r['p_fav_ah25'])}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # BLOQUE INFERIOR DIVIDIDO (IZQUIERDA: PODIO + CÓRNERS | DERECHA: GOLES, BTTS, PORTERÍA A CERO)
        col_left, col_right = st.columns([1, 1])

        with col_left:
            s1, p1 = r["top_3_scores"][0]
            s2, p2 = r["top_3_scores"][1]
            s3, p3 = r["top_3_scores"][2]
            d1, a1 = prob_to_fair_odds(p1)
            d2, a2 = prob_to_fair_odds(p2)
            d3, a3 = prob_to_fair_odds(p3)

            st.markdown(f"""
            <div class="section-sub">🏅 PODIO DE MARCADORES EXACTOS (DIXON-COLES)</div>
            <div class="podium-grid">
                <div class="podium-card gold">
                    <div class="podium-medal">🥇 ORO</div>
                    <div class="podium-score">{s1[0]} - {s1[1]}</div>
                    <div class="podium-prob">{p1*100:.1f}%</div>
                    <div class="podium-odd">Fair: {d1:.2f} ({a1})</div>
                </div>
                <div class="podium-card silver">
                    <div class="podium-medal">🥈 PLATA</div>
                    <div class="podium-score">{s2[0]} - {s2[1]}</div>
                    <div class="podium-prob">{p2*100:.1f}%</div>
                    <div class="podium-odd">Fair: {d2:.2f} ({a2})</div>
                </div>
                <div class="podium-card bronze">
                    <div class="podium-medal">🥉 BRONCE</div>
                    <div class="podium-score">{s3[0]} - {s3[1]}</div>
                    <div class="podium-prob">{p3*100:.1f}%</div>
                    <div class="podium-odd">Fair: {d3:.2f} ({a3})</div>
                </div>
            </div>

            <div class="section-sub">🚩 PROYECCIÓN DE CÓRNERS (LÍNEA {r['corner_line']})</div>
            <div class="market-row-2">
                <div class="quant-card">
                    <div class="qc-title">OVER {r['corner_line']} CÓRNERS (Proy: {r['total_corners']:.1f})</div>
                    <div class="qc-prob" style="color:#00ff9d;">{r['p_corners_over']*100:.1f}%</div>
                    <div class="qc-odds">{format_odds_line(r['p_corners_over'])}</div>
                </div>
                <div class="quant-card">
                    <div class="qc-title">UNDER {r['corner_line']} CÓRNERS ({r['exp_corners_home']:.1f} vs {r['exp_corners_away']:.1f})</div>
                    <div class="qc-prob" style="color:#ffb800;">{r['p_corners_under']*100:.1f}%</div>
                    <div class="qc-odds">{format_odds_line(r['p_corners_under'])}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_right:
            st.markdown(f"""
            <div class="section-sub">⚽ MÉTRICAS DE GOLES, BTTS & PORTERÍA A CERO</div>
            <div class="market-row-2">
                <div class="quant-card">
                    <div class="qc-title">OVER 2.5 GOLES / UNDER 2.5</div>
                    <div class="qc-prob" style="color:#00ff9d;">{r['p_over25']*100:.1f}% <span style="font-size:0.85rem; color:#8b949e;">/ {r['p_under25']*100:.1f}%</span></div>
                    <div class="qc-odds">O2.5: {prob_to_fair_odds(r['p_over25'])[0]:.2f} ({prob_to_fair_odds(r['p_over25'])[1]})</div>
                </div>
                <div class="quant-card">
                    <div class="qc-title">OVER 3.5 GOLES / UNDER 3.5</div>
                    <div class="qc-prob" style="color:#00f0ff;">{r['p_over35']*100:.1f}% <span style="font-size:0.85rem; color:#8b949e;">/ {r['p_under35']*100:.1f}%</span></div>
                    <div class="qc-odds">O3.5: {prob_to_fair_odds(r['p_over35'])[0]:.2f} ({prob_to_fair_odds(r['p_over35'])[1]})</div>
                </div>
            </div>
            <div class="market-row-2">
                <div class="quant-card">
                    <div class="qc-title">AMBOS ANOTAN (BTTS SÍ / NO)</div>
                    <div class="qc-prob">{r['p_btts_yes']*100:.1f}% <span style="font-size:0.85rem; color:#8b949e;">/ {r['p_btts_no']*100:.1f}%</span></div>
                    <div class="qc-odds">Sí: {prob_to_fair_odds(r['p_btts_yes'])[0]:.2f} | No: {prob_to_fair_odds(r['p_btts_no'])[0]:.2f}</div>
                </div>
                <div class="quant-card">
                    <div class="qc-title">PORTERÍA A CERO (CLEAN SHEET)</div>
                    <div class="qc-prob">{r['p_cs_home']*100:.1f}% <span style="font-size:0.85rem; color:#8b949e;">/ {r['p_cs_away']*100:.1f}%</span></div>
                    <div class="qc-odds">Loc: {prob_to_fair_odds(r['p_cs_home'])[0]:.2f} | Vis: {prob_to_fair_odds(r['p_cs_away'])[0]:.2f}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<hr style='border:0; border-top:1px solid rgba(0,240,255,0.15); margin: 18px 0 32px 0;'>", unsafe_allow_html=True)
else:
    st.info("👆 Configura los 9 cruces en el panel superior y presiona **EJECUTAR ESCÁNER CUANTITATIVO UCL** para desplegar el Radar Ejecutivo y los modelos de 90 minutos.")
