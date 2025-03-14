import pandas as pd
import random

# Definindo tipos de dados para cada placeholder
NUMERO = 'number'
PALAVRA = 'word'
CAUSAS = 'word'
HORAS = 'hours'  # Para frases que exigem tempo em horas

# Frases negativas com metadados de tipo
negativas = [
    ("Aumento de {}% nas áreas afetadas por desastres naturais devido às mudanças climáticas", [NUMERO]),
    ("Níveis de poluição atmosférica atingem patamares alarmantes em áreas urbanas", []),
    ("Desmatamento descontrolado agrava a crise ambiental em regiões críticas", []),
    ("Escassez de água potável afeta comunidades vulneráveis em diversas localidades", []),
    ("Derramamento de óleo causa danos irreparáveis à vida marinha e ecossistemas costeiros", []),
    ("Aumento da frequência de eventos climáticos extremos causa destruição e deslocamento de populações", []),
    ("Contaminação do solo por resíduos tóxicos ameaça a saúde humana e a segurança alimentar", []),
    ("Perda de biodiversidade acelera o desequilíbrio ecológico em ecossistemas frágeis", []),
    ("Avanço do garimpo ilegal causa devastação ambiental e conflitos sociais em áreas protegidas", []),
    ("Crise hídrica se agrava com a má gestão dos recursos e a falta de investimentos em infraestrutura", []),
    ("Queimadas florestais destroem habitats naturais e liberam gases poluentes na atmosfera", []),
    ("Assoreamento de rios compromete o abastecimento de água e a navegabilidade", []),
    ("Construção de barragens causa impactos ambientais e sociais em comunidades ribeirinhas", []),
    ("Desperdício de alimentos contribui para o aumento das emissões de gases de efeito estufa", []),
    ("Exploração predatória de recursos naturais ameaça a sustentabilidade do planeta", []),
    ("Falta de saneamento básico causa poluição da água e proliferação de doenças", []),
    ("Descarte inadequado de resíduos sólidos agrava a poluição do solo e da água", []),
    ("Aumento do nível do mar ameaça cidades costeiras e ecossistemas litorâneos", []),
    ("Acidificação dos oceanos causa danos à vida marinha e à pesca", []),
    ("Proliferação de espécies invasoras ameaça a biodiversidade nativa", []),
    ("Aumento da temperatura global causa o derretimento das geleiras e o aumento do nível do mar", []),
    ("Desmatamento ilegal cresce {}% na região", [NUMERO]),
    ("Falta de recursos compromete o combate a desastres ambientais em {}", [PALAVRA]),
    ("Cerca de {}% dos desastres são causados por ações antrópicas", [NUMERO]),
    ("Risco elevado de desastres por causa de {}", [PALAVRA]),
    ("Desastres se agravam por conta de {}", [CAUSAS]),
    ("Aumento de desastres impulsionado por {}", [CAUSAS]),
    ("Escassez de recursos eleva o risco de desastres por {}", [PALAVRA]),
    ("Comunidades sofrem com {} desastres próximos", [NUMERO]),
    ("Leis ambientais falham em {}% dos casos de crimes ambientais", [NUMERO]),
    ("Deficiências em planos de contingência deixam {} comunidades vulneráveis", [NUMERO]),
    ("Condições climáticas extremas elevam o risco de {}% nos desastres", [NUMERO]),
    ("Ventos fortes agravam o avanço de desastres, elevando em {}% os riscos", [NUMERO]),
    ("Desastres aumentam, porém a intervenção é insuficiente", []),
    ("Desastres se alastram rapidamente, contudo as medidas de segurança falham", []),
    ("Ação preventiva é implementada, entretanto os desastres se dispersam sem controle", []),
    ("Medidas de contenção são tomadas, todavia os desastres se expandem", []),
    ("Desastres atingem patamar recorde", []),
    ("Desmatamento ilegal cresce em áreas protegidas", []),
    ("Desastres aumentam devido a estiagem", []),
    ("Áreas degradadas por desastres superam {} mil hectares", [NUMERO]),
    ("População local ameaçada por expansão de desastres", []),
    ("Desastres avançam para áreas urbanas, colocando vidas em risco", []),
    ("Poluição atinge nível crítico devido a desastres", []),
    ("Controle de desastres é insuficiente para conter danos", []),
    ("Risco de extinção aumenta para espécies ameaçadas", []),
    ("Desmatamento ilegal impulsiona desastres", []),
    ("Aumento nos casos de desastres", []),
    ("Bombeiros fazem ações preventivas, mas desastres saem de controle", []),
    ("Falta de saneamento básico agrava a situação", []),
]

