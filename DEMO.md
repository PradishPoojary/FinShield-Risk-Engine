# 🖥️ FinShield Execution Demo

Since local execution may be restricted on enterprise assets, this document serves as a visual trace of the FinShield Risk Engine in a live environment.

### 1. API Documentation & Schema Discovery
FinShield automatically generates OpenAPI (Swagger) specifications. This allows banking gateways to seamlessly integrate with our endpoints.

![Swagger UI](assets/swagger_ui.png)

### 2. Real-Time AI Inference (Blocked Transaction)
In this scenario, a high-value transaction is attempted via a Cryptocurrency merchant. 
* The Pydantic model successfully parses and validates the data types.
* The Random Forest model evaluates the feature set against historical rules.
* The system accurately blocks the transaction, returning a structural JSON response to the banking gateway.

![API Response](assets/api_response.png)

