from fastapi import FastAPI, HTTPException
from .schemas import ArithmeticRequest
import os

app = FastAPI()

# This should be set as an environment variable in production
VALID_SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey123")

@app.post("/calculate")
async def calculate(request: ArithmeticRequest):
    # Validate secret key
    if request.secret_key != VALID_SECRET_KEY:
        raise HTTPException(status_code=403, detail="Invalid secret key")
    
    # Validate operator
    operator = request.operator.lower()
    if operator not in ["add", "subtract", "multiply", "divide"]:
        raise HTTPException(status_code=400, detail="Invalid operator. Use add, subtract, multiply, or divide")
    
    # Perform calculation
    try:
        if operator == "add":
            result = request.number1 + request.number2
        elif operator == "subtract":
            result = request.number1 - request.number2
        elif operator == "multiply":
            result = request.number1 * request.number2
        elif operator == "divide":
            if request.number2 == 0:
                raise HTTPException(status_code=400, detail="Cannot divide by zero")
            result = request.number1 / request.number2
        
        return {
            "result": result,
            "operation": f"{request.number1} {operator} {request.number2}",
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}