# Frases positivas com metadados de tipo
positivas = [
    ("Investimentos em energias renováveis impulsionam a transição para uma economia de baixo carbono", []),
    ("Implementação de práticas agrícolas sustentáveis promove a conservação do solo e da água", []),
    ("Criação de unidades de conservação protege a biodiversidade e os serviços ecossistêmicos", []),
    ("Adoção de políticas de gestão integrada de recursos hídricos garante o abastecimento para as futuras gerações", []),
    ("Desenvolvimento de tecnologias limpas reduz a poluição e os impactos ambientais da indústria", []),
    ("Promoção da educação ambiental conscientiza a população sobre a importância da sustentabilidade", []),
    ("Recuperação de áreas degradadas restaura ecossistemas e promove a recuperação da biodiversidade", []),
    ("Implementação de sistemas de tratamento de esgoto reduz a poluição da água e melhora a saúde pública", []),
    ("Incentivo ao consumo consciente e à economia circular reduz o desperdício de recursos naturais", []),
    ("Fortalecimento da fiscalização ambiental combate crimes e infrações que prejudicam o meio ambiente", []),
    ("Queimadas controladas previnem {}% dos desastres", [NUMERO]),
    ("Número de desastres recua {}%", [NUMERO]),
    ("Plano de combate reduz o risco de desastres em {} regiões", [NUMERO]),
    ("Áreas se recuperam após ação eficaz", []),
    ("Bombeiros atuam com sucesso em {} ocorrências de desastres", [NUMERO]),
    ("Monitoramento eficiente diminui os desastres em {}%", [NUMERO]),
    ("Campanha de prevenção resulta em {}% menos desastres", [NUMERO]),
    ("Tecnologia avançada auxilia no controle de {} desastres", [NUMERO]),
    ("Desastres controlados em apenas {} horas graças a respostas rápidas", [HORAS]),
    ("Proteção ambiental reforça a capacidade de resposta aos desastres", []),
    ("Estratégia preventiva reduz em {}% os desastres", [NUMERO]),
    ("Intervenção rápida diminui {}% dos desastres", [NUMERO]),
    ("Métodos inovadores amenizam os desastres em {}%", [NUMERO]),
    ("Ação coordenada controla desastres em {} regiões", [NUMERO]),
    ("Resposta eficaz controlou os desastres em {} horas", [HORAS]),
    ("Dados recentes apontam {} nos últimos meses", [PALAVRA]),
    ("Ações comunitárias reduzem desastres em {} regiões", [NUMERO]),
    ("Tecnologia de previsão detecta desastres em apenas {} minutos", [NUMERO]),
    ("Políticas públicas reduzem o desmatamento em {}%", [NUMERO]),
    ("Recuperação de áreas devolve {} hectares", [NUMERO]),
    ("Parceria com comunidades controla {} desastres", [NUMERO]),
    ("Desastres controlados previnem danos em {} hectares", [NUMERO]),
    ("Monitoramento via satélite reduz o tempo de resposta para {} horas", [HORAS]),
    ("Campanha educativa conscientiza {} comunidades sobre prevenção", [NUMERO]),
    ("Intervenção ambiental resulta em queda de {}% nos desastres", [NUMERO]),
    ("Ferramentas de inteligência artificial mapeiam {} riscos potenciais", [NUMERO]),
    ("Lei de proteção amplia as áreas seguras em {}%", [NUMERO]),
    ("Bombeiros extinguem desastres em {} horas com equipamentos modernos", [HORAS]),
    ("Recuperação de nascentes diminui o risco de desastres em {}%", [NUMERO]),
    ("Ações integradas elevam a segurança ambiental, reduzindo {} desastres", [NUMERO]),
    ("Investimentos em prevenção demonstram {}% de melhoria na resposta aos desastres", [NUMERO]),
    ("Medidas de contenção mostram eficácia", []),
    ("Monitoramento assegura a redução dos riscos", []),
    ("Intervenção rápida previne a propagação, o bioma se mantém protegido", []),
    ("Ação integrada reduz desastres, índices de segurança melhoram", []),
    ("Operação de combate é eficiente, resposta supera os desafios", []),
    ("Desastres caem drasticamente", []),
    ("Controle eficaz reduz desastres", []),
    ("Monitoramento previne propagação de desastres", []),
    ("Áreas degradadas recuperam-se graças a ações ambientais", []),
    ("Tecnologia garante resposta rápida a desastres", []),
    ("Políticas públicas reduzem desmatamento em {}%", [NUMERO]),
    ("População local adere a práticas sustentáveis contra desastres", []),
    ("Desastres controlados preservam biodiversidade", []),
    ("Intervenção rápida evita danos a comunidades", []),
    ("{} é comemorada", [PALAVRA]),
    ("Desastres em {}", [PALAVRA]),
]

