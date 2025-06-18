import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
from data.time_trends_data import (
    get_total_cases_by_date_range,
    get_risky_time_by_date_range,
    get_risky_day_by_date_range,
    get_risky_month_by_date_range,
    get_crime_by_time_of_day,
    get_crime_by_day_of_week,
    get_crime_by_month,
    get_crime_category_by_daytime,
    get_crime_category_by_weekday,
    get_crime_category_by_month,
    get_crime_detail_table,
    get_months_list,
    get_weekdays_list,
    get_daytime_list,
    get_crime_categories_list,
    get_filtered_total_incidents 
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
            risky_time_data = get_risky_time_by_date_range(start_date, end_date)
            risky_day_data = get_risky_day_by_date_range(start_date, end_date)
            risky_month_data = get_risky_month_by_date_range(start_date, end_date)
            df_time_of_day = get_crime_by_time_of_day(start_date, end_date)
            df_days_of_week = get_crime_by_day_of_week(start_date, end_date)
            df_crime_by_month = get_crime_by_month(start_date, end_date)
            
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
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div class="metric-container">
                        <div class="metric-title">
                            <i class="fa-solid fa-clock white-icon"></i>
                            <span>Risky Time</span>
                            <div class="tooltip">
                                <span class="tooltip-icon"></span>
                                <span class="tooltiptext">Waktu dengan kejahatan tertinggi</span>
                            </div>
                        </div>
                       <div class="metric-value">{risky_time_data['daytime']}</div>
                        <div class="metric-delta">
                            <i class="fas fa-arrow-up metric-delta-arrow"></i>
                            <span>{risky_time_data['total_incidents']:,} Cases</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)    
            
            with col3:
                st.markdown(f"""
                    <div class="metric-container">
                        <div class="metric-title">
                            <i class="fa-solid fa-cloud-sun white-icon"></i>
                            <span>Risky Day</span>
                            <div class="tooltip">
                                <span class="tooltip-icon"></span>
                                <span class="tooltiptext">Hari dengan kejahatan tertinggi</span>
                            </div>
                        </div>
                        <div class="metric-value">{risky_day_data['weekday']}</div>
                        <div class="metric-delta">
                            <i class="fas fa-arrow-up metric-delta-arrow"></i>
                            <span>{risky_day_data['total_incidents']:,} Cases</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                    <div class="metric-container">
                        <div class="metric-title">
                            <i class="fas fa-calendar-alt white-icon"></i>
                            <span>Risky Month</span>
                            <div class="tooltip">
                                <span class="tooltip-icon"></span>
                                <span class="tooltiptext">Bulan dengan kejahatan tertinggi</span>
                            </div>
                        </div>
                        <div class="metric-value">{risky_month_data['month_name']}</div>
                        <div class="metric-delta">
                            <i class="fas fa-arrow-up metric-delta-arrow"></i>
                            <span>{risky_month_data['total_incidents']:,} Cases</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)

            with col1:
                if not df_time_of_day.empty:
                    time_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
                    
                    fig_time = px.pie(
                        df_time_of_day, 
                        names='daytime', 
                        values='total_cases', 
                        title='Crime Distribution by Time of Day',
                        hole=0.3,
                        color_discrete_sequence=time_colors
                    )
                    fig_time.update_traces(textinfo='percent+label')
                    fig_time.update_layout(
                        showlegend=True,
                        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.01)
                    )
                    st.plotly_chart(fig_time, use_container_width=True)
                else:
                    st.warning("No data available for the selected date range")

            with col2:
                if not df_days_of_week.empty:
                    alternating_colors = ['#8979FF', '#FFFFFF', '#8979FF', '#FFFFFF', '#8979FF', '#FFFFFF', '#8979FF']
                    
                    fig_day = px.bar(
                        df_days_of_week, 
                        x='weekday', 
                        y='total_incidents', 
                        title='Crime by Day of the Week'
                    )
                    fig_day.update_traces(
                        marker=dict(
                            color=alternating_colors[:len(df_days_of_week)],
                            line=dict(color='#8979FF', width=2),  
                            opacity=0.8
                        )
                    )
                    fig_day.update_layout(
                        xaxis_title="Day of Week",
                        yaxis_title="Total Incidents",
                        xaxis={'categoryorder': 'array'}
                    )
                    st.plotly_chart(fig_day, use_container_width=True)
                else:
                    st.warning("No data available for the selected date range")

            st.markdown("---")
            
            if not df_crime_by_month.empty:
                fig_month = px.line(
                    df_crime_by_month, 
                    x='month_name', 
                    y='total_incidents', 
                    title='Crime Trends by Month',
                    markers=True
                )
                fig_month.update_layout(
                    xaxis_title="Month",
                    yaxis_title="Total Incidents"
                )
                fig_month.update_traces(
                    line=dict(color='#8979FF', width=3),
                    marker=dict(size=8, color='#8979FF')
                )
                st.plotly_chart(fig_month, use_container_width=True)
            else:
                st.warning("No data available for the selected date range")

            st.markdown("---")
            st.markdown("#### Perbandingan Per Kategori Kejahatan")

            tab1, tab2, tab3 = st.tabs(["🕒 Berdasarkan Waktu", "☀️ Berdasarkan Hari", "🗓️ Berdasarkan Bulan"])
            
            with tab1:
                # Crime Category by Daytime
                df_category_daytime = get_crime_category_by_daytime(start_date, end_date)
                
                if not df_category_daytime.empty:
                    fig_category_daytime = px.bar(
                        df_category_daytime,
                        x='daytime',
                        y='total_incidents',
                        color='crime_category',
                        title='Distribusi Kategori Kejahatan berdasarkan Waktu',
                        barmode='group',
                        color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
                    )
                    fig_category_daytime.update_layout(
                        xaxis_title="Waktu",
                        yaxis_title="Total Kejadian",
                        legend_title="Kategori Kejahatan",
                        xaxis={'categoryorder': 'array', 'categoryarray': ['Dini hari', 'Pagi', 'Siang', 'Sore', 'Malam']}
                    )
                    st.plotly_chart(fig_category_daytime, use_container_width=True)
                else:
                    st.warning("No data available for crime category by daytime")

            with tab2:
                # Weekday
                df_category_weekday = get_crime_category_by_weekday(start_date, end_date)
                
                if not df_category_weekday.empty:
                    fig_category_weekday = px.bar(
                        df_category_weekday,
                        x='weekday',
                        y='total_incidents',
                        color='crime_category',
                        title='Distribusi Kategori Kejahatan berdasarkan Hari',
                        barmode='group',
                        color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
                    )
                    fig_category_weekday.update_layout(
                        xaxis_title="Hari",
                        yaxis_title="Total Kejadian",
                        legend_title="Kategori Kejahatan",
                        xaxis={'categoryorder': 'array', 'categoryarray': ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']}
                    )
                    st.plotly_chart(fig_category_weekday, use_container_width=True)
                else:
                    st.warning("No data available for crime category by weekday")

            with tab3:
                # Month
                df_category_month = get_crime_category_by_month(start_date, end_date)
                
                if not df_category_month.empty:
                    fig_category_month = px.bar(
                        df_category_month,
                        x='month_name',
                        y='total_incidents',
                        color='crime_category',
                        title='Distribusi Kategori Kejahatan berdasarkan Bulan',
                        barmode='group',
                        color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
                    )
                    fig_category_month.update_layout(
                        xaxis_title="Bulan",
                        yaxis_title="Total Kejadian",
                        legend_title="Kategori Kejahatan",
                        xaxis={'categoryorder': 'array', 'categoryarray': ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']}
                    )
                    st.plotly_chart(fig_category_month, use_container_width=True)
                else:
                    st.warning("No data available for crime category by month")

            # Tabel Crime Detail
            st.markdown("---")
            st.markdown("#### Detail Kejahatan per Waktu")

            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                months_list = get_months_list()
                selected_month = st.selectbox(
                    "Pilih Bulan:",
                    options=["Semua"] + months_list,
                    index=0
                )
            
            with col2:
                weekdays_list = get_weekdays_list()
                selected_weekday = st.selectbox(
                    "Pilih Hari:",
                    options=["Semua"] + weekdays_list,
                    index=0
                )
            
            with col3:
                daytime_list = get_daytime_list()
                selected_daytime = st.selectbox(
                    "Pilih Waktu:",
                    options=["Semua"] + daytime_list,
                    index=0
                )
            
            with col4:
                crime_categories_list = get_crime_categories_list()
                selected_crime_category = st.selectbox(
                    "Pilih Kategori Kejahatan:",
                    options=["Semua"] + crime_categories_list,
                    index=0
                )

            crime_detail_data = get_crime_detail_table(
                start_date, 
                end_date,
                selected_month if selected_month != "Semua" else None,
                selected_weekday if selected_weekday != "Semua" else None,
                selected_daytime if selected_daytime != "Semua" else None,
                selected_crime_category if selected_crime_category != "Semua" else None
            )
            
            if not crime_detail_data.empty:
                display_data = crime_detail_data.copy()
                
                display_data['Status Penangkapan'] = display_data['arrest_status'].map({
                    True: '✅ Ditangkap',
                    False: '❌ Tidak Ditangkap'
                })
                
                final_display = display_data[[
                    'location_category', 'location_description', 'primary_type', 
                    'description', 'Status Penangkapan'
                ]].copy()
                
                final_display = final_display.rename(columns={
                    'location_category': 'Kategori Area',
                    'location_description': 'Lokasi',
                    'primary_type': 'Jenis Kejahatan',
                    'description': 'Deskripsi Kejahatan'
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
                        selected_month == "Semua" and 
                        selected_weekday == "Semua" and 
                        selected_daytime == "Semua" and 
                        selected_crime_category == "Semua"
                    )
                    
                    if all_filters_selected:
                        filtered_total_incidents = total_cases
                        label_text = "Total Kejadian"
                    else:
                        filtered_total_incidents = get_filtered_total_incidents(
                            start_date, end_date,
                            selected_month if selected_month != "Semua" else None,
                            selected_weekday if selected_weekday != "Semua" else None,
                            selected_daytime if selected_daytime != "Semua" else None,
                            selected_crime_category if selected_crime_category != "Semua" else None
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
                    arrest_rate = (crime_detail_data['arrest_status'] == True).mean() * 100 if not crime_detail_data.empty else 0
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
                    unique_crimes = display_data['primary_type'].nunique() if not display_data.empty else 0
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

                if not all_filters_selected and filtered_total_incidents != total_cases:
                    st.info(f"📊 **Perbandingan:** Dari total {total_cases:,} kasus, terdapat {filtered_total_incidents:,} kasus yang sesuai dengan filter yang dipilih ({(filtered_total_incidents/total_cases*100):.1f}% dari total)")
                elif all_filters_selected:
                    st.info(f"📊 **Status:** Menampilkan semua {total_cases:,} kasus dalam rentang waktu yang dipilih")
                
            else:
                st.warning("Tidak ada data yang tersedia untuk filter yang dipilih")

    else:
        st.warning("Silakan pilih rentang waktu yang valid (tanggal mulai dan tanggal akhir).")