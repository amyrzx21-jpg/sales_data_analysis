# %%
# Exploratory Data Analysis
# Import Library
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
# Exploratory Data Analysis
# Cleaning Data
df = pd.read_csv('sales_data.csv')
df['unit_price'] = df["unit_price"].fillna(df['unit_price'].shift(1) + df['unit_price'].shift(-1))/2
df['region'] = df['region'].fillna("unknown")
df["category"] = df['category'].str.capitalize()
df['order_date'] = pd.to_datetime(df['order_date'])
df = df.drop_duplicates()

# Basic Data Exploration
print("Data Shape:",df.shape)
print("\n Data Types:",df.dtypes)
print("\n Missing Values:")
print(df.isnull().sum())
print("\n Descriptive Statistics")
print(df.describe())
#Formatting Helper
def format_revenue(x):
    if x >= 1_000_000_000:
        return f"{x/1_000_000_000:.2f}B"
    elif x >= 1_000_000:
        return f"{x/1_000_000:.2f}M"
    else:
        return f"{x:.0f}"
    
# Total Sales by Category 
category_sales = df.groupby('category')["total_price"].sum().sort_values(ascending=False)
print(category_sales)

# Category Sales Chart
def millions(count, pos):
    return f"{count/1_000_000:.0f}M"

plt.figure(figsize=(10, 6))
plt.bar(category_sales.index , category_sales.values)
plt.title("Total Sales by Category")
plt.xlabel("Category")
plt.ylabel("Total Sales")
plt.grid(axis="y" , alpha= 0.30)
plt.gca().yaxis.set_major_formatter(FuncFormatter(millions))
plt.tight_layout()

# %%
# Category Analysis
result = df.groupby("category").agg({"total_price":["sum","mean"], "order_id":["count"]})
result.columns=["Total sales","Average purchase","order"]
result = result.reset_index()
print(result)

# %%
# Avrage Phurchase by Category
avg_category = df.groupby("category")["total_price"].mean()
plt.figure(figsize=(10 , 6))
bars = plt.bar(avg_category.index , avg_category.values)

plt.bar_label(bars , fmt="%.0f")
plt.title("Avrage Phurchase by Category")
plt.xlabel("Category")
plt.ylabel("Average Purchase")
plt.grid(axis="y" , alpha=0.3)
plt.tight_layout()

# %%
# Produt Performance
product_performance = df.groupby("product").agg(total_sales=('total_price','sum'),total_quantity=("quantity",'sum'),
                                                avg_unit_price=("unit_price",'mean')).sort_values("total_sales",ascending=False)


product_performance["total_sales_display"] = product_performance['total_sales'].apply(format_revenue)
product_performance['avg_unit_display'] = product_performance['avg_unit_price'].apply(format_revenue)
top_revenue = product_performance.sort_values('total_sales',ascending=False)
print(top_revenue[["total_sales_display","total_quantity","avg_unit_display"]].head(10))

# %%
# Best Sales Day
check_order = df.groupby('order_date')["total_price"].sum()
best_day = check_order.idxmax()
best_sale = check_order.max()
print(best_day,best_sale)


# %%
# Daily Sales Trend
check_order = df.groupby("order_date")["total_price"].sum().reset_index()
check_order.columns = ["order date","total sales"]

def millions(count,position):
    return f"{count/1_000_000:.0f}M"

plt.figure(figsize=(12, 6))
plt.plot(check_order["order date"],check_order["total sales"])
plt.title('Daily Sales Trend')
plt.xlabel('Order Date')
plt.xticks(check_order["order date"][::14],rotation = 45 )
plt.ylabel('Total Sales')
plt.grid(alpha= 0.3)

plt.gca().yaxis.set_major_formatter(FuncFormatter(millions))
plt.tight_layout()
 
# %%
# Region Analysis & Region Chart
region_payment = df.groupby("region")['total_price'].sum()

def million(count , pos):
    return f"{count/1_000_000:.0f}M"

