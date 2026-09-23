import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from alpaca.trading.client import TradingClient
from datetime import datetime

# ==========================================
# INSTELLINGEN
# ==========================================
API_KEY = "PKTF56354E6F7FPCMTNCWV3YV5"
SECRET_KEY = "5z4pRB5NXjBMvcXix6ywptgffZc4w8XTJNzoESBsqFgK"

tickers = ["NVDA", "AVGO", "MSFT", "AMD", "GOOGL"]
korte_periode = 20
lange_periode = 50
start_kapitaal = 100000

# ==========================================
# PAGINA CONFIGURATIE
# ==========================================
st.set_page_config(
    page_title="Quant Terminal",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CSS STYLING
# ==========================================
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0e1117 0%, #1a1f2e 100%);
    }
    
    .main-header {
        font-family: 'Courier New', monospace;
        font-size: 1.6rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00d4ff 0%, #00ff88 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 2px;
        margin-bottom: 0;
    }
    
    .sub-header {
        font-family: 'Courier New', monospace;
        color: #8892a6;
        font-size: 0.8rem;
        letter-spacing: 1px;
    }
    
    .kpi-card {
        background: linear-gradient(135deg, #1e2430 0%, #2a3142 100%);
        border: 1px solid #00d4ff33;
        border-radius: 6px;
        padding: 0.6rem 0.8rem;
        box-shadow: 0 2px 8px rgba(0, 212, 255, 0.08);
    }
    
    .kpi-label {
        color: #8892a6;
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-family: 'Courier New', monospace;
    }
    
    .kpi-value {
        color: #ffffff;
        font-size: 1.05rem;
        font-weight: 700;
        font-family: 'Courier New', monospace;
        margin-top: 0.15rem;
    }
    
    .kpi-delta-pos {
        color: #00ff88;
        font-size: 0.7rem;
        font-family: 'Courier New', monospace;
    }
    
    .kpi-delta-neg {
        color: #ff3b5c;
        font-size: 0.7rem;
        font-family: 'Courier New', monospace;
    }
    
    .section-header {
        font-family: 'Courier New', monospace;
        color: #00d4ff;
        font-size: 0.9rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        border-bottom: 1px solid #00d4ff33;
        padding-bottom: 0.4rem;
        margin-top: 1.2rem;
        margin-bottom: 0.8rem;
    }
    
    .stDataFrame {
        border-radius: 6px;
        overflow: hidden;
    }
    
    [data-testid="stSidebar"] {
        background: #0e1117;
        border-right: 1px solid #00d4ff22;
    }
    
    [data-testid="stSidebar"] * {
        color: #d1d9e6 !important;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #00d4ff !important;
        font-family: 'Courier New', monospace;
        letter-spacing: 1px;
    }
    
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] li,
    [data-testid="stSidebar"] span {
        color: #d1d9e6 !important;
        font-size: 0.9rem;
    }
    
    [data-testid="stSidebar"] strong {
        color: #00ff88 !important;
    }
    
    [data-testid="stSidebar"] code {
        color: #00d4ff !important;
        background: #1e2430 !important;
        padding: 2px 6px;
        border-radius: 3px;
        font-family: 'Courier New', monospace;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .status-live {
        display: inline-block;
        width: 8px;
        height: 8px;
        background: #00ff88;
        border-radius: 50%;
        box-shadow: 0 0 10px #00ff88;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.4; }
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown('<p class="main-header">⚡ QUANT TERMINAL</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">v2.0 | PAPER TRADING</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("### ⚙️ Strategic Config")
    st.markdown(f"""
    - **Strategy:** MA Crossover
    - **Fast MA:** {korte_periode} days
    - **Slow MA:** {lange_periode} days
    - **Stop-Loss:** 5%
    - **Rebalance:** Yearly
    """)
    
    st.markdown("---")
    st.markdown("### 📊 Trading Universe")
    for t in tickers:
        st.markdown(f"- `{t}`")
    
    st.markdown("---")
    st.markdown("""
    <div style='color: #ffb800; font-size: 0.85rem; font-family: Courier New; padding: 0.8rem; background: #2a3142; border-radius: 6px; border-left: 3px solid #ffb800;'>
    ⚠️ <b>PAPER TRADING MODE</b><br>
    No real capital at risk
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================
col_header_left, col_header_right = st.columns([3, 1])

with col_header_left:
    st.markdown('<p class="main-header">⚡ QUANT TRADING TERMINAL</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sub-header"><span class="status-live"></span> LIVE | {datetime.now().strftime("%A, %d %B %Y | %H:%M:%S")}</p>', unsafe_allow_html=True)

with col_header_right:
    st.markdown("""
    <div style='text-align: right; font-family: Courier New; color: #8892a6; font-size: 0.75rem; padding-top: 0.8rem;'>
    ALPACA MARKETS<br>
    PAPER ACCOUNT
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# VERBINDEN MET ALPACA
# ==========================================
@st.cache_resource
def verbind_alpaca():
    return TradingClient(API_KEY, SECRET_KEY, paper=True)

try:
    trading_client = verbind_alpaca()
    account = trading_client.get_account()
except Exception as e:
    st.error(f"Connection failed: {e}")
    st.stop()

# ==========================================
# KPI CARDS - ACCOUNT OVERZICHT
# ==========================================
st.markdown('<p class="section-header">◆ Account Overview</p>', unsafe_allow_html=True)

cash = float(account.cash)
portfolio_value = float(account.portfolio_value)
buying_power = float(account.buying_power)
winst = portfolio_value - start_kapitaal
winst_pct = (winst / start_kapitaal) * 100

col1, col2, col3, col4 = st.columns(4, gap="small")

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Cash Balance</div>
        <div class="kpi-value">${cash:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Portfolio Value</div>
        <div class="kpi-value">${portfolio_value:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Buying Power</div>
        <div class="kpi-value">${buying_power:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    delta_class = "kpi-delta-pos" if winst >= 0 else "kpi-delta-neg"
    pijltje = "▲" if winst >= 0 else "▼"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total P&L</div>
        <div class="kpi-value">${winst:,.2f}</div>
        <div class="{delta_class}">{pijltje} {winst_pct:+.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# HUIDIGE POSITIES
# ==========================================
st.markdown('<p class="section-header">◆ Open Positions</p>', unsafe_allow_html=True)

try:
    posities = trading_client.get_all_positions()
    
    if not posities:
        st.info("No open positions. Awaiting entry signals...")
    else:
        totaal_marktwaarde = sum(float(p.market_value) for p in posities)
        totaal_pl = sum(float(p.unrealized_pl) for p in posities)
        aantal_winst = sum(1 for p in posities if float(p.unrealized_pl) > 0)
        
        col1, col2, col3, col4 = st.columns(4, gap="small")
        with col1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Open Positions</div>
                <div class="kpi-value">{len(posities)}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Market Value</div>
                <div class="kpi-value">${totaal_marktwaarde:,.2f}</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            delta_class = "kpi-delta-pos" if totaal_pl >= 0 else "kpi-delta-neg"
            pijltje = "▲" if totaal_pl >= 0 else "▼"
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Unrealized P&L</div>
                <div class="kpi-value">${totaal_pl:,.2f}</div>
                <div class="{delta_class}">{pijltje} {totaal_pl/totaal_marktwaarde*100:+.2f}%</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            win_rate = (aantal_winst / len(posities) * 100) if posities else 0
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Win Rate</div>
                <div class="kpi-value">{win_rate:.0f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        positie_data = []
        for p in posities:
            pl_pct = float(p.unrealized_plpc) * 100
            positie_data.append({
                "Symbol": p.symbol,
                "Qty": float(p.qty),
                "Entry": float(p.avg_entry_price),
                "Current": float(p.current_price),
                "Value": float(p.market_value),
                "P&L": float(p.unrealized_pl),
                "P&L %": pl_pct,
                "Status": "🟢 PROFIT" if pl_pct > 0 else "🔴 LOSS"
            })
        
        df_posities = pd.DataFrame(positie_data)
        
        st.dataframe(
            df_posities.style.format({
                "Entry": "${:,.2f}",
                "Current": "${:,.2f}",
                "Value": "${:,.2f}",
                "P&L": "${:,.2f}",
                "P&L %": "{:+.2f}%"
            }).background_gradient(subset=["P&L %"], cmap="RdYlGn"),
            width='stretch',
            hide_index=True
        )
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown("#### Portfolio Allocation")
            fig_pie = go.Figure(data=[go.Pie(
                labels=df_posities["Symbol"],
                values=df_posities["Value"],
                hole=0.5,
                marker=dict(colors=['#00d4ff', '#00ff88', '#ffb800', '#ff3b5c', '#a855f7']),
                textinfo='label+percent',
                textfont=dict(family="Courier New", size=12)
            )])
            fig_pie.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=320,
                showlegend=False,
                margin=dict(t=20, b=20, l=20, r=20)
            )
            st.plotly_chart(fig_pie, width='stretch')
        
        with col_chart2:
            st.markdown("#### P&L per Position")
            kleuren = ['#00ff88' if x > 0 else '#ff3b5c' for x in df_posities["P&L"]]
            fig_bar = go.Figure(data=[go.Bar(
                x=df_posities["Symbol"],
                y=df_posities["P&L"],
                marker_color=kleuren,
                text=df_posities["P&L"].apply(lambda x: f"${x:,.0f}"),
                textposition='outside',
                textfont=dict(family="Courier New", size=11)
            )])
            fig_bar.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=320,
                margin=dict(t=20, b=20, l=20, r=20),
                yaxis_title="P&L ($)",
                xaxis_title=""
            )
            st.plotly_chart(fig_bar, width='stretch')
        
except Exception as e:
    st.error(f"Error fetching positions: {e}")

# ==========================================
# LIVE SIGNALEN
# ==========================================
st.markdown('<p class="section-header">◆ Signal Monitor</p>', unsafe_allow_html=True)

signaal_data = []
grafiek_data = {}

with st.spinner("Analyzing market signals..."):
    for ticker in tickers:
        try:
            data = yf.download(ticker, period="6mo", auto_adjust=True, progress=False)
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)
            
            data["MA20"] = data["Close"].rolling(korte_periode).mean()
            data["MA50"] = data["Close"].rolling(lange_periode).mean()
            
            laatste_prijs = float(data["Close"].iloc[-1])
            laatste_ma20 = float(data["MA20"].iloc[-1])
            laatste_ma50 = float(data["MA50"].iloc[-1])
            
            koop_signaal = laatste_ma20 > laatste_ma50
            verschil_pct = ((laatste_ma20 / laatste_ma50) - 1) * 100
            
            signaal_data.append({
                "Symbol": ticker,
                "Price": laatste_prijs,
                "MA20": laatste_ma20,
                "MA50": laatste_ma50,
                "Spread %": verschil_pct,
                "Signal": "🟢 BUY" if koop_signaal else "🔴 SELL"
            })
            
            grafiek_data[ticker] = data
            
        except Exception as e:
            signaal_data.append({
                "Symbol": ticker,
                "Price": 0,
                "MA20": 0,
                "MA50": 0,
                "Spread %": 0,
                "Signal": "⚠️ ERROR"
            })

df_signalen = pd.DataFrame(signaal_data)

st.dataframe(
    df_signalen.style.format({
        "Price": "${:,.2f}",
        "MA20": "${:,.2f}",
        "MA50": "${:,.2f}",
        "Spread %": "{:+.2f}%"
    }).background_gradient(subset=["Spread %"], cmap="RdYlGn"),
    width='stretch',
    hide_index=True
)

# ==========================================
# INTERACTIEVE GRAFIEK
# ==========================================
st.markdown('<p class="section-header">◆ Technical Analysis</p>', unsafe_allow_html=True)

geselecteerd = st.selectbox("Select asset:", tickers, label_visibility="collapsed")

if geselecteerd in grafiek_data:
    data = grafiek_data[geselecteerd]
    
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.75, 0.25],
        subplot_titles=(f"{geselecteerd} - Price Action", "Volume")
    )
    
    fig.add_trace(go.Scatter(
        x=data.index, y=data["Close"],
        mode='lines', name='Price',
        line=dict(color='#00d4ff', width=2)
    ), row=1, col=1)
    
    fig.add_trace(go.Scatter(
        x=data.index, y=data["MA20"],
        mode='lines', name=f'MA{korte_periode}',
        line=dict(color='#ffb800', width=1.5)
    ), row=1, col=1)
    
    fig.add_trace(go.Scatter(
        x=data.index, y=data["MA50"],
        mode='lines', name=f'MA{lange_periode}',
        line=dict(color='#ff3b5c', width=1.5)
    ), row=1, col=1)
    
    if "Volume" in data.columns:
        fig.add_trace(go.Bar(
            x=data.index, y=data["Volume"],
            name='Volume',
            marker_color='#6c757d'
        ), row=2, col=1)
    
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=550,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=40, b=20, l=20, r=20)
    )
    
    fig.update_xaxes(showgrid=True, gridcolor='#1e2430')
    fig.update_yaxes(showgrid=True, gridcolor='#1e2430')
    
    st.plotly_chart(fig, width='stretch')

# ==========================================
# LOG BESTAND
# ==========================================
st.markdown('<p class="section-header">◆ Activity Log</p>', unsafe_allow_html=True)

try:
    with open("quant_strategy.log", "r") as f:
        log_regels = f.readlines()
    
    laatste_regels = log_regels[-15:]
    st.code("".join(laatste_regels), language="log")
except FileNotFoundError:
    st.warning("No log file found. Run your strategy first.")

# ==========================================
# FOOTER
# ==========================================
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: #8892a6; font-family: Courier New; font-size: 0.7rem;'>
⚡ QUANT TRADING TERMINAL v2.0 | Last refresh: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}<br>
PAPER TRADING MODE - NO REAL CAPITAL AT RISK
</div>
""", unsafe_allow_html=True)