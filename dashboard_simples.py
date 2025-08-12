import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Dashboard ESG - Indicadores de Sustentabilidade",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para estilização
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E8B57;
        text-align: center;
        font-weight: bold;
        margin-bottom: 1.5rem;
        padding: 1rem;
        background: linear-gradient(90deg, #f0f8f0, #e8f5e8);
        border-radius: 10px;
        border-left: 5px solid #2E8B57;
    }
    
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .environmental { background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); }
    .social { background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%); }
    .governance { background: linear-gradient(135deg, #FF9800 0%, #F57C00 100%); }
    
    .status-excellent { color: #28a745; font-weight: bold; }
    .status-good { color: #17a2b8; font-weight: bold; }
    .status-attention { color: #dc3545; font-weight: bold; }
    
    .alert-success {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #c3e6cb;
        margin: 0.5rem 0;
    }
    
    .alert-warning {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #ffeaa7;
        margin: 0.5rem 0;
    }
    
    .section-divider {
        border-bottom: 3px solid #2E8B57;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Função para carregar dados simulados
@st.cache_data
def carregar_dados_esg():
    """Carrega dados simulados dos indicadores ESG"""
    
    # Criando dados realistas para demonstração
    indicadores_data = {
        'Pilar': [
            # Environmental (8 indicadores)
            'Environmental', 'Environmental', 'Environmental', 'Environmental',
            'Environmental', 'Environmental', 'Environmental', 'Environmental',
            # Social (8 indicadores)  
            'Social', 'Social', 'Social', 'Social',
            'Social', 'Social', 'Social', 'Social',
            # Governance (8 indicadores)
            'Governance', 'Governance', 'Governance', 'Governance',
            'Governance', 'Governance', 'Governance', 'Governance'
        ],
        'Indicador': [
            # Environmental
            'Emissões CO2', 'Consumo Energia', 'Consumo Água', 'Resíduos Recicláveis',
            'Digitalização', 'Eficiência Energética', 'Energia Renovável', 'Pegada Carbono',
            # Social
            'Diversidade Gênero', 'Diversidade Étnica', 'Pessoas com Deficiência', 'Satisfação Funcionários',
            'Horas Treinamento', 'Turnover', 'Acidentes Trabalho', 'Projetos Sociais',
            # Governance
            'Transparência', 'Compliance Score', 'Auditoria Externa', 'Comitês Independentes',
            'Políticas Atualizadas', 'Denúncias Resolvidas', 'Tempo Resposta', 'Reuniões Governança'
        ],
        'Valor_Atual': [
            # Environmental
            450, 1200, 8500, 78, 85, 7.2, 25, 15,
            # Social  
            52, 35, 8, 8.1, 42, 12, 2, 15,
            # Governance
            89, 8.8, 9.2, 75, 92, 95, 5, 24
        ],
        'Meta_2024': [
            # Environmental
            400, 1000, 7500, 85, 90, 8.0, 35, 20,
            # Social
            50, 40, 10, 8.5, 45, 10, 0, 20,
            # Governance  
            95, 9.0, 9.5, 80, 95, 98, 3, 24
        ],
        'Unidade': [
            # Environmental
            'ton', 'MWh', 'm³', '%', '%', 'score', '%', '%',
            # Social
            '%', '%', '%', 'score', 'horas', '%', 'casos', 'projetos',
            # Governance
            '%', 'score', 'score', '%', '%', '%', 'dias', 'reuniões'
        ]
    }
    
    df = pd.DataFrame(indicadores_data)
    
    # Função para calcular performance
    def calcular_performance(row):
        """Calcula performance baseada no tipo de indicador"""
        # Indicadores onde menor é melhor
        indicadores_menor_melhor = [
            'Emissões CO2', 'Consumo Energia', 'Consumo Água', 
            'Turnover', 'Acidentes Trabalho', 'Tempo Resposta'
        ]
        
        if row['Indicador'] in indicadores_menor_melhor:
            # Para estes indicadores, performance = (meta/valor_atual) * 100
            if row['Valor_Atual'] == 0:
                return 100
            performance = (row['Meta_2024'] / row['Valor_Atual']) * 100
        else:
            # Para os outros indicadores, performance = (valor_atual/meta) * 100
            if row['Meta_2024'] == 0:
                return 0
            performance = (row['Valor_Atual'] / row['Meta_2024']) * 100
        
        # Limitar entre 0 e 150%
        return max(0, min(150, performance))
    
    df['Performance'] = df.apply(calcular_performance, axis=1)
    
    # Dados de evolução mensal
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    evolucao = pd.DataFrame({
        'Mes': meses,
        'Environmental': [65, 68, 71, 74, 76, 78, 81, 83, 85, 87, 89, 91],
        'Social': [72, 74, 76, 78, 79, 81, 83, 84, 86, 87, 89, 90], 
        'Governance': [85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96]
    })
    
    return df, evolucao

def calcular_scores_esg(df):
    """Calcula os scores ESG por pilar e geral"""
    scores = {}
    for pilar in df['Pilar'].unique():
        scores[pilar] = df[df['Pilar'] == pilar]['Performance'].mean()
    
    score_geral = sum(scores.values()) / len(scores)
    return scores, score_geral

def classificar_performance(score):
    """Classifica a performance e retorna classe CSS"""
    if score >= 90:
        return "🟢 Excelente", "status-excellent"
    elif score >= 75:
        return "🟡 Bom", "status-good"
    else:
        return "🔴 Atenção", "status-attention"

# ====== INÍCIO DA APLICAÇÃO STREAMLIT ======

# Título principal
st.markdown('<h1 class="main-header">🌱 Dashboard ESG - Indicadores de Sustentabilidade</h1>', 
            unsafe_allow_html=True)

# Carregamento dos dados
try:
    df_indicadores, df_evolucao = carregar_dados_esg()
    st.success("✅ Dados carregados com sucesso!")
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.stop()

# SIDEBAR - Filtros
st.sidebar.header("🔧 Filtros e Configurações")

# Filtro de pilares
pilares_disponiveis = df_indicadores['Pilar'].unique()
pilares_selecionados = st.sidebar.multiselect(
    "Pilares ESG:",
    options=pilares_disponiveis,
    default=pilares_disponiveis
)

# Filtro de período
periodo = st.sidebar.selectbox(
    "Período de Referência:",
    options=['2024', '2023', '2022'],
    index=0
)

# Opção de benchmark
mostrar_benchmark = st.sidebar.checkbox("Mostrar Benchmark de Mercado", value=True)

# Filtrar dados
df_filtrado = df_indicadores[df_indicadores['Pilar'].isin(pilares_selecionados)]

# Calcular scores
scores, score_geral = calcular_scores_esg(df_filtrado)

# ====== MÉTRICAS PRINCIPAIS ======
st.markdown('<h2 class="section-divider">📊 Scores ESG</h2>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    classificacao, _ = classificar_performance(score_geral)
    st.metric("Score ESG Geral", f"{score_geral:.1f}", f"{classificacao}")

with col2:
    if 'Environmental' in scores:
        classificacao_env, _ = classificar_performance(scores['Environmental'])
        st.metric("🌍 Environmental", f"{scores['Environmental']:.1f}", f"{classificacao_env}")

with col3:
    if 'Social' in scores:
        classificacao_social, _ = classificar_performance(scores['Social'])
        st.metric("👥 Social", f"{scores['Social']:.1f}", f"{classificacao_social}")

with col4:
    if 'Governance' in scores:
        classificacao_gov, _ = classificar_performance(scores['Governance'])
        st.metric("⚖️ Governance", f"{scores['Governance']:.1f}", f"{classificacao_gov}")

# ====== GRÁFICOS ======
st.markdown('<h2 class="section-divider">📈 Visualizações</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Gráfico de barras - Performance por indicador
    st.subheader("Performance por Indicador")
    
    if not df_filtrado.empty:
        # Definir cores por pilar
        cores_pilar = {
            'Environmental': '#4CAF50',
            'Social': '#2196F3', 
            'Governance': '#FF9800'
        }
        
        fig_bar = px.bar(
            df_filtrado,
            x='Performance',
            y='Indicador',
            color='Pilar',
            orientation='h',
            color_discrete_map=cores_pilar,
            title="Performance dos Indicadores ESG (%)"
        )
        
        # Adicionar linha de referência em 100%
        fig_bar.add_vline(x=100, line_dash="dash", line_color="red", 
                         annotation_text="Meta (100%)")
        
        fig_bar.update_layout(height=500, showlegend=True)
        st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    # Gráfico Radar ESG
    st.subheader("Radar ESG")
    
    if len(scores) >= 3:
        fig_radar = go.Figure()
        
        # Scores atuais
        pilares_nomes = list(scores.keys())
        scores_valores = list(scores.values())
        
        fig_radar.add_trace(go.Scatterpolar(
            r=scores_valores,
            theta=pilares_nomes,
            fill='toself',
            name='Performance Atual',
            line=dict(color='#2E8B57', width=3),
            fillcolor='rgba(46, 139, 87, 0.3)'
        ))
        
        # Benchmark (se selecionado)
        if mostrar_benchmark:
            benchmark_scores = [85, 80, 88]  # Valores simulados de benchmark
            fig_radar.add_trace(go.Scatterpolar(
                r=benchmark_scores,
                theta=pilares_nomes,
                fill='toself',
                name='Benchmark Mercado',
                line=dict(color='#ff7f0e', width=2, dash='dash'),
                fillcolor='rgba(255, 127, 14, 0.1)'
            ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            height=400
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)

# ====== EVOLUÇÃO TEMPORAL ======
st.markdown('<h2 class="section-divider">📈 Evolução Histórica</h2>', unsafe_allow_html=True)

if not df_evolucao.empty:
    fig_evolucao = go.Figure()
    
    cores_evolucao = {'Environmental': '#4CAF50', 'Social': '#2196F3', 'Governance': '#FF9800'}
    
    for pilar in pilares_selecionados:
        if pilar in df_evolucao.columns:
            fig_evolucao.add_trace(go.Scatter(
                x=df_evolucao['Mes'],
                y=df_evolucao[pilar],
                mode='lines+markers',
                name=pilar,
                line=dict(color=cores_evolucao[pilar], width=3),
                marker=dict(size=8)
            ))
    
    fig_evolucao.update_layout(
        title="Evolução dos Scores ESG ao Longo do Ano",
        xaxis_title="Mês",
        yaxis_title="Score ESG",
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_evolucao, use_container_width=True)

# ====== TABELA DETALHADA ======
st.markdown('<h2 class="section-divider">📋 Indicadores Detalhados</h2>', unsafe_allow_html=True)

if not df_filtrado.empty:
    # Preparar dados para exibição
    df_display = df_filtrado.copy()
    df_display['Valor_Formatado'] = df_display['Valor_Atual'].astype(str) + ' ' + df_display['Unidade']
    df_display['Meta_Formatada'] = df_display['Meta_2024'].astype(str) + ' ' + df_display['Unidade']
    df_display['Performance_Formatada'] = df_display['Performance'].round(1).astype(str) + '%'
    
    # Adicionar coluna de status
    df_display['Status'] = df_display['Performance'].apply(
        lambda x: '🟢 Excelente' if x >= 90 else '🟡 Bom' if x >= 75 else '🔴 Atenção'
    )
    
    st.dataframe(
        df_display[['Pilar', 'Indicador', 'Valor_Formatado', 'Meta_Formatada', 'Performance_Formatada', 'Status']],
        column_config={
            "Pilar": "Pilar ESG",
            "Indicador": "Indicador", 
            "Valor_Formatado": "Valor Atual",
            "Meta_Formatada": "Meta 2024",
            "Performance_Formatada": "Performance",
            "Status": "Status"
        },
        hide_index=True,
        use_container_width=True
    )

# ====== ALERTAS E RECOMENDAÇÕES ======
st.markdown('<h2 class="section-divider">🚨 Alertas e Recomendações</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("⚠️ Indicadores Críticos")
    
    indicadores_criticos = df_filtrado[df_filtrado['Performance'] < 75]
    
    if len(indicadores_criticos) > 0:
        for _, row in indicadores_criticos.iterrows():
            st.markdown(f'<div class="alert-warning">🔴 <strong>{row["Indicador"]}</strong> ({row["Pilar"]}): {row["Performance"]:.1f}%</div>', 
                       unsafe_allow_html=True)
    else:
        st.markdown('<div class="alert-success">✅ Todos os indicadores estão dentro do esperado!</div>', 
                   unsafe_allow_html=True)

with col2:
    st.subheader("🌟 Destaques Positivos")
    
    indicadores_excelentes = df_filtrado[df_filtrado['Performance'] >= 100]
    
    if len(indicadores_excelentes) > 0:
        for _, row in indicadores_excelentes.iterrows():
            st.markdown(f'<div class="alert-success">🟢 <strong>{row["Indicador"]}</strong> ({row["Pilar"]}): {row["Performance"]:.1f}%</div>', 
                       unsafe_allow_html=True)
    else:
        st.info("Nenhum indicador superou 100% da meta ainda.")

# ====== SIDEBAR - EXPORTAÇÃO ======
st.sidebar.markdown("---")
st.sidebar.subheader("📥 Exportar Dados")

if st.sidebar.button("📊 Gerar Relatório Completo"):
    st.sidebar.success("Relatório ESG gerado!")

# Download dos dados
csv_data = df_filtrado.to_csv(index=False, encoding='utf-8')
st.sidebar.download_button(
    label="📄 Download CSV",
    data=csv_data,
    file_name=f"indicadores_esg_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
    mime="text/csv"
)

# ====== FOOTER ======
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #666; padding: 20px;">
    📅 <strong>Última atualização:</strong> {datetime.now().strftime('%d/%m/%Y às %H:%M')} | 
    👤 <strong>Responsável:</strong> Setor de Governança e Estratégia
</div>
""", unsafe_allow_html=True)