plt.figure(figsize=(9,6))
bars = plt.bar(region_payment.index , region_payment.values)
label =[ f"{values/1_000_000:.0f}M"
        for values in region_payment.values]
plt.title('Total Sales by Region')
plt.xlabel("Category")
plt.ylabel('Total Sales')
plt.bar_label(bars, labels= label)
plt.gca().yaxis.set_major_formatter(FuncFormatter(million))
plt.grid(axis="y" , alpha=0.3)
plt.tight_layout()
# %%
# Sales by Category & Region Chart
def million (count,pos):
   return f"{count/1_000_000:.0f}  M"
category_region_sales = df.groupby(["category", "region"])["total_price"].sum().unstack()

category_region_sales.plot(kind= "bar",stacked=True ,figsize=(12 ,6))

plt.title("Sales by Category & Region")
plt.xlabel("Category")
plt.ylabel("Total Sales")
plt.xticks(rotation = 0)
plt.gca().yaxis.set_major_formatter(FuncFormatter(million))
plt.grid(axis="y", alpha= 0.4)
plt.tight_layout()
# %%
# Sales By Category & Region Heatmap
category_region_sales = df.groupby(["category", "region"])["total_price"].sum().unstack()

annot = (category_region_sales / 1_000_000).round(0).astype(int).astype(str)+"M"  

plt.figure(figsize=(12 , 6))

sns.heatmap(category_region_sales/1_000_000, annot=annot, fmt="", cbar_kws={"label":"sales(million)"})

plt.title("Sales by Category & Region")
plt.xlabel("Region")
plt.ylabel("Category")
plt.xticks(rotation = 0)
plt.tight_layout()
# %%

#Sales by Day of Week
df["order_date"] = pd.to_datetime(df["order_date"])
df["day_name"] = df['order_date'].dt.day_name()
day_sales = df.groupby("day_name")['total_price'].sum()
def million (count , pos):
    return f"{count/1_000_000}M"

label = [f"{values/1_000_000:.0f}M"
         for values in day_sales.values]

plt.figure(figsize=(10 ,6))
bars = plt.bar(day_sales.index , day_sales.values)
plt.title("sales by day of week")
plt.xlabel("day of week")
plt.ylabel('total_sales') 
plt.bar_label(bars ,labels= label)
plt.gca().yaxis.set_major_formatter(FuncFormatter(million))
plt.grid(axis="y" , alpha= 0.3)
plt.tight_layout()

# %%
# Quantity vs Total Price Correlation
plt.figure(figsize=(10,6))
plt.scatter(df['quantity'],df['total_price'],alpha=0.5)
plt.title("Quantity vs Total Price")
plt.xlabel("Quantity")
plt.ylabel("Total Price")
plt.grid(alpha=0.3)
plt.tight_layout()
correlation = df['quantity'].corr(df['total_price'])
print(correlation)

# %%
# Distribution Total Sales with Histogram
plt.figure(figsize=(12, 6))
plt.hist(df['total_price'] , bins=30, alpha= 0.8, edgecolor="black")
plt.title("Distribution of Total Price",fontsize=14)
plt.xlabel("Total Price")
plt.ylabel("Number of Order")
plt.grid(axis="y",alpha=0.4)
plt.tight_layout()

# %%
# Total Price Destributiob with Boxplot
fig , ax = plt.subplots(figsize=(12,4))

total_sell= df['total_price'].dropna()

ax.boxplot(total_sell,orientation= "horizontal")

ax.set_title("distribution for total price")
ax.set_xlabel("total price")
plt.tight_layout()

# %%
# Tatal Sales Quantile & Outlier Analysis
q1 = df['total_price'].quantile(0.25)
q3 = df['total_price'].quantile(0.75)
iqr = q3 - q1

lower_bound= q1 - 1.5* iqr
upper_bound = q3 + 1.5* iqr
outliers = df[(df["total_price"] < lower_bound) | (df['total_price'] > upper_bound)]
print(outliers['category'].value_counts())
print(outliers['product'].value_counts())

