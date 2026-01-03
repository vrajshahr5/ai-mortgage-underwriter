# credit_score: 300-850
# loan_amount:  500000-1000000
# property_value: loan amount - 2000000
# monthly_income: 30000-500000
# monthly_debt: 0-50000
# employment_status: employed/unemployed

# Default risk increases when:
# credit_score: < 600
# ltv > 0.8
# Dti > 0.4
# unemployed

import random
import pandas as pd

def generate_synthetic_data(n_samples:int):
    data = []
    for _ in range(n_samples):
        credit_score = random.randint(300,850)
        loan_amount = random.randint(200000,500000)
        property_value = loan_amount + random.randint(50000,2000000)
        monthly_income = random.randint(5000,10000)
        monthly_debt = random.randint(0,50000)
        employment_status = random.choice(['employed','unemployed'])

        ltv = loan_amount / property_value
        dti = monthly_debt / monthly_income


        increase_risk = 0
        if credit_score < 600:
            increase_risk += 1
        if ltv > 0.8:
            increase_risk += 1
        if dti > 0.4:
            increase_risk += 1
        if employment_status == 'unemployed':
            increase_risk += 1

        if increase_risk >=2:
            default_risk = 1
        else:
            default_risk = 0

        data.append({
            'credit_score': credit_score,
            'loan_amount': loan_amount,
            'property_value': property_value,
            'monthly_income': monthly_income,
            'monthly_debt': monthly_debt,
            'employment_status': employment_status,
            'default_risk': default_risk
        })
        
    return pd.DataFrame(data)



    



        

        

        

        
    




    

    


    


    







