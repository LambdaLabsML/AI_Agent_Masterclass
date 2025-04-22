# Customer Retention and Churn Risk Report

## Executive Summary
* The overall churn risk rate is 24.49%
* Customers with higher education (PhD, Postgraduate, Graduate) have a churn risk rate of 23.08%, 20.00%, and 25.00% respectively.
* Customers with different marital statuses have varying churn risk rates.
* 24.49% of customers are at risk of churning.

## Churn Risk Identification Methodology
* Customers with Recency > 90 days are flagged as high risk.
* Customers who have lodged a complaint (Complain = 1) are flagged as high risk.
* Overall Churn Risk is calculated by combining the above two conditions.

## Churn Risk Rates Overall and by Segment
* Overall Churn Risk Rate: 24.49%
Education|Churn_Risk
PhD|0.23076923076923078
Graduate|0.25
Postgraduate|0.2
Basic|0.24444444444444444
High School|0.25
Marital|Churn_Risk
Single|0.25
Married|0.2
Divorced|0.2727272727272727
Separated|0.25
Widow|0.22222222222222222

## At-Risk Customer Profile Summary
* Number of at-risk customers: 24
* At-risk customers have an average Recency of 73.33 days.
* At-risk customers have an average Income of 94491.19.

## Retention Strategy Recommendations
* Offer loyalty programs to customers with high Recency values.
* Improve customer service to reduce complaints.
* Targeted marketing campaigns towards customers with higher education and different marital statuses.

### Methodology
* The churn risk is identified based on Recency and Complain variables.
* Churn risk rates are calculated for overall customers and by Education and Marital Status.
* At-risk customer profiles are identified based on the churn risk flag.