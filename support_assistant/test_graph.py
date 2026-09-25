from graph import graph


# ---------------------------------------
# Test 1: Policy question
# ---------------------------------------

policy_result = graph.invoke({
    "query": "What is the delivery fee?"
})

print("\n==============================")
print("POLICY QUESTION RESULT")
print("==============================")

print(policy_result["response"].model_dump())


# ---------------------------------------
# Test 2: General question
# ---------------------------------------

general_result = graph.invoke({
    "query": "What is the capital of India?"
})

print("\n==============================")
print("GENERAL QUESTION RESULT")
print("==============================")

print(general_result["response"].model_dump())