SELECT * FROM sqlpython3.expense;
      ##1total amount spent on each category
SELECT Category, SUM(Amount)
FROM sqlpython3.expense
GROUP BY Category;
      ##2total amount spent using each payment mode 
SELECT payment_mode, SUM(Amount)
FROM sqlpython3.expense
GROUP BY payment_mode;
      ##3 the total cashback received across all transactions
SELECT  sum(Cashback)
FROM sqlpython3.expense;
      ## 4 Which are the top 5 most expensive categories in terms of spending?
SELECT Category, SUM(Amount) AS Total_Spending
FROM sqlpython3.expense
GROUP BY Category
ORDER BY Total_Spending DESC
LIMIT 5;
     ## 5 How much was spent on transportation using different payment modes?
SELECT Payment_Mode, SUM(Amount) AS Total_Spent
FROM sqlpython3.expense
WHERE Category = 'transport'
GROUP BY Payment_Mode;
     ## 6 Which transactions resulted in cashback?
SELECT *  
FROM sqlpython3.expense  
WHERE Cashback > 0;
     ## 7 What is the total spending in each month of the year?
SELECT MONTH(Date) AS Month, SUM(Amount) AS Total_Spending
FROM sqlpython3.expense
GROUP BY MONTH(Date)
ORDER BY Month;
    ##8 Which months have the highest spending in categories like "investment", "subscription" or "stationary"?
    SELECT MONTH(Date) AS Month, Category, SUM(Amount) AS Total_Spending
FROM sqlpython3.expense
WHERE Category IN ("investment", "subscription" or "stationary")
GROUP BY MONTH(Date), Category
ORDER BY Total_Spending DESC;
    ## 9 Are there any recurring expenses that occur during specific months of the year ('investment', 'subscription',"fees")?
SELECT MONTH(Date) AS Month, Category, COUNT(*) AS Occurrences, SUM(Amount) AS Total_Spending
FROM sqlpython3.expense
WHERE Category IN ('investment', 'subscription',"fees" ) 
GROUP BY MONTH(Date), Category
ORDER BY Month, Category;
   ## 10 How much cashback or rewards were earned in each month?
SELECT MONTH(Date) AS Month, SUM(Cashback) AS Total_Cashback
FROM sqlpython3.expense
GROUP BY MONTH(Date)
ORDER BY Month; 
    ## 11 How has your overall spending changed over time (e.g., increasing, decreasing, remaining stable)?
SELECT YEAR(Date) AS Year, MONTH(Date) AS Month, SUM(Amount) AS Total_Spending
FROM sqlpython3.expense
GROUP BY YEAR(Date), MONTH(Date)
ORDER BY Year, Month; 
  ## 12 Are there any patterns in grocery spending (e.g., higher spending on weekends, increased spending during specific seasons)?
SELECT DAYNAME(Date) AS Day, SUM(Amount) AS Total_Spending, COUNT(*) AS Transactions
FROM sqlpython3.expense
WHERE Category = 'sports & fitness'
GROUP BY Day
ORDER BY FIELD(Day, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday');
    ## 13 Define High and Low Priority Categories
SELECT 
    Category, 
    SUM(Amount) AS Total_Spending,
    CASE 
        WHEN Category IN ('investment', 'transport', 'stationary', 'sports & fitness', 'fees') 
        THEN 'High Priority'
        WHEN Category IN ('subscription') 
        THEN 'Low Priority'
        ELSE 'Uncategorized'
    END AS Priority_Level
FROM sqlpython3.expense
GROUP BY Category, Priority_Level
ORDER BY Priority_Level DESC, Total_Spending DESC;
   ## 14  Which category contributes the highest percentage of the total spending?
SELECT 
    Category, 
    SUM(Amount) AS Total_Spending, 
    (SUM(Amount) / (SELECT SUM(Amount) FROM sqlpython3.expense) * 100) AS Percentage_Contribution
FROM sqlpython3.expense
GROUP BY Category
ORDER BY Total_Spending DESC
LIMIT 1;
     ## 15 amount greater than 400
use sqlpython3;
select * from expense where Amount > 400;
  ## 16 data where  amount > 400 and payment_mode="debit card"
select * from expense where Amount > 400 and payment_mode="debit card"; 
    ## 17  data where category ="fees" and  payment_mode="debit card"
select * from expense where category ="fees" and  payment_mode="debit card"; 
    ## 18 data where there are some categories 
select category from expense where description="cricket" group by category having Amount > 600 order by category desc;
     ## 19  year wise total spending
select year(date) as year ,sum(Amount) as total_spending
from sqlpython3.expense
group by year(date)
order by year;
use sqlpython3;
      ## 20 Total amount spent (excluding refunds):
SELECT SUM(Amount - cashback) AS total_spent FROM expense;
  ## 21 Total amount spent on 'netflix subscription':
SELECT SUM(Amount) AS total_netflix
FROM expense
WHERE description LIKE '%netflix subscription%'; 
  #22 Average spending per day:
SELECT AVG(daily_total) AS average_daily_spending FROM (
  SELECT date, SUM(Amount - Cashback) AS daily_total
  FROM expense
  GROUP BY date
) AS daily_data;
   ## 23 Total spent on 'pen and pencil':
SELECT SUM(Amount - Cashback) AS total_stationary
FROM expense
WHERE description LIKE '%pen and pencil%';
   ## 24 Days with spending over ₹2000:
SELECT date, SUM(Amount -Cashback) AS total_spent
FROM expense
GROUP BY date
HAVING SUM(Amount -Cashback) > 2000;
   ## 25 Number of transactions per category:
SELECT category, COUNT(*) AS transaction_count
FROM expense
GROUP BY Category;




