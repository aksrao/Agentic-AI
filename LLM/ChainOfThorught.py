from single_shot import get_oss_completion

prompt = """
A company offers two subscription plans:

Plan A: ₹300 per month + ₹2 per API call
Plan B: ₹500 per month + ₹1 per API call

Determine the minimum number of API calls for which Plan B becomes cheaper than Plan A.

First, write out the cost equations for both plans.
Then solve the inequality step by step.
Finally, state the minimum number of API calls.
"""

response = get_oss_completion(prompt)

print(response.choices[0].message.content)