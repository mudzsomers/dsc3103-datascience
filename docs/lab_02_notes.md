# Lab 2 Notes

I rejected rows with negative prices, invalid dates, duplicate rows, and
duplicate IDs since these values were nonsensical and unrecoverable, but
imputed missing market values with "Unknown" since a missing market is
plausible rather than impossible, and normalized commodity casing since
"MAIZE"/"Maize" clearly represent the same real-world entity. I
distinguished an outlier from an error by checking whether a value was
physically possible: a price of -2000 is impossible, so it is treated as
an error rather than a genuine extreme value, whereas a very high but
positive price would be a legitimate outlier. If this cleaned data were
later used for a prediction task, leakage would occur if any information
about the target (price) that would only be available after the fact was
included as a feature, or if cleaning decisions such as imputing "Unknown"
were derived using information from a test set rather than applied
consistently and independently of any train/test split.