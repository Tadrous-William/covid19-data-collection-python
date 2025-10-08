# 🦠 Automated COVID-19 Data Collection (2022–2024) Using Python

This project automates the process of collecting and cleaning daily **COVID-19 data** for **15 countries** from **January 2022 to December 2024**.  
Data is fetched from the **Our World in Data (OWID)** COVID-19 dataset and exported as a clean CSV file ready for analysis or visualization.

---

## 📊 Objectives
- Collect daily COVID-19 data for 15 selected countries  
- Include key indicators:
  - New Cases  
  - New Deaths  
  - Total Vaccinations  
  - Stringency Index  
- Handle missing values using forward fill and interpolation  
- Export the final cleaned dataset to CSV format

---

## ⚙️ Tools & Technologies
- **Python** (pandas, requests)
- **Jupyter Notebook / VS Code**
- **Data Source:** [Our World in Data COVID-19 Dataset](https://ourworldindata.org/covid-data)
- **Output Format:** CSV

---

## 🧩 Data Pipeline
1. Retrieve dataset from OWID API  
2. Filter for 15 selected countries  
3. Clean and handle missing values  
4. Format date range (2022–2024)  
5. Export results to CSV  


