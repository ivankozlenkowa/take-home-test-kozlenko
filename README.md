# Python take-home-test

Expose an API for querying salary data:

- The goal of this exercise is to design a read-only API (REST) that returns one or more records from the provided dataset
- Don't worry about any web application concerns other than serializing JSON and returning via a GET request.
- Filter by one or more fields/attributes (e.g. /compensation_data?salary[gte]=120000&primary_location=Portland)
- Sort by one or more fields/attributes (e.g. /compensation_data?sort=salary)
- Extra: return a sparse fieldset (e.g. /compensation_data?fields=first_name,last_name,salary)

# Install and run
1. Create [virtual environment](https://docs.python.org/3/library/venv.html)
2. Install dependencies: ```pip install -r requirments.txt```
3. Run tests: ```pytest tests.py```
4. Run: ```uvicorn main:app```

# API Parameters
*GET /compensation_data/columns/* - returns list of available columns

*GET /compensation_data/* - return data based on parameters provided (all parameters are optional)
 - "fields" - use to pass a list of comma-separated column names returned (case sensitive!); use endpoint *GET /compensation_data/columns/* to get exact column names
 - "sort" - pass one or more column names to sort by (column names are case sensitive), ASC by default
 - filter parameters: provided in format <column_name>[<operator>]
 -- supported operators: "gt", "gte", "lt" , "lte", "ne" (not equals to) ,"eq" (equals to)
 -- range comparison operators ("gt", "gte", "lt" , "lte") are only available for numeric and date columns
 -- example: find records with "Timestamp" < "01/01/2024": ```Timestamp[lt]=01/01/2024```

# Example requests
### Get available column names
request ```curl 'localhost:8000/compensation_data/columns/'```
response: 
```json 
[
    "Timestamp",
    "Employment Type",
    "Company Name",
    "Company Size - # Employees",
    "Primary Location (Country)",
    "Primary Location (City)",
    "Industry in Company",
    "Public or Private Company",
    "Years Experience in Industry",
    "Years of Experience in Current Company  ",
    "Job Title In Company",
    "Job Ladder",
    "Job Level",
    "Required Hours Per Week",
    "Actual Hours Per Week",
    "Highest Level of Formal Education Completed",
    "Total Base Salary in 2018 (in USD)",
    "Total Bonus in 2018 (cumulative annual value in USD)",
    "Total Stock Options/Equity in 2018 (cumulative annual value in USD)",
    "Health Insurance Offered",
    "Annual Vacation (in Weeks)",
    "Are you happy at your current position?",
    "Do you plan to resign in the next 12 months?",
    "What are your thoughts about the direction of your industry?",
    "Gender",
    "Final Question: What are the top skills (you define what that means) that you believe will be necessary for job growth in your industry over the next 10 years?",
    "Have you ever done a bootcamp? If so was it worth it?"
]
```
### Get data without filters
request ```curl 'localhost:8000/compensation_data/'```
response (only the first two records shown):
```json
[
    {
        "Timestamp": "2019-09-11T01:57:44",
        "Employment Type": "Full-time",
        "Company Name": "Army IT",
        "Company Size - # Employees": "1-19",
        "Primary Location (Country)": "United States (US)",
        "Primary Location (City)": "Fort Campbell",
        "Industry in Company": "IT",
        "Public or Private Company": "Military",
        "Years Experience in Industry": "2-5",
        "Years of Experience in Current Company  ": "0-2",
        "Job Title In Company": "IT Specialist ",
        "Job Ladder": "Newtork Admin",
        "Job Level": "1 (I)",
        "Required Hours Per Week": "40+",
        "Actual Hours Per Week": "50-69",
        "Highest Level of Formal Education Completed": "High School",
        "Total Base Salary in 2018 (in USD)": 24000.0,
        "Total Bonus in 2018 (cumulative annual value in USD)": 0.0,
        "Total Stock Options/Equity in 2018 (cumulative annual value in USD)": 0.0,
        "Health Insurance Offered": "Yes",
        "Annual Vacation (in Weeks)": "6+",
        "Are you happy at your current position?": "No",
        "Do you plan to resign in the next 12 months?": "Yes",
        "What are your thoughts about the direction of your industry?": "I can't do shit. Contractors do all the work and i just usually help people out with the simplest things. Mostly user caused. Ex: Changing PDFs from explorer to Adobe. Cable not plugged in.",
        "Gender": "Male",
        "Final Question: What are the top skills (you define what that means) that you believe will be necessary for job growth in your industry over the next 10 years?": "Networking with CISCO products and encryption devices.",
        "Have you ever done a bootcamp? If so was it worth it?": "No - never did one"
    },
    {
        "Timestamp": "2019-09-11T02:11:42",
        "Employment Type": "Full-time",
        "Company Name": "Costco Wholesale",
        "Company Size - # Employees": "100,000+",
        "Primary Location (Country)": "United States (US)",
        "Primary Location (City)": "Seattle (Issaquah)",
        "Industry in Company": "Retail",
        "Public or Private Company": "Public",
        "Years Experience in Industry": "2-5",
        "Years of Experience in Current Company  ": "10-20",
        "Job Title In Company": "Network Support Analyst I",
        "Job Ladder": "Newtork Admin",
        "Job Level": "1 (I)",
        "Required Hours Per Week": "40+",
        "Actual Hours Per Week": "50-69",
        "Highest Level of Formal Education Completed": "High School",
        "Total Base Salary in 2018 (in USD)": 57000.0,
        "Total Bonus in 2018 (cumulative annual value in USD)": 0.0,
        "Total Stock Options/Equity in 2018 (cumulative annual value in USD)": 0.0,
        "Health Insurance Offered": "Yes",
        "Annual Vacation (in Weeks)": "4",
        "Are you happy at your current position?": "It's Complicated",
        "Do you plan to resign in the next 12 months?": "Yes",
        "What are your thoughts about the direction of your industry?": "The direction of my industry is widely seen as great. As for the company, unfortunately we are understaffed in many people's opinion. 13 on 24x7/365 support. Multiple Jobs rolled into one position. Projects being rolled out without proper knowledge and support from design side. Business side dictates what is needed with no input from IT side. Relegated to the Business side principles while a tenured cashier is paid (with their bi-yearly Bonuses) more than an analyst at IT. ",
        "Gender": "Male",
        "Final Question: What are the top skills (you define what that means) that you believe will be necessary for job growth in your industry over the next 10 years?": "Network Automation (Ansible), Python, Certifications",
        "Have you ever done a bootcamp? If so was it worth it?": "No - never did one"
    }
]
```
### Data with filters
request:
 - select "Timestamp", "Employment Type", "Company Name", "Total Base Salary in 2018 (in USD)"
 - where "Total Base Salary in 2018 (in USD)" <= 24000
 - and "Timestamp" > "2019-09-11T05:24:53"
 - order by "Company Name" ASC
```
curl 'localhost:8000/compensation_data/?fields=Timestamp%2CEmployment+Type%2CCompany+Name%2CTotal+Base+Salary+in+2018+%28in+USD%29&Total+Base+Salary+in+2018+%28in+USD%29%5Blte%5D=24000&Timestamp%5Bgt%5D=2019-09-11T05%3A24%3A53&sort=Company+Name'
```
response
```json
[
    {
        "Timestamp": "2019-09-11T11:06:01",
        "Employment Type": "Full-time", 
        "Company Name": "Abc123",
        "Total Base Salary in 2018 (in USD)": 46.0
    },
    {
        "Timestamp": "2019-09-11T22:39:36",
        "Employment Type": "Full-time",
        "Company Name": "NDA",
        "Total Base Salary in 2018 (in USD)": 14500.0},
    {
        "Timestamp": "2019-09-20T10:25:07", 
        "Employment Type": "Full-time",
        "Company Name": "Opti Ltd",
        "Total Base Salary in 2018 (in USD)": 22600.0
    }
]
```
