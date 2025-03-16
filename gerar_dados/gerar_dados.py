import pandas as pd
import random

# Definindo tipos de dados para cada placeholder
NUMERO = 'number'
PALAVRA = 'word'
CAUSAS = ["ações humanas", "negligência", "descuidos ambientais", "práticas agrícolas inadequadas", "falta de fiscalização", "desmatamento criminosos"]
HORAS = 'hours'  # Para frases que exigem tempo em horas
ESPECIES_AMEACADAS = ["tigres", "baleias", "pandas", "corais", "veados-camelo"]
LOCALIZACAO = ["Amazônia", "manguezais", "florestas tropicais", "oceano Pacífico", "região amazônica"]
RESULTADO_POSITIVO = ["recuperação", "melhoria", "crescimento", "preservação", "redução", "sucesso", "avanço", "aumento", "proteção", "revitalização"]
ECOSISTEMAS = ["rios", "parques nacionais", "matas ciliares", "ecossistemas costeiros"]
TECNOLOGIA = ["energia solar", "energia eólica", "hidrogênio verde", "captura de carbono", "veículos elétricos", "biocombustíveis", "tecnologia de reciclagem", "sistemas de irrigação sustentável", "sensores ambientais"]
PALAVRA_DESASTRE = ["enchentes", "incêndios florestais", "deslizamentos", "secas", "desmatamento", "inundações", "tempestades", "tsunamis", "desastres ambientais"]
ACAO_AMBIENTAL = ["reflorestamento", "reciclagem", "energia renovável", "redução de plásticos", "proteção de espécies", "combate a poluição", "conservação de ecossistemas", "plantio de árvores", "redução de emissões", "uso sustentável de recursos"]
ACAO_AMBIENTAL_NEGATIVA = ["desmatamento ilegal", "poluição industrial", "exploração predatória", "queimadas ilegais", "descarte inadequado", "desregulamentação ambiental"]
RESULTADO_NEGATIVO = ["destruição", "declínio", "colapso", "extinção", "aumento", "falha", "perda", "contaminação", "redução", "desaparecimento"]
PALAVRAS_AUMENTO = ["aumento","elevação","acrescimo","alta"]
PALAVRAS_BAIXA = ["queda", "redução", "diminuição", "declínio", "baixa", "abatimento"]

