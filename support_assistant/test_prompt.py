from prompts import SUPPORT_PROMPT


context = """
Zepto delivers grocery and household essentials to serviceable pin
codes within 10 to 30 minutes of order confirmation. Standard delivery
is free on orders over INR 149; orders below this threshold incur a
flat INR 25 delivery fee.
"""

question = "What is the delivery fee?"

prompt = SUPPORT_PROMPT.format(
    context=context,
    question=question
)

print(prompt)