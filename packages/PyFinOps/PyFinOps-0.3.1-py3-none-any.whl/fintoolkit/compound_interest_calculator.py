from decimal import Decimal, getcontext

# Set the precision high enough to handle financial calculations
getcontext().prec = 28


class CompoundInterestCalculator:
    def __init__(self, principal: float, annual_rate: float, times_compounded: int, years: int):
        """
        Initializes the CompoundInterestCalculator with investment details.

        Parameters:
        - principal: The initial investment amount.
        - annual_rate: The annual interest rate (in percentage).
        - times_compounded: The number of times interest is compounded per year.
        - years: The total number of years the money is invested for.
        """
        self.principal = Decimal(principal)
        self.annual_rate = Decimal(annual_rate)
        self.times_compounded = times_compounded
        self.years = years
        self.rate_per_period = self.annual_rate / Decimal(self.times_compounded) / Decimal(100)

    def calculate_future_value(self) -> Decimal:
        """
        Calculate the future value of the investment.

        Returns:
        - future_value: The calculated future value of the investment.
        """
        future_value = self.principal * (1 + self.rate_per_period) ** (self.times_compounded * self.years)
        return future_value.quantize(Decimal('0.01'))  # Rounds to 2 decimal places

    def display_investment_details(self):
        """
        Display the investment details including the principal, future value, and total interest earned.
        """
        future_value = self.calculate_future_value()
        total_interest = future_value - self.principal

        print(f"Principal: ${self.principal.quantize(Decimal('0.01'))}")
        print(f"Future Value: ${future_value}")
        print(f"Total Interest Earned: ${total_interest.quantize(Decimal('0.01'))}")
