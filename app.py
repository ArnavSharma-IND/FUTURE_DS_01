import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales Analytics Dashboard", layout="wide")

st.title("Sales Analytics Dashboard")

uploaded_file = st.file_uploader("C:/Users/Arnav Sharma/Desktop/Resume/Internship/Future Interns Data Science And Analytics/online_retail.csv", type=["csv"])

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')

    df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]

    df = df.dropna(subset=['CustomerID'])

    df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]

    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

    df['Revenue'] = df['Quantity'] * df['UnitPrice']

    df['Year'] = df['InvoiceDate'].dt.year
    df['Month'] = df['InvoiceDate'].dt.strftime('%b')

    st.sidebar.header("Filters")

    countries = st.sidebar.multiselect(
        "Select Country",
        options=df['Country'].unique(),
        default=df['Country'].unique()
    )

    years = st.sidebar.multiselect(
        "Select Year",
        options=sorted(df['Year'].unique()),
        default=sorted(df['Year'].unique())
    )

    filtered_df = df[
        (df['Country'].isin(countries)) &
        (df['Year'].isin(years))
    ]

    total_revenue = filtered_df['Revenue'].sum()
    total_orders = filtered_df['InvoiceNo'].nunique()
    total_customers = filtered_df['CustomerID'].nunique()
    total_quantity = filtered_df['Quantity'].sum()
    avg_order_value = total_revenue / total_orders if total_orders else 0

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(" Revenue", f"£{total_revenue:,.0f}")
    col2.metric(" Orders", f"{total_orders:,}")
    col3.metric(" Customers", f"{total_customers:,}")
    col4.metric(" Quantity", f"{total_quantity:,}")
    col5.metric(" Avg Order", f"£{avg_order_value:,.2f}")

    st.markdown("---")

    monthly_sales = filtered_df.groupby(
        pd.Grouper(key='InvoiceDate', freq='M')
    )['Revenue'].sum().reset_index()

    fig1 = px.line(
        monthly_sales,
        x='InvoiceDate',
        y='Revenue',
        title='Revenue Over Time'
    )

    st.plotly_chart(fig1, use_container_width=True)

    top_products = (
        filtered_df.groupby('Description')['Revenue']
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig2 = px.bar(
        top_products,
        x='Revenue',
        y='Description',
        orientation='h',
        title='Top 10 Products by Revenue'
    )

    st.plotly_chart(fig2, use_container_width=True)

    country_sales = (
        filtered_df.groupby('Country')['Revenue']
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig3 = px.bar(
        country_sales,
        x='Country',
        y='Revenue',
        title='Top Countries by Revenue'
    )

    st.plotly_chart(fig3, use_container_width=True)

    fig4 = px.pie(
        country_sales,
        names='Country',
        values='Revenue',
        title='Revenue Share by Country'
    )

    st.plotly_chart(fig4, use_container_width=True)

    top_customers = (
        filtered_df.groupby('CustomerID')['Revenue']
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    st.subheader("🏆 Top Customers")

    st.dataframe(top_customers)

    csv = filtered_df.to_csv(index=False).encode('utf-8')

    st.download_button(
        "⬇ Download Cleaned Data",
        csv,
        "cleaned_sales_data.csv",
        "text/csv"
    )

else:
    st.info("Upload your Online Retail CSV file to begin.")