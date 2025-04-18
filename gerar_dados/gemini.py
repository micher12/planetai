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
		"content: Você é um classificador de noticias sobre o meio ambiente. Analise o contexto da noticia, pois o meio ambiente não envolve apenas a natureza. Classifique-as como positiva, negativa ou irrelevante. 0 será negativa, 1 será positiva e 2 irrelevante. Apenas responda irrelevante se a noticias não tiver nenhuma relação com o meio ambiente. Responda apenas com 0,1,2"

		"role: assistant",
		f"content: {text}"
	]

	response = client.models.generate_content(
		model="gemini-2.0-flash-thinking-exp-01-21",
		contents=messages,
	)

	return response.text


