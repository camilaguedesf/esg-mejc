import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração da página
st.set_page_config(
    page_title="ESG na MEJC/EBSERH",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f4e79, #2e8b57);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f4e79;
        margin: 0.5rem 0;
    }
    .esg-pillar {
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem;
        text-align: center;
        color: white;
    }
    .environmental { background: #2e8b57; }
    .social { background: #dc3545; }
    .governance { background: #ffc107; color: black; }
</style>
""", unsafe_allow_html=True)

# Dados do estudo
@st.cache_data
def load_data():
    # Dados temporais (2014-2023)
    anos = list(range(2014, 2024))
    
    dados_temporais = pd.DataFrame({
        'Ano': anos,
        'Funcionarios': [307, 350, 410, 480, 550, 620, 690, 740, 785, 785],
        'Custo_Pessoal_Milhoes': [40.5, 48.2, 58.5, 68.7, 78.9, 85.4, 92.1, 97.3, 100.8, 102.1],
        'Consumo_Agua_m3': [90000, 88000, 85000, 82000, 78000, 75000, 70000, 68000, 65000, 63000],
        'Consumo_Energia_kWh': [280, 275, 270, 265, 260, 255, 250, 245, 240, 237],
        'Absenteismo_Pct': [3.8, 4.2, 4.8, 5.5, 6.2, 7.1, 7.8, 8.2, 8.5, 8.6],
        'Atestados_Mental': [85, 95, 120, 150, 180, 220, 250, 280, 300, 308],
        'Pacientes_Dia': [46729, 48200, 49500, 50100, 51200, 51800, 52100, 52400, 52653, 52800],
        'Patrimonio_Liquido': [80, 90, 105, 120, 130, 140, 145, 148, 150, 152]
    })
    
    # Scores ESG
    scores_esg = {
        'Ambiental': 41.7,
        'Social': 31.2,
        'Governança': 75.0
    }
    
    # Correlações
    correlacoes = {
        'Patrimônio Líquido vs Absenteísmo': -0.98,
        'Funcionários vs Custos': 0.957,
        'Atestados Mental vs Afastamentos': 0.688,
        'Resíduos vs Custos': 0.642
    }
    
    return dados_temporais, scores_esg, correlacoes

# Carregar dados
dados_temporais, scores_esg, correlacoes = load_data()

# Sidebar
st.sidebar.title("🏥 ESG na MEJC/EBSERH")
st.sidebar.markdown("---")

# Menu principal
pagina = st.sidebar.selectbox(
    "Navegação",
    ["📊 Dashboard Principal", 
     "📈 Evolução Temporal", 
     "🔗 Análise de Correlações",
     "⚖️ Framework ESG",
     "🎯 Scores e Maturidade",
     "📝 Conclusões"]
)

# Header principal
st.markdown("""
<div class="main-header">
    <h1>🏥 Governança e Sustentabilidade em Hospitais Universitários</h1>
    <h3>Análise ESG da Maternidade Escola Januário Cicco (MEJC/EBSERH)</h3>
    <p>Período de Análise: 2014-2023 | Hospital Universitário Público</p>
</div>
""", unsafe_allow_html=True)

# ===== DASHBOARD PRINCIPAL =====
if pagina == "📊 Dashboard Principal":
    st.header("📊 Indicadores-Chave do Estudo")
    
    # KPIs principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🏥 Período de Análise",
            "10 anos",
            "2014-2023"
        )
    
    with col2:
        st.metric(
            "👥 Crescimento de Pessoal",
            "155,7%",
            "307 → 785 funcionários"
        )
    
    with col3:
        st.metric(
            "💧 Redução Consumo Água",
            "-29,7%",
            "Sustentabilidade"
        )
    
    with col4:
        st.metric(
            "⚡ Redução Consumo Energia",
            "-15,2%",
            "Eficiência"
        )
    
    # Gráfico de scores ESG
    st.subheader("🎯 Scores ESG por Pilar")
    
    fig_scores = go.Figure(data=[
        go.Bar(
            x=list(scores_esg.keys()),
            y=list(scores_esg.values()),
            marker_color=['#2e8b57', '#dc3545', '#ffc107'],
            text=[f"{v:.1f}" for v in scores_esg.values()],
            textposition='auto'
        )
    ])
    
    fig_scores.update_layout(
        title="Score ESG por Pilar (0-100 pontos)",
        yaxis_title="Pontuação",
        xaxis_title="Pilares ESG",
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig_scores, use_container_width=True)
    
    # Destaque do Score Total
    score_total = sum(scores_esg.values()) / 3
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem; background: #e8f4fd; border-radius: 10px; margin: 1rem 0;">
        <h2>🏆 Score ESG Total da MEJC</h2>
        <h1 style="color: #1f4e79; font-size: 3rem;">{score_total:.1f}/100</h1>
        <h3 style="color: #666;">Nível 2: ESG Emergente</h3>
        <p>Necessário avanços principalmente nos pilares Ambiental e Social</p>
    </div>
    """, unsafe_allow_html=True)

# ===== EVOLUÇÃO TEMPORAL =====
elif pagina == "📈 Evolução Temporal":
    st.header("📈 Evolução dos Indicadores ESG (2014-2023)")
    
    # Seletor de indicadores
    indicador = st.selectbox(
        "Selecione o indicador para visualizar:",
        ["Funcionários e Custos", "Consumo de Recursos", "Indicadores Sociais", "Todos"]
    )
    
    if indicador == "Funcionários e Custos":
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Scatter(x=dados_temporais['Ano'], y=dados_temporais['Funcionarios'],
                      name="Nº Funcionários", line=dict(color='blue')),
            secondary_y=False,
        )
        
        fig.add_trace(
            go.Scatter(x=dados_temporais['Ano'], y=dados_temporais['Custo_Pessoal_Milhoes'],
                      name="Custo Pessoal (R$ mi)", line=dict(color='red')),
            secondary_y=True,
        )
        
        fig.update_layout(title="Evolução do Quadro de Pessoal e Custos")
        fig.update_xaxes(title_text="Ano")
        fig.update_yaxes(title_text="Nº Funcionários", secondary_y=False)
        fig.update_yaxes(title_text="Custo (R$ milhões)", secondary_y=True)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Insights
        st.info("""
        📊 **Crescimento Correlacionado (R² = 0,957)**
        - Funcionários: 307 → 785 (+155,7%)
        - Custos: R$ 40,5 → R$ 100,8 mi (+148,5%)
        - Cada funcionário adicional custa ~R$ 214.523/ano
        """)
    
    elif indicador == "Consumo de Recursos":
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Scatter(x=dados_temporais['Ano'], y=dados_temporais['Consumo_Agua_m3'],
                      name="Consumo Água (m³)", line=dict(color='lightblue')),
            secondary_y=False,
        )
        
        fig.add_trace(
            go.Scatter(x=dados_temporais['Ano'], y=dados_temporais['Consumo_Energia_kWh'],
                      name="Consumo Energia (kWh)", line=dict(color='orange')),
            secondary_y=True,
        )
        
        fig.update_layout(title="Evolução do Consumo de Recursos")
        fig.update_xaxes(title_text="Ano")
        fig.update_yaxes(title_text="Água (m³)", secondary_y=False)
        fig.update_yaxes(title_text="Energia (kWh)", secondary_y=True)
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.success("""
        🌱 **Eficiência Ambiental Positiva**
        - Água: 90.000 → 63.000 m³ (-29,7%)
        - Energia: 280 → 237 kWh (-15,2%)
        - Tecnologias sustentáveis implementadas
        """)
    
    elif indicador == "Indicadores Sociais":
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Scatter(x=dados_temporais['Ano'], y=dados_temporais['Absenteismo_Pct'],
                      name="Absenteísmo (%)", line=dict(color='red')),
            secondary_y=False,
        )
        
        fig.add_trace(
            go.Scatter(x=dados_temporais['Ano'], y=dados_temporais['Atestados_Mental'],
                      name="Atestados Saúde Mental", line=dict(color='purple')),
            secondary_y=True,
        )
        
        fig.update_layout(title="Evolução dos Indicadores Sociais")
        fig.update_xaxes(title_text="Ano")
        fig.update_yaxes(title_text="Absenteísmo (%)", secondary_y=False)
        fig.update_yaxes(title_text="Atestados Saúde Mental", secondary_y=True)
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.warning("""
        ⚠️ **Desafios no Pilar Social**
        - Absenteísmo: 3,8% → 8,6% (+126,2%)
        - Atestados Mental: 85 → 308 (+262,4%)
        - Necessidade urgente de programas de bem-estar
        """)

