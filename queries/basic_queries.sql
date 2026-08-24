--10 Basic Questions (Warm-up & Data Exploration)
--High-Value Location Identification: 
--1. Find all cities where the average account balance of customers exceeds $50,000, ordered from highest to lowest.
select b."City", round(CAST(AVG(b."Account_Balance") AS numeric),2) as avg_balance
from banking_data_enriched b
group by b."City" 
having round(CAST(AVG(b."Account_Balance") AS numeric),2)>50000;

--2. Credit Score Breakdown: 
--Count how many active customers fall into the "Excellent" credit category (Credit Score \(\ge \) 750).
SELECT 
    bde."Customer_Name", 
    bde."Credit_Score",
    CASE
        WHEN bde."Credit_Score" >= 750 THEN 'Excellent'
        WHEN bde."Credit_Score" >= 600 AND bde."Credit_Score" < 750 THEN 'Best'
        WHEN bde."Credit_Score" >= 500 AND bde."Credit_Score" < 600 THEN 'Good'
        ELSE 'Normal'
    END AS "Credit Category"
FROM banking_data_enriched bde;

select Count(*) as "Excellent_Customer_Count"  from banking_data_enriched bde 
where bde."Credit_Score" >=750;

--3. Loan Portfolio Volume: 
--Calculate the total amount of money currently disbursed across all "Active" home loans.
--select bde."Loan_Type", bde."Loan_Amount"  , bde."Loan_Status" 
select sum(bde."Loan_Amount") as total_active_amt_of_house_loan
from banking_data_enriched bde 
where bde."Loan_Type" ='Home' and bde."Loan_Status"  ='Active';

--4. Segment Penetration: 
--Find the total number of unique customers assigned to each customer_segment (e.g., Retail, Wealth, Corporate).
select bde."Customer_Segment",count(distinct bde."Customer_ID") as unique_customer
from banking_data_enriched bde 
group by bde."Customer_Segment" ;

--5. Digital Adoption Rate: 
--Calculate the percentage of total customers who are registered as either online_banking_users or mobile_banking_users.
with customers_count as(
	select 
	count( distinct case
		when "Online_Banking_Usage" ='Yes' or "Mobile_Banking_Usage" ='Yes'
		then "Customer_ID"
	end) as digital_customers,
	
	count( distinct "Customer_ID") as total_customers
	from banking_data_enriched  
)
select total_customers, digital_customers, round((digital_customers * 100.0/total_customers),2) as digital_adoption_rate
from customers_count;

--6. Demographic Filtering: 
--List the names and Account Type of all VIP customers living in the province of "Kathmandu" or "Lalitpur" who are over the age of 40.
select "Customer_Name" , "Account_Type", "Customer_Segment" , "City"  
from banking_data_enriched
where "Age" >40 
and "Customer_Segment" ='Vip' 
and "City" in ('Kathmandu', 'Lalitpur');

--7. Investment Risk Snapshot: 
--Find the maximum, minimum, and average investment amount for customers categorized under the "High Risk" segment.
--with investment_measures as(
select  
	max("Investment_Amount") as maximum_invest_amt, 
	min("Investment_Amount") as minimum_invest_amt, 
	avg("Investment_Amount") as avg_invest_amt
from banking_data_enriched
where "Risk_Category" ='High';

--8. New Account Volume: 
--Count how many new accounts were opened in the last quarter of the previous fiscal year, grouped by account_type.
select "Account_Type", count(distinct "Customer_ID")
from banking_data_enriched
where 
	"Account_Open_Date" >= '2026-04-16' and
	"Account_Open_Date" <= '2026-07-15'
group by "Account_Type";

--9. Churn Overview: 
--Calculate the absolute number and percentage of customers who have churned (is_churned = 1).
select 
	count(distinct case 
		when "Churn_Status" = 'Yes' then "Customer_ID"
	end )as churned_customers,
	count(distinct "Customer_ID") as total_customers,
	round((count(distinct case when "Churn_Status" ='Yes' then "Customer_ID" end)*100.0)/
	nullif(count(distinct "Customer_ID"),0),2) as churn_percentage
from banking_data_enriched;

--10. Transaction Outliers: 
--Retrieve the top 5 largest transaction amounts executed during the current year, along with the account_id and date.
select * from banking_data_enriched bde ;

select "Account_Number", "Date"
from banking_data_enriched;