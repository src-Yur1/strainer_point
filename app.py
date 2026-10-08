import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import hashlib
import qrcode
import io
from datetime import datetime
import base64

# ==============================================================================
# 1. CONFIGURAÇÕES DA PÁGINA E DESIGN SYSTEM (MONA SANS + HUBOT SANS + NEON)
# ==============================================================================
st.set_page_config(
   page_title="Strainer Point | SAD Lei do Bem",
    page_icon="space_invader.jpg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injeção de CSS e Tipografia Avançada
st.markdown("""
<style>
    /* Importação de Mona Sans e Hubot Sans */
    @import url('https://cdn.jsdelivr.net/npm/@github/mona-sans@1.0.1/dist/Mona-Sans.min.css');
    @import url('https://cdn.jsdelivr.net/npm/@github/hubot-sans@1.0.1/dist/Hubot-Sans.min.css');

    :root {
        --font-main: 'Mona Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        --font-tech: 'Hubot Sans', 'Mona Sans', sans-serif;
        --font-code: 'SFMono-Regular', Consolas, Menlo, 'Liberation Mono', Courier, monospace;
        --primary-glow: #00FF87;
        --primary-deep: #0b1f14;
        --card-bg: rgba(13, 24, 18, 0.65);
    }

    /* 1. Tipografia Global e Fundo */
    html, body, [class*="css"], .stApp {
        font-family: var(--font-main) !important;
        background: radial-gradient(circle at 50% -10%, #0b1f14 0%, #060b08 45%, #030604 100%) !important;
        color: #E2E8F0 !important;
    }

    /* 2. Blocos de Código (Monospace Oficial) */
    code, pre, .stCode, div[data-testid="stMarkdownContainer"] code {
        font-family: var(--font-code) !important;
        font-size: 13px !important;
        background: rgba(0, 255, 135, 0.08) !important;
        color: #00FF87 !important;
        border: 1px solid rgba(0, 255, 135, 0.25) !important;
        border-radius: 6px !important;
        padding: 3px 6px !important;
    }

    /* 3. Títulos e Badges com Tipografia Mona Sans e Hubot Sans */
    .hero-badge {
        display: inline-block;
        font-family: var(--font-tech) !important;
        background: rgba(0, 255, 135, 0.12);
        border: 1px solid var(--primary-glow);
        color: var(--primary-glow);
        padding: 4px 14px;
        border-radius: 9999px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        margin-bottom: 8px;
        box-shadow: 0 0 15px rgba(0, 255, 135, 0.2);
    }
    
    .main-header {
        font-family: var(--font-main) !important;
        font-size: 28px;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: -0.8px;
        margin-bottom: 4px;
    }
    .main-header span {
        color: var(--primary-glow);
        text-shadow: 0 0 24px rgba(0, 255, 135, 0.45);
    }
    
    .sub-header {
        font-size: 14.5px;
        color: #94A3B8;
        margin-bottom: 24px;
    }

    /* 4. Cartões Glassmorphism com Animação de Elevação e Expansão */
    .glass-card {
        background: var(--card-bg);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(0, 255, 135, 0.2);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5), inset 0 0 15px rgba(0, 255, 135, 0.03);
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 18px;
        transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1), 
                    border-color 0.35s ease, 
                    box-shadow 0.35s ease !important;
    }
    .glass-card:hover {
        transform: translateY(-4px) scale(1.01) !important;
        border-color: rgba(0, 255, 135, 0.5) !important;
        box-shadow: 0 16px 40px rgba(0, 0, 0, 0.7), 0 0 25px rgba(0, 255, 135, 0.2) !important;
    }

    /* 5. Alertas & Contradições */
    .alert-glass {
        background: rgba(38, 12, 16, 0.75);
        border: 1px solid #EF4444;
        box-shadow: 0 0 25px rgba(239, 68, 68, 0.25);
        border-radius: 14px;
        padding: 16px;
        margin: 14px 0;
        color: #FECACA;
        transition: transform 0.3s ease;
    }
    .alert-glass:hover { transform: scale(1.008); }

    .warning-glass {
        background: rgba(41, 28, 8, 0.75);
        border: 1px solid #F59E0B;
        box-shadow: 0 0 25px rgba(245, 158, 11, 0.25);
        border-radius: 14px;
        padding: 16px;
        margin: 14px 0;
        color: #FDE68A;
    }

    .success-glass {
        background: rgba(10, 36, 22, 0.8);
        border: 1px solid var(--primary-glow);
        box-shadow: 0 0 30px rgba(0, 255, 135, 0.3);
        border-radius: 14px;
        padding: 16px;
        margin: 14px 0;
        color: #DCFCE7;
    }

    /* 6. Badges Oficiais no Formato Pill (Hubot Sans) */
    .badge-elegivel, .badge-ressalva, .badge-nao, .badge-insuf {
        font-family: var(--font-tech) !important;
        letter-spacing: 0.6px;
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 11px;
        display: inline-block;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .badge-elegivel:hover, .badge-ressalva:hover, .badge-nao:hover, .badge-insuf:hover {
        transform: scale(1.05);
    }
    .badge-elegivel { background: rgba(0, 255, 135, 0.15); color: #00FF87; border: 1px solid #00FF87; }
    .badge-ressalva { background: rgba(245, 158, 11, 0.15); color: #F59E0B; border: 1px solid #F59E0B; }
    .badge-nao { background: rgba(239, 68, 68, 0.15); color: #EF4444; border: 1px solid #EF4444; }
    .badge-insuf { background: rgba(148, 163, 184, 0.15); color: #CBD5E1; border: 1px solid #94A3B8; }

    /* 7. Botões Clicáveis com Animação Suave de Ampliação */
    .stButton > button, .stDownloadButton > button {
        font-family: var(--font-tech) !important;
        background: linear-gradient(135deg, #00FF87 0%, #10B981 100%) !important;
        color: #020604 !important;
        font-weight: 800 !important;
        letter-spacing: 0.5px !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 11px 26px !important;
        box-shadow: 0 4px 20px rgba(0, 255, 135, 0.35) !important;
        cursor: pointer !important;
        transform: scale(1) translateY(0) !important;
        transition: transform 0.28s cubic-bezier(0.34, 1.56, 0.64, 1), 
                    box-shadow 0.28s ease, 
                    filter 0.28s ease !important;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        transform: scale(1.045) translateY(-3px) !important;
        box-shadow: 0 12px 32px rgba(0, 255, 135, 0.75) !important;
        filter: brightness(1.1) !important;
    }
    .stButton > button:active, .stDownloadButton > button:active {
        transform: scale(0.97) translateY(1px) !important;
        box-shadow: 0 4px 14px rgba(0, 255, 135, 0.4) !important;
    }

    /* 8. Barra Lateral & Gatilhos de Navegação */
    section[data-testid="stSidebar"] {
        background-color: #050a07 !important;
        border-right: 1px solid rgba(0, 255, 135, 0.15) !important;
    }
    button[data-testid="stSidebarCollapseButton"], 
    div[data-testid="collapsedControl"] button {
        background: rgba(13, 24, 18, 0.7) !important;
        border: 1px solid rgba(0, 255, 135, 0.3) !important;
        border-radius: 10px !important;
        color: #00FF87 !important;
        box-shadow: 0 0 12px rgba(0, 255, 135, 0.15) !important;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    button[data-testid="stSidebarCollapseButton"]:hover, 
    div[data-testid="collapsedControl"] button:hover {
        background: rgba(0, 255, 135, 0.2) !important;
        border-color: #00FF87 !important;
        transform: scale(1.08) !important;
        box-shadow: 0 0 20px rgba(0, 255, 135, 0.4) !important;
    }
    div[data-testid="stSidebar"] div[data-testid="stRadio"] > div[role="radiogroup"] {
        gap: 6px !important;
    }
    div[data-testid="stSidebar"] div[data-testid="stRadio"] label {
        font-family: var(--font-tech) !important;
        background: rgba(13, 24, 18, 0.5) !important;
        border: 1px solid rgba(0, 255, 135, 0.16) !important;
        border-radius: 12px !important;
        padding: 10px 14px !important;
        margin-bottom: 5px !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    div[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover {
        background: rgba(0, 255, 135, 0.08) !important;
        border-color: rgba(0, 255, 135, 0.5) !important;
        transform: translateX(4px) scale(1.015) !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4), 0 0 14px rgba(0, 255, 135, 0.18) !important;
    }
    div[data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) {
        background: rgba(0, 255, 135, 0.15) !important;
        border-color: #00FF87 !important;
        box-shadow: 0 0 18px rgba(0, 255, 135, 0.25), inset 0 0 8px rgba(0, 255, 135, 0.08) !important;
    }
    div[data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) p {
        color: #00FF87 !important;
        font-weight: 700 !important;
        text-shadow: 0 0 10px rgba(0, 255, 135, 0.35) !important;
    }

    /* 9. Métricas e Inputs */
    div[data-testid="stMetricValue"] {
        font-family: var(--font-tech) !important;
        color: #00FF87 !important;
        font-weight: 800 !important;
        font-size: 32px !important;
    }
    div[data-testid="stMetricLabel"] {
        font-family: var(--font-tech) !important;
        color: #94A3B8 !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px;
    }
    div[data-baseweb="select"] > div, .stTextInput > div > div > input, .stTextArea textarea {
        background-color: rgba(15, 26, 20, 0.8) !important;
        border: 1px solid rgba(0, 255, 135, 0.25) !important;
        color: #F8FAFC !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. GERADOR DE QR CODE DINÂMICO
# ==============================================================================
def gerar_qr_code(url: str):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#030805", back_color="#00FF87")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

# ==============================================================================
# 3. BASE DE CASOS HISTÓRICOS DE CALIBRAÇÃO (PRJ01 A PRJ20)
# ==============================================================================
HISTORICOS_CALIBRACAO = {
    "PRJ01": {
        "titulo": "Algoritmo Quântico de Otimização de Rota Logística de Caixa",
        "classe": "Elegível",
        "score": 920,
        "fundamentacao": "Investigação experimental de nova formulação matemática com superação de incerteza tecnológica real.",
        "evidencia_chave": "EVID_MED_01 (medicoes.csv: 15 ensaios comparativos de convergência)."
    },
    "PRJ05": {
        "titulo": "Motor de Inferência de Crédito para Produtores Rurais Familiares",
        "classe": "Com ressalvas",
        "score": 730,
        "fundamentacao": "Mérito experimental robusto nas tarefas de modelagem; contudo, faltou validação empírica para dados de cooperativas agrícolas.",
        "evidencia_chave": "EVID_MED_04 (medicoes.csv: erro de 24% não superado no recorte de cooperativas)."
    },
    "PRJ08": {
        "titulo": "Parametrização e Configuração de Ferramenta Comercial de ITSM",
        "classe": "Não elegível",
        "score": 240,
        "fundamentacao": "Configuração e integração de pacote de mercado já existente; atividade caracterizada como engenharia de rotina.",
        "evidencia_chave": "EVID_DOC_02 (Manual do fornecedor aplicado sem inovação técnica)."
    },
    "PRJ12": {
        "titulo": "Reconhecimento de Voz Regionalizado para Atendimento em Agências",
        "classe": "Evidência insuficiente",
        "score": 480,
        "fundamentacao": "Alegações arquiteturais sem arquivo primário de medições empíricas com acurácia de fonemas. Falta o elo probatório essencial.",
        "evidencia_chave": "Elo ausente: Ausência de 'medicoes.csv' com testes de taxa de erro de palavra (WER)."
    }
}

# ==============================================================================
# 4. BASE DE CASOS DE ANÁLISE ATIVA (PRJ21 A PRJ40)
# ==============================================================================
PROJETOS_AVALIACAO = {
    "PRJ24": {
        "titulo": "Mecanismo Preditivo de Risco de Crédito sob Cenários de Estresse Severo",
        "unidade": "Diretoria de Gestão de Riscos / P&D Interno",
        "natureza_informada": "Pesquisa Aplicada e Desenvolvimento Experimental",
        "scores": {"C1: Novidade": 160, "C2: Criatividade": 170, "C3: Incerteza": 160, "C4: Metodologia": 120, "C5: Reprodutibilidade": 130},
        "score_total": 740,
        "classificacao_ia": "Com ressalvas",
        "contradicao": {
            "detectada": True,
            "entrevista": "Líder técnico afirmou em entrevista estabilidade de 98% para todas as safras.",
            "registro_primario": "Arquivo 'medicoes.csv' (linha 142, EVID_MED_04) registra falha de convergência com 22% de erro no cenário de sequeiro.",
            "regra": "Prevalência do registro numérico primário versionado sobre depoimento verbal."
        },
        "ressalva": {
            "recorte": "Algoritmo preditivo para safras irrigadas (ATIV_01 a ATIV_03). Exclui ATIV_04 (rotina de front-end).",
            "limitacao": "Instabilidade não superada no subcenário de safras de sequeiro.",
            "evidencia_necessaria": "Relatório de ensaios com hiperparâmetros ajustados para convergência em safras de sequeiro."
        },
        "elo_ausente": "",
        "atividades": [
            {"ID": "ATIV_01", "Fase": "Formulação", "Descrição": "Modelagem de hipóteses matemáticas", "Evidência ID": "EVID_DOC_01", "Arquivo": "dossie.pdf", "Status": "Localizada"},
            {"ID": "ATIV_02", "Fase": "Experimentação", "Descrição": "Ensaios com choques estocásticos", "Evidência ID": "EVID_MED_04", "Arquivo": "medicoes.csv", "Status": "Localizada"},
            {"ID": "ATIV_03", "Fase": "Validação", "Descrição": "Testes comparativos com modelo legado", "Evidência ID": "EVID_MED_07", "Arquivo": "resultados.csv", "Status": "Localizada"},
            {"ID": "ATIV_04", "Fase": "Implantação", "Descrição": "Ajuste de interface e pipeline", "Evidência ID": "EVID_DOC_05", "Arquivo": "homologacao.txt", "Status": "Localizada"}
        ]
    },
    "PRJ21": {
        "titulo": "Plataforma de Reconhecimento Biométrico Facial com Iluminação Desfavorável",
        "unidade": "Gerência de Inovação Digital",
        "natureza_informada": "Desenvolvimento Experimental",
        "scores": {"C1: Novidade": 180, "C2: Criatividade": 180, "C3: Incerteza": 190, "C4: Metodologia": 170, "C5: Reprodutibilidade": 180},
        "score_total": 900,
        "classificacao_ia": "Elegível",
        "contradicao": {"detectada": False},
        "ressalva": {},
        "elo_ausente": "",
        "atividades": [
            {"ID": "ATIV_01", "Fase": "P&D", "Descrição": "Convolução customizada para baixa luz", "Evidência ID": "EVID_MED_01", "Arquivo": "medicoes.csv", "Status": "Localizada"}
        ]
    },
    "PRJ22": {
        "titulo": "Migração de Banco de Dados Legado para Nuvem e Parametrização ERP",
        "unidade": "Superintendência de TI",
        "natureza_informada": "Desenvolvimento Tecnológico",
        "scores": {"C1: Novidade": 30, "C2: Criatividade": 40, "C3: Incerteza": 40, "C4: Metodologia": 50, "C5: Reprodutibilidade": 50},
        "score_total": 210,
        "classificacao_ia": "Não elegível",
        "contradicao": {"detectada": False},
        "ressalva": {},
        "elo_ausente": "",
        "atividades": [
            {"ID": "ATIV_01", "Fase": "Operação", "Descrição": "Instalação de conectores de mercado", "Evidência ID": "EVID_DOC_02", "Arquivo": "manual.pdf", "Status": "Localizada"}
        ]
    },
    "PRJ23": {
        "titulo": "Otimizador de Microcrédito Territorial via Grafos Espaciais",
        "unidade": "Hubine / Desenvolvimento Regional",
        "natureza_informada": "Pesquisa Aplicada",
        "scores": {"C1: Novidade": 120, "C2: Criatividade": 130, "C3: Incerteza": 110, "C4: Metodologia": 80, "C5: Reprodutibilidade": 70},
        "score_total": 510,
        "classificacao_ia": "Evidência insuficiente",
        "contradicao": {"detectada": False},
        "ressalva": {},
        "elo_ausente": "Inexistência de registros no 'medicoes.csv' para comprovar acurácia das arestas dos grafos.",
        "atividades": [
            {"ID": "ATIV_01", "Fase": "Concepção", "Descrição": "Mapeamento teórico de grafos", "Evidência ID": "EVID_DOC_01", "Arquivo": "slides.pdf", "Status": "Localizada"}
        ]
    }
}

for i in range(25, 41):
    pid = f"PRJ{i}"
    PROJETOS_AVALIACAO[pid] = {
        "titulo": f"Iniciativa de Automação e Análise Preditiva {pid}",
        "unidade": "Tecnologia Bancária",
        "natureza_informada": "Desenvolvimento Experimental",
        "scores": {"C1: Novidade": 140, "C2: Criatividade": 140, "C3: Incerteza": 150, "C4: Metodologia": 130, "C5: Reprodutibilidade": 140},
        "score_total": 700,
        "classificacao_ia": "Com ressalvas" if i % 2 == 0 else "Elegível",
        "contradicao": {"detectada": False},
        "ressalva": {"recorte": "Escopo experimental homologado", "limitacao": "Métrica preliminar", "evidencia_necessaria": "Log versionado"},
        "elo_ausente": "",
        "atividades": [{"ID": "ATIV_01", "Fase": "Testes", "Descrição": "Ensaios empíricos", "Evidência ID": "EVID_MED_01", "Arquivo": "medicoes.csv", "Status": "Localizada"}]
    }

# ==============================================================================
# 5. BARRA LATERAL (MENU & QR CODE)
# ==============================================================================
with st.sidebar:
    st.markdown('<div class="hero-badge">BANCO DO NORDESTE • P&D</div>', unsafe_allow_html=True)
    
    # Código que lê e embute a imagem de forma segura no HTML
    try:
        with open("space_invader.jpg", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        img_src = f"data:image/jpeg;base64,{encoded_string}"
    except Exception:
        img_src = "" # Caso a imagem falte por um segundo, o app não trava

    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 5px;">
            <img src="{img_src}" style="width: 32px; height: 32px; border-radius: 6px; object-fit: cover;">
            <h2 style="margin: 0; font-family: var(--font-main); font-weight: 800; color: #FFFFFF; font-size: 24px;">Strainer Point</h2>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    st.caption("Sistema de Apoio à Decisão – Lei do Bem")
    st.markdown("---")
 # ==============================================================================
    tela = st.radio(
        "Navegação:",
        [
            "1. Ingestão & Processamento",
            "2. Dashboard Executivo",
            "3. Mesa de Análise & Frascati",
            "4. Validação & Dossiê",
            "5. Calibração & Históricos (PRJ01–20)"
        ]
    )
    
    st.markdown("---")
    st.markdown("#### 📱 **Acesso Mobile ao Protótipo**")
    url_publica = "https://strainerpoint.site"
    qr_bytes = gerar_qr_code(url_publica)
    st.image(qr_bytes, caption="Aponte a câmera para testar", width=140)
    st.caption("🔒 **Auditabilidade:** Responde ao teste dos 3 anos (quem, quando, regra e prova).")

     # CRÉDITOS FORMATADOS SEM EXIBIR CÓDIGO CRU
    creditos_html = """
    <div style="
        background: rgba(0, 255, 135, 0.04); 
        border: 1px solid rgba(0, 255, 135, 0.18); 
        border-radius: 12px; 
            padding: 12px; 
            margin-top: 10px;
            box-shadow: 0 0 15px rgba(0, 255, 135, 0.05);
        ">
            <p style="
                margin: 0 0 8px 0; 
                font-family: var(--font-tech); 
                font-size: 10px; 
                color: #00FF87; 
                text-transform: uppercase; 
                letter-spacing: 1.2px;
                text-align: center;
                font-weight: 700;
            ">⚡ CORPO TÉCNICO</p>
            
            <div style="text-align: left; font-size: 12px; font-family: var(--font-main); line-height: 1.4;">
                <p style="margin: 3px 0; color: #E2E8F0;">
                    <b style="color: #FFFFFF;">Vitória Bravo Araújo Matos</b><br>
                    <span style="color: #94A3B8; font-size: 11px;">Líder e Designer</span>
                </p>
                <p style="margin: 6px 0 3px 0; color: #E2E8F0; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 4px;">
                    <b style="color: #FFFFFF;">Yuri Gabriel da Silva Fernandes</b><br>
                    <span style="color: #94A3B8; font-size: 11px;">Programador</span>
                </p>
                <p style="margin: 6px 0 3px 0; color: #E2E8F0; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 4px;">
                    <b style="color: #FFFFFF;">Keyciane dos Santos Cruz</b><br>
                    <span style="color: #94A3B8; font-size: 11px;">Programadora</span>
                </p>
                <p style="margin: 6px 0 0 0; color: #E2E8F0; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 4px;">
                    <b style="color: #FFFFFF;">Kayroni de Melo Alvarenga</b><br>
                    <span style="color: #94A3B8; font-size: 11px;">Engenheiro de Software</span>
                </p>
            </div>
        </div>
    """
    
    st.write("")
    st.markdown(creditos_html, unsafe_allow_html=True)


# ==============================================================================
# TELA 1: INGESTÃO & PROCESSAMENTO
# ==============================================================================
if tela == "1. Ingestão & Processamento":
    st.markdown('<div class="hero-badge">ETAPA 01 • INGESTÃO</div>', unsafe_allow_html=True)
    st.markdown('<p class="main-header">Ingestão & <span>Catalogação de Evidências</span></p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Carregue arquivos novos ou processe lotes da massa para catalogação de evidências por ID único.</p>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 📂 **Upload de Novo Pacote de Projeto**")
        up = st.file_uploader("Selecione ZIP contendo dossiê, atividades e evidências:", type=["zip", "csv", "pdf"])
        if up:
            st.success(f"Arquivo `{up.name}` carregado e validado estruturalmente.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### ⚡ **Processamento em Lote (Hackathon)**")
        st.selectbox("Lote de Trabalho:", ["Casos de Análise Ativa (PRJ21 a PRJ40)", "Casos Históricos de Referência (PRJ01 a PRJ20)"])
        st.write("")
        if st.button("🚀 Executar Esteira de Análise Semântica", use_container_width=True):
            p = st.progress(0)
            txt = st.empty()
            passos = [
                "Indexando evidências primárias (EVID_MED_xx, EVID_DOC_xx)...",
                "Confrontando transcrições com linhas numéricas de 'medicoes.csv'...",
                "Aferindo os 5 critérios de Frascati (escala de 0 a 1.000 pts)...",
                "Consolidando matrizes de rastreabilidade e divergências..."
            ]
            for idx, ps in enumerate(passos):
                import time
                time.sleep(0.3)
                p.progress((idx + 1) * 25)
                txt.text(ps)
            st.success("✅ Esteira concluída! 20 projetos processados e catalogados.")
        st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# TELA 2: DASHBOARD EXECUTIVO
# ==============================================================================
elif tela == "2. Dashboard Executivo":
    st.markdown('<div class="hero-badge">ETAPA 02 • VISÃO GERAL</div>', unsafe_allow_html=True)
    st.markdown('<p class="main-header">Dashboard <span>Executivo da Carteira</span></p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Métricas consolidadas de conformidade tributária segundo as 4 classificações oficiais da Lei do Bem.</p>', unsafe_allow_html=True)
    
    dados = []
    for pid, pdata in PROJETOS_AVALIACAO.items():
        dados.append({"ID": pid, "Título": pdata["titulo"], "Unidade": pdata["unidade"], "Score Frascati": pdata["score_total"], "Recomendação": pdata["classificacao_ia"]})
    df_exec = pd.DataFrame(dados)
    cont = df_exec["Recomendação"].value_counts()
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.metric("Elegíveis", cont.get("Elegível", 0), help="P&D comprovado sem ressalvas.")
        st.markdown('</div>', unsafe_allow_html=True)
    with m2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.metric("Com Ressalvas", cont.get("Com ressalvas", 0), help="P&D com restrição técnica ou de escopo.")
        st.markdown('</div>', unsafe_allow_html=True)
    with m3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.metric("Não Elegíveis", cont.get("Não elegível", 0), help="Atividades de engenharia de rotina ou operação.")
        st.markdown('</div>', unsafe_allow_html=True)
    with m4:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.metric("Evidência Insuf.", cont.get("Evidência insuficiente", 0), help="Faltam dados essenciais para caracterização.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    cg, ct = st.columns([1.1, 1.9])
    with cg:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 🎯 **Distribuição Percentual da Carteira**")
        fig_donut = px.pie(
            df_exec, names="Recomendação", hole=0.6,
            color="Recomendação",
            color_discrete_map={
                "Elegível": "#00FF87",
                "Com ressalvas": "#F59E0B",
                "Não elegível": "#EF4444",
                "Evidência insuficiente": "#64748B"
            }
        )
        fig_donut.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#E2E8F0', family='Mona Sans'),
            margin=dict(t=10, b=10, l=10, r=10),
            height=280,
            showlegend=True
        )
        st.plotly_chart(fig_donut, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with ct:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 📋 **Projetos Avaliados (Filtro por Categoria)**")
        filtro = st.multiselect("Filtrar por Status:", ["Elegível", "Com ressalvas", "Não elegível", "Evidência insuficiente"], default=["Elegível", "Com ressalvas", "Não elegível", "Evidência insuficiente"])
        st.dataframe(df_exec[df_exec["Recomendação"].isin(filtro)], use_container_width=True, height=230)
        st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# TELA 3: MESA DE ANÁLISE & FRASCATI (CORREÇÃO DE RANGE E RADAR)
# ==============================================================================
elif tela == "3. Mesa de Análise & Frascati":
    st.markdown('<div class="hero-badge">ETAPA 03 • MESA DE ANÁLISE</div>', unsafe_allow_html=True)
    st.markdown('<p class="main-header">Mesa de Análise & <span>Espelho de Competências</span></p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Análise detalhada por critério de Frascati com detecção e saneamento interativo de divergências.</p>', unsafe_allow_html=True)
    
    sel_pid = st.selectbox("Selecione o projeto para análise aprofundada:", list(PROJETOS_AVALIACAO.keys()), index=0)
    prj = PROJETOS_AVALIACAO[sel_pid]
    
    if f"{sel_pid}_saneado" not in st.session_state:
        st.session_state[f"{sel_pid}_saneado"] = False

    saneado = st.session_state[f"{sel_pid}_saneado"]
    
    st.markdown(f"### 📌 **{sel_pid}: {prj['titulo']}**")
    st.caption(f"Unidade: {prj['unidade']} | Natureza Informada pela Equipe (Autodeclaração): *{prj['natureza_informada']}*")
    
    if prj["contradicao"].get("detectada", False):
        if not saneado:
            st.markdown(f"""
            <div class="alert-glass">
                <b>🚨 DIVERGÊNCIA ENTRE FONTES IDENTIFICADA (Prevalência do Registro Primário):</b><br>
                • <b>Depoimento (Entrevista):</b> {prj['contradicao']['entrevista']}<br>
                • <b>Registro Primário Empírico:</b> {prj['contradicao']['registro_primario']}<br>
                • <b>Critério Aplicado:</b> {prj['contradicao']['regra']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="success-glass">
                <b>✅ DIVERGÊNCIA SANEADA COM SUCESSO:</b><br>
                Novo registro primário <code>EVID_MED_08_complementar.csv</code> anexado. Os ensaios adicionais comprovaram estabilização da taxa de erro em 1,8% no subcenário de sequeiro. Ressalva superada!
            </div>
            """, unsafe_allow_html=True)
            
    if sel_pid == "PRJ24":
        with st.expander("🛠️ **Painel de Ação: Simular Saneamento da Ressalva (Live Demo)**", expanded=not saneado):
            if not saneado:
                st.write("A equipe do projeto foi notificada a apresentar ensaios complementares para sanar a ressalva do cenário de sequeiro.")
                col_up, col_btn = st.columns([3, 1])
                with col_up:
                    st.text_input("Evidência Primária Complementar:", value="EVID_MED_08_complementar.csv (Ensaios de Hiperparâmetros v2)")
                with col_btn:
                    st.write("")
                    st.write("")
                    if st.button("📥 Anexar e Recalcular Nota", use_container_width=True):
                        st.session_state[f"{sel_pid}_saneado"] = True
                        st.rerun()
            else:
                if st.button("🔄 Restaurar Estado Original com Divergência", use_container_width=True):
                    st.session_state[f"{sel_pid}_saneado"] = False
                    st.rerun()

    scores_atuais = prj["scores"].copy()
    if saneado and sel_pid == "PRJ24":
        scores_atuais["C4: Metodologia"] = 180
        score_total = sum(scores_atuais.values())
        rec_atual = "Elegível"
    else:
        score_total = prj["score_total"]
        rec_atual = prj["classificacao_ia"]

    c_radar, c_detalhe = st.columns(2)
    with c_radar:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 🕸️ **Radar de Frascati (0 a 1.000 pts)**")
        cats = list(scores_atuais.keys())
        vals = list(scores_atuais.values())
        
        fig_r = go.Figure()
        fig_r.add_trace(go.Scatterpolar(
            r=vals + vals[:1],
            theta=cats + cats[:1],
            fill='toself',
            name='Score',
            line_color='#00FF87',
            fillcolor='rgba(0, 255, 135, 0.22)'
        ))
        fig_r.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True, 
                    range=(0, 200),
                    tickfont=dict(size=10, color='#94A3B8'), 
                    gridcolor='rgba(255,255,255,0.08)'
                ),
                angularaxis=dict(tickfont=dict(size=11, color='#E2E8F0'), gridcolor='rgba(255,255,255,0.08)')
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            height=320,
            margin=dict(t=20, b=20, l=35, r=35)
        )
        st.plotly_chart(fig_r, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c_detalhe:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 🎯 **Espelho de Pontuação Detalhado**")
        for k, v in scores_atuais.items():
            st.write(f"• **{k}:** `{v} / 200 pts`")
        st.markdown(f"### **Total Consolidado:** <span style='color: #00FF87;'>{score_total} / 1.000 pts</span>", unsafe_allow_html=True)
        
        badge_class = "badge-elegivel" if rec_atual == "Elegível" else "badge-ressalva" if rec_atual == "Com ressalvas" else "badge-nao"
        st.markdown(f"Recomendação Preliminar: <span class='{badge_class}'>{rec_atual.upper()}</span>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    if rec_atual == "Com ressalvas":
        st.markdown(f"""
        <div class="warning-glass">
            <b>⚠️ Detalhamento Obrigatório da Ressalva:</b><br>
            • <b>Recorte Sustentado:</b> {prj['ressalva']['recorte']}<br>
            • <b>Limitação Específica:</b> {prj['ressalva']['limitacao']}<br>
            • <b>Evidência Necessária para Sanar:</b> {prj['ressalva']['evidencia_necessaria']}
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("#### 🔗 **Matriz de Rastreabilidade Fato-Atividade-Evidência**")
    df_ativ_exibir = pd.DataFrame(prj["atividades"])
    if saneado and sel_pid == "PRJ24":
        nova_linha = pd.DataFrame([{
            "ID": "ATIV_02.1",
            "Fase": "Saneamento",
            "Descrição": "Ensaios de hiperparâmetros complementares (convergência de sequeiro)",
            "Evidência ID": "EVID_MED_08_complementar",
            "Arquivo": "medicoes_complementares.csv",
            "Status": "Anexada e Validada"
        }])
        df_ativ_exibir = pd.concat([df_ativ_exibir, nova_linha], ignore_index=True)
        
    st.dataframe(df_ativ_exibir, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# TELA 4: VALIDAÇÃO HUMANA & DOSSIÊ AUDITÁVEL
# ==============================================================================
elif tela == "4. Validação & Dossiê":
    st.markdown('<div class="hero-badge">ETAPA 04 • HOMOLOGAÇÃO</div>', unsafe_allow_html=True)
    st.markdown('<p class="main-header">Validação Humana & <span>Dossiê Auditável</span></p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">O analista valida a recomendação preliminar, formaliza a decisão soberana e emite o documento com hash.</p>', unsafe_allow_html=True)
    
    sel_pid = st.selectbox("Selecione o projeto para homologação:", list(PROJETOS_AVALIACAO.keys()), index=0)
    prj = PROJETOS_AVALIACAO[sel_pid]
    
    c_form, c_prev = st.columns(2)
    with c_form:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### ✍️ **Parecer do Analista Responsável**")
        decisao = st.selectbox("Classificação Final (Decisão do Analista):", ["Com ressalvas", "Elegível", "Não elegível", "Evidência insuficiente"], index=0 if prj["classificacao_ia"] == "Com ressalvas" else 1)
        parecer = st.text_area("Justificativa Técnica:", value=f"Recomendação preliminar acolhida. O enquadramento em '{decisao}' resguarda o banco contra glosas fiscais ao excluir a atividade operacional de rotina (ATIV_04) da fruição fiscal.", height=120)
        
        ca, cb = st.columns(2)
        with ca: mat = st.text_input("Matrícula do Analista:", "BNB-84920")
        with cb: nome = st.text_input("Nome do Responsável:", "Carlos Eduardo Menezes")
        
        timestamp = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
        hash_audit = hashlib.sha256(f"{sel_pid}{decisao}{parecer}{mat}{timestamp}".encode()).hexdigest()[:24]
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c_prev:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 📄 **Dossiê Auditável Consolidado**")
        espelho_formatado = "\n".join([f"- {k}: {v}/200 pts" for k, v in prj['scores'].items()])
        dossie_txt = f"""# DOSSIÊ TÉCNICO DE ENQUADRAMENTO - LEI DO BEM
**PROJETO:** {sel_pid} — {prj['titulo']}
**CLASSIFICAÇÃO HOMOLOGADA:** {decisao.upper()}
**HASH DE INTEGRIDADE:** `{hash_audit}`

---
### 1. Trilha de Auditoria (Teste dos Três Anos)
- **Normas Aplicadas:** Manual de Frascati (2.1–2.5); Lei nº 11.196/2005 (art. 17); Decreto nº 5.798/2006.
- **Evidências Primárias:** EVID_DOC_01, EVID_MED_04 (medicoes.csv), EVID_MED_07.
- **Responsável:** {nome} (Matrícula: {mat})
- **Data e Hora:** {timestamp}

---
### 2. Espelho de Frascati ({prj['score_total']} / 1.000 pts)
{espelho_formatado}

---
### 3. Parecer Técnico Final
{parecer}
"""
        st.text_area("Visualização do Dossiê:", dossie_txt, height=230)
        st.download_button("📥 Baixar Dossiê (.MD)", dossie_txt, file_name=f"dossie_{sel_pid}.md", mime="text/markdown", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# TELA 5: CALIBRAÇÃO & HISTÓRICOS (PRJ01 A PRJ20)
# ==============================================================================
elif tela == "5. Calibração & Históricos (PRJ01–20)":
    st.markdown('<div class="hero-badge">BENCHMARK • CALIBRAÇÃO</div>', unsafe_allow_html=True)
    st.markdown('<p class="main-header">Base de Calibração & <span>Históricos Classificados</span></p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Casos de referência oficiais para calibração de critérios e aprendizado de padrões de fundamentação probatória.</p>', unsafe_allow_html=True)
    
    st.info("💡 **Diretriz do Guia do Participante:** Os projetos históricos (PRJ01–PRJ20) servem como padrão de fundamentação e calibração de rigor técnico. A classificação de novos projetos não deve ser feita por semelhança, mas sim a partir das evidências do próprio caso sob análise.")
    
    cols = st.columns(2)
    for idx, (h_id, h_data) in enumerate(HISTORICOS_CALIBRACAO.items()):
        col_dest = cols[idx % 2]
        badge_class = "badge-elegivel" if h_data["classe"] == "Elegível" else "badge-ressalva" if h_data["classe"] == "Com ressalvas" else "badge-nao" if h_data["classe"] == "Não elegível" else "badge-insuf"
        
        with col_dest:
            st.markdown(f"""
            <div class="glass-card">
                <span class="hero-badge">{h_id}</span><br>
                <b style="font-size: 16px; color: #FFFFFF;">{h_data['titulo']}</b><br>
                <div style="margin: 8px 0;">
                    Status: <span class="{badge_class}">{h_data['classe'].upper()}</span> 
                    &nbsp;|&nbsp; Score: <b style="color: #00FF87;">{h_data['score']}/1.000 pts</b>
                </div>
                <p style="color: #94A3B8; font-size: 13px; margin-top: 6px;"><b>Fundamentação:</b> {h_data['fundamentacao']}</p>
                <code style="color: #00FF87; background: rgba(0,255,135,0.08); padding: 4px 8px; border-radius: 6px;">{h_data['evidencia_chave']}</code>
            </div>
            """, unsafe_allow_html=True)