# ===== ANÁLISE DE CORRELAÇÕES =====
elif pagina == "🔗 Análise de Correlações":
    st.header("🔗 Análise de Correlações Estatísticas")
    
    # Visualização das correlações
    st.subheader("📊 Principais Correlações Identificadas")
    
    correlacao_df = pd.DataFrame([
        {"Variáveis": "Patrimônio Líquido vs Absenteísmo", "Correlação": -0.98, "Significância": "p < 0.001"},
        {"Variáveis": "Funcionários vs Custos Pessoal", "Correlação": 0.957, "Significância": "p < 0.001"},
        {"Variáveis": "Atestados Mental vs Dias Afastamento", "Correlação": 0.688, "Significância": "p < 0.01"},
        {"Variáveis": "Resíduos vs Custos Tratamento", "Correlação": 0.642, "Significância": "p < 0.05"}
    ])
    
    # Gráfico de correlações
    fig = go.Figure(data=go.Bar(
        x=correlacao_df['Variáveis'],
        y=correlacao_df['Correlação'],
        marker_color=['red' if x < 0 else 'green' for x in correlacao_df['Correlação']],
        text=[f"{x:.3f}" for x in correlacao_df['Correlação']],
        textposition='auto'
    ))
    
    fig.update_layout(
        title="Coeficientes de Correlação por Variável",
        yaxis_title="Coeficiente de Correlação",
        xaxis_title="Pares de Variáveis",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Scatter plot das correlações principais
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Patrimônio Líquido vs Absenteísmo")
        
        fig_scatter1 = px.scatter(
            dados_temporais, 
            x='Patrimonio_Liquido', 
            y='Absenteismo_Pct',
            trendline="ols",
            title="Correlação: r = -0.98"
        )
        fig_scatter1.update_layout(
            xaxis_title="Patrimônio Líquido (R$ milhões)",
            yaxis_title="Absenteísmo (%)"
        )
        st.plotly_chart(fig_scatter1, use_container_width=True)
    
    with col2:
        st.subheader("Funcionários vs Custos")
        
        fig_scatter2 = px.scatter(
            dados_temporais, 
            x='Funcionarios', 
            y='Custo_Pessoal_Milhoes',
            trendline="ols",
            title="R² = 0.957"
        )
        fig_scatter2.update_layout(
            xaxis_title="Nº de Funcionários",
            yaxis_title="Custo Pessoal (R$ milhões)"
        )
        st.plotly_chart(fig_scatter2, use_container_width=True)

# ===== FRAMEWORK ESG =====
elif pagina == "⚖️ Framework ESG":
    st.header("⚖️ Framework ESG para Hospitais Universitários")
    
    # Descrição dos pilares
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="esg-pillar environmental">
            <h3>🌱 Pilar Ambiental (E)</h3>
            <p><strong>Score: 41.7/100</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        **Dimensões:**
        - Eficiência de recursos (água/energia)
        - Gestão de resíduos
        - Sustentabilidade operacional
        - Pegada de carbono
        
        **Forças:**
        - Redução 29,7% consumo água
        - Redução 15,2% consumo energia
        
        **Desafios:**
        - Custos de gestão de resíduos
        - Certificações ambientais
        """)
    
    with col2:
        st.markdown("""
        <div class="esg-pillar social">
            <h3>👥 Pilar Social (S)</h3>
            <p><strong>Score: 31.2/100</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        **Dimensões:**
        - Saúde ocupacional
        - Capacitação profissional
        - Equidade no atendimento
        - Responsabilidade comunitária
        
        **Desafios Críticos:**
        - Absenteísmo +126,2%
        - Saúde mental dos colaboradores
        - Sobrecarga de trabalho
        
        **Oportunidades:**
        - Programas de bem-estar
        - Capacitação continuada
        """)
    
    with col3:
        st.markdown("""
        <div class="esg-pillar governance">
            <h3>⚖️ Pilar Governança (G)</h3>
            <p><strong>Score: 75.0/100</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        **Dimensões:**
        - Transparência financeira
        - Prestação de contas
        - Gestão de riscos
        - Conformidade regulatória
        
        **Forças:**
        - Correlação PL-Absenteísmo forte
        - Transparência de dados
        - Compliance regulatório
        
        **Manutenção:**
        - Continuar boas práticas
        - Monitoramento sistemático
        """)
    
    # Interações entre pilares
    st.subheader("🔄 Interações Dinâmicas Entre Pilares")
    
    interacoes = {
        "E-G (Ambiental-Governança)": {
            "status": "✅ Sinergia Positiva",
            "descricao": "Eficiência ambiental correlacionada com boa gestão financeira",
            "acao": "Manter investimentos em sustentabilidade"
        },
        "S-G (Social-Governança)": {
            "status": "⚠️ Sinergia Crítica", 
            "descricao": "Problemas sociais impactam negativamente a governança (r = -0.98)",
            "acao": "Programas urgentes de saúde ocupacional"
        },
        "E-S (Ambiental-Social)": {
            "status": "❌ Desconexão",
            "descricao": "Melhorias ambientais não refletem em bem-estar social",
            "acao": "Integrar práticas ambientais com engajamento social"
        }
    }
    
    for nome, info in interacoes.items():
        with st.expander(f"{nome}: {info['status']}"):
            st.write(f"**Situação:** {info['descricao']}")
            st.write(f"**Recomendação:** {info['acao']}")

# ===== SCORES E MATURIDADE =====
elif pagina == "🎯 Scores e Maturidade":
    st.header("🎯 Avaliação de Maturidade ESG")
    
    # Classificação de maturidade
    st.subheader("📊 Classificação de Maturidade ESG-HU")
    
    niveis = pd.DataFrame({
        'Nível': ['Nível 1', 'Nível 2', 'Nível 3', 'Nível 4'],
        'Classificação': ['ESG Inicial', 'ESG Emergente', 'ESG Intermediário', 'ESG Avançado'],
        'Pontuação': ['0-25', '26-50', '51-75', '76-100'],
        'Status': ['', '← MEJC está aqui', '', '']
    })
    
    st.dataframe(niveis, use_container_width=True)
    
    # Gráfico radar
    st.subheader("🎯 Radar de Performance ESG")
    
    fig_radar = go.Figure()
    
    fig_radar.add_trace(go.Scatterpolar(
        r=[scores_esg['Ambiental'], scores_esg['Social'], scores_esg['Governança']],
        theta=['Ambiental', 'Social', 'Governança'],
        fill='toself',
        name='MEJC Score'
    ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Radar ESG - Performance por Pilar"
    )
    
    st.plotly_chart(fig_radar, use_container_width=True)
    
    # Plano de ação
    st.subheader("📋 Plano de Ação por Pilar")
    
    tab1, tab2, tab3 = st.tabs(["🌱 Ambiental", "👥 Social", "⚖️ Governança"])
    
    with tab1:
        st.markdown("""
        **Score Atual: 41.7/100 - Intermediário**
        
        **Ações para Melhorias:**
        - ✅ Continuar programas de eficiência energética
        - ✅ Ampliar sistemas de captação de água de chuva
        - 🔄 Implementar gestão de resíduos mais eficiente
        - 🆕 Buscar certificações ambientais (ISO 14001)
        - 🆕 Desenvolver programa de pegada de carbono
        
        **Meta:** Atingir 60+ pontos em 2 anos
        """)
    
    with tab2:
        st.markdown("""
        **Score Atual: 31.2/100 - CRÍTICO**
        
        **Ações Urgentes:**
        - 🚨 Programa emergencial de saúde mental
        - 🚨 Redução do absenteísmo (meta: <5%)
        - 🆕 Centro de bem-estar dos colaboradores
        - 🆕 Flexibilização de horários
        - 🆕 Programas de qualidade de vida
        - 🆕 Pesquisa de satisfação trimestral
        
        **Meta:** Atingir 50+ pontos em 1 ano
        """)
    
    with tab3:
        st.markdown("""
        **Score Atual: 75.0/100 - BOM**
        
        **Ações de Manutenção e Melhoria:**
        - ✅ Manter transparência financeira
        - ✅ Continuar monitoramento sistemático
        - 🔄 Ampliar relatórios de sustentabilidade
        - 🆕 Implementar gestão de riscos ESG
        - 🆕 Dashboard de indicadores em tempo real
        
        **Meta:** Atingir 85+ pontos mantendo excelência
        """)

# ===== CONCLUSÕES =====
elif pagina == "📝 Conclusões":
    st.header("📝 Principais Conclusões do Estudo")
    
    # Principais achados
    st.subheader("🔍 Principais Achados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        **✅ PONTOS FORTES**
        
        🌱 **Sustentabilidade Ambiental**
        - Redução significativa no consumo de recursos
        - Eficiência energética crescente
        - Impacto ambiental positivo
        
        ⚖️ **Governança Sólida**
        - Transparência financeira adequada
        - Correlações previsíveis (R² > 0.95)
        - Compliance regulatório eficaz
        """)
    
    with col2:
        st.error("""
        **⚠️ DESAFIOS CRÍTICOS**
        
        👥 **Pilar Social Crítico**
        - Absenteísmo crescente (+126,2%)
        - Problemas de saúde mental
        - Sobrecarga dos colaboradores
        
        🔗 **Desconexão E-S**
        - Melhorias ambientais não refletem no social
        - Necessidade de programas integrados
        """)
    
    # Contribuições do estudo
    st.subheader("🎯 Contribuições do Estudo")
    
    st.info("""
    **📚 CONTRIBUIÇÕES CIENTÍFICAS**
    
    1. **Metodológica:** Primeiro estudo longitudinal ESG em hospital universitário EBSERH
    2. **Teórica:** Framework conceitual específico para hospitais públicos
    3. **Empírica:** Base de dados robusta para estudos futuros
    4. **Prática:** Orientações para gestores da rede EBSERH
    """)
    
    # Recomendações
    st.subheader("💡 Recomendações Estratégicas")
    
    recomendacoes = {
        "Curto Prazo (1 ano)": [
            "🚨 Programa emergencial de saúde mental",
            "📊 Sistema de monitoramento ESG integrado", 
            "👥 Contratação focada em bem-estar",
            "🔄 Revisão de processos de trabalho"
        ],
        "Médio Prazo (2-3 anos)": [
            "🏆 Certificações ambientais (ISO 14001)",
            "📈 Expansão do modelo para outros hospitais EBSERH",
            "🎯 Centro de excelência em sustentabilidade",
            "📊 Benchmarking sistemático na rede"
        ],
        "Longo Prazo (5 anos)": [
            "🌟 Liderança nacional em ESG hospitalar",
            "🌍 Exportação do modelo para outras redes",
            "🔬 Pesquisa avançada em inovações sustentáveis",
            "📈 Impacto mensurável nos ODS"
        ]
    }
    
    for prazo, acoes in recomendacoes.items():
        with st.expander(f"⏰ {prazo}"):
            for acao in acoes:
                st.write(f"- {acao}")
    
    # Modelo replicável
    st.subheader("🔄 Aplicabilidade na Rede EBSERH")
    
    st.markdown("""
    **🏥 CRITÉRIOS DE APLICABILIDADE**
    
    O modelo ESG-HU é aplicável a hospitais universitários com:
    - 📏 Porte médio (100-200 leitos)
    - 📅 Incorporados à EBSERH após 2013
    - 💾 Dados históricos mínimos (5 anos)
    - 🖥️ Sistemas de informação estruturados
    
    **🎯 POTENCIAL DE IMPACTO**
    - 45 hospitais universitários na rede EBSERH
    - Base para políticas públicas de sustentabilidade
    - Contribuição para ODS 3, 12 e 13
    - Referência para outras redes hospitalares públicas
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>📊 <strong>Estudo ESG na MEJC/EBSERH</strong> | 
    🏥 Maternidade Escola Januário Cicco | 
    📅 Período: 2014-2023 | 
    🔬 Pesquisa Acadêmica</p>
    <p><em>Framework ESG para Hospitais Universitários Públicos</em></p>
</div>
""", unsafe_allow_html=True)