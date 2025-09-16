import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import io

# Configuração da página
st.set_page_config(
    page_title="IG-SEST Dashboard - MEJC-UFRN",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #2c5aa0 0%, #1e3c72 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #2c5aa0;
    }
    
    .conforme {
        color: #28a745;
        font-weight: bold;
    }
    
    .nao-conforme {
        color: #dc3545;
        font-weight: bold;
    }
    
    .dimension-header {
        background: #f8f9fa;
        padding: 1rem;
        border-left: 4px solid #2c5aa0;
        margin: 1rem 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Dados das conformidades
@st.cache_data
def load_data():
    """Carrega os dados de conformidade do MEJC-UFRN"""
    
    data = [
        # DIMENSÃO 1: CONSELHOS E DIRETORIA
        {"questao": "Q2", "descricao": "Colegiado Executivo se reúne semanalmente", "dimensao": "Conselhos e Diretoria", "fonte": "Boas práticas", "status": "Conforme", "prioridade": "Média"},
        {"questao": "Q4", "descricao": "Colex participa de capacitações em gestão hospitalar", "dimensao": "Conselhos e Diretoria", "fonte": "Boas práticas", "status": "Não Conforme", "prioridade": "Alta"},
        {"questao": "Q5", "descricao": "Colex participa de capacitações em governança corporativa", "dimensao": "Conselhos e Diretoria", "fonte": "Boas práticas", "status": "Não Conforme", "prioridade": "Alta"},
        {"questao": "Q6", "descricao": "Colex aprecia relatório de capacitação anualmente", "dimensao": "Conselhos e Diretoria", "fonte": "IG-Sest e Decreto nº 8.945/2016", "status": "Não Conforme", "prioridade": "Média"},
        {"questao": "Q7", "descricao": "Colex aprecia relatório de denúncias trimestralmente", "dimensao": "Conselhos e Diretoria", "fonte": "Boas práticas", "status": "Não Conforme", "prioridade": "Média"},
        {"questao": "Q8", "descricao": "Colex aprecia relatório AOC trimestralmente", "dimensao": "Conselhos e Diretoria", "fonte": "Boas práticas", "status": "Conforme", "prioridade": "Média"},
        {"questao": "Q10", "descricao": "Colex aprecia relatório CSI semestralmente", "dimensao": "Conselhos e Diretoria", "fonte": "IG-Sest e Resolução CGPAR nº 41/2022", "status": "Não Conforme", "prioridade": "Alta"},
        {"questao": "Q11", "descricao": "Colex delibera sobre AOC e PAC", "dimensao": "Conselhos e Diretoria", "fonte": "Boas práticas", "status": "Conforme", "prioridade": "Alta"},
        {"questao": "Q13", "descricao": "Colex aprecia execução do PAC trimestralmente", "dimensao": "Conselhos e Diretoria", "fonte": "Boas práticas", "status": "Conforme", "prioridade": "Média"},
        {"questao": "Q15", "descricao": "Colex delibera sobre Plano de Contratações Anual", "dimensao": "Conselhos e Diretoria", "fonte": "IESGO-TCU", "status": "Conforme", "prioridade": "Média"},
        {"questao": "Q17", "descricao": "Colex delibera sobre PDTI anualmente", "dimensao": "Conselhos e Diretoria", "fonte": "IESGO-TCU", "status": "Não Conforme", "prioridade": "Média"},
        {"questao": "Q18", "descricao": "Colex aprecia execução do PDTI semestralmente", "dimensao": "Conselhos e Diretoria", "fonte": "IESGO-TCU", "status": "Não Conforme", "prioridade": "Média"},
        {"questao": "Q19", "descricao": "Comitê de Governança Digital ativo", "dimensao": "Conselhos e Diretoria", "fonte": "Resolução CGPAR/ME 41/2022", "status": "Não Conforme", "prioridade": "Alta"},
        {"questao": "Q20", "descricao": "Núcleo de Gestão do AGHU ativo", "dimensao": "Conselhos e Diretoria", "fonte": "Portaria 630/2019", "status": "Conforme", "prioridade": "Média"},
        {"questao": "Q22", "descricao": "Plano de Transição de Gestão implementado", "dimensao": "Conselhos e Diretoria", "fonte": "Boas práticas", "status": "Não Conforme", "prioridade": "Média"},
        {"questao": "Q23", "descricao": "Conselho Consultivo funcionando", "dimensao": "Conselhos e Diretoria", "fonte": "Boas práticas", "status": "Não Conforme", "prioridade": "Alta"},
        {"questao": "Q24", "descricao": "Conselho Consultivo com representação adequada", "dimensao": "Conselhos e Diretoria", "fonte": "Boas práticas", "status": "Não Conforme", "prioridade": "Alta"},
        {"questao": "Q25", "descricao": "Comissão de Desenvolvimento de Pessoal ativa", "dimensao": "Conselhos e Diretoria", "fonte": "Boas práticas", "status": "Conforme", "prioridade": "Média"},
        {"questao": "Q27", "descricao": "Comissão de Mediação e Conciliação ativa", "dimensao": "Conselhos e Diretoria", "fonte": "Boas práticas", "status": "Conforme", "prioridade": "Média"},
        
        # DIMENSÃO 2: TRANSPARÊNCIA
        {"questao": "Q29", "descricao": "PDE considera processos prioritários", "dimensao": "Transparência", "fonte": "Boas práticas", "status": "Conforme", "prioridade": "Média"},
        {"questao": "Q31", "descricao": "PDE considera pesquisas de satisfação", "dimensao": "Transparência", "fonte": "IESGO-TCU", "status": "Conforme", "prioridade": "Média"},
        {"questao": "Q33", "descricao": "Colex aprecia relatório do PDE quadrimestralmente", "dimensao": "Transparência", "fonte": "Portaria SEI VP nº 01/2025", "status": "Conforme", "prioridade": "Média"},
        {"questao": "Q35", "descricao": "PDE considera diagnóstico ambiental", "dimensao": "Transparência", "fonte": "Boas práticas", "status": "Não Conforme", "prioridade": "Baixa"},
        {"questao": "Q36", "descricao": "Colex delibera revisão anual do PDE", "dimensao": "Transparência", "fonte": "Portaria SEI VP nº 01/2025", "status": "Conforme", "prioridade": "Média"},
        {"questao": "Q38", "descricao": "Investimentos AOC constam no PDE", "dimensao": "Transparência", "fonte": "IESGO-TCU", "status": "Conforme", "prioridade": "Média"},
        {"questao": "Q51", "descricao": "Atende 100% requisitos transparência CGU", "dimensao": "Transparência", "fonte": "Boas práticas", "status": "Conforme", "prioridade": "Alta"},
        {"questao": "Q53", "descricao": "Atualiza informações contratos/orçamento mensalmente", "dimensao": "Transparência", "fonte": "IESGO-TCU e IG-SEST", "status": "Não Conforme", "prioridade": "Média"},
        {"questao": "Q54", "descricao": "Divulga atas do Colegiado Executivo", "dimensao": "Transparência", "fonte": "Boas práticas", "status": "Não Conforme", "prioridade": "Média"},
        {"questao": "Q55", "descricao": "Divulga atas do Conselho Consultivo", "dimensao": "Transparência", "fonte": "Boas práticas", "status": "Não Conforme", "prioridade": "Baixa"},
        {"questao": "Q56", "descricao": "Divulga currículo dos ocupantes de cargos", "dimensao": "Transparência", "fonte": "IG-SEST", "status": "Conforme", "prioridade": "Média"},
        {"questao": "Q58", "descricao": "Divulga procedimentos licitatórios", "dimensao": "Transparência", "fonte": "IG-SEST e Lei nº 13.303/2016", "status": "Não Conforme", "prioridade": "Média"},
        {"questao": "Q59", "descricao": "Divulga Relatório de Gestão anualmente", "dimensao": "Transparência", "fonte": "IG-Sest", "status": "Conforme", "prioridade": "Média"},
        {"questao": "Q61", "descricao": "Publica relatório de acesso à informação", "dimensao": "Transparência", "fonte": "IESGO-TCU e Lei 12.527/2011", "status": "Conforme", "prioridade": "Média"},
        {"questao": "Q63", "descricao": "Publica agenda de compromissos públicos", "dimensao": "Transparência", "fonte": "IESGO-TCU", "status": "Conforme", "prioridade": "Média"},
        {"questao": "Q65", "descricao": "Publica número de denúncias", "dimensao": "Transparência", "fonte": "Boas práticas", "status": "Conforme", "prioridade": "Média"},
        {"questao": "Q67", "descricao": "Publica Boletim de Serviços mensalmente", "dimensao": "Transparência", "fonte": "Boas práticas", "status": "Conforme", "prioridade": "Média"},
        {"questao": "Q69", "descricao": "Realiza pesquisa de satisfação do ensino", "dimensao": "Transparência", "fonte": "IESGO-TCU", "status": "Conforme", "prioridade": "Média"},
        {"questao": "Q71", "descricao": "Realiza pesquisa de clima organizacional", "dimensao": "Transparência", "fonte": "IESGO-TCU", "status": "Não Conforme", "prioridade": "Média"},
        {"questao": "Q72", "descricao": "Realiza pesquisa de satisfação usuários SUS", "dimensao": "Transparência", "fonte": "IESGO-TCU", "status": "Conforme", "prioridade": "Média"},
        {"questao": "Q74", "descricao": "Realiza pesquisa de satisfação pesquisadores", "dimensao": "Transparência", "fonte": "IESGO-TCU e Boas Práticas Clínicas", "status": "Não Conforme", "prioridade": "Baixa"},
        
        # DIMENSÃO 3: GERENCIAMENTO DE RISCOS, CONTROLES E AUDITORIA
        {"questao": "Q40", "descricao": "Realiza treinamento sobre Código de Ética", "dimensao": "Riscos e Controles", "fonte": "IESGO-TCU e IG-Sest", "status": "Conforme", "prioridade": "Alta"},
        {"questao": "Q42", "descricao": "Orienta empregados sobre Código de Ética", "dimensao": "Riscos e Controles", "fonte": "IG-Sest, IBGC e Lei nº 13.303/2016", "status": "Conforme", "prioridade": "Alta"},
        {"questao": "Q44", "descricao": "Treinamento sobre conflito de interesses", "dimensao": "Riscos e Controles", "fonte": "IG-Sest, IBGC e Lei nº 6.404/1976", "status": "Não Conforme", "prioridade": "Média"},
        {"questao": "Q45", "descricao": "Possui Plano de Continuidade de Negócios", "dimensao": "Riscos e Controles", "fonte": "Boas práticas", "status": "Não Conforme", "prioridade": "Alta"},
        {"questao": "Q46", "descricao": "Colex aprecia relatório de riscos semestralmente", "dimensao": "Riscos e Controles", "fonte": "Boas práticas", "status": "Não Conforme", "prioridade": "Alta"},
        {"questao": "Q47", "descricao": "Colex aprecia incidentes assistenciais trimestralmente", "dimensao": "Riscos e Controles", "fonte": "Boas práticas", "status": "Não Conforme", "prioridade": "Alta"},
        {"questao": "Q48", "descricao": "Colex delibera sobre matriz de riscos", "dimensao": "Riscos e Controles", "fonte": "Boas práticas", "status": "Não Conforme", "prioridade": "Alta"},
        {"questao": "Q49", "descricao": "Possui plano de contingência climática", "dimensao": "Riscos e Controles", "fonte": "IG-Sest", "status": "Não Conforme", "prioridade": "Média"},
        {"questao": "Q50", "descricao": "Possui ETIR implementada", "dimensao": "Riscos e Controles", "fonte": "IG-Sest e Decreto nº 10.748/2021", "status": "Não Conforme", "prioridade": "Alta"},
        
        # RESPONSABILIDADE SOCIAL
        {"questao": "Q75", "descricao": "Programas de saúde do trabalhador", "dimensao": "Responsabilidade Social", "fonte": "IG-Sest e Decreto Legislativo nº 2/1992", "status": "Conforme", "prioridade": "Média"},
        {"questao": "Q77", "descricao": "Colex aprecia relatório PCDs e PNPs", "dimensao": "Responsabilidade Social", "fonte": "IESGO-TCU", "status": "Não Conforme", "prioridade": "Média"},
        {"questao": "Q78", "descricao": "Divulga ocupantes por gênero e raça", "dimensao": "Responsabilidade Social", "fonte": "IG-Sest", "status": "Não Conforme", "prioridade": "Média"},
        {"questao": "Q79", "descricao": "Programa mulheres vítimas de violência", "dimensao": "Responsabilidade Social", "fonte": "Boas práticas", "status": "Não Conforme", "prioridade": "Baixa"},
        {"questao": "Q80", "descricao": "Normas de acessibilidade em contratações", "dimensao": "Responsabilidade Social", "fonte": "IESGO-TCU", "status": "Não Conforme", "prioridade": "Média"},
        {"questao": "Q81", "descricao": "Proporcionalidade de gênero em cargos", "dimensao": "Responsabilidade Social", "fonte": "IG-SEST", "status": "Não Conforme", "prioridade": "Média"},
        {"questao": "Q82", "descricao": "Proporcionalidade racial em cargos", "dimensao": "Responsabilidade Social", "fonte": "Boas práticas", "status": "Não Conforme", "prioridade": "Média"},
        {"questao": "Q83", "descricao": "Ações de diversidade e inclusão", "dimensao": "Responsabilidade Social", "fonte": "IESGO-TCU", "status": "Não Conforme", "prioridade": "Média"},
        {"questao": "Q84", "descricao": "Ações de saúde pública com comunidade", "dimensao": "Responsabilidade Social", "fonte": "Boas práticas", "status": "Não Conforme", "prioridade": "Baixa"},
        {"questao": "Q85", "descricao": "Inclusão de grupos marginalizados", "dimensao": "Responsabilidade Social", "fonte": "Boas práticas", "status": "Não Conforme", "prioridade": "Média"},
        {"questao": "Q86", "descricao": "Programas de voluntariado", "dimensao": "Responsabilidade Social", "fonte": "IESGO-TCU", "status": "Não Conforme", "prioridade": "Baixa"},
        
        # SUSTENTABILIDADE
        {"questao": "Q87", "descricao": "Atende 70% conformidade ambiental", "dimensao": "Sustentabilidade", "fonte": "Boas práticas", "status": "Não Conforme", "prioridade": "Média"},
        {"questao": "Q88", "descricao": "Possui Plano de Logística Sustentável", "dimensao": "Sustentabilidade", "fonte": "IESGO-TCU", "status": "Não Conforme", "prioridade": "Média"},
        {"questao": "Q89", "descricao": "Publica inventário gases efeito estufa", "dimensao": "Sustentabilidade", "fonte": "IG-Sest", "status": "Não Conforme", "prioridade": "Baixa"},
    ]
    
    return pd.DataFrame(data)

# Função para criar gráficos
def create_overview_charts(df):
    """Cria gráficos de visão geral"""
    
    # Gráfico de pizza - Status geral
    status_counts = df['status'].value_counts()
    
    fig_pie = go.Figure(data=[go.Pie(
        labels=status_counts.index,
        values=status_counts.values,
        hole=0.4,
        marker_colors=['#28a745', '#dc3545'],
        textinfo='label+percent+value',
        textfont_size=14
    )])
    
    fig_pie.update_layout(
        title="Distribuição Geral de Conformidades",
        title_x=0.5,
        font=dict(size=14),
        showlegend=True,
        height=400
    )
    
    # Gráfico de barras por dimensão
    dimension_summary = df.groupby(['dimensao', 'status']).size().unstack(fill_value=0)
    
    fig_bar = go.Figure()
    
    fig_bar.add_trace(go.Bar(
        name='Conforme',
        x=dimension_summary.index,
        y=dimension_summary.get('Conforme', 0),
        marker_color='#28a745'
    ))
    
    fig_bar.add_trace(go.Bar(
        name='Não Conforme',
        x=dimension_summary.index,
        y=dimension_summary.get('Não Conforme', 0),
        marker_color='#dc3545'
    ))
    
    fig_bar.update_layout(
        title="Conformidades por Dimensão",
        xaxis_title="Dimensões",
        yaxis_title="Número de Questões",
        barmode='stack',
        height=400,
        xaxis_tickangle=-45
    )
    
    return fig_pie, fig_bar

def create_priority_chart(df):
    """Cria gráfico de prioridades das não conformidades"""
    
    non_conformes = df[df['status'] == 'Não Conforme']
    priority_counts = non_conformes['prioridade'].value_counts()
    
    colors = {'Alta': '#dc3545', 'Média': '#fd7e14', 'Baixa': '#ffc107'}
    
    fig = go.Figure(data=[go.Bar(
        x=priority_counts.index,
        y=priority_counts.values,
        marker_color=[colors[p] for p in priority_counts.index],
        text=priority_counts.values,
        textposition='auto'
    )])
    
    fig.update_layout(
        title="Não Conformidades por Prioridade",
        xaxis_title="Prioridade",
        yaxis_title="Número de Questões",
        height=400
    )
    
    return fig

def calculate_metrics(df):
    """Calcula métricas principais"""
    
    total_questoes = len(df)
    conformes = len(df[df['status'] == 'Conforme'])
    nao_conformes = len(df[df['status'] == 'Não Conforme'])
    taxa_conformidade = (conformes / total_questoes) * 100
    
    # Métricas por dimensão
    dim_metrics = df.groupby('dimensao')['status'].agg(['count', lambda x: (x == 'Conforme').sum()]).round(2)
    dim_metrics.columns = ['total', 'conformes']
    dim_metrics['taxa'] = (dim_metrics['conformes'] / dim_metrics['total'] * 100).round(1)
    
    return {
        'total': total_questoes,
        'conformes': conformes,
        'nao_conformes': nao_conformes,
        'taxa_conformidade': taxa_conformidade,
        'dimensoes': dim_metrics
    }

def export_to_excel(df):
    """Gera arquivo Excel para download"""
    
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Planilha principal
        df.to_excel(writer, sheet_name='Conformidades', index=False)
        
        # Resumo por dimensão
        summary = df.groupby(['dimensao', 'status']).size().unstack(fill_value=0)
        summary['Total'] = summary.sum(axis=1)
        summary['Taxa_Conformidade'] = (summary.get('Conforme', 0) / summary['Total'] * 100).round(2)
        summary.to_excel(writer, sheet_name='Resumo_Dimensoes')
        
        # Não conformidades por prioridade
        non_conf = df[df['status'] == 'Não Conforme']
        priority_summary = non_conf.groupby('prioridade').size().to_frame('Quantidade')
        priority_summary.to_excel(writer, sheet_name='Nao_Conformidades')
    
    return output.getvalue()

# APLICAÇÃO PRINCIPAL
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏥 Dashboard IG-SEST</h1>
        <h3>Maternidade Escola Januário Cicco - UFRN</h3>
        <p>Análise de Conformidades em Governança Corporativa</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Carrega dados
    df = load_data()
    metrics = calculate_metrics(df)
    
    # Sidebar
    st.sidebar.title("🔧 Filtros e Controles")
    
    # Filtros
    dimensoes_selecionadas = st.sidebar.multiselect(
        "Dimensões:",
        options=df['dimensao'].unique(),
        default=df['dimensao'].unique()
    )
    
    status_selecionado = st.sidebar.multiselect(
        "Status:",
        options=df['status'].unique(),
        default=df['status'].unique()
    )
    
    prioridade_selecionada = st.sidebar.multiselect(
        "Prioridade:",
        options=df['prioridade'].unique(),
        default=df['prioridade'].unique()
    )
    
    # Filtrar dados
    df_filtered = df[
        (df['dimensao'].isin(dimensoes_selecionadas)) &
        (df['status'].isin(status_selecionado)) &
        (df['prioridade'].isin(prioridade_selecionada))
    ]
    
    # Métricas principais
    st.markdown("## 📊 Métricas Principais")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total de Questões",
            value=metrics['total'],
            delta=None
        )
    
    with col2:
        st.metric(
            label="Questões Conformes",
            value=metrics['conformes'],
            delta=f"{metrics['taxa_conformidade']:.1f}%"
        )
    
    with col3:
        st.metric(
            label="Não Conformes",
            value=metrics['nao_conformes'],
            delta=f"-{100-metrics['taxa_conformidade']:.1f}%"
        )
    
    with col4:
        # Comparação com padrão EBSERH (95.65%)
        delta_ebserh = metrics['taxa_conformidade'] - 95.65
        st.metric(
            label="vs. Padrão EBSERH",
            value=f"{metrics['taxa_conformidade']:.1f}%",
            delta=f"{delta_ebserh:.1f}%"
        )
    
    # Gráficos principais
    st.markdown("## 📈 Visão Geral")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_pie, fig_bar = create_overview_charts(df_filtered)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Gráfico de prioridades
    st.markdown("## ⚠️ Análise de Prioridades")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_priority = create_priority_chart(df_filtered)
        st.plotly_chart(fig_priority, use_container_width=True)
    
    with col2:
        st.markdown("### Principais Não Conformidades")
        alta_prioridade = df_filtered[
            (df_filtered['status'] == 'Não Conforme') & 
            (df_filtered['prioridade'] == 'Alta')
        ]
        
        for _, row in alta_prioridade.head(5).iterrows():
            st.markdown(f"**{row['questao']}:** {row['descricao'][:50]}...")
    
    # Performance por dimensão
    st.markdown("## 🎯 Performance por Dimensão")
    
    for dim in metrics['dimensoes'].index:
        with st.expander(f"{dim} - {metrics['dimensoes'].loc[dim, 'taxa']}% de conformidade"):
            dim_data = df[df['dimensao'] == dim]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total", int(metrics['dimensoes'].loc[dim, 'total']))
            with col2:
                st.metric("Conformes", int(metrics['dimensoes'].loc[dim, 'conformes']))
            with col3:
                st.metric("Taxa", f"{metrics['dimensoes'].loc[dim, 'taxa']}%")
            
            # Tabela detalhada da dimensão
            st.dataframe(
                dim_data[['questao', 'descricao', 'status', 'prioridade', 'fonte']],
                use_container_width=True
            )
    
    # Tabela completa
    st.markdown("## 📋 Tabela Detalhada")
    
    # Aplicar estilo baseado no status
    def highlight_status(val):
        if val == 'Conforme':
            return 'background-color: #d4edda; color: #155724'
        elif val == 'Não Conforme':
            return 'background-color: #f8d7da; color: #721c24'
        return ''
    
    # Renomear colunas com acentos e maiúsculas
    df_display = df_filtered.rename(columns={
        'questao': 'Questão',
        'descricao': 'Descrição',
        'dimensao': 'Dimensão',
        'fonte': 'Fonte',
        'status': 'Status',
        'prioridade': 'Prioridade'
    })
    
    styled_df = df_display.style.applymap(highlight_status, subset=['Status'])
    st.dataframe(styled_df, use_container_width=True, height=400)
    
    # Exportação
    st.markdown("## 💾 Exportação de Dados")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Gerar Relatório Excel", type="primary"):
            excel_file = export_to_excel(df)
            st.download_button(
                label="⬇️ Download Excel",
                data=excel_file,
                file_name=f"IGSEST_MEJC_UFRN_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    with col2:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📄 Download CSV",
            data=csv,
            file_name=f"conformidades_mejc_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with col3:
        if st.button("🔄 Atualizar Dados"):
            st.cache_data.clear()
            st.experimental_rerun()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        f"Relatório gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')} | "
        "Maternidade Escola Januário Cicco - UFRN"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()