# Import necessary libraries
import requests
import gradio as gr

# Correct API and header configuration
API_URL = "https://currency-converter5.p.rapidapi.com/currency/convert"
API_KEY = "8761e77f8amsh33186f2d032dc55p16ec2fjsn6e86a54041e5"  
headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "currency-converter5.p.rapidapi.com"
}

def currency_converter(amount: float, from_currency: str, to_currency: str):
    # Set API parameters
    params = {
        "from": from_currency,
        "to": to_currency,
        "amount": amount
    }

    try:
        response = requests.get(API_URL, headers=headers, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()

        if "rates" in data:
            conversion_rate = data["rates"][to_currency]["rate"]
            converted_amount = float(conversion_rate) * amount
            return f"{amount} {from_currency} = {converted_amount} {to_currency}"
        else:
            return "Error: Unable to fetch conversion rate. Please try again."

    except requests.exceptions.RequestException as e:
        return f"API Error: {str(e)}"

def launch_interface():
    with gr.Blocks() as demo:
        gr.Markdown("# Currency Converter Tool")
        
        # Input elements
        amount_input = gr.Number(label="Amount", value=1)
        from_currency = gr.Dropdown(label="From Currency", choices=["USD", "EUR", "GBP", "JPY"], value="USD")
        to_currency = gr.Dropdown(label="To Currency", choices=["USD", "EUR", "GBP", "JPY"], value="EUR")

        # Output display
        output_text = gr.Textbox(label="Conversion Result")

        # Button to trigger conversion
        convert_button = gr.Button("Convert Currency")

        # Define button action
        convert_button.click(
            fn=currency_converter, 
            inputs=[amount_input, from_currency, to_currency], 
            outputs=output_text
        )
    
    demo.launch()

# Launch the Gradio interface
launch_interface()
