from argparse import ArgumentParser
import sys


def get_min_payment(balance, fees):
    """Gets arguments from the remaning_payments function or the main function and performs calculations on arguments. Returns values 
    to remaning_payments or main functions
    Args:
        balance, fees
    Returns:
        min_payment
    """
    
    percent_balance = 0.02

    # Performs an operation to get the min_payment value
    min_payment = ((balance * percent_balance) + fees)

    # Checks the min_payment value. if it does not meet the threshold the value is updated
    if min_payment < 25:
        min_payment = 25
        return (min_payment)
    elif min_payment >= 25:
        return(min_payment)
    
def interest_charged(b, a):
    """Gets arguments from the remaining_payments function and performs a calculation on arguments.Returns arguments to main function
    Args:
        b, a
    Returns:
        i
    """
    
    y = 365
    d = 30
    a *= .01
    
    # Performs operation to get interest
    i = (a/y)*b*d

    # Returns value
    return(i)

def remaining_payments(balance, apr, targetamount = 5000, credit_line = None, fees = 0):
    """Gets arguments from the main function and values from calling the get_min_payment function and the interest charged function.
    Performs calculations until balance = 0 then returns values to the main function
    Args:
        balance, apr, targetamount, credit_line, fees
    Returns:
        i, twenty_five, fifty, seventy_five
    """
    
    # Counters set to count number of times loop runs
    i = 0 
    seventy_five = 0
    fifty = 0
    twenty_five = 0
    
    min_payment = 0 
    
    # Loop runs for as long as the balance is positive
    while balance > 0:
        
        if targetamount is None:
            min_payment = get_min_payment(balance, fees)
        else:
            min_payment = targetamount
        
        total_payment = (min_payment - interest_charged(balance, apr))

        if total_payment < 0:
            return("Card balance cannot be paid off.")
        
        # Balance is updated
        balance -=total_payment
            
        # Counters are updated

        if balance > (0.75 * credit_line):
            seventy_five += 1
        if balance > (0.5 * credit_line):
            fifty += 1
        if balance > (0.25 * credit_line):
            twenty_five += 1
        i += 1
    # Values are returned
    return(i, twenty_five, fifty, seventy_five)

def main(balance, apr, credit_line = 5000, targetamount = None, fees = 0):
    """Gets arguments from parse_args function. Calls other functions to perfrom operations. Eventually returns infromation to user
    Args:
        balance, apr, credit_line, targetamount, fees
    Returns:
        balance, apr, credit_line, targetamount, fees
    """
    
    # Calls get_min_payment for recommend_payment
    recommend_payment = get_min_payment(balance, fees)

    print(f"Your recommended starting minimum payment is ${recommend_payment}")

    pays_minimum = False
    
    # Calls remaining_payments
    remaining_payments(balance, apr, targetamount, credit_line, fees)
    
    if targetamount is None:
        pays_minimum = True
        print(f"If you pay the minimum payments each month, you will pay off the balance in {remaining_payments(balance, apr, targetamount, credit_line, fees)[0]} payments.")
    elif targetamount < recommend_payment:
        print("Your target payment is less than the minimum payment for this credit card")
    else:
        if pays_minimum == True:
            print(f"If you pay the minimum payments each month, you will pay off the balance in {remaining_payments(balance, apr, targetamount, credit_line, fees)[0]} payments.")
        elif pays_minimum == False:
            print(f"If you make payments of ${int(recommend_payment)}, you will pay off the balance in {remaining_payments(balance, apr, targetamount, credit_line, fees)[0]} payments.")
            
    # Returns information to user
    return(f"You will spend a total of {remaining_payments(balance, apr, targetamount, credit_line, fees)[1]} months over 25% of the credit line \nYou will spend a total of {remaining_payments(balance, apr, targetamount, credit_line, fees)[2]} months over 50% of the credit line \nYou will spend a total of {remaining_payments(balance, apr, targetamount, credit_line, fees)[3]} months over 75% of the credit line")
    



def parse_args(args_list):
    """Takes a list of strings from the command prompt and passes them through as
    arguments
    Args:
        args_list (list) : the list of strings from the command prompt
    Returns:
        args (ArgumentParser)
    """
    parser = ArgumentParser()
    parser.add_argument('balance_amount', type = float, help = 'The total amount of balance left on the credit account')
    parser.add_argument('apr', type = int, help = 'The annual APR, should be an int between 1 and 100')
    parser.add_argument('credit_line', type = int, help = 'The maximum amount of balance allowed on the credit line.')
    parser.add_argument('--payment', type = int, default = None, help = 'The amount the user wants to pay per payment, should be a positive number')
    parser.add_argument('--fees', type = float, default = 0, help = 'The fees that are applied monthly.')
    # parse and validate arguments
    args = parser.parse_args(args_list)
    if args.balance_amount < 0:
        raise ValueError("balance amount must be positive")
    if not 0 <= args.apr <= 100:
        raise ValueError("APR must be between 0 and 100")
    if args.credit_line < 1:
        raise ValueError("credit line must be positive")
    if args.payment is not None and args.payment < 0:
        raise ValueError("number of payments per year must be positive")
    if args.fees < 0:
        raise ValueError("fees must be positive")
    return args

if __name__ == "__main__":
    try:
        arguments = parse_args(sys.argv[1:])
    except ValueError as e:
        sys.exit(str(e))
    print(main(arguments.balance_amount, arguments.apr, credit_line = arguments.credit_line, targetamount = arguments.payment, fees = arguments.fees))