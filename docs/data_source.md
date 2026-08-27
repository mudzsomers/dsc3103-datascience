# Data Source Classification

## Type of data
This is **structured data**. It is stored as a CSV file where every row
has the same fixed set of 8 columns. Even though many values are missing
or contain error placeholders, the schema itself does not vary between
rows — this is what distinguishes structured data from semi-structured
data like JSON, where the fields can differ per record.

## Variables
- Transaction ID — unique identifier for each sale
- Item — the product sold (e.g. Coffee, Cake, Salad, Sandwich)
- Quantity — number of units purchased in the transaction
- Price Per Unit — price of one unit of the item
- Total Spent — total amount paid for the transaction
- Payment Method — how the customer paid (Cash, Credit Card, Digital Wallet)
- Location — where the sale happened (Takeaway or In-store)
- Transaction Date — the date the transaction occurred

## Target and features
- **Target:** Total Spent (if the goal is to predict sales revenue)
- **Candidate features:** Item, Quantity, Price Per Unit, Payment Method,
  Location, Transaction Date