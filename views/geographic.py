import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
from data.geographic_data import (
    get_total_cases_by_date_range,
    get_crime_hotspot_category_by_date_range,
    get_risky_area_by_date_range,
    get_total_areas,
    get_map_data_by_date_range,
    get_crime_by_location_category,
    get_top_location_descriptions,
    get_crime_details_by_date_range,
    get_location_categories,
    get_crime_categories,
    get_filtered_total_incidents_geographic  
)

def show():
    today = date.today()
    start_of_year = date(today.year, 1, 1)

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("""
            <div style="text-align: right; padding-top: 5px;">
                <strong>Rentang Waktu :</strong>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        date_range = st.date_input(
            label="",
            value=(start_of_year, today),
            min_value=date(2001, 1, 1),
            max_value=today,
            label_visibility="collapsed"
        )

    if len(date_range) == 2:
        start_date = date_range[0]
        end_date = date_range[1]

        if start_date > end_date:
            st.error("Tanggal mulai tidak boleh lebih besar dari tanggal akhir")
        else:
            # Fetch data from database
            total_cases = get_total_cases_by_date_range(start_date, end_date)
            hotspot_category, hotspot_cases = get_crime_hotspot_category_by_date_range(start_date, end_date)
            risky_area, risky_cases = get_risky_area_by_date_range(start_date, end_date)
            total_areas = get_total_areas()
            map_data = get_map_data_by_date_range(start_date, end_date)
            location_crime_data = get_crime_by_location_category(start_date, end_date)
            top_locations_data = get_top_location_descriptions(start_date, end_date, limit=5)
            
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown(f"""
                    <div class="metric-container">
                        <div class="metric-title">
                            <i class="fa-solid fa-chart-simple white-icon"></i>
                            <span style="font-size: 0.9em;">Total Cases</span>
                            <div class="tooltip">
                                <span class="tooltip-icon"></span>
                                <span class="tooltiptext">Jumlah total kasus yang terjadi</span>
                            </div>
                        </div>
                        <div class="metric-value" style="font-size: 1.8em;">{total_cases:,}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div class="metric-container">
                        <div class="metric-title">
                            <i class="fas fa-fire white-icon"></i>
                            <span style="font-size: 0.9em;">Crime Hotspot</span>
                            <div class="tooltip">
                                <span class="tooltip-icon"></span>
                                <span class="tooltiptext">Kategori area dengan kejahatan tertinggi</span>
                            </div>
                        </div>
                        <div class="metric-value" style="font-size: 0.9em; line-height: 1.2;">{hotspot_category if hotspot_category else 'N/A'}</div>
                        <div class="metric-delta">
                            <i class="fas fa-arrow-up metric-delta-arrow"></i>
                            <span style="font-size: 0.8em;">{hotspot_cases:,} Cases</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                    <div class="metric-container">
                        <div class="metric-title">
                            <i class="fas fa-road white-icon"></i>
                            <span style="font-size: 0.9em;">Risky Area</span>
                            <div class="tooltip">
                                <span class="tooltip-icon"></span>
                                <span class="tooltiptext">Lokasi paling berisiko</span>
                            </div>
                        </div>
                        <div class="metric-value" style="font-size: 0.9em; line-height: 1.2;">{risky_area if risky_area else 'N/A'}</div>
                        <div class="metric-delta">
                            <i class="fas fa-arrow-up metric-delta-arrow"></i>
                            <span style="font-size: 0.8em;">{risky_cases:,} Cases</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                    <div class="metric-container">
                        <div class="metric-title">
                            <i class="fas fa-layer-group white-icon"></i>
                            <span style="font-size: 0.9em;">Total Area</span>
                            <div class="tooltip">
                                <span class="tooltip-icon"></span>
                                <span class="tooltiptext">Jumlah area yang dipantau</span>
                            </div>
                        </div>
                        <div class="metric-value" style="font-size: 1.8em;">{total_areas:,}</div>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown("---")
            
            # Crime Distribution Map
            st.subheader("Crime Distribution Map")

            if not map_data.empty:
                color_map = {
                    'Street and Narcotics Crimes': '#347433',
                    'Battery Crimes': '#FFC107', 
                    'Burglary': '#45B7D1',
                    'Theft Crimes': '#FF6F3C',
                    'Property Crimes': '#B22222'
                }

                fig = go.Figure()
                
                for category in map_data['crime_category'].unique():
                    category_data = map_data[map_data['crime_category'] == category]
                    
                    fig.add_trace(go.Scattermapbox(
                        lat=category_data['latitude'],
                        lon=category_data['longitude'],
                        mode='markers',
                        marker=dict(
                            size=category_data['total_incidents'].apply(lambda x: min(max(x/10, 5), 20)),
                            color=color_map.get(category, '#95A5A6'),
                            opacity=0.7
                        ),
                        text=category_data.apply(lambda row: 
                            f"<b>{row['primary_type']}</b><br>" +
                            f"Location: {row['location_description']}<br>" +
                            f"Category: {row['crime_category']}<br>" +
                            f"Incidents: {row['total_incidents']}", axis=1),
                        hovertemplate='%{text}<extra></extra>',
                        name=category
                    ))
                
                fig.update_layout(
                    mapbox=dict(
                        accesstoken=None,  
                        style="open-street-map",
                        center=dict(
                            lat=map_data['latitude'].mean(),
                            lon=map_data['longitude'].mean()
                        ),
                        zoom=10
                    ),
                    height=600,
                    margin=dict(l=0, r=0, t=0, b=0),
                    showlegend=True,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.1,
                        xanchor="center",
                        x=0.5,
                        bgcolor="rgba(255,255,255,0.9)",
                        bordercolor="Black",
                        borderwidth=1,
                        font=dict(color="black", size=12)
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
            else:
                st.warning("Tidak ada data lokasi (latitude/longitude) untuk rentang tanggal yang dipilih.")
            
            st.markdown("---")

            col1, col2 = st.columns(2)
            
            # Crime by Location Category
            with col1:
                if not location_crime_data.empty:
                    location_totals = location_crime_data.groupby('location_category')['total_incidents'].sum().reset_index()
                    location_totals = location_totals.sort_values('total_incidents', ascending=False)

                    total_all = location_totals['total_incidents'].sum()
                    location_totals['percentage'] = (location_totals['total_incidents'] / total_all * 100).round(1)

                    hover_data = []
                    for _, row in location_totals.iterrows():
                        loc_cat = row['location_category']
                        incidents = row['total_incidents']

                        loc_crimes = location_crime_data[location_crime_data['location_category'] == loc_cat]
                        top_crime = loc_crimes.groupby('crime_category')['total_incidents'].sum().sort_values(ascending=False).head(1)
                        
                        if not top_crime.empty:
                            top_crime_name = top_crime.index[0]
                            top_crime_count = top_crime.iloc[0]
                            hover_text = f"{loc_cat}<br>Total: {incidents:,} kejadian<br>Jenis tertinggi: {top_crime_name}<br>({top_crime_count:,} kejadian)"
                        else:
                            hover_text = f"{loc_cat}<br>Total: {incidents:,} kejadian"
                        
                        hover_data.append(hover_text)

                    fig_donut = go.Figure(data=[go.Pie(
                        labels=location_totals['location_category'],
                        values=location_totals['total_incidents'],
                        hole=0.4,
                        hovertemplate='%{customdata}<extra></extra>',
                        customdata=hover_data,
                        textinfo='percent',
                        textposition='auto',
                        marker=dict(
                            colors=['#347433', '#FFC107', '#45B7D1', '#FF6F3C', '#B22222'],
                            line=dict(color='#FFFFFF', width=2)
                        )
                    )])
                    
                    fig_donut.update_layout(
                         title=dict(
                            text="Kejahatan per Kategori Lokasi",
                            font=dict(size=16)
                        ),
                        height=400,
                        showlegend=True,
                        legend=dict(
                            orientation="v",
                            yanchor="middle",
                            y=0.5,
                            xanchor="left",
                            x=1.05,
                            font=dict(size=10)
                        ),
                        margin=dict(l=20, r=20, t=20, b=20)
                    )
                    
                    st.plotly_chart(fig_donut, use_container_width=True)
                else:
                    st.warning("Tidak ada data untuk chart kategori lokasi.")
            
            # Lokasi Kejahatan Tertinggi
            with col2:                          
                if not top_locations_data.empty:
                    location_desc_totals = top_locations_data.groupby(['location_description', 'location_category']).agg({
                        'total_incidents': 'sum'
                    }).reset_index()

                    location_desc_totals = location_desc_totals.sort_values('total_incidents', ascending=False).head(5)

                    hover_data = []
                    for _, row in location_desc_totals.iterrows():
                        loc_desc = row['location_description']
                        loc_cat = row['location_category']
                        incidents = row['total_incidents']

                        loc_crimes = top_locations_data[top_locations_data['location_description'] == loc_desc]
                        top_crime = loc_crimes.groupby('crime_category')['total_incidents'].sum().sort_values(ascending=False).head(1)
                        
                        if not top_crime.empty:
                            top_crime_name = top_crime.index[0]
                            top_crime_count = top_crime.iloc[0]
                            hover_text = f"{loc_desc}<br>Kategori: {loc_cat}<br>Total: {incidents:,} kejadian<br>Jenis tertinggi: {top_crime_name}<br>({top_crime_count:,} kejadian)"
                        else:
                            hover_text = f"{loc_desc}<br>Kategori: {loc_cat}<br>Total: {incidents:,} kejadian"
                        
                        hover_data.append(hover_text)

                    max_value = location_desc_totals['total_incidents'].max()
                    y_max = max_value * 1.15  

                    fig_bar = go.Figure(data=[go.Bar(
                        x=[desc[:15] + '...' if len(desc) > 15 else desc for desc in location_desc_totals['location_description']],
                        y=location_desc_totals['total_incidents'],
                        marker=dict(
                            color=['#347433', '#FFC107', '#45B7D1', '#FF6F3C', '#B22222'],
                            line=dict(color='#FFFFFF', width=1)
                        ),
                        hovertemplate='%{customdata}<extra></extra>',
                        customdata=hover_data,
                        text=location_desc_totals['total_incidents'],
                        textposition='outside'
                    )])
                    
                    fig_bar.update_layout(
                        title=dict(
                            text="Lokasi Kejahatan Tertinggi",
                            font=dict(size=16),
                            x=0.5
                        ),
                        height=400,
                        xaxis_title="Lokasi",
                        yaxis_title="Jumlah Kejadian",
                        margin=dict(l=20, r=20, t=50, b=100),
                        xaxis=dict(
                            tickangle=45,
                            tickmode='array',
                            tickvals=list(range(len(location_desc_totals))),
                            ticktext=[desc[:15] + '...' if len(desc) > 15 else desc for desc in location_desc_totals['location_description']]
                        ),
                        yaxis=dict(
                            range=[0, y_max] 
                        )
                    )
                    
                    st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.warning("Tidak ada data untuk chart top lokasi.")
            
            st.markdown("---")
            
            # Tabel Detail Kejahatan per Area
            st.markdown("#### Detail Kejahatan per Area")

            col1, col2 = st.columns(2)
            
            with col1:
                location_categories = get_location_categories()
                selected_location_category = st.selectbox(
                    "Pilih Kategori Area:",
                    options=location_categories,
                    index=0
                )
            
            with col2:
                crime_categories = get_crime_categories()
                selected_crime_category = st.selectbox(
                    "Pilih Kategori Kejahatan:",
                    options=crime_categories,
                    index=0
                )

            crime_details = get_crime_details_by_date_range(
                start_date, 
                end_date, 
                selected_location_category, 
                selected_crime_category
            )
            
            if not crime_details.empty:
                display_data = crime_details.copy()

                display_data['Tanggal'] = display_data.apply(
                    lambda row: f"{row['day']:02d}-{row['month']:02d}-{row['year']}", 
                    axis=1
                )
                
                display_data['Waktu'] = display_data['daytime']
                
                display_data['Status Penangkapan'] = display_data['arrest_status'].map({
                    True: '✅ Ditangkap',
                    False: '❌ Tidak Ditangkap'
                })

                final_display = display_data[['location_description', 'primary_type', 'crime_description', 'Tanggal', 'Waktu', 'Status Penangkapan']].copy()
                final_display = final_display.rename(columns={
                    'location_description': 'Lokasi',
                    'primary_type': 'Jenis Kejahatan',
                    'crime_description': 'Deskripsi Kejahatan'
                })
                
                st.dataframe(
                    final_display,
                    use_container_width=True,
                    height=400,
                    hide_index=True
                )

                st.markdown("##### Statistik Ringkasan")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    all_filters_selected = (
                        selected_location_category == "Semua Area" and 
                        selected_crime_category == "Semua Kategori"
                    )
                    
                    if all_filters_selected:
                        filtered_total_incidents = total_cases
                        label_text = "Total Kejadian"
                    else:
                        filtered_total_incidents = get_filtered_total_incidents_geographic(
                            start_date, end_date,
                            selected_location_category if selected_location_category != "Semua Area" else None,
                            selected_crime_category if selected_crime_category != "Semua Kategori" else None
                        )
                        label_text = "Total Kejadian (Terfilter)"
                    
                    st.markdown(f"""
                        <div style="
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            color: white;
                            padding: 20px;
                            border-radius: 10px;
                            text-align: center;
                            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                            margin: 10px 0;
                        ">
                            <div style="font-size: 24px; font-weight: bold; margin-bottom: 5px;">
                                {filtered_total_incidents:,}
                            </div>
                            <div style="font-size: 14px; opacity: 0.9;">
                                {label_text}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    arrest_rate = (crime_details['arrest_status'] == True).mean() * 100
                    st.markdown(f"""
                        <div style="
                            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                            color: white;
                            padding: 20px;
                            border-radius: 10px;
                            text-align: center;
                            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                            margin: 10px 0;
                        ">
                            <div style="font-size: 24px; font-weight: bold; margin-bottom: 5px;">
                                {arrest_rate:.1f}%
                            </div>
                            <div style="font-size: 14px; opacity: 0.9;">
                                Tingkat Penangkapan
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    unique_crimes = display_data['primary_type'].nunique()
                    st.markdown(f"""
                        <div style="
                            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                            color: white;
                            padding: 20px;
                            border-radius: 10px;
                            text-align: center;
                            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                            margin: 10px 0;
                        ">
                            <div style="font-size: 24px; font-weight: bold; margin-bottom: 5px;">
                                {unique_crimes:,}
                            </div>
                            <div style="font-size: 14px; opacity: 0.9;">
                                Jenis Kejahatan Unik
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                if all_filters_selected:
                    st.info(f"📊 **Status:** Menampilkan semua {total_cases:,} kasus dalam rentang waktu yang dipilih")
                else:
                    if filtered_total_incidents > 0:
                        percentage = (filtered_total_incidents/total_cases*100) if total_cases > 0 else 0
                        st.info(f"📊 **Perbandingan:** Dari total {total_cases:,} kasus, terdapat {filtered_total_incidents:,} kasus yang sesuai dengan filter yang dipilih ({percentage:.1f}% dari total)")
                    else:
                        st.warning(f"📊 **Tidak ada data:** Tidak ditemukan kasus yang sesuai dengan filter yang dipilih dari total {total_cases:,} kasus")
                       
            else:
                st.warning("Tidak ada data kejahatan untuk kategori area dan rentang tanggal yang dipilih.")
    else:
        st.warning("Silakan pilih rentang waktu yang valid (tanggal mulai dan tanggal akhir).")