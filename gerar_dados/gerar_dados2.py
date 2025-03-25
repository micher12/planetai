import random
import csv

# Listas de palavras-chave para preencher os templates
PALAVRAS_BAIXA = ["queda", "redução", "diminuição", "declínio", "baixa"]
PALAVRAS_POSITIVA = ["melhoria", "recuperação", "preservação", "proteção", "conservação"]
PALAVRAS_AUMENTO = ["aumento", "elevação", "acréscimo", "alta", "crescimento"]
PALAVRAS_NEGATIVA = ["destruição", "degradação", "poluição", "devastação", "contaminação"]

# Templates expandidos para frases positivas
TEMPLATES_POSITIVOS = [
    ("Amazônia registra {} do desmatamento em relação ao ano passado.", PALAVRAS_BAIXA),
    ("Novo projeto de lei propõe {} na proteção de áreas verdes.", PALAVRAS_POSITIVA),
    ("Campanha de conscientização resulta em {} do uso de plásticos.", PALAVRAS_BAIXA),
    ("Iniciativa local promove {} de habitats naturais.", PALAVRAS_POSITIVA),
    ("Tecnologia inovadora contribui para {} na qualidade do ar.", PALAVRAS_POSITIVA),
    ("Programa de reflorestamento alcança {} de áreas degradadas.", PALAVRAS_POSITIVA),
    ("Energia renovável representa {} na matriz energética do país.", PALAVRAS_AUMENTO),
    ("A implementação de políticas ambientais rigorosas resultou em uma {} significativa das emissões de carbono.", PALAVRAS_BAIXA),
    ("A adoção de energias renováveis está em {} constante, beneficiando o meio ambiente.", PALAVRAS_AUMENTO),
    ("A conscientização pública sobre reciclagem levou a uma {} notável no uso de materiais recicláveis.", PALAVRAS_AUMENTO),
    ("Dados oficiais mostram {} de 12% nas taxas de desmatamento na região amazônica.", PALAVRAS_BAIXA),
    ("Unidades de conservação conseguem {} na prevenção do desmatamento.", PALAVRAS_POSITIVA),
    ("Políticas de preservação promovem {} na proteção da floresta.", PALAVRAS_POSITIVA),
    ("Estratégias de monitoramento levam a {} do desmatamento ilegal.", PALAVRAS_BAIXA),
    ("Pesquisa revela {} na emissão de gases do efeito estufa.", PALAVRAS_BAIXA),
    ("Iniciativas verdes contribuem para {} nas emissões de carbono.", PALAVRAS_BAIXA),
    ("Empresas adotam tecnologias limpas, resultando em {} nas emissões industriais.", PALAVRAS_BAIXA),
    ("Energia renovável impulsiona {} de emissões de carbono.", PALAVRAS_BAIXA),
    ("Programas de conservação alcançam {} na proteção de espécies ameaçadas.", PALAVRAS_AUMENTO),
    ("Número de espécies protegidas registra {} em áreas de preservação.",PALAVRAS_AUMENTO),
    ("Pesquisadores comemoram {} no sucesso de projetos de recuperação de fauna.",PALAVRAS_POSITIVA),
    ("A preservação de habitats naturais resulta em {} na biodiversidade local.", PALAVRAS_POSITIVA),
    ("A recuperação de áreas degradadas promove {} na qualidade do solo.", PALAVRAS_POSITIVA),
    ("A reciclagem de resíduos sólidos leva a {} de lixo urbano.", PALAVRAS_BAIXA),
    ("A preservação de áreas verdes urbanas resulta em {} na qualidade de vida da população.", PALAVRAS_POSITIVA),
    ("A recuperação de rios poluídos promove {} na qualidade da água.", PALAVRAS_POSITIVA),
    ("A reutilização de materiais descartados leva a {} de resíduos.", PALAVRAS_BAIXA),
    ("A preservação de ecossistemas frágeis resulta em {} na proteção da fauna e flora.", PALAVRAS_POSITIVA),
    ("A recuperação de áreas degradadas promove {} na qualidade do ar.", PALAVRAS_POSITIVA),
    ("A preservação de áreas costeiras resulta em {} na proteção de ecossistemas marinhos.", PALAVRAS_POSITIVA),
    ("A reciclagem de materiais plásticos leva a {} da poluição.", PALAVRAS_BAIXA),
    ("A preservação de florestas tropicais promove {} na proteção de espécies ameaçadas.", PALAVRAS_POSITIVA),
    ("A recuperação de áreas degradadas leva a {} na qualidade do solo.", PALAVRAS_POSITIVA),
    ("Projetos de reflorestamento promovem {} na recuperação de áreas degradadas.", PALAVRAS_POSITIVA),
    ("Comunidades locais lideram com {} em iniciativas de restauração ecológica.", PALAVRAS_AUMENTO),
    ("Tecnologias de recuperação ambiental resultam em {} na regeneração de ecossistemas.", PALAVRAS_POSITIVA),

]

