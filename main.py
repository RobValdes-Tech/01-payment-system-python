from abc import ABC, abstractmethod
from fastapi import FastAPI, HTTPException

# 1. EL CONTRATO (INTERFAZ PURA USANDO CLASE ABSTRACTA)
class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> None:
        pass

# 2. IMPLEMENTACIONES CONCRETAS
class CreditCardProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> None:
        print(f"💳 [Python] Tarjeta de Crédito procesada: ${amount}")

class UpiProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> None:
        print(f"📱 [Python] UPI procesado: ${amount}")

app = FastAPI()

# 3. REGISTRO DE ESTRATEGIAS (Diccionario que mapea los procesadores)
payment_registry = {
    "creditcard": CreditCardProcessor(),
    "upi": UpiProcessor()
}

# 4. ENDPOINT HTTP POLIMÓRFICO
@app.post("/api/payments/{method}")
def pay(method: str, amount: float):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="El monto debe ser mayor a cero")
        
    processor = payment_registry.get(method.lower())
    if not processor:
        raise HTTPException(status_code=400, detail="Método de pago no soportado")
    
    # Invocación polimórfica
    processor.process_payment(amount)
    return {"message": "Procesando pago en Python..."}
