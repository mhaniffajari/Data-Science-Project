# Credit-Risk-Modeling
 a credit lending company has a number of creditors who defaulted as much as 4969 or 8% of the total creditors. The total loss incurred by the company as a result of the loan was $2,704,876,771. As Data scientist, I have task to mitigate the default creditors. Machine learning can predict a target with train dataset. By that ability, I created model to predict score applicants from their repayment capability.

Train dataset have 54050 credit applicant.  before that, train dataset have filtered with approved. Test dataset set have 13008 credit applicant. 

Loan model with logistic regression algorithm has 66% AUC, 91.8% accuracy and no overfitting indication. Model can predict score of applicant based on their repayment capability. Applicant separated split a decile based on their score.

Applicant with Decile 1-4 high risk default probability. I recommended to rejected applicant with decile 1. Decile 2-4 can bring them with high interest rate. Decile 5-7 have medium risk category. We can bring medium interest rate to them. Decile 8-10 have low risk category. We can bring low interest rate and higher credit limit

Based on distribution applicant from test dataset, 40% of applicant have high risk probability. Financial institutions must selective to approved credit applicant. Given approprite interest rate or credit limit can help financial Financial institutions to migate loss.