# Frases negativas com metadados de tipo
negativas = [
    ("{} em {} sofre {} devido a {}.", [ECOSISTEMAS, LOCALIZACAO, RESULTADO_NEGATIVO, ACAO_AMBIENTAL_NEGATIVA]),
    ("Poluição por falta de {} afeta {} cidades.", [TECNOLOGIA, NUMERO]),
    ("Número de {} em {} cai {}%.", [ECOSISTEMAS, LOCALIZACAO, NUMERO]),
    ("Projeto de {} falha, aumentando {}% de {}.", [ACAO_AMBIENTAL, NUMERO, PALAVRA_DESASTRE]),
    ("População de {} desaparece da {}.", [ESPECIES_AMEACADAS, LOCALIZACAO]),
    ("Contaminação por {} atinge {}% da {}.", [ACAO_AMBIENTAL_NEGATIVA, NUMERO, LOCALIZACAO]),
    ("O {} em {} enfrenta {} após {}.", [ECOSISTEMAS, LOCALIZACAO, RESULTADO_NEGATIVO, ACAO_AMBIENTAL_NEGATIVA]),
    ("Desmatamento em {} desencadeia {} no {}.", [LOCALIZACAO, RESULTADO_NEGATIVO, ECOSISTEMAS]),
    ("Falta de {} agrava {} de {} em {}.", [TECNOLOGIA, RESULTADO_NEGATIVO, ECOSISTEMAS, LOCALIZACAO]),
    ("Número de {} em {} despenca {}% por causa de {} desenfreada.", [ECOSISTEMAS, LOCALIZACAO, NUMERO, ACAO_AMBIENTAL_NEGATIVA]),
    ("Ameaça de {} sobe {}% em {} após {} sem controle.", [ESPECIES_AMEACADAS, NUMERO, LOCALIZACAO, ACAO_AMBIENTAL_NEGATIVA]),
    ("Falha em {} gera {} de {} na região de {}.", [ACAO_AMBIENTAL_NEGATIVA, RESULTADO_NEGATIVO, ECOSISTEMAS, LOCALIZACAO]),
    ("Declínio de {} em {} atinge {}% após {} persistente.", [ECOSISTEMAS, LOCALIZACAO, NUMERO, ACAO_AMBIENTAL_NEGATIVA]),
    ("Crise de {} se agrava em {} com {} descontrolado.", [ECOSISTEMAS, LOCALIZACAO, ACAO_AMBIENTAL_NEGATIVA]),
    ("Contaminação por {} eleva {}% da área de {} em {}.", [ACAO_AMBIENTAL_NEGATIVA, NUMERO, ECOSISTEMAS, LOCALIZACAO]),
    ("Perda de {} em {} soma {}% e coloca {} em risco.", [ECOSISTEMAS, LOCALIZACAO, NUMERO, ESPECIES_AMEACADAS]),
    ("{} em {} colapsa após {} de {} sem intervenção.", [ECOSISTEMAS, LOCALIZACAO, RESULTADO_NEGATIVO, ACAO_AMBIENTAL_NEGATIVA]),
    ("Bacia de {} em {} sofre {} devido a {} irresponsável.", [ECOSISTEMAS, LOCALIZACAO, RESULTADO_NEGATIVO, ACAO_AMBIENTAL_NEGATIVA]),
    ("Falta de {} em {} impulsiona {} nos {}.", [TECNOLOGIA, LOCALIZACAO, RESULTADO_NEGATIVO, ECOSISTEMAS]),
    ("Queima de {} em {} gera {} devastador nos {}.", [ACAO_AMBIENTAL_NEGATIVA, LOCALIZACAO, RESULTADO_NEGATIVO, ECOSISTEMAS]),
    ("Queda de {} intensifica {} dos {} em {}.", [NUMERO, RESULTADO_NEGATIVO, ECOSISTEMAS, LOCALIZACAO]),
    ("Atuação de {} agrava {} em {} e reduz {}% de {}.", [ACAO_AMBIENTAL_NEGATIVA, RESULTADO_NEGATIVO, LOCALIZACAO, NUMERO, ESPECIES_AMEACADAS]),
    ("Ausência de {} em {} resulta em {} dos {}.", [TECNOLOGIA, LOCALIZACAO, RESULTADO_NEGATIVO, ECOSISTEMAS]),
    ("Aumento de {} em {} acarreta {} agravamento de {}.", [NUMERO, LOCALIZACAO, RESULTADO_NEGATIVO, PALAVRA_DESASTRE]),
    ("Poluição por {} em {} gera {} contaminação dos {}.", [TECNOLOGIA, LOCALIZACAO, RESULTADO_NEGATIVO, ECOSISTEMAS]),
    ("Desorganização de {} em {} leva a {} declínio dos {}.", [ACAO_AMBIENTAL_NEGATIVA, LOCALIZACAO, RESULTADO_NEGATIVO, ECOSISTEMAS]),
    ("Falta de fiscalização em {} eleva {}% de {} devido a {}.", [LOCALIZACAO, NUMERO, PALAVRA_DESASTRE, ACAO_AMBIENTAL_NEGATIVA]),
    ("Fragmentação de {} em {} ocasiona {} extinção dos {}.", [ECOSISTEMAS, LOCALIZACAO, RESULTADO_NEGATIVO, ESPECIES_AMEACADAS]),
    ("Infestação de {} em {} desencadeia {} nos {}.", [PALAVRA_DESASTRE, LOCALIZACAO, RESULTADO_NEGATIVO, ECOSISTEMAS]),
    ("Acúmulo de {} em {} intensifica {} dos {}.", [TECNOLOGIA, LOCALIZACAO, RESULTADO_NEGATIVO, ECOSISTEMAS]),
    ("Rompimento de {} em {} acarreta {} perda dos {}.", [ACAO_AMBIENTAL_NEGATIVA, LOCALIZACAO, RESULTADO_NEGATIVO, ECOSISTEMAS]),
    ("Crescimento de {} em {} piora {} do {} local.", [NUMERO, LOCALIZACAO, RESULTADO_NEGATIVO, ECOSISTEMAS]),
    ("Ação de {} em {} resulta em {} desastrosos para os {}.", [ACAO_AMBIENTAL_NEGATIVA, LOCALIZACAO, RESULTADO_NEGATIVO, ECOSISTEMAS]),
    ("Falta de {} gera {} colapso nos {} de {}.", [TECNOLOGIA, RESULTADO_NEGATIVO, ECOSISTEMAS, LOCALIZACAO]),
    ("Declínio de {} em {} atinge {}% das {} devido a {}.", [ECOSISTEMAS, LOCALIZACAO, NUMERO, ESPECIES_AMEACADAS, ACAO_AMBIENTAL_NEGATIVA]),
    ("Impacto de {} em {} causa {} deterioração dos {}.", [ACAO_AMBIENTAL_NEGATIVA, LOCALIZACAO, RESULTADO_NEGATIVO, ECOSISTEMAS]),
    ("Crise ambiental em {} se agrava com {} desmedida e {} dos {}.", [LOCALIZACAO, ACAO_AMBIENTAL_NEGATIVA, RESULTADO_NEGATIVO, ECOSISTEMAS]),
    ("Enchentes tem {} nas últimas semanas em ", [PALAVRAS_AUMENTO]),
    ("{} no nível do rio causa inundações", [PALAVRAS_AUMENTO]),
    ("Incidência de eventos climáticos extremos registra {} {} em razão de condições desfavoráveis", [PALAVRAS_AUMENTO, NUMERO]),
    ("Riscos ambientais em {} em áreas vulneráveis", [PALAVRAS_AUMENTO]),
    ("Ecossistemas comprometidos devido {} de eventos de risco", [PALAVRAS_AUMENTO]),
    ("Áreas protegidas sofrem com desastres ambientais", []),
    ("Ações como {} devastam {} hectares de biomas", [ACAO_AMBIENTAL_NEGATIVA, NUMERO]),
    ("Elevado risco de desastres atribuído à {}", [PALAVRA_DESASTRE]),
    ("Monitoramento revela {} de {}% nos eventos de risco", [PALAVRAS_AUMENTO, NUMERO]),
    ("Condições extremas agravam os {}", [PALAVRA_DESASTRE]),
    ("Comunidades próximas enfrentam risco devido à {}", [PALAVRA_DESASTRE]),
    ("Eventos de risco ameaçam {} espécies nativas", [NUMERO]),
    ("Principais causas dos desastres ambientais: {}", [CAUSAS]),
    ("Riscos ambientais se intensificam devido a {}", [CAUSAS]),
    ("Risco elevado de desastres por causa de {}", [PALAVRA_DESASTRE]),
    ("Biomas em perigo devido à {}", [ACAO_AMBIENTAL_NEGATIVA]),
    ("Desastres se agravam por conta de {}", [CAUSAS]),
    ("Aumento de eventos de risco impulsionado por {}", [CAUSAS]),
    ("Cerca de {}% dos desastres são ilegais e não controlados", [NUMERO]),
    ("Escassez de recursos eleva o risco de desastres por {}", [PALAVRA_DESASTRE]),
    ("Espécies ameaçadas sofrem {} com {} eventos de risco", [RESULTADO_NEGATIVO, NUMERO]),
    ("Descuido humano responde por {}% dos desastres", [NUMERO]),
    ("Áreas de proteção integral sofrem {} de {} hectares para desastres", [RESULTADO_NEGATIVO, NUMERO]),
    ("Comunidades indígenas sofrem com {} eventos de risco próximos", [NUMERO]),
    ("Poluição atinge níveis críticos após {} dias de desastres", [NUMERO]),
    ("Leis ambientais falham em {}% dos casos de {}", [NUMERO, ACAO_AMBIENTAL_NEGATIVA]),
    ("Invasões em terras públicas geram {} novos eventos de risco", [NUMERO]),
    ("Incidente acidental em áreas urbanas causa {} em {} construções", [RESULTADO_NEGATIVO, NUMERO]),
    ("Falta de recursos compromete o combate a desastres em {}", [PALAVRA_DESASTRE]),
    ("Ações como {} crescem {}% em áreas vulneráveis", [ACAO_AMBIENTAL_NEGATIVA, NUMERO]),
    ("Ciclo de desastres impede a recuperação de ecossistemas em {}", [PALAVRA_DESASTRE]),
    ("Acúmulo de resíduos causa {} de {}% no risco de desastres", [PALAVRAS_AUMENTO, NUMERO]),
    ("Deficiências em planos de contingência deixam {} comunidades vulneráveis", [NUMERO]),
    ("Condições climáticas extremas causam {} de {}% nos desastres", [PALAVRAS_AUMENTO, NUMERO]),
    ("Fatores climáticos intensos impulsionam {} eventos de risco", [NUMERO]),
    ("Eventos climáticos agravam o avanço dos desastres, causando {} de {}% nos riscos", [PALAVRAS_AUMENTO, NUMERO]),
    ("Equipes de emergência tentam conter desastres, mas os {} saem de controle", [PALAVRA_DESASTRE]),
    ("Riscos ambientais registram {}, porém a intervenção é insuficiente", [PALAVRAS_AUMENTO]),
    ("Desastres como {} se alastram rapidamente, contudo as medidas de segurança falham", [PALAVRA_DESASTRE]),
    ("Ação preventiva é implementada, entretanto os {} se dispersam sem controle", [PALAVRA_DESASTRE]),
    ("Medidas de contenção são tomadas, todavia os eventos de {} se expandem", [PALAVRA_DESASTRE]),
    ("Eventos de risco atingem patamar de {} recorde", [RESULTADO_NEGATIVO]),
    ("Ações como {} crescem em áreas protegidas", [ACAO_AMBIENTAL_NEGATIVA]),
    ("Riscos registram {} devido a condições climáticas extremas", [PALAVRAS_AUMENTO]),
    ("Áreas degradadas por desastres superam {} mil hectares", [NUMERO]),
    ("População local ameaçada por expansão de {}", [PALAVRA_DESASTRE]),
    ("Eventos de risco avançam para áreas urbanas, causando {} em vidas", [RESULTADO_NEGATIVO]),
    ("Poluição atinge nível crítico devido a {}", [PALAVRA_DESASTRE]),
    ("Controle de desastres é insuficiente para conter {}", [RESULTADO_NEGATIVO]),
    ("Risco de {} aumenta para espécies ameaçadas", [RESULTADO_NEGATIVO]),
    ("Ações como {} impulsionam eventos de risco", [ACAO_AMBIENTAL_NEGATIVA]),
    ("Biomas têm {} nos casos de desastres", [PALAVRAS_AUMENTO]),
]

