from models import AnswerResponse


response = AnswerResponse(
    answer="Based on the retrieved context: Standard delivery is free on orders over INR 149.",
    sources=["doc1"],
    confidence=1.0
)

print(response)
print(response.model_dump())