from google import genai
from dotenv import load_dotenv
import os;

def classify(text):

	load_dotenv()
	apikey = os.getenv("GEMINI_API_KEY")
        
	if not apikey:
		raise ValueError("Chave de API não encontrada. Configure a variável de ambiente GEMINI_API_KEY.")
        

	client = genai.Client(api_key=apikey)

	messages = [
		"role: user",
		"content: Você é um profissional em meio ambiente, com base em seu conhecimento analise a notícia e fale se ela é boa = 1, ruim = 0 ou irrelevante = 0. Responda apenas com números, sendo 0 = ruim, 1 = boa, 2 = irrelevante."

		"role: assistant",
		f"content: {text}"
	]

	response = client.models.generate_content(
		model="gemini-2.0-flash",
		contents=messages,
	)

	return response.text