# Frases positivas com metadados de tipo
positivas = [
    ("Queimadas controladas previnem {}% dos desastres", [NUMERO]),
    ("Intervenção rápida diminui {}% dos desastres ambientais.",[NUMERO]),
    ("Voluntários se unem para ajudar vítimas de {} .",[PALAVRA_DESASTRE]),
    ("Ação de {} salva {} espécies ameaçadas.",[ACAO_AMBIENTAL, NUMERO]),
    ("Recuperação de {} hectares de {} gera esperança.",[NUMERO, PALAVRA_DESASTRE]),
    ("Tecnologia de {} reduz emissões em {}% na indústria.",[TECNOLOGIA, NUMERO]),
    ("Número de {} aumenta {}% após programa de proteção.",[ECOSISTEMAS, NUMERO]),
    ("Projeto de {} com comunidades reduz {}% de {} .",[ACAO_AMBIENTAL, NUMERO, PALAVRA_DESASTRE]),
    ("Uso de {} reduz poluição em {} cidades.",[TECNOLOGIA, NUMERO]),
    ("População de {} alcança recuperação.",[LOCALIZACAO]),
    ("Iniciativa de {} recupera {} km de {} .", [ACAO_AMBIENTAL, NUMERO, PALAVRA_DESASTRE]),
    ("Voluntários se unem para ajudar vítimas de {}", [PALAVRA_DESASTRE]),
    ("Tecnologia {} captura {} toneladas de CO₂ anualmente.", [TECNOLOGIA, NUMERO]),
    ("Reflorestamento de {} hectares fortalece a preservação ambiental.", [NUMERO]),
    ("Iniciativa de {} aumenta {}% da biodiversidade local.", [ACAO_AMBIENTAL, NUMERO]),
    ("Tecnologia verde de {} reduz emissões em {}% no setor industrial.", [TECNOLOGIA, NUMERO]),
    ("Projeto de {} com comunidades eleva o desenvolvimento sustentável em {} cidades.", [ACAO_AMBIENTAL, NUMERO]),
    ("Recuperação de {} km² de habitats restaura o equilíbrio ecológico.", [NUMERO]),
    ("Parceria entre {} e {} impulsiona a conservação de {} hectares.", [LOCALIZACAO, ACAO_AMBIENTAL, NUMERO]),
    ("Investimento em energia renovável diminui custos em {}% no setor energético.", [NUMERO]),
    ("Educação ambiental em {} escolas fomenta a consciência ecológica.", [NUMERO]),
    ("Colaboração de {} resulta na restauração de {} áreas naturais.", [ACAO_AMBIENTAL, NUMERO]),
    ("Voluntários se unem para recuperar {} hectares de florestas nativas.", [NUMERO]),
    ("Níveis de {} estão caindo.", [ACAO_AMBIENTAL_NEGATIVA]),
    ("Bacia de {} em {} celebra {} graças a {} comprometida.", [ECOSISTEMAS, LOCALIZACAO, RESULTADO_POSITIVO, ACAO_AMBIENTAL]),
    ("Implantação de {} em {} impulsiona {} nos {}.", [TECNOLOGIA, LOCALIZACAO, RESULTADO_POSITIVO, ECOSISTEMAS]),
    ("Queima controlada de {} em {} gera {} renovação dos {}.", [ACAO_AMBIENTAL, LOCALIZACAO, RESULTADO_POSITIVO, ECOSISTEMAS]),
    ("Aumento de {} em {} resulta em {} crescimento dos {}.", [NUMERO, LOCALIZACAO, RESULTADO_POSITIVO, ECOSISTEMAS]),
    ("Atuação de {} em {} assegura {} preservação das {}.", [ACAO_AMBIENTAL, LOCALIZACAO, RESULTADO_POSITIVO, ESPECIES_AMEACADAS]),
    ("Presença de {} em {} promove {} recuperação dos {}.", [TECNOLOGIA, LOCALIZACAO, RESULTADO_POSITIVO, ECOSISTEMAS]),
    ("Expansão de {} em {} fomenta {} restauração dos {}.", [NUMERO, LOCALIZACAO, RESULTADO_POSITIVO, ECOSISTEMAS]),
    ("Iniciativa de {} em {} gera {} avanço na proteção dos {}.", [ACAO_AMBIENTAL, LOCALIZACAO, RESULTADO_POSITIVO, ECOSISTEMAS]),
    ("Redução de {} em {} reflete {} equilíbrio ecológico nos {}.", [TECNOLOGIA, LOCALIZACAO, RESULTADO_POSITIVO, ECOSISTEMAS]),
    ("Projeto de {} em {} alcança {} recuperação e harmonização dos {}.", [ACAO_AMBIENTAL, LOCALIZACAO, RESULTADO_POSITIVO, ECOSISTEMAS]),
    ("Empresas lançam campanha de arrecadação de alimentos para famílias carentes", []),
    ("Artistas se apresentam em show beneficente para ajudar instituições de caridade", []),
    ("Comunidades se mobilizam para construir casas para famílias desabrigadas", []),
    ("Jovens criam projeto social para ajudar moradores de rua", []),
    ("Idosos se reúnem para praticar atividades físicas e promover a saúde", []),
    ("Crianças aprendem sobre a importância da reciclagem em escola", []),
    ("Famílias se unem para plantar árvores e revitalizar praça", []),
    ("Vizinhos se organizam para promover a segurança no bairro", []),
    ("Medidas preventivas reduzem {}% dos riscos de desastres ambientais", [NUMERO]),
    ("Incidência de eventos climáticos extremos recua {}% em áreas vulneráveis" ,[NUMERO]),
    ("Plano de mitigação diminui o risco de assoreamento em {} rios" ,[NUMERO]),
    ("Áreas afetadas se recuperam após ações eficazes" ,[]),
    ("Equipes de emergência atuam com sucesso em {} eventos de inundação" ,[NUMERO]),
    ("Monitoramento eficiente reduz os riscos ambientais em {}%" ,[NUMERO]),
    ("Campanha de prevenção resulta em {}% menos incidentes ambientais" ,[NUMERO]),
    ("Tecnologia avançada auxilia no controle de {} desastres ambientais" ,[NUMERO]),
    ("Resposta rápida contém eventos de risco em apenas {} horas" ,[HORAS]),
    ("Proteção ambiental reforça a capacidade de resposta a emergências" ,[]),
    ("Estratégia preventiva reduz em {}% os riscos de desastres naturais" ,[NUMERO]),
    ("Intervenção rápida diminui {}% dos eventos climáticos extremos" ,[NUMERO]),
    ("Métodos inovadores amenizam os riscos ambientais em {}%" ,[NUMERO]),
    ("Ação coordenada controla desastres em {} regiões" ,[NUMERO]),
    ("Resposta eficaz conteve o desastre em {} horas" ,[HORAS]),
    ("Dados recentes apontam {} nos índices de desmatamento dos últimos meses" ,[PALAVRAS_BAIXA]),
    ("Eventos ambientais evidenciam {} nos últimos meses" ,[PALAVRAS_BAIXA]),
    ("Desastres naturais demonstram {} nos últimos meses" ,[PALAVRAS_BAIXA]),
    ("Incidentes ambientais registram {} nos últimos meses" ,[PALAVRAS_BAIXA]),
    ("Riscos no bioma indicam {} nos últimos meses" ,[PALAVRAS_BAIXA]),
    ("Ações comunitárias reduzem desastres em {} regiões" ,[NUMERO]),
    ("Tecnologia de previsão detecta riscos em apenas {} minutos" ,[NUMERO]),
    ("Políticas públicas diminuem o desmatamento em {}%" ,[NUMERO]),
    ("Recuperação de áreas degradadas devolve {} hectares ao ecossistema" ,[NUMERO]),
    ("Parceria com comunidades indígenas controla {} eventos de risco" ,[NUMERO]),
    ("Medidas preventivas evitam danos em {} hectares" ,[NUMERO]),
    ("Monitoramento via satélite reduz o tempo de resposta para {} horas" ,[HORAS]),
    ("Campanha educativa conscientiza {} comunidades sobre prevenção" ,[NUMERO]),
    ("Intervenção ambiental resulta em queda de {}% nos incidentes de risco" ,[NUMERO]),
    ("Ferramentas de inteligência artificial mapeiam {} riscos potenciais" ,[NUMERO]),
    ("Lei de proteção amplia as áreas seguras em {}%" ,[NUMERO]),
    ("Equipes de emergência contêm desastres em {} horas com equipamentos modernos" ,[HORAS]),
    ("Recuperação de nascentes reduz o risco de secas em {}%" ,[NUMERO]),
    ("Ações integradas elevam a segurança ambiental, reduzindo {} eventos de risco" ,[NUMERO]),
    ("Investimentos em prevenção demonstram {}% de melhoria na resposta a emergências" ,[NUMERO]),
    ("Riscos ambientais em queda, medidas de contenção mostram eficácia" ,[]),
    ("Prevenção controlada, monitoramento assegura a redução dos riscos" ,[]),
    ("Intervenção rápida previne a propagação de desastres, o bioma se mantém protegido" ,[]),
    ("Ação integrada reduz incidentes, índices de segurança melhoram" ,[]),
    ("Operação de combate é eficiente, resposta supera os desafios ambientais" ,[]),
    ("Eventos de risco caem drasticamente no bioma" ,[]),
    ("Controle eficaz diminui desastres em áreas protegidas" ,[]),
    ("Monitoramento previne a propagação de riscos ambientais" ,[]),
    ("Áreas degradadas recuperam-se graças a ações ambientais" ,[]),
    ("Tecnologia garante resposta rápida a eventos de risco" ,[]),
    ("Políticas públicas reduzem o desmatamento em {}%" ,[NUMERO]),
    ("População local adere a práticas sustentáveis contra desastres ambientais" ,[]),
    ("Medidas preventivas preservam a biodiversidade" ,[]),
    ("Intervenção rápida evita danos a comunidades vulneráveis" ,[]),
    ("{} de desastres ambientais é comemorada no bioma" ,[PALAVRAS_BAIXA]),
    ("Riscos ambientais em {}" ,[PALAVRAS_BAIXA]),
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
    ("Celebridade surpreende fãs com novo projeto artístico", []),
    ("Atleta conquista medalha de ouro em competição internacional", []),
    ("Cantor lança álbum inovador e alcança sucesso imediato", []),
    ("Estrela do cinema estreia filme que quebra recordes de bilheteria", []),
    ("Influenciador digital viraliza com dicas de estilo de vida", []),
    ("Jornalista revela detalhes inéditos dos bastidores de um programa de TV", []),
    ("Chef renomado inaugura restaurante com conceito revolucionário", []),
    ("Estilista apresenta coleção surpreendente em evento exclusivo", []),
    ("Polêmico muda completamente seu visual e gera repercussão", []),
    ("Cantora emociona público com performance ao vivo", []),
    ("Celebridade engaja causas sociais em campanha beneficente", []),
    ("Exclusivo: bastidores de um evento que reuniu os maiores nomes do entretenimento", []),
    ("Nova colaboração entre e promete agitar as paradas musicais", []),
    ("Reality show: participante se destaca com atitude inovadora", []),
    ("Empresário lança startup que promete revolucionar o mercado", []),
    ("Evento cultural reúne ícones da música e da arte em celebração única", []),
    ("Estrela do pop lança clipe surpreendente nas redes sociais", []),
    ("Apresentador divulga detalhes de seu próximo grande projeto", []),
    ("Celebridade marca presença em festa exclusiva com figuras internacionais", []),
    ("Entrevista reveladora: abre o jogo sobre sua vida pessoal e novos desafios", [])
]

