**Issues observed in raw data**

1. Location is missing in nearly one third of all rows, roughly three thousand two hundred rows out of ten thousand. That is a very large gap in what should be a simple two value field.

2. Payment method is missing in over a quarter of all rows, roughly two thousand five hundred rows out of ten thousand. Combined with location, this means a huge portion of transactions cannot be properly categorized.

3. Quantity, price per unit, and total spent are all being stored as text rather than numbers. This happens because the literal word error appears scattered inside these columns, and a single non numeric value is enough to force the entire column to be read as text.

4. The words unknown and error appear as if they were legitimate categories inside payment method and location, rather than being treated as missing data.

5. In transaction date specifically, the word unknown is actually the single most frequently occurring value in the entire column, appearing more often than any real calendar date.

**Something to  note.** Transaction ID has no missing values and no duplicates across all ten thousand rows, so it does not need attention going into next week's cleaning work.