import streamlit as st
import pandas as pd
from datasets import load_dataset

# Загрузка датасетов с Hugging Face
benchmark_dataset = load_dataset("evilfreelancer/msnp-tests", split="train")
# server_dataset = load_dataset("evilfreelancer/msnp-servers", split="train")

# Преобразование в DataFrame
df_benchmark = pd.DataFrame(benchmark_dataset)
df_server = pd.read_csv('server_specs.csv')

# Объединение данных по названию сервера
df = pd.merge(df_benchmark, df_server, left_on="Server Name", right_on="Server Name", how="left")

st.title("Лидерборд производительности моделей")

# Фильтры в боковой панели
with st.sidebar:
    st.header("Фильтры")
    model_options = st.multiselect("Выберите модель:", options=df["Model"].unique())
    gpu_options = st.multiselect("Выберите GPU:", options=df["GPUs"].unique())
    quantization_options = st.multiselect("Квантование:", options=df["Quantization"].unique())
    context_length_options = st.multiselect("Длина контекста:", options=sorted(df["Context Length"].unique()))
    start_type_options = st.multiselect("Тип запуска:", options=df["Start Type"].unique())
    power_options = st.multiselect("Макс. мощность GPU (Вт):", options=df["GPU Max Power (W)"].unique())
    server_options = st.multiselect("Выберите сервер:", options=df["Server Name"].unique())

# Применение фильтров
filtered_df = df.copy()
if model_options:
    filtered_df = filtered_df[filtered_df["Model"].isin(model_options)]
if gpu_options:
    filtered_df = filtered_df[filtered_df["GPUs"].isin(gpu_options)]
if quantization_options:
    filtered_df = filtered_df[filtered_df["Quantization"].isin(quantization_options)]
if context_length_options:
    filtered_df = filtered_df[filtered_df["Context Length"].isin(context_length_options)]
if start_type_options:
    filtered_df = filtered_df[filtered_df["Start Type"].isin(start_type_options)]
if power_options:
    filtered_df = filtered_df[filtered_df["GPU Max Power (W)"].isin(power_options)]
if server_options:
    filtered_df = filtered_df[filtered_df["Server Name"].isin(server_options)]

# Опции сортировки
st.header("Опции сортировки")
sort_by = st.selectbox(
    "Сортировать по:",
    options=filtered_df.columns,
    index=filtered_df.columns.get_loc("Duration (sec)")
)
ascending = st.radio("Порядок:", ("Возрастание", "Убывание")) == "Возрастание"

# Отображение таблицы
st.dataframe(filtered_df.sort_values(by=sort_by, ascending=ascending).reset_index(drop=True))

# Добавление ссылок на тесты
st.markdown("## Примечания")
st.markdown("Нажмите на ссылки в колонке 'Test Link' для подробностей.")

# Отображение спецификаций сервера при выборе записи
if st.checkbox("Показать спецификации сервера"):
    selected_index = st.number_input(
        "Введите номер записи для просмотра спецификаций сервера:",
        min_value=0,
        max_value=len(filtered_df)-1,
        value=0,
        step=1
    )
    selected_server = filtered_df.iloc[selected_index]["Server Name"]
    server_specs = df_server[df_server["Server Name"] == selected_server]
    if not server_specs.empty:
        st.subheader(f"Спецификации сервера: {selected_server}")
        st.table(server_specs.drop(columns=["Server Name"]).transpose())
    else:
        st.write("Спецификации для выбранного сервера недоступны.")