# %%
# Monthly Performance
daily_sales = df.groupby("order_date", as_index=False)["total_price"].sum().sort_values(by="total_price",ascending=False).head(10)
monthly_sales = df.groupby(df["order_date"].dt.to_period("M"))["total_price"].sum()
monthly_sales = monthly_sales.reset_index()
monthly_sales.columns = ["month","total_price"]

fig , ax = plt.subplots(figsize=(12, 5))
ax.plot(monthly_sales["month"].astype(str),monthly_sales["total_price"],marker = "o")
ax.set_title ("Monthly Sales Trend")
ax.set_xlabel("Month")
ax.set_ylabel("Total Sales")

plt.xticks(rotation= 45)
plt.tight_layout()

complete_month = monthly_sales[monthly_sales["month"].astype(str)<"2026-07"]

best_month = complete_month.loc[complete_month['total_price'].idxmax()]
worst_month = complete_month.loc[complete_month["total_price"].idxmin()]
print("Best Month: ")
print(best_month)
print("worst Month: ")
print(worst_month)

# %%
# Payment Performance
payment_performance = df.groupby("payment_method").agg(total_sale = ("total_price","sum"),
                                                       total_order = ("order_id","count"),
                                                       avg_order_value= ("total_price","mean")
                                                       ).sort_values(by="total_sale", ascending=False)

payment_performance["avg_order_value_display"] = payment_performance["avg_order_value"].apply(format_revenue)
payment_performance["total_sale_display"] = payment_performance["total_sale"].apply(format_revenue)

plt.figure(figsize=(12,6))
plt.bar(payment_performance.index , payment_performance['total_sale'])
plt.title("Payment Method Sales")
plt.xlabel("payment method")
plt.ylabel("total sales")
plt.tight_layout()

# %%
# Region Performance
region_performance = df.groupby("region").agg(total_sale= ("total_price","sum"),
                                              total_order= ("order_id","count"),
                                              total_quantity= ("quantity","sum")).sort_values(by="total_sale",ascending=False)

region_performance["total_sale_display"] = region_performance["total_sale"].apply(format_revenue)
print(region_performance[["total_sale_display","total_order","total_quantity"]])

plt.figure(figsize=(10 ,6))
plt.bar(region_performance.index,region_performance["total_sale"])
plt.title("Total Sales By Region")
plt.xlabel("Region")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.tight_layout()

# %%
# Exploratory Data Analysis
# Customer Performance
customer_performance = df.groupby("customer_id").agg(total_spent = ("total_price","sum"),
                                                     total_orders = ("order_id","count"))
    
customer_performance["total_spent_display"] = customer_performance["total_spent"].apply(format_revenue)
top_customers = (customer_performance.sort_values(by="total_spent",ascending=False).head(10))

plt.figure(figsize=(13,6))
plt.bar(top_customers.index.astype(str),top_customers['total_spent'])
plt.title("TOP 10 CUSTOMERS BY TOTAL SPENT")
plt.xlabel("Customer ID")
plt.ylabel("Total Spnet")
plt.tight_layout()

#%% [markdown]
# Business Insights
#
# ## Category Performance
# Electronics generated thr highest total sales revenue among the categories.
#
# ## Product Performance
# Laptop was top-performing product by total sales, generating approximately 1.79B in revenue.
#
# ## Quantity & Revenue
# The correlation between quantity & total price was approximately 0.25, indicating that quantity alone does not strongly explain revenue.
# 
# ## Monthly Performance
# Among the complete month, the fifth month has highest total sales, while the second month had the lowest.
# 
# ## Sales by Day
# Monday had the highest sales, while sunday had the lowest sales.
#
# ## Outlier Analysis
# The IQR method was used to identift unusual total-price transactions.
#
# ## Category & Region
# Sales performance varied across categories and region, highlighting areas that may deserve futher business attention.