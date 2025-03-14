from google import genai

def classify(text):

	client = genai.Client(api_key="AIzaSyClQ1dnOtQPxiGAEzl0HCbL7iOSUjFg7rY")

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