# Frases irrelevantes
irrelevantes = [
    ("Ator famoso anuncia novo projeto cinematográfico", []),
    ("Cantora lança novo álbum e conquista o topo das paradas de sucesso", []),
    ("Equipe esportiva vence campeonato e celebra com a torcida", []),
    ("Político anuncia medidas para impulsionar a economia do país", []),
    ("Empresário de sucesso revela segredos para alcançar o sucesso nos negócios", []),
    ("Celebridade compartilha detalhes de sua vida pessoal em entrevista exclusiva", []),
    ("Novo smartphone chega ao mercado com recursos inovadores", []),
    ("Apresentador de TV anuncia sua saída do programa após anos de sucesso", []),
    ("Escritor lança novo livro e participa de sessão de autógrafos", []),
    ("Chef renomado abre novo restaurante com cardápio exclusivo", []),
    ("Casal de famosos anuncia gravidez e compartilha a novidade com os fãs", []),
    ("Artista plástico inaugura exposição com obras inéditas", []),
    ("Banda de rock faz show histórico e emociona o público", []),
    ("Cientistas descobrem nova espécie de animal em expedição na Amazônia", []),
    ("Astronautas realizam missão espacial e fazem importantes descobertas", []),
    ("Estudantes protestam por melhorias na educação e mais investimentos", []),
    ("Trabalhadores entram em greve por melhores salários e condições de trabalho", []),
    ("Governo anuncia pacote de medidas para combater a inflação", []),
    ("Justiça condena réu por crime de corrupção", []),
    ("Polícia prende quadrilha especializada em roubo de carros", []),
    ("Médicos realizam cirurgia inédita e salvam a vida de paciente", []),
    ("Voluntários se unem para ajudar vítimas de enchente", []),
    ("Empresas lançam campanha de arrecadação de alimentos para famílias carentes", []),
    ("Artistas se apresentam em show beneficente para ajudar instituições de caridade", []),
    ("Comunidades se mobilizam para construir casas para famílias desabrigadas", []),
    ("Jovens criam projeto social para ajudar moradores de rua", []),
    ("Idosos se reúnem para praticar atividades físicas e promover a saúde", []),
    ("Crianças aprendem sobre a importância da reciclagem em escola", []),
    ("Famílias se unem para plantar árvores e revitalizar praça", []),
    ("Vizinhos se organizam para promover a segurança no bairro", []),
]

# Gerar dados alternados
dados = []
for i in range(200):
    if i % 3 == 0:
        # Negativo (0)
        frase_template, tipos = random.choice(negativas)
        args = []
        for tipo in tipos:
            if tipo == NUMERO:
                args.append(str(random.randint(10, 90)))
            elif tipo == PALAVRA:
                args.append(random.choice(["seca", "inundações", "tempestades", "poluição", "desmatamento", "erosão", "chuva ácida", "escassez de água"]))
            elif tipo == CAUSAS:
                args.append(random.choice(["ações humanas", "mudanças climáticas", "descaso", "falta de planejamento", "exploração descontrolada", "negligência", "interesses econômicos"]))
        # Formatar a frase
        frase = frase_template.format(*args)
        dados.append({"title": frase, "date": None, "url": None, "content": frase, "class": 0})
    elif i % 3 == 1:
        # Positivo (1)
        frase_template, tipos = random.choice(positivas)
        args = []
        for tipo in tipos:
            if tipo == NUMERO:
                args.append(str(random.randint(10, 90)))
            elif tipo == HORAS:
                args.append(str(random.randint(1, 24)))
            elif tipo == PALAVRA:
                args.append(random.choice(["avanço", "melhora", "progresso", "recuperação", "estabilização", "conscientização"]))
        # Formatar a frase
        frase = frase_template.format(*args)
        dados.append({"title": frase, "date": None, "url": None, "content": frase, "class": 1})
    else:
        # Irrelevante (2)
        frase_template, tipos = random.choice(irrelevantes)
        args = []
        # Formatar a frase
        frase = frase_template.format(*args)
        dados.append({"title": frase, "date": None, "url": None, "content": frase, "class": 2})

# Salvar em CSV
df = pd.DataFrame(dados)
df = df[["title", "date", "url", "content", "class"]]  # Garante a ordem das colunas
df.to_csv("data_sintetica.csv", index=False)
print("Dados gerados com sucesso em data.csv")