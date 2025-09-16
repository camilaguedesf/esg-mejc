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
    page_title="IG-SEST Painel - MEJC-UFRN",
    page_icon="",
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
        {"questão": "Q2", "descrição": "Colegiado Executivo se reúne semanalmente", "dimensão": "Conselhos e Diretoria", "fonte": "Boas práticas", "status": "Conforme", "prioridade": "Média"},
        {"questão": "Q4", "descrição": "Colex participa de capacitações em gestão hospitalar", "dimensão": "Conselhos e Diretoria", "fonte": "Boas práticas", "status": "Não Conforme", "prioridade": "Alta"},
        {"questão": "Q5", "descrição": "Colex participa de capacitações em governança corporativa", "dimensão": "Conselhos e Diretoria", "fonte": "Boas práticas", "status": "Não Conforme", "prioridade": "Alta"},
        {"questão": "Q6", "descrição": "Colex aprecia relatório de capacitação anualmente", "dimensão": "Conselhos e Diretoria", "fonte": "IG-Sest e Decreto nº 8.945/2016", "status": "Não Conforme", "prioridade": "Média"},
        {"questão": "Q7", "descrição": "Colex aprecia relatório de denúncias trimestralmente", "dimensão": "Conselhos e Diretoria", "fonte": "Boas práticas", "status": "Não Conforme", "prioridade": "Média"},
        {"questão": "Q8", "descrição": "Colex aprecia relatório AOC trimestralmente", "dimensão": "Conselhos e Diretoria", "fonte": "Boas práticas", "status": "Conforme", "prioridade": "Média"},
        {"questão": "Q10", "descrição": "Colex aprecia relatório CSI semestralmente", "dimensão": "Conselhos e Diretoria", "fonte": "IG-Sest e Resolução CGPAR nº 41/2022", "status": "Não Conforme", "prioridade": "Alta"},
        {"questão": "Q11", "descrição": "Colex delibera sobre AOC e PAC", "dimensão": "Conselhos e Diretoria", "fonte": "Boas práticas", "status": "Conforme", "prioridade": "Alta"},
        {"questão": "Q13", "descrição": "Colex aprecia execução do PAC trimestralmente", "dimensão": "Conselhos e Diretoria", "fonte": "Boas práticas", "status": "Conforme", "prioridade": "Média"},
        {"questão": "Q15", "descrição": "Colex delibera sobre Plano de Contratações Anual", "dimensão": "Conselhos e Diretoria", "fonte": "IESGO-TCU", "status": "Conforme", "prioridade": "Média"},
        {"questão": "Q17", "descrição": "Colex delibera sobre PDTI anualmente", "dimensão": "Conselhos e Diretoria", "fonte": "IESGO-TCU", "status": "Não Conforme", "prioridade": "Média"},
        {"questão": "Q18", "descrição": "Colex aprecia execução do PDTI semestralmente", "dimensão": "Conselhos e Diretoria", "fonte": "IESGO-TCU", "status": "Não Conforme", "prioridade": "Média"},
        {"questão": "Q19", "descrição": "Comitê de Governança Digital ativo", "dimensão": "Conselhos e Diretoria", "fonte": "Resolução CGPAR/ME 41/2022", "status": "Não Conforme", "prioridade": "Alta"},
        {"questão": "Q20", "descrição": "Núcleo de Gestão do AGHU ativo", "dimensão": "Conselhos e Diretoria", "fonte": "Portaria 630/2019", "status": "Conforme", "prioridade": "Média"},
        {"questão": "Q22", "descrição": "Plano de Transição de Gestão implementado", "dimensão": "Conselhos e Diretoria", "fonte": "Boas práticas", "status": "Não Conforme", "prioridade": "Média"},
        {"questão": "Q23", "descrição": "Conselho Consultivo funcionando", "dimensão": "Conselhos e Diretoria", "fonte": "Boas práticas", "status": "Não Conforme", "prioridade": "Alta"},
        {"questão": "Q24", "descrição": "Conselho Consultivo com representação adequada", "dimensão": "Conselhos e Diretoria", "fonte": "Boas práticas", "status": "Não Conforme", "prioridade": "Alta"},
        {"questão": "Q25", "descrição": "Comissão de Desenvolvimento de Pessoal ativa", "dimensão": "Conselhos e Diretoria", "fonte": "Boas práticas", "status": "Conforme", "prioridade": "Média"},
        {"questão": "Q27", "descrição": "Comissão de Mediação e Conciliação ativa", "dimensão": "Conselhos e Diretoria", "fonte": "Boas práticas", "status": "Conforme", "prioridade": "Média"},
        
        # DIMENSÃO 2: TRANSPARÊNCIA
        {"questão": "Q29", "descrição": "PDE considera processos prioritários", "dimensão": "Transparência", "fonte": "Boas práticas", "status": "Conforme", "prioridade": "Média"},
        {"questão": "Q31", "descrição": "PDE considera pesquisas de satisfação", "dimensão": "Transparência", "fonte": "IESGO-TCU", "status": "Conforme", "prioridade": "Média"},
        {"questão": "Q33", "descrição": "Colex aprecia relatório do PDE quadrimestralmente", "dimensão": "Transparência", "fonte": "Portaria SEI VP nº 01/2025", "status": "Conforme", "prioridade": "Média"},
        {"questão": "Q35", "descrição": "PDE considera diagnóstico ambiental", "dimensão": "Transparência", "fonte": "Boas práticas", "status": "Não Conforme", "prioridade": "Baixa"},
        {"questão": "Q36", "descrição": "Colex delibera revisão anual do PDE", "dimensão": "Transparência", "fonte": "Portaria SEI VP nº 01/2025", "status": "Conforme", "prioridade": "Média"},
        {"questão": "Q38", "descrição": "Investimentos AOC constam no PDE", "dimensão": "Transparência", "fonte": "IESGO-TCU", "status": "Conforme", "prioridade": "Média"},
        {"questão": "Q51", "descrição": "Atende 100% requisitos transparência CGU", "dimensão": "Transparência", "fonte": "Boas práticas", "status": "Conforme", "prioridade": "Alta"},
        {"questão": "Q53", "descrição": "Atualiza informações contratos/orçamento mensalmente", "dimensão": "Transparência", "fonte": "IESGO-TCU e IG-SEST", "status": "Não Conforme", "prioridade": "Média"},
        {"questão": "Q54", "descrição": "Divulga atas do Colegiado Executivo", "dimensão": "Transparência", "fonte": "Boas práticas", "status": "Não Conforme", "prioridade": "Média"},
        {"questão": "Q55", "descrição": "Divulga atas do Conselho Consultivo", "dimensão": "Transparência", "fonte": "Boas práticas", "status": "Não Conforme", "prioridade": "Baixa"},
        {"questão": "Q56", "descrição": "Divulga currículo dos ocupantes de cargos", "dimensão": "Transparência", "fonte": "IG-SEST", "status": "Conforme", "prioridade": "Média"},
        {"questão": "Q58", "descrição": "Divulga procedimentos licitatórios", "dimensão": "Transparência", "fonte": "IG-SEST e Lei nº 13.303/2016", "status": "Não Conforme", "prioridade": "Média"},
        {"questão": "Q59", "descrição": "Divulga Relatório de Gestão anualmente", "dimensão": "Transparência", "fonte": "IG-Sest", "status": "Conforme", "prioridade": "Média"},
        {"questão": "Q61", "descrição": "Publica relatório de acesso à informação", "dimensão": "Transparência", "fonte": "IESGO-TCU e Lei 12.527/2011", "status": "Conforme", "prioridade": "Média"},
        {"questão": "Q63", "descrição": "Publica agenda de compromissos públicos", "dimensão": "Transparência", "fonte": "IESGO-TCU", "status": "Conforme", "prioridade": "Média"},
        {"questão": "Q65", "descrição": "Publica número de denúncias", "dimensão": "Transparência", "fonte": "Boas práticas", "status": "Conforme", "prioridade": "Média"},
        {"questão": "Q67", "descrição": "Publica Boletim de Serviços mensalmente", "dimensão": "Transparência", "fonte": "Boas práticas", "status": "Conforme", "prioridade": "Média"},
        {"questão": "Q69", "descrição": "Realiza pesquisa de satisfação do ensino", "dimensão": "Transparência", "fonte": "IESGO-TCU", "status": "Conforme", "prioridade": "Média"},
        {"questão": "Q71", "descrição": "Realiza pesquisa de clima organizacional", "dimensão": "Transparência", "fonte": "IESGO-TCU", "status": "Não Conforme", "prioridade": "Média"},
        {"questão": "Q72", "descrição": "Realiza pesquisa de satisfação usuários SUS", "dimensão": "Transparência", "fonte": "IESGO-TCU", "status": "Conforme", "prioridade": "Média"},
        {"questão": "Q74", "descrição": "Realiza pesquisa de satisfação pesquisadores", "dimensão": "Transparência", "fonte": "IESGO-TCU e Boas Práticas Clínicas", "status": "Não Conforme", "prioridade": "Baixa"},
        
        # DIMENSÃO 3: GERENCIAMENTO DE RISCOS, CONTROLES E AUDITORIA
        {"questão": "Q40", "descrição": "Realiza treinamento sobre Código de Ética", "dimensão": "Riscos e Controles", "fonte": "IESGO-TCU e IG-Sest", "status": "Conforme", "prioridade": "Alta"},
        {"questão": "Q42", "descrição": "Orienta empregados sobre Código de Ética", "dimensão": "Riscos e Controles", "fonte": "IG-Sest, IBGC e Lei nº 13.303/2016", "status": "Conforme", "prioridade": "Alta"},
        {"questão": "Q44", "descrição": "Treinamento sobre conflito de interesses", "dimensão": "Riscos e Controles", "fonte": "IG-Sest, IBGC e Lei nº 6.404/1976", "status": "Não Conforme", "prioridade": "Média"},
        {"questão": "Q45", "descrição": "Possui Plano de Continuidade de Negócios", "dimensão": "Riscos e Controles", "fonte": "Boas práticas", "status": "Não Conforme", "prioridade": "Alta"},
        {"questão": "Q46", "descrição": "Colex aprecia relatório de riscos semestralmente", "dimensão": "Riscos e Controles", "fonte": "Boas práticas", "status": "Não Conforme", "prioridade": "Alta"},
        {"questão": "Q47", "descrição": "Colex aprecia incidentes assistenciais trimestralmente", "dimensão": "Riscos e Controles", "fonte": "Boas práticas", "status": "Não Conforme", "prioridade": "Alta"},
        {"questão": "Q48", "descrição": "Colex delibera sobre matriz de riscos", "dimensão": "Riscos e Controles", "fonte": "Boas práticas", "status": "Não Conforme", "prioridade": "Alta"},
        {"questão": "Q49", "descrição": "Possui plano de contingência climática", "dimensão": "Riscos e Controles", "fonte": "IG-Sest", "status": "Não Conforme", "prioridade": "Média"},
        {"questão": "Q50", "descrição": "Possui ETIR implementada", "dimensão": "Riscos e Controles", "fonte": "IG-Sest e Decreto nº 10.748/2021", "status": "Não Conforme", "prioridade": "Alta"},
        
        # RESPONSABILIDADE SOCIAL
        {"questão": "Q75", "descrição": "Programas de saúde do trabalhador", "dimensão": "Responsabilidade Social", "fonte": "IG-Sest e Decreto Legislativo nº 2/1992", "status": "Conforme", "prioridade": "Média"},
        {"questão": "Q77", "descrição": "Colex aprecia relatório PCDs e PNPs", "dimensão": "Responsabilidade Social", "fonte": "IESGO-TCU", "status": "Não Conforme", "prioridade": "Média"},
        {"questão": "Q78", "descrição": "Divulga ocupantes por gênero e raça", "dimensão": "Responsabilidade Social", "fonte": "IG-Sest", "status": "Não Conforme", "prioridade": "Média"},
        {"questão": "Q79", "descrição": "Programa mulheres vítimas de violência", "dimensão": "Responsabilidade Social", "fonte": "Boas práticas", "status": "Não Conforme", "prioridade": "Baixa"},
        {"questão": "Q80", "descrição": "Normas de acessibilidade em contratações", "dimensão": "Responsabilidade Social", "fonte": "IESGO-TCU", "status": "Não Conforme", "prioridade": "Média"},
        {"questão": "Q81", "descrição": "Proporcionalidade de gênero em cargos", "dimensão": "Responsabilidade Social", "fonte": "IG-SEST", "status": "Não Conforme", "prioridade": "Média"},
        {"questão": "Q82", "descrição": "Proporcionalidade racial em cargos", "dimensão": "Responsabilidade Social", "fonte": "Boas práticas", "status": "Não Conforme", "prioridade": "Média"},
        {"questão": "Q83", "descrição": "Ações de diversidade e inclusão", "dimensão": "Responsabilidade Social", "fonte": "IESGO-TCU", "status": "Não Conforme", "prioridade": "Média"},
        {"questão": "Q84", "descrição": "Ações de saúde pública com comunidade", "dimensão": "Responsabilidade Social", "fonte": "Boas práticas", "status": "Não Conforme", "prioridade": "Baixa"},
        {"questão": "Q85", "descrição": "Inclusão de grupos marginalizados", "dimensão": "Responsabilidade Social", "fonte": "Boas práticas", "status": "Não Conforme", "prioridade": "Média"},
        {"questão": "Q86", "descrição": "Programas de voluntariado", "dimensão": "Responsabilidade Social", "fonte": "IESGO-TCU", "status": "Não Conforme", "prioridade": "Baixa"},
        
        # SUSTENTABILIDADE
        {"questão": "Q87", "descrição": "Atende 70% conformidade ambiental", "dimensão": "Sustentabilidade", "fonte": "Boas práticas", "status": "Não Conforme", "prioridade": "Média"},
        {"questão": "Q88", "descrição": "Possui Plano de Logística Sustentável", "dimensão": "Sustentabilidade", "fonte": "IESGO-TCU", "status": "Não Conforme", "prioridade": "Média"},
        {"questão": "Q89", "descrição": "Publica inventário gases efeito estufa", "dimensão": "Sustentabilidade", "fonte": "IG-Sest", "status": "Não Conforme", "prioridade": "Baixa"},
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
    dimension_summary = df.groupby(['dimensão', 'status']).size().unstack(fill_value=0)
    
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
    dim_metrics = df.groupby('dimensão')['status'].agg(['count', lambda x: (x == 'Conforme').sum()]).round(2)
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
        summary = df.groupby(['dimensão', 'status']).size().unstack(fill_value=0)
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
        <h1> Painel IG-SEST</h1>
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
        options=df['dimensão'].unique(),
        default=df['dimensão'].unique()
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
        (df['dimensão'].isin(dimensoes_selecionadas)) &
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
            st.markdown(f"**{row['questão']}:** {row['descrição'][:50]}...")
    
    # Performance por dimensão
    st.markdown("## 🎯 Performance por Dimensão")
    
    for dim in metrics['dimensoes'].index:
        with st.expander(f"{dim} - {metrics['dimensoes'].loc[dim, 'taxa']}% de conformidade"):
            dim_data = df[df['dimensão'] == dim]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total", int(metrics['dimensoes'].loc[dim, 'total']))
            with col2:
                st.metric("Conformes", int(metrics['dimensoes'].loc[dim, 'conformes']))
            with col3:
                st.metric("Taxa", f"{metrics['dimensoes'].loc[dim, 'taxa']}%")
            
            # Tabela detalhada da dimensão
            st.dataframe(
                dim_data[['questão', 'descrição', 'status', 'prioridade', 'fonte']],
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
        'questão': 'Questão',
        'descrição': 'Descrição',
        'dimensão': 'Dimensão',
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