# Gerar dados alternados
dados = []
for i in range(100):
    if i % 3 == 0:
        # Negativo (0)
        frase_template, tipos = random.choice(negativas)
        args = []
        for tipo in tipos:
            if (tipo == NUMERO):
                args.append(str(random.randint(10, 90)))
            elif (tipo == HORAS):
                args.append(str(random.randint(1, 24)))
            elif (tipo == ESPECIES_AMEACADAS):
                args.append(random.choice(ESPECIES_AMEACADAS))
            elif (tipo == LOCALIZACAO):
                args.append(random.choice(LOCALIZACAO))
            elif (tipo == ECOSISTEMAS):
                args.append(random.choice(ECOSISTEMAS))
            elif (tipo == TECNOLOGIA):
                args.append(random.choice(TECNOLOGIA))
            elif (tipo == PALAVRA_DESASTRE):
                args.append(random.choice(PALAVRA_DESASTRE))
            elif (tipo == ACAO_AMBIENTAL):
                args.append(random.choice(ACAO_AMBIENTAL))
            elif (tipo == ACAO_AMBIENTAL_NEGATIVA):
                args.append(random.choice(ACAO_AMBIENTAL_NEGATIVA))
            elif (tipo == RESULTADO_NEGATIVO):
                args.append(random.choice(RESULTADO_NEGATIVO))
            elif (tipo == RESULTADO_POSITIVO):
                args.append(random.choice(RESULTADO_POSITIVO))
            elif (tipo == PALAVRAS_AUMENTO):
                args.append(random.choice(PALAVRAS_AUMENTO))
            elif (tipo == PALAVRAS_BAIXA):
                args.append(random.choice(PALAVRAS_BAIXA))
            elif (tipo == CAUSAS):
                args.append(random.choice(CAUSAS))
        
        # Verifica se o número de argumentos corresponde ao número de placeholders
        if len(args) == frase_template.count("{}"):
            # Formatar a frase
            frase = frase_template.format(*args)
            dados.append({"title": frase, "date": None, "url": None, "content": frase, "class": 0})
        else:
            print(f"Erro: número de argumentos ({len(args)}) não corresponde ao número de placeholders na frase: '{frase_template}'")
    elif i % 3 == 1:
        frase_template, tipos = random.choice(positivas)
        args = []
        for tipo in tipos:
            if (tipo == NUMERO):
                args.append(str(random.randint(10, 90)))
            elif (tipo == HORAS):
                args.append(str(random.randint(1, 24)))
            elif (tipo == ESPECIES_AMEACADAS):
                args.append(random.choice(ESPECIES_AMEACADAS))
            elif (tipo == LOCALIZACAO):
                args.append(random.choice(LOCALIZACAO))
            elif (tipo == ECOSISTEMAS):
                args.append(random.choice(ECOSISTEMAS))
            elif (tipo == TECNOLOGIA):
                args.append(random.choice(TECNOLOGIA))
            elif (tipo == PALAVRA_DESASTRE):
                args.append(random.choice(PALAVRA_DESASTRE))
            elif (tipo == ACAO_AMBIENTAL):
                args.append(random.choice(ACAO_AMBIENTAL))
            elif (tipo == ACAO_AMBIENTAL_NEGATIVA):
                args.append(random.choice(ACAO_AMBIENTAL_NEGATIVA))
            elif (tipo == RESULTADO_NEGATIVO):
                args.append(random.choice(RESULTADO_NEGATIVO))
            elif (tipo == RESULTADO_POSITIVO):
                args.append(random.choice(RESULTADO_POSITIVO))
            elif (tipo == PALAVRAS_AUMENTO):
                args.append(random.choice(PALAVRAS_AUMENTO))
            elif (tipo == PALAVRAS_BAIXA):
                args.append(random.choice(PALAVRAS_BAIXA))
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
df.to_csv("APS/gerar_dados/data_sintetica.csv", index=False)
print("Dados gerados com sucesso em data.csv")