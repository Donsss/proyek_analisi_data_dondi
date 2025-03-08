import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def hitung_total_penyewa_per_tahun(data, tahun):
    data['dteday'] = pd.to_datetime(data['dteday'])
    data['tahun'] = data['dteday'].dt.year
    total_penyewa = data[data['tahun'] == tahun]['cnt'].sum()
    return total_penyewa

def hitung_total_musim(data):
    season_df = data.groupby(by="season").agg({"cnt": "sum"}).reset_index()
    season_df.columns = ['Musim', 'Total'] 
    return season_df

def hitung_total_cuaca(data):
    weather_df = data.groupby(by="weathersit").agg({"cnt": "sum"}).reset_index()
    weather_df.columns = ['cuaca', 'Total'] 
    return weather_df

def hitung_total_penyewa(data):
    total_rentals = data[['casual', 'registered']].sum().reset_index()
    total_rentals.columns = ['Type', 'Count']
    return total_rentals

data = pd.read_csv('Dashboard/all_data.csv')

st.header('Bike Sharing Dashboard :bike:')
st.subheader('Tren Penyewa Sepeda')

total_sewa_2011 = hitung_total_penyewa_per_tahun(data, 2011)
total_sewa_2012 = hitung_total_penyewa_per_tahun(data, 2012)
musim_data = hitung_total_musim(data)
total_cuaca = hitung_total_cuaca(data)
total_penyewa = hitung_total_penyewa(data)

col1, col2 = st.columns(2)
with col1:
    st.metric("Total penyewa 2011", value=total_sewa_2011)
with col2:
    st.metric("Total Penyewa 2012", value=total_sewa_2012)


col1, col2 = st.columns(2)

with col1:
    data_2011 = data[data['dteday'].dt.year == 2011]

    bulan_2011 = data_2011.resample('M', on='dteday').agg({"cnt": "sum"})
    bulan_2011.index = bulan_2011.index.strftime('%B')
    bulan_2011 = bulan_2011.reset_index()

    plt.figure(figsize=(7, 5))
    plt.plot(bulan_2011["dteday"], bulan_2011["cnt"], marker='o', linewidth=2, color="#72BCD4")
    plt.title("Jumlah Penyewa Setiap Bulan (2011)", loc="center", fontsize=20)
    plt.xticks(fontsize=10, rotation=45)
    plt.yticks(fontsize=10)
    st.pyplot(plt)

with col2:
    data_2012 = data[data['dteday'].dt.year == 2012]

    bulan_2012 = data_2012.resample('M', on='dteday').agg({"cnt": "sum"})
    bulan_2012.index = bulan_2012.index.strftime('%B')
    bulan_2012 = bulan_2012.reset_index()

    plt.figure(figsize=(7, 5))
    plt.plot(bulan_2012["dteday"], bulan_2012["cnt"], marker='o', linewidth=2, color="#72BCD4")
    plt.title("Jumlah Penyewa Setiap Bulan (2012)", loc="center", fontsize=20)
    plt.xticks(fontsize=10, rotation=45)
    plt.yticks(fontsize=10)
    st.pyplot(plt)

st.subheader('Analisis Jumlah Penyewa Berdasarkan Musim')

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Musim Dingin", value=musim_data[musim_data['Musim'] == "Musim Dingin"]['Total'].values[0])
with col2:
    st.metric("Total Musim Gugur", value=musim_data[musim_data['Musim'] == "Musim Gugur"]['Total'].values[0])
with col3:
    st.metric("Total Musim Panas", value=musim_data[musim_data['Musim'] == "Musim Panas"]['Total'].values[0])
with col4:
    st.metric("Total Musim Semi", value=musim_data[musim_data['Musim'] == "Musim Semi"]['Total'].values[0])

season_df = data.groupby(by="season").agg({"cnt":"sum"})

colors = ["#D3D3D3", "#D3D3D3", "#72BCD4", "#D3D3D3"]

plt.figure(figsize=(6, 3))
sns.barplot(data=season_df, x='season', y='cnt', palette=colors, legend=False)
plt.title('Jumlah Penyewa Setiap Musim')
plt.ylabel(None)
plt.xlabel(None)
plt.xticks()
plt.show()
st.pyplot(plt)

st.subheader('Analisis Penyewa Berdasarkan Kondisi Cuaca')

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Saat Berawan :cloud:", value=total_cuaca[total_cuaca['cuaca'] == "Berawan"]['Total'].values[0])
with col2:
    st.metric("Total Saat Cerah :mostly_sunny:", value=total_cuaca[total_cuaca['cuaca'] == "Cerah"]['Total'].values[0])
with col3:
    st.metric("Total Saat Hujan :rain_cloud:", value=total_cuaca[total_cuaca['cuaca'] == "Hujan"]['Total'].values[0])

weather_df = data.groupby(by="weathersit").agg({"cnt": "sum"}).reset_index()

colors = ['#A0C4FF', '#B9FBC0', '#FFC3A0', '#FF677D']

plt.figure(figsize=(6, 3))
plt.pie(weather_df['cnt'], labels=weather_df['weathersit'], colors=colors,autopct='%1.1f%%', startangle=90)
plt.title('Persentase Banyak Penyewa Berdasarkan Cuaca')
plt.show()
st.pyplot(plt)

st.subheader('Analisis Penyewa Berdasarkan Casual dan Registered')

col1, col2 = st.columns(2)
with col1:
    st.metric("Total Casual :copyright:", value=total_penyewa[total_penyewa['Type'] == "casual"]['Count'].values[0])
with col2:
    st.metric("Total Registered :registered:", value=total_penyewa[total_penyewa['Type'] == "registered"]['Count'].values[0])

total_rentals = data[['casual', 'registered']].sum().reset_index()
total_rentals.columns = ['Type', 'Count']

colors = ["#D3D3D3", "#72BCD4"]

plt.figure(figsize=(6, 3))
plt.pie(total_rentals['Count'], labels=total_rentals['Type'], colors=colors, autopct='%1.1f%%', startangle=90)
plt.title('Persentase Jumlah Penyewaan Casual dan Registered') 
plt.show()
st.pyplot(plt)

st.subheader('Analisis Penyewa Berdasarkan Hari')

days_df = data.groupby(by="weekday").agg({"cnt":"sum"}).reset_index()

days_order = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
days_df['weekday'] = pd.Categorical(days_df['weekday'], categories=days_order, ordered=True)

colors = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3","#D3D3D3","#72BCD4", "#D3D3D3"]

plt.figure(figsize=(6, 3))
sns.barplot(data=days_df, x='cnt', y='weekday', palette=colors)
plt.title('Jumlah Penyewa Setiap Hari')
plt.xticks()  
plt.xlabel(None)
plt.ylabel(None)
plt.show()
st.pyplot(plt)

st.caption('Copyright :copyright: Dondi Setiawan')
