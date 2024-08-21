
import argparse
from pyfinops.sip_calculator import SIPCalculator
from pyfinops.compound_interest_calculator import CompoundInterestCalculator


def sip_calculator():
    """CLI for SIP Calculator"""
    parser = argparse.ArgumentParser(description="Calculate the future value of a SIP investment.")
    parser.add_argument("--monthly-investment", type=float, required=True, help="Monthly investment amount")
    parser.add_argument("--annual-rate", type=float, required=True, help="Annual interest rate (percentage)")
    parser.add_argument("--years", type=int, required=True, help="Investment duration in years")

    args = parser.parse_args()

    sip = SIPCalculator(args.monthly_investment, args.annual_rate, args.years)
    future_value = sip.calculate_future_value()

    print(f"Future Value of SIP: ${future_value}")
    sip.display_sip_details()


def compound_interest_calculator():
    """CLI for Compound Interest Calculator"""
    parser = argparse.ArgumentParser(description="Calculate the future value of an investment using compound interest.")
    parser.add_argument("--principal", type=float, required=True, help="Initial principal amount")
    parser.add_argument("--annual-rate", type=float, required=True, help="Annual interest rate (percentage)")
    parser.add_argument("--times-compounded", type=int, required=True,
                        help="Number of times interest is compounded per year")
    parser.add_argument("--years", type=int, required=True, help="Investment duration in years")

    args = parser.parse_args()

    compound_interest = CompoundInterestCalculator(
        args.principal, args.annual_rate, args.times_compounded, args.years
    )
    future_value = compound_interest.calculate_future_value()

    print(f"Future Value of Investment: ${future_value}")
    compound_interest.display_investment_details()
