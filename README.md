# ds3870_final_project
Final Project for DS3870 - Used Car Sales

Data for this project was acceses from Kaggle usign a KPI to creat a local filepath. 
https://www.kaggle.com/datasets/tunguz/used-car-auction-prices/data

Description of the data: Where it came from, how it was collected (if you know), what the important/interesting features are, etc…
    The dataset comes from Kaggle, and the author noted that it was privately scraped from online. The dataset has more than 500,000 records, but they are not all fully populated. The interesting features are MMR, selling price, vehicle year, and VIN. MMR (Manheim Market Report) is a value that estimates the wholesale pricing of vehicles, using Canadian and US datasets. It is updated nightly. 


Some questions we wanted to answer include: 
- What causes the difference between the MMR and the final auction selling price? 
- Is it related to seller, make, model, trim, etc.
- Which makes/models/trim levels hold their value the best?
- Do certain sellers do better? (less depreciation vs. avg) 
- In which locations (rust belt) is car condition more or less important to buyers?
- Which cars more closely follow MMR (based on mileage count, condition, brand, etc)

Methods/graphs we plan on creating for the project
- Sale price of individual models over time (year) (Sale price vs. MMR)
- Model that investigates which variables are the most accurate at predicting auctioned price 
- LASSO would be useful for investigating which features are important for selling price, and the delta from MMR.
- Scatterplot Mileage vs. MMR/Sale Price
- Heatmap of where cars sell where sales price is greater than MMR

