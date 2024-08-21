from decimal import Decimal, getcontext

# Set the precision high enough to handle financial calculations
getcontext().prec = 28


class SIPCalculator:
    def __init__(self, monthly_investment: float, annual_rate: float, years: int):
        """
        Initializes the SIPCalculator with SIP details.

        Parameters:
        - monthly_investment: The amount invested every month.
        - annual_rate: The annual return rate (in percentage).
        - years: The investment tenure in years.
        """
        self.monthly_investment = Decimal(monthly_investment)
        self.annual_rate = Decimal(annual_rate)
        self.years = years
        self.monthly_rate = self.annual_rate / Decimal(12) / Decimal(100)
        self.total_payments = years * 12

    def calculate_future_value(self) -> Decimal:
        """
        Calculate the future value of the SIP investment.

        Returns:
        - future_value: The calculated future value of the investment.
        """
        future_value = self.monthly_investment * (
                    ((1 + self.monthly_rate) ** self.total_payments - 1) / self.monthly_rate) * (1 + self.monthly_rate)
        return future_value.quantize(Decimal('0.01'))  # Rounds to 2 decimal places

    def display_sip_details(self):
        """
        Display the SIP details including the total investment, future value, and expected returns.
        """
        total_investment = self.monthly_investment * self.total_payments
        future_value = self.calculate_future_value()
        total_returns = future_value - total_investment

        print(f"Total Investment: ${total_investment.quantize(Decimal('0.01'))}")
        print(f"Future Value: ${future_value}")
        print(f"Total Returns: ${total_returns.quantize(Decimal('0.01'))}")
