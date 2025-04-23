# Marketing Performance Report for SpaceOutfitters (03/2025)

## Executive Summary
* Overall churn risk rate: 0.12%
* Churn risk rates by Education:
Basic           0.125
Graduate        0.105
High School     0.115
PhD             0.135
Postgraduate    0.095
dtype: float64
* Churn risk rates by Marital Status:
Divorced     0.130
Married      0.100
Separated    0.140
Single       0.110
Widow        0.120
dtype: float64
* Number of at-risk customers by Education and Marital Status:
Education     Marital  
Basic        Divorced     10
             Married       8
             Separated     6
             Single        4
             Widow        12
Graduate     Divorced      8
             Married       6
             Separated     4
             Single        6
             Widow         2
High School  Divorced     12
             Married       8
             Separated     6
             Single        8
             Widow         4
PhD          Divorced     14
             Married       6
             Separated    10
             Single        8
             Widow         6
Postgraduate Divorced     10
             Married       8
             Separated     8
             Single        6
             Widow         4
dtype: int64

## Churn Risk Identification Methodology
### Methodology
* Used Recency and Complain columns to identify high-risk customers.
* Applied threshold of 90 days for Recency.

## Churn Risk Rates Overall and by Segment
### Methodology
* Calculated overall churn risk rate by dividing the number of high-risk customers by the total number of customers.
* Segmented churn risk rates by Education and Marital Status using groupby operations.

## At-Risk Customer Profile Summary
### Methodology
* Identified at-risk customers based on Recency and Complain columns.
* Summarized at-risk customer profiles by Education and Marital Status.

## Retention Strategy Recommendations
### Methodology
* Recommended retention strategies based on the analysis of at-risk customers.
* Suggested targeting customers with Recency > 90 days and those who have lodged complaints with personalized retention strategies.