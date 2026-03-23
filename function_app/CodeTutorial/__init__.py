import azure.functions as func
import json
import os
from openai import OpenAI

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
        code_input = body.get("code")

        if not code_input:
            return func.HttpResponse("Provide code", status_code=400)

        client = OpenAI(
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            base_url=os.environ["AZURE_OPENAI_ENDPOINT"]
        )

        prompt = f"""
You are a senior developer.

Convert the following code into a beginner-friendly tutorial.

Include:
- What the code does
- Step-by-step explanation
- Example
- Summary

Code:
{code_input}
"""

        response = client.responses.create(
            model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
            input=prompt
        )

        tutorial = response.output[0].content[0].text

        return func.HttpResponse(
            json.dumps({"tutorial": tutorial}),
            mimetype="application/json"
        )

    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)