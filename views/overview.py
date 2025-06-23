import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data.overview_data import (
    get_total_cases,
    get_common_crime,
    get_trend_case,
    get_arrest_rate,
    get_crime_history_data,
    get_arrest_rates_by_category,
    get_cases_by_category,
    get_domestic_status_by_category
)

def show():  
    # Fetch real data from database
    total_cases = get_total_cases()
    common_crime = get_common_crime()
    trend_case = get_trend_case()
    arrest_rate = get_arrest_rate()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-title">
                    <i class="fa-solid fa-chart-simple white-icon"></i>
                    <span>Total Cases</span>
                    <div class="tooltip">
                        <span class="tooltip-icon"></span>
                        <span class="tooltiptext">Jumlah total kasus yang terjadi</span>
                    </div>
                </div>
                <div class="metric-value">{total_cases:,}</div>
                 <div class="metric-delta">
                    <i></i>
                    <span>  </span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-title">
                    <i class="fa-solid fa-magnifying-glass-plus white-icon"></i>
                    <span>Common Crime</span>
                    <div class="tooltip">
                        <span class="tooltip-icon"></span>
                        <span class="tooltiptext">Jenis kejahatan yang paling sering terjadi</span>
                    </div>
                </div>
                <div class="metric-value">{common_crime['primary_type'].upper()}</div>
                <div class="metric-delta">
                    <i class="fas fa-arrow-up metric-delta-arrow"></i>
                    <span>{common_crime['incident_count']:,} Cases</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-title">
                    <i class="fa-solid fa-arrow-trend-up white-icon"></i>
                    <span>Trend Case</span>
                    <div class="tooltip">
                        <span class="tooltip-icon"></span>
                        <span class="tooltiptext">Kasus terbanyak di bulan ini</span>
                    </div>
                </div>
                <div class="metric-value">{trend_case['primary_type'].upper()}</div>
                <div class="metric-delta">
                    <i class="fas fa-arrow-up metric-delta-arrow"></i>
                    <span>{trend_case['year']}/{trend_case['month']:02d}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-title">
                    <i class="fa-solid fa-percent white-icon"></i>
                    <span>Arrest Rate</span>
                    <div class="tooltip">
                        <span class="tooltip-icon"></span>
                        <span class="tooltiptext">Persentase tingkat penangkapan</span>
                    </div>
                </div>
                <div class="metric-value">{arrest_rate}%</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Crime History")
    df_monthly = get_crime_history_data()
    if not df_monthly.empty:
        df_monthly['Arrest_Percentage'] = (df_monthly['Arrested Cases'] / df_monthly['Total Crime'] * 100).round(2)

        fig_history = go.Figure()

        fig_history.add_trace(go.Scatter(
            x=df_monthly['Year'],
            y=df_monthly['Total Crime'],
            mode='lines',
            name='Total Crime',
            line=dict(color='#8979FF', width=4, shape='spline'),
            fill='tonexty',
            fillcolor='rgba(137, 121, 255, 0.1)',
            hovertemplate='<b>%{fullData.name}</b><br>' +
                        'Year: %{x}<br>' +
                        'Total Cases: %{y:,}<br>' +
                        '<extra></extra>'
        ))

        fig_history.add_trace(go.Scatter(
            x=df_monthly['Year'],
            y=df_monthly['Arrested Cases'],
            mode='lines',
            name='Arrested Cases',
            line=dict(color='#FF6B6B', width=4, shape='spline'),
            fill='tonexty',
            fillcolor='rgba(255, 107, 107, 0.1)',
            customdata=df_monthly['Arrest_Percentage'],
            hovertemplate='<b>%{fullData.name}</b><br>' +
                        'Year: %{x}<br>' +
                        'Arrested Cases: %{y:,}<br>' +
                        'Arrest Rate: %{customdata}%<br>' +
                        '<extra></extra>'
        ))
        
        fig_history.update_layout(
            title='Total Crime and Arrests Over Years',
            xaxis_title="Year",
            yaxis_title="Number of Cases",
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            title_font=dict(size=18, color='white'),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            ),
            xaxis=dict(
                gridcolor='rgba(128,128,128,0.2)',
                showgrid=True,
                zeroline=False
            ),
            yaxis=dict(
                gridcolor='rgba(128,128,128,0.2)',
                showgrid=True,
                zeroline=False
            ),
            margin=dict(l=0, r=0, t=60, b=0)
        )
        
        st.plotly_chart(fig_history, use_container_width=True)
    else:
        st.error("No data available for crime history chart")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        df_arrest_rates = get_arrest_rates_by_category()
        if not df_arrest_rates.empty:
            fig_arrest = px.bar(df_arrest_rates, x='Crime Type', y='Arrest Rate', 
                            title='Arrest Rate per Crime Category')
            gradient_colors = []
            for i in range(len(df_arrest_rates)):
                ratio = i / (len(df_arrest_rates) - 1) if len(df_arrest_rates) > 1 else 0
                
                r = int(137 + (255 - 137) * ratio)
                g = int(121 + (255 - 121) * ratio)
                b = int(255 + (255 - 255) * ratio)
                
                gradient_colors.append(f'rgb({r}, {g}, {b})')
            
            max_value = df_arrest_rates['Arrest Rate'].max()
            y_max = max_value * 1.15 
            
            fig_arrest.update_traces(
                marker=dict(
                    color=gradient_colors,
                    line=dict(color='rgba(0,0,0,0.2)', width=1)
                ),
                texttemplate='%{y:.1f}%',
                textposition='outside'
            )
            fig_arrest.update_layout(
                xaxis_title="Crime Category",
                yaxis_title="Arrest Rate (%)",
                xaxis_tickangle=-45,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                title_font=dict(size=16, color='white'),
                xaxis=dict(
                    gridcolor='rgba(128,128,128,0.2)',
                    showgrid=False,
                    zeroline=False
                ),
                yaxis=dict(
                    gridcolor='rgba(128,128,128,0.2)',
                    showgrid=True,
                    zeroline=False,
                    range=[0, y_max]  
                ),
                margin=dict(l=0, r=0, t=60, b=0)  
            )
            st.plotly_chart(fig_arrest, use_container_width=True)
        else:
            st.error("No data available for arrest rate chart")

    with col2:
        df_cases_category = get_cases_by_category()
        if not df_cases_category.empty:
            colorful_palette = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#F7DC6F', '#BB8FCE', '#85C1E9', '#F8C471', '#82E0AA']
            
            fig_category_pie = px.pie(df_cases_category, names='crime_category', values='total_cases', 
                                    title='Total Cases by Category',
                                    color_discrete_sequence=colorful_palette)
            fig_category_pie.update_traces(textinfo='percent+label')
            fig_category_pie.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                title_font=dict(size=16, color='white'),
                margin=dict(l=0, r=0, t=60, b=0)  
            )
            st.plotly_chart(fig_category_pie, use_container_width=True)
        else:
            st.error("No data available for cases by category chart")

    st.markdown("---")
   
    df_domestic_status = get_domestic_status_by_category()
    if not df_domestic_status.empty:
        max_domestic = df_domestic_status['domestic_cases'].max()
        max_non_domestic = df_domestic_status['non_domestic_cases'].max()
        max_value = max(max_domestic, max_non_domestic)
        y_max = max_value * 1.15 

        fig_domestic = go.Figure()

        fig_domestic.add_trace(go.Bar(
            name='Domestic Cases',
            x=df_domestic_status['crime_category'],
            y=df_domestic_status['domestic_cases'],
            marker_color='#FF6B6B',
            text=df_domestic_status['domestic_cases'],
            textposition='outside',
            texttemplate='%{text:,}'
        ))

        fig_domestic.add_trace(go.Bar(
            name='Non-Domestic Cases',
            x=df_domestic_status['crime_category'],
            y=df_domestic_status['non_domestic_cases'],
            marker_color='#4ECDC4',
            text=df_domestic_status['non_domestic_cases'],
            textposition='outside',
            texttemplate='%{text:,}'
        ))
        
        fig_domestic.update_layout(
            title='Domestic Status Comparison by Crime Category',
            barmode='group',
            xaxis_title="Crime Category",
            yaxis_title="Number of Cases",
            xaxis_tickangle=-45,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            title_font=dict(size=16, color='white'),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            ),
            xaxis=dict(
                gridcolor='rgba(128,128,128,0.2)',
                showgrid=False,
                zeroline=False
            ),
            yaxis=dict(
                gridcolor='rgba(128,128,128,0.2)',
                showgrid=True,
                zeroline=False,
                range=[0, y_max]  
            ),
            margin=dict(l=0, r=0, t=80, b=0)  
        )
        
        st.plotly_chart(fig_domestic, use_container_width=True)
    else:
        st.error("No data available for domestic status comparison chart")