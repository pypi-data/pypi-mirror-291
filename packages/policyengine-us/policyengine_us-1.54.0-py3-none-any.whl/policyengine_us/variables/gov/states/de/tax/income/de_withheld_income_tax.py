from policyengine_us.model_api import *


class de_withheld_income_tax(Variable):
    value_type = float
    entity = Person
    label = "Delaware withheld income tax"
    defined_for = StateCode.DE
    unit = USD
    definition_period = YEAR

    def formula(person, period, parameters):
        employment_income = person("irs_employment_income", period)
        p = parameters(period).gov.states.de.tax.income
        # We apply the base standard deduction amount
        standard_deduction = p.deductions.standard.amount["SINGLE"]
        reduced_employment_income = max_(
            employment_income - standard_deduction, 0
        )
        return p.rate.calc(reduced_employment_income)
