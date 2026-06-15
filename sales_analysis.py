import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("C:/Users/Arnav Sharma/Desktop/Resume/Internship/Future Interns Data Science And Analytics/online_retail.csv", encoding='ISO-8859-1')

df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]

df = df.dropna(subset=['CustomerID'])

df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]

df['Revenue'] = df['Quantity'] * df['UnitPrice']

df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

df['Year'] = df['InvoiceDate'].dt.year
df['Month'] = df['InvoiceDate'].dt.month_name()

print("Cleaned Dataset Shape:", df.shape)


total_revenue = df['Revenue'].sum()
total_orders = df['InvoiceNo'].nunique()
total_customers = df['CustomerID'].nunique()
total_quantity = df['Quantity'].sum()
avg_order_value = total_revenue / total_orders

print("\n===== KPI SUMMARY =====")
print(f"Total Revenue: £{total_revenue:,.2f}")
print(f"Total Orders: {total_orders}")
print(f"Total Customers: {total_customers}")
print(f"Total Quantity Sold: {total_quantity}")
print(f"Average Order Value: £{avg_order_value:,.2f}")


monthly_sales = df.groupby(
    pd.Grouper(key='InvoiceDate', freq='M')
)['Revenue'].sum()

plt.figure(figsize=(12,6))
monthly_sales.plot(marker='o')
plt.title("Revenue Over Time")
plt.xlabel("Date")
plt.ylabel("Revenue")
plt.grid()
plt.show()


top_products = df.groupby('Description')['Revenue'] \
                 .sum() \
                 .sort_values(ascending=False) \
                 .head(10)

plt.figure(figsize=(10,6))
top_products.sort_values().plot(kind='barh')
plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue")
plt.show()


country_sales = df.groupby('Country')['Revenue'] \
                  .sum() \
                  .sort_values(ascending=False) \
                  .head(10)

plt.figure(figsize=(10,6))
country_sales.plot(kind='bar')
plt.title("Top Countries by Revenue")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.show()


top_customers = df.groupby('CustomerID')['Revenue'] \
                  .sum() \
                  .sort_values(ascending=False) \
                  .head(10)

print("\nTop 10 Customers:")
print(top_customers)

df.to_csv("cleaned_sales_data.csv", index=False)

print("\nAnalysis completed successfully!")