# Templates expandidos para frases negativas
TEMPLATES_NEGATIVOS = [
    ("Amazônia registra {} do desmatamento em relação ao ano passado.", PALAVRAS_AUMENTO),
    ("Novo relatório indica {} na emissão de gases poluentes.", PALAVRAS_AUMENTO),
    ("Incêndios florestais causam {} em vasta área de mata nativa.", PALAVRAS_NEGATIVA),
    ("Poluição de rios atinge {} crítico em várias cidades.", PALAVRAS_NEGATIVA),
    ("Desmatamento ilegal leva a {} de espécies endêmicas.", PALAVRAS_NEGATIVA),
    ("Exploração de recursos naturais causa {} em ecossistemas frágeis.", PALAVRAS_NEGATIVA),
    ("A falta de regulamentação ambiental levou a um {} alarmante na poluição do ar.", PALAVRAS_AUMENTO),
    ("O desmatamento desenfreado está causando uma {} devastadora na biodiversidade.", PALAVRAS_NEGATIVA),
    ("A contaminação dos oceanos por plásticos está em {} constante, ameaçando a vida marinha.", PALAVRAS_AUMENTO),
    ("Mudanças climáticas levam a {} de eventos climáticos extremos.", PALAVRAS_AUMENTO),
    ("A Mata Atlântica registra {} em atividades de extração ilegal de madeira.", PALAVRAS_AUMENTO),
    ("Áreas urbanas relatam {} nos níveis de poluição do ar devido a emissões industriais.", PALAVRAS_AUMENTO),
    ("Rios em zonas industriais apresentam {} na contaminação por resíduos químicos.", PALAVRAS_AUMENTO),
    ("Vazamentos de petróleo causam {} aos ecossistemas marinhos.", PALAVRAS_NEGATIVA),
    ("O desmatamento leva à {} de habitats naturais.", PALAVRAS_NEGATIVA),
    ("A queima de combustíveis fósseis resulta em {} da atmosfera.", PALAVRAS_NEGATIVA),
    ("O aquecimento global está causando {} nos níveis do mar.", PALAVRAS_AUMENTO),
    ("Eventos climáticos extremos estão se tornando mais frequentes, levando a {} nas comunidades afetadas.", PALAVRAS_NEGATIVA),
    ("A destruição de habitats está conduzindo à {} de espécies ameaçadas.", PALAVRAS_NEGATIVA),
    ("Apesar das regulamentações, a mineração ilegal continua a causar {} nos ecossistemas fluviais.", PALAVRAS_NEGATIVA),
    ("A falta de infraestrutura de gestão de resíduos resulta em {} da poluição plástica nos oceanos.", PALAVRAS_AUMENTO),
    ("A poluição do ar nas cidades está ligada a {} em doenças respiratórias.", PALAVRAS_AUMENTO),
    ("Fontes de água contaminadas levam a {} em doenças transmitidas pela água.", PALAVRAS_AUMENTO),
    ("A degradação ambiental resulta em {} dos serviços ecossistêmicos, afetando as economias locais.", PALAVRAS_NEGATIVA),
    ("Esforços de conservação falhos levaram a {} em áreas protegidas.", PALAVRAS_NEGATIVA),
    ("Financiamento insuficiente para programas ambientais resulta em {} dos objetivos de conservação.", PALAVRAS_NEGATIVA),
    ("Negligência corporativa no descarte de resíduos causa {} em corpos d’água locais.", PALAVRAS_NEGATIVA),
    ("A expansão da agricultura industrial leva a {} na fertilidade do solo.", PALAVRAS_NEGATIVA),
    ("O desmatamento desloca povos indígenas, causando {} de seu patrimônio cultural.", PALAVRAS_NEGATIVA),
    ("A sobrepesca está levando à {} dos estoques de peixes nos oceanos.", PALAVRAS_NEGATIVA),
    ("O uso de pesticidas na agricultura resulta em {} das populações de polinizadores.", PALAVRAS_NEGATIVA),
    ("A rápida urbanização está causando {} em espaços verdes nas cidades.", PALAVRAS_NEGATIVA),
    ("A construção de barragens leva à {} dos ecossistemas fluviais e ao deslocamento de comunidades.", PALAVRAS_NEGATIVA),
    ("As mudanças climáticas estão intensificando secas, levando a {} na escassez de água.", PALAVRAS_AUMENTO),
    ("O aumento das temperaturas está causando {} na frequência de ondas de calor.", PALAVRAS_AUMENTO),
    ("Sem ação imediata, enfrentamos {} na perda de biodiversidade.", PALAVRAS_AUMENTO),
]

# Templates expandidos para frases irrelevantes
FRASES_IRRELEVANTES = [
    "Ator famoso anuncia novo projeto cinematográfico.",
    "Time de futebol conquista campeonato nacional.",
    "Economia do país cresce 2% no último trimestre.",
    "Nova tendência de moda toma conta das passarelas.",
    "Cantora lança novo álbum após hiato de três anos.",
    "Festival de cinema atrai celebridades internacionais.",
    "Empresa de tecnologia lança novo smartphone.",
    "A nova série de TV está fazendo sucesso entre os jovens.",
    "O mercado de ações registrou uma alta histórica hoje.",
    "A moda verão deste ano traz cores vibrantes e estampas florais.",
    "Time de futebol contrata novo treinador.",
    "Startup lança aplicativo de compartilhamento de serviços.",
    "Banda internacional anuncia turnê mundial.",
    "Restaurante gourmet inaugura nova filial.",
    "Empresa de tecnologia desenvolve produto inovador.",
    "Celebridade lança linha de moda sustentável.",
    "Festival de música prepara edição especial.",
    "Artista plástico apresenta exposição internacional.",
    "Universidade desenvolve pesquisa em inteligência artificial.",
    "Novo modelo de smartphone é lançado no mercado.",
    "Escritor renomado lança livro de memórias.",
    "Competição internacional de esportes será realizada.",
    "Chef famoso inaugura restaurante de culinária contemporânea.",
    "Empresa de games anuncia novo jogo eletrônico."
]

# Função para gerar frases positivas
def gerar_frase_positiva():
    template, palavras = random.choice(TEMPLATES_POSITIVOS)
    palavra = random.choice(palavras)
    return template.format(palavra)

# Função para gerar frases negativas
def gerar_frase_negativa():
    template, palavras = random.choice(TEMPLATES_NEGATIVOS)
    palavra = random.choice(palavras)
    return template.format(palavra)

# Função para gerar frases irrelevantes
def gerar_frase_irrelevante():
    return random.choice(FRASES_IRRELEVANTES)

# Função para gerar frases alternadas
def gerar_frases_alternadas(n=5):
    frases = []
    for _ in range(n):
        frases.append((gerar_frase_positiva(), 1))  # Positivo
        frases.append((gerar_frase_negativa(), 0))  # Negativo
        frases.append((gerar_frase_irrelevante(), 2))  # Irrelevante
    return frases

# Função para salvar em CSV
def salvar_em_csv(frases, nome_arquivo='gerar_dados/frases_ambientais.csv'):
    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(['title',"date","url","content",'class'])  # Cabeçalho
        for frase, classificacao in frases:
            escritor.writerow([frase, "","", frase, classificacao])

# Exemplo de uso
if __name__ == "__main__":
    frases = gerar_frases_alternadas(33)  # Gera 5 conjuntos de frases alternadas
    salvar_em_csv(frases)
    print(f"Frases salvas em 'frases_ambientais.csv'.")