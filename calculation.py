import math

def calculate_loan(salary, interests, loan_period, dsr_ratio, saving_money):

    salary = int(salary)
    dsr_ratio = float(dsr_ratio)
    avbl_money_month = salary*dsr_ratio/100/12

    interests = float(interests)/100
    interets_month = interests/12

    loan_period = int(loan_period)
    period_month = loan_period*12
    saving_money = int(saving_money)

    #########원리금 균등########
    num1 = interets_month*(interets_month+1)**period_month
    num2 = (1+interets_month)**period_month-1
    wonli_result = round(avbl_money_month*num2/num1,-2)

    #원리금 일반
    max_price1 = round(wonli_result * 10/7,-2)
    need_money1 = max_price1 - wonli_result
    more_need_money1 = need_money1- saving_money
    wonli_70 = cal_result(wonli_result,max_price1,need_money1,more_need_money1)

    #원리금 생초
    max_price1_1 = round(wonli_result * 10/8,-2)
    need_money1_1 = max_price1_1 - wonli_result
    more_need_money1_1 = need_money1_1- saving_money
    wonli_80 = cal_result(wonli_result,max_price1_1,need_money1_1,more_need_money1_1)

    #########원금 균등########
    num3 = period_month*avbl_money_month*12
    num4 = 6*(period_month*interets_month+interets_month+2)
    wonkum_result = round(num3/num4,-2)

    #원리금 일반
    max_price2 = round(wonkum_result * 10/7,-2)
    need_money2 = max_price2 - wonkum_result
    more_need_money2 = need_money2- saving_money
    wonkum_70 = cal_result(wonkum_result,max_price2,need_money2,more_need_money2)

    #원리금 생초
    max_price2_2 = round(wonkum_result * 10/8,-2)
    need_money2_2 = max_price2_2 - wonkum_result
    more_need_money2_2 = need_money2_2- saving_money
    wonkum_80 = cal_result(wonkum_result,max_price2_2,need_money2_2,more_need_money2_2)

    return wonli_70,wonli_80,wonkum_70,wonkum_80

class cal_result:
    def __init__(self,result,max_price,need_money,more_need_money):
        self._result = format(int(result),',d')
        self._max_price = format(int(max_price),',d')
        self._need_money = format(int(need_money),',d')
        self._more_need_money = format(int(more_need_money),',d')

def calculate_monthpay(monthpay, interests, loan_period, saving_money):

    interests = float(interests)/100
    interets_month = interests/12

    loan_period = int(loan_period)
    period_month = loan_period*12
    saving_money = int(saving_money)

    ########원리금균등########
    num1 = interets_month*(interets_month+1)**period_month
    num2 = (1+interets_month)**period_month-1
    wonli_result = round(monthpay*num2/num1,-2)

    #원리금균등 일반
    max_price1 = round(wonli_result * 10/7,-2)
    need_money1 = max_price1 - wonli_result
    more_need_money1 = need_money1- saving_money
    wonli_70 = cal_result(wonli_result,max_price1,need_money1,more_need_money1)


    #원리금균등 생초    
    max_price1_1 = round(wonli_result * 10/8,-2)
    need_money1_1 = max_price1_1 - wonli_result
    more_need_money1_1 = need_money1_1- saving_money
    wonli_80 = cal_result(wonli_result,max_price1_1,need_money1_1,more_need_money1_1)


    #########원금균등########
    num3 = period_month*monthpay*12
    num4 = 6*(period_month*interets_month+interets_month+2)
    wonkum_result = round(num3/num4,-2)
    
    #원금균등일반
    max_price2 = round(wonkum_result * 10/7,-2)
    need_money2 = max_price2 - wonkum_result
    more_need_money2 = need_money2- saving_money
    wonkum_70 = cal_result(wonkum_result,max_price2,need_money2,more_need_money2)
    

    #원금균등생초
    max_price2_2 = round(wonkum_result * 10/8,-2)
    need_money2_2 = max_price2 - wonkum_result
    more_need_money2_2 = need_money2_2- saving_money
    wonkum_80 = cal_result(wonkum_result,max_price2_2,need_money2_2,more_need_money2_2)

    return wonli_70,wonli_80,wonkum_70,wonkum_80
