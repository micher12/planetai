import pandas as pd
import random

# Definindo tipos de dados para cada placeholder
NUMERO = 'number'
CAUSAS = [
    "ações humanas",
    "negligência",
    "descuidos ambientais",
    "práticas agrícolas inadequadas",
    "falta de fiscalização",
    "desmatamento criminoso",
    "poluição industrial",
    "urbanização desordenada",
    "exploração excessiva de recursos",
    "mudanças climáticas",
    "poluição por plásticos",
    "emissões veiculares",
    "mineração ilegal",
    "espécies invasoras",
    "pesca predatória",
    "queimadas ilegais",
    "consumo excessivo",
    "gestão inadequada de água",
    "falta de conscientização ambiental",
    "políticas insuficientes",
    "ganância corporativa",
    "crescimento populacional",
    "degradação do solo",
    "acidificação oceânica",
    "turismo excessivo",
    "uso excessivo de agrotóxicos",
    "dependência de combustíveis fósseis",
    "tráfico de animais",
    "poluição generalizada",
    "falta de reciclagem",
    "negação climática",
    "conflitos armados",
    "gestão inadequada de resíduos",
    "corrupção ambiental",
    "monoculturas",
    "esgotamento de recursos",
    "acidentes industriais",
    "sobrepovoamento",
    "práticas culturais danosas",
    "perda de biodiversidade",
    "sobrepastejo",
    "expansão urbana irregular",
    "poluição sonora e luminosa",
    "lixo eletrônico",
    "consumo excessivo de moda",
    "construção de hidrelétricas",
    "falta de investimento em renováveis",
    "uso excessivo de plástico",
    "sobre-exploração de aquíferos",
    "legislação ambiental frágil",
    "pecuária intensiva",
    "irrigação ineficiente",
    "planejamento urbano inadequado",
    "dependência industrial de fósseis",
    "falta de cooperação global"
]
HORAS = 'hours'  # Para frases que exigem tempo em horas
ESPECIES_AMEACADAS = ["tigres", "baleias", "pandas", "corais", "veados-camelo"]
LOCALIZACAO = ["Amazônia", "manguezais", "florestas tropicais", "oceano Pacífico", "região amazônica"]
RESULTADO_POSITIVO = ["recuperação", "melhoria", "crescimento", "preservação", "redução", "sucesso", "avanço", "aumento", "proteção", "revitalização"]
ECOSISTEMAS = ["rios", "parques nacionais", "matas ciliares", "ecossistemas costeiros"]
TECNOLOGIA = ["energia solar", "energia eólica", "hidrogênio verde", "captura de carbono", "veículos elétricos", "biocombustíveis", "tecnologia de reciclagem", "sistemas de irrigação sustentável", "sensores ambientais"]
PALAVRA_DESASTRE = ["enchentes", "incêndios florestais", "deslizamentos", "secas", "desmatamento", "inundações", "tempestades", "tsunamis", "desastres ambientais","inundamento","Contaminação hídrica","Contaminação atmosférica","Erosão do solo",]
ACAO_AMBIENTAL = ["reflorestamento", "reciclagem", "energia renovável", "redução de plásticos", "proteção de espécies", "combate a poluição", "conservação de ecossistemas", "plantio de árvores", "redução de emissões", "uso sustentável de recursos"]
ACAO_AMBIENTAL_NEGATIVA = ["enchentes","desmatamento ilegal", "poluição industrial", "exploração predatória", "queimadas ilegais", "descarte inadequado", "desregulamentação ambiental", "Derramamento de óleo", "Despejo de resíduos tóxicos","Extração mineral predatória","Poluição sonora"]
RESULTADO_NEGATIVO = ["destruição", "declínio", "colapso", "extinção", "desaparecimento"]
PALAVRAS_AUMENTO = ["aumento","elevação","acrescimo","alta"]
PALAVRAS_BAIXA = ["queda", "redução", "diminuição", "declínio", "baixa", "abatimento"]

# Frases negativas com metadados de tipo
negativas = [
    ("Os {} em {} sofrem {} devido a {}.", [ECOSISTEMAS, LOCALIZACAO, RESULTADO_NEGATIVO, ACAO_AMBIENTAL_NEGATIVA]),
    ("A poluição por falta de {} afeta {} cidades.", [TECNOLOGIA, NUMERO]),
    ("O número de {} em {} cai em {}%.", [ECOSISTEMAS, LOCALIZACAO, NUMERO]),
    ("O projeto de {} falha, aumentando {}% de {}.", [ACAO_AMBIENTAL, NUMERO, PALAVRA_DESASTRE]),
    ("A população de {} desaparece em {}.", [ESPECIES_AMEACADAS, LOCALIZACAO]),
    ("A contaminação por {} atinge {}% da área de {}.", [ACAO_AMBIENTAL_NEGATIVA, NUMERO, LOCALIZACAO]),
    ("Os {} em {} enfrentam {} após {}.", [ECOSISTEMAS, LOCALIZACAO, RESULTADO_NEGATIVO, ACAO_AMBIENTAL_NEGATIVA]),
    ("O desmatamento em {} desencadeia {} nos {}.", [LOCALIZACAO, RESULTADO_NEGATIVO, ECOSISTEMAS]),
    ("A falta de {} agrava o {} dos {} em {}.", [TECNOLOGIA, RESULTADO_NEGATIVO, ECOSISTEMAS, LOCALIZACAO]),
    ("O número de {} em {} despenca {}% por conta de {} desenfreada.", [ECOSISTEMAS, LOCALIZACAO, NUMERO, ACAO_AMBIENTAL_NEGATIVA]),
    ("A ameaça às {} sobe {}% em {} após {} sem controle.", [ESPECIES_AMEACADAS, NUMERO, LOCALIZACAO, ACAO_AMBIENTAL_NEGATIVA]),
    ("Devido à {}, ocorre {} nos {} da região de {}.", [ACAO_AMBIENTAL_NEGATIVA, RESULTADO_NEGATIVO, ECOSISTEMAS, LOCALIZACAO]),
    ("O declínio de {} em {} atinge {}% após {} persistente.", [ECOSISTEMAS, LOCALIZACAO, NUMERO, ACAO_AMBIENTAL_NEGATIVA]),
    ("A crise de {} se agrava em {} com {} descontrolada.", [ECOSISTEMAS, LOCALIZACAO, ACAO_AMBIENTAL_NEGATIVA]),
    ("A contaminação por {} eleva {}% da área dos {} em {}.", [ACAO_AMBIENTAL_NEGATIVA, NUMERO, ECOSISTEMAS, LOCALIZACAO]),
    ("A perda de {} em {} soma {}% e coloca {} em risco.", [ECOSISTEMAS, LOCALIZACAO, NUMERO, ESPECIES_AMEACADAS]),
    ("Os {} em {} colapsam após {} de {} sem intervenção.", [ECOSISTEMAS, LOCALIZACAO, RESULTADO_NEGATIVO, ACAO_AMBIENTAL_NEGATIVA]),
    ("A bacia de {} em {} sofre {} devido a {} irresponsável.", [ECOSISTEMAS, LOCALIZACAO, RESULTADO_NEGATIVO, ACAO_AMBIENTAL_NEGATIVA]),
    ("A falta de {} em {} impulsiona {} nos {}.", [TECNOLOGIA, LOCALIZACAO, RESULTADO_NEGATIVO, ECOSISTEMAS]),
    ("A {} em {} gera um {} devastador nos {}.", [ACAO_AMBIENTAL_NEGATIVA, LOCALIZACAO, RESULTADO_NEGATIVO, ECOSISTEMAS]),
    ("A queda de {} intensifica o {} dos {} em {}.", [NUMERO, RESULTADO_NEGATIVO, ECOSISTEMAS, LOCALIZACAO]),
    ("A atuação de {} agrava o {} em {} e reduz {}% das {}.", [ACAO_AMBIENTAL_NEGATIVA, RESULTADO_NEGATIVO, LOCALIZACAO, NUMERO, ESPECIES_AMEACADAS]),
    ("A ausência de {} em {} resulta em {} dos {}.", [TECNOLOGIA, LOCALIZACAO, RESULTADO_NEGATIVO, ECOSISTEMAS]),
    ("O aumento de {} em {} acarreta um agravamento de {}.", [NUMERO, LOCALIZACAO, PALAVRA_DESASTRE]),
    ("A poluição por {} em {} provoca {} contaminação nos {}.", [TECNOLOGIA, LOCALIZACAO, RESULTADO_NEGATIVO, ECOSISTEMAS]),
    ("A desorganização de {} em {} leva a um {} declínio dos {}.", [ACAO_AMBIENTAL_NEGATIVA, LOCALIZACAO, RESULTADO_NEGATIVO, ECOSISTEMAS]),
    ("A falta de fiscalização em {} eleva {}% de {} devido a {}.", [LOCALIZACAO, NUMERO, PALAVRA_DESASTRE, ACAO_AMBIENTAL_NEGATIVA]),
    ("A fragmentação de {} em {} ocasiona a {} extinção das {}.", [ECOSISTEMAS, LOCALIZACAO, RESULTADO_NEGATIVO, ESPECIES_AMEACADAS]),
    ("A infestação de {} em {} desencadeia {} nos {}.", [PALAVRA_DESASTRE, LOCALIZACAO, RESULTADO_NEGATIVO, ECOSISTEMAS]),
    ("O acúmulo de {} em {} intensifica {} dos {}.", [TECNOLOGIA, LOCALIZACAO, RESULTADO_NEGATIVO, ECOSISTEMAS]),
    ("O rompimento de uma barragem em {} acarreta {} perda dos {}.", [LOCALIZACAO, RESULTADO_NEGATIVO, ECOSISTEMAS]),
    ("O crescimento de {} em {} piora {} dos {} locais.", [NUMERO, LOCALIZACAO, RESULTADO_NEGATIVO, ECOSISTEMAS]),
    ("A ação de {} em {} resulta em {} desastrosos para os {}.", [ACAO_AMBIENTAL_NEGATIVA, LOCALIZACAO, RESULTADO_NEGATIVO, ECOSISTEMAS]),
    ("A falta de {} em {} gera {} nos {}.", [TECNOLOGIA, LOCALIZACAO, RESULTADO_NEGATIVO, ECOSISTEMAS]),
    ("O declínio de {} em {} atinge {}% das {} devido a {}.", [ECOSISTEMAS, LOCALIZACAO, NUMERO, ESPECIES_AMEACADAS, ACAO_AMBIENTAL_NEGATIVA]),
    ("O impacto de {} em {} causa uma {} deterioração dos {}.", [ACAO_AMBIENTAL_NEGATIVA, LOCALIZACAO, RESULTADO_NEGATIVO, ECOSISTEMAS]),
    ("A crise ambiental em {} se agrava com {} desmedida e {} dos {}.", [LOCALIZACAO, ACAO_AMBIENTAL_NEGATIVA, RESULTADO_NEGATIVO, ECOSISTEMAS]),
    ("As enchentes apresentaram {} nas últimas semanas.", [PALAVRAS_AUMENTO]),
    ("O {} no nível do rio causa inundações.", [PALAVRAS_AUMENTO]),
    ("A incidência de eventos climáticos extremos registra {} {} em razão de condições desfavoráveis.", [PALAVRAS_AUMENTO, NUMERO]),
    ("Os riscos ambientais se intensificam com {} em áreas vulneráveis.", [PALAVRAS_AUMENTO]),
    ("Ecossistemas comprometidos devido a {} de eventos de risco.", [PALAVRAS_AUMENTO]),
    ("Áreas protegidas sofrem com desastres ambientais.", []),
    ("Ações como {} devastam {} hectares de biomas.", [ACAO_AMBIENTAL_NEGATIVA, NUMERO]),
    ("Elevado risco de desastres atribuído a {}.", [PALAVRA_DESASTRE]),
    ("O monitoramento revela {} de {}% nos eventos de risco.", [PALAVRAS_AUMENTO, NUMERO]),
    ("Condições extremas agravam os {}.", [PALAVRA_DESASTRE]),
    ("Comunidades próximas enfrentam risco devido a {}.", [PALAVRA_DESASTRE]),
    ("Eventos de risco ameaçam {} espécies nativas.", [NUMERO]),
    ("Comunidades locais solicitam ajuda devido à {}",[CAUSAS]),
    ("Principais causas dos desastres ambientais são: {}.", [CAUSAS]),
    ("Os riscos ambientais se intensificam devido a {}.", [CAUSAS]),
    ("Risco elevado de desastres por causa de {}.", [PALAVRA_DESASTRE]),
    ("Biomas estão em perigo devido a {}.", [ACAO_AMBIENTAL_NEGATIVA]),
    ("Os desastres se agravam por conta de {}.", [CAUSAS]),
    ("O aumento de eventos de risco é impulsionado por {}.", [CAUSAS]),
    ("Cerca de {}% dos desastres são ilegais e não controlados.", [NUMERO]),
    ("A escassez de recursos eleva o risco de desastres devido a {}.", [PALAVRA_DESASTRE]),
    ("Espécies ameaçadas sofrem {} com {} eventos de risco.", [RESULTADO_NEGATIVO, NUMERO]),
    ("O descuido humano responde por {}% dos desastres.", [NUMERO]),
    ("Áreas de proteção integral sofrem {} de {} hectares devido a desastres.", [RESULTADO_NEGATIVO, NUMERO]),
    ("Comunidades indígenas sofrem com {} eventos de risco próximos.", [NUMERO]),
    ("A poluição atinge níveis críticos após {} dias de desastres.", [NUMERO]),
    ("As leis ambientais falham em {}% dos casos de {}.", [NUMERO, ACAO_AMBIENTAL_NEGATIVA]),
    ("Invasões em terras públicas geram {} novos eventos de risco.", [NUMERO]),
    ("Um incidente acidental em áreas urbanas causa {} em {} comunidades.", [RESULTADO_NEGATIVO, NUMERO]),
    ("A falta de recursos compromete o combate aos desastres causados por {}.", [PALAVRA_DESASTRE]),
    ("Ações como {} crescem {}% em áreas vulneráveis.", [ACAO_AMBIENTAL_NEGATIVA, NUMERO]),
    ("O ciclo de desastres impede a recuperação dos ecossistemas afetados por {}.", [PALAVRA_DESASTRE]),
    ("O acúmulo de resíduos causa {} de {}% no risco de desastres.", [PALAVRAS_AUMENTO, NUMERO]),
    ("As deficiências em planos de contingência deixam {} comunidades vulneráveis.", [NUMERO]),
    ("Condições climáticas extremas causam {} de {}% nos desastres.", [PALAVRAS_AUMENTO, NUMERO]),
    ("Fatores climáticos intensos impulsionam {} eventos de risco.", [NUMERO]),
    ("Eventos climáticos agravam o avanço dos desastres, causando {} de {}% nos riscos.", [PALAVRAS_AUMENTO, NUMERO]),
    ("Equipes de emergência tentam conter desastres, mas os {} saem de controle.", [PALAVRA_DESASTRE]),
    ("Os riscos ambientais registram {} devido a condições climáticas extremas.", [PALAVRAS_AUMENTO]),
    ("Os desastres como {} se alastram rapidamente, contudo as medidas de segurança falham.", [PALAVRA_DESASTRE]),
    ("Uma ação preventiva é implementada, entretanto os {} se dispersam sem controle.", [PALAVRA_DESASTRE]),
    ("Medidas de contenção são tomadas, todavia os eventos de {} se expandem.", [PALAVRA_DESASTRE]),
    ("Eventos de risco atingem um patamar de {} recorde.", [RESULTADO_NEGATIVO]),
    ("Ações como {} crescem em áreas protegidas.", [ACAO_AMBIENTAL_NEGATIVA]),
    ("Os riscos registram {} devido a condições climáticas extremas.", [PALAVRAS_AUMENTO]),
    ("Áreas degradadas por desastres superam {} mil hectares.", [NUMERO]),
    ("A população local é ameaçada pela expansão de {}.", [PALAVRA_DESASTRE]),
    ("Eventos de risco avançam para áreas urbanas, causando {} em vidas.", [RESULTADO_NEGATIVO]),
    ("A poluição atinge nível crítico devido a {}.", [PALAVRA_DESASTRE]),
    ("O controle de desastres é insuficiente para conter {}.", [RESULTADO_NEGATIVO]),
    ("O risco de {} aumenta para as espécies ameaçadas.", [RESULTADO_NEGATIVO]),
    ("Ações como {} impulsionam eventos de risco.", [ACAO_AMBIENTAL_NEGATIVA]),
    ("Os biomas apresentam {} nos casos de desastres.", [PALAVRAS_AUMENTO]),
    ("Industria que não utilizam {} intensifica {} e desencadeia {} de debates sobre a degradação ambiental.", [ACAO_AMBIENTAL, CAUSAS, PALAVRAS_AUMENTO]),
    ("Iniciativa de {} que acabou ocasionando impactos ambientais e intensifica {} e desencadeia {} de debates sobre a rejeição.", [ACAO_AMBIENTAL, CAUSAS, PALAVRAS_AUMENTO]),
    ("Programa que promovia {} na verdade não compria com o que era previsto.", [ACAO_AMBIENTAL]),
]

# Frases positivas com metadados de tipo
positivas = [
    ("Queimadas controladas previnem {}% dos focos de incêndio.", [NUMERO]),
    ("A intervenção rápida diminui {}% dos desastres ambientais.", [NUMERO]),
    ("Voluntários se unem para ajudar as vítimas de {}.", [PALAVRA_DESASTRE]),
    ("A ação de {} salva {} espécies ameaçadas.", [ACAO_AMBIENTAL, NUMERO]),
    ("A recuperação de {} hectares de {} gera esperança.", [NUMERO, PALAVRA_DESASTRE]),
    ("A tecnologia de {} reduz as emissões em {}% na indústria.", [TECNOLOGIA, NUMERO]),
    ("O número de {} aumenta {}% após um programa de proteção.", [ECOSISTEMAS, NUMERO]),
    ("O projeto de {} com as comunidades reduz {}% de {}.", [ACAO_AMBIENTAL, NUMERO, PALAVRA_DESASTRE]),
    ("O uso de {} reduz a poluição em {} cidades.", [TECNOLOGIA, NUMERO]),
    ("A população de {} alcança a recuperação.", [LOCALIZACAO]),
    ("A iniciativa de {} recupera {} km de {}.", [ACAO_AMBIENTAL, NUMERO, PALAVRA_DESASTRE]),
    ("Voluntários se unem para ajudar as vítimas de {}.", [PALAVRA_DESASTRE]),
    ("A tecnologia {} captura {} toneladas de CO₂ anualmente.", [TECNOLOGIA, NUMERO]),
    ("O reflorestamento de {} hectares fortalece a preservação ambiental.", [NUMERO]),
    ("A iniciativa de {} aumenta {}% da biodiversidade local.", [ACAO_AMBIENTAL, NUMERO]),
    ("A tecnologia verde de {} reduz as emissões em {}% no setor industrial.", [TECNOLOGIA, NUMERO]),
    ("O projeto de {} com as comunidades eleva o desenvolvimento sustentável em {} cidades.", [ACAO_AMBIENTAL, NUMERO]),
    ("A recuperação de {} km² de habitats restaura o equilíbrio ecológico.", [NUMERO]),
    ("A parceria entre {} e {} impulsiona a conservação de {} hectares.", [LOCALIZACAO, ACAO_AMBIENTAL, NUMERO]),
    ("O investimento em energia renovável diminui os custos em {}% no setor energético.", [NUMERO]),
    ("A educação ambiental em {} escolas fomenta a consciência ecológica.", [NUMERO]),
    ("A colaboração de {} resulta na restauração de {} áreas naturais.", [ACAO_AMBIENTAL, NUMERO]),
    ("Voluntários se unem para recuperar {} hectares de florestas nativas.", [NUMERO]),
    ("Os níveis de {} estão em queda.", [ACAO_AMBIENTAL_NEGATIVA]),
    ("A bacia de {} em {} celebra {} graças à {} comprometida.", [ECOSISTEMAS, LOCALIZACAO, RESULTADO_POSITIVO, ACAO_AMBIENTAL]),
    ("A implantação de {} em {} impulsiona {} nos {}.", [TECNOLOGIA, LOCALIZACAO, RESULTADO_POSITIVO, ECOSISTEMAS]),
    ("A queima controlada de {} em {} promove {} renovação dos {}.", [ACAO_AMBIENTAL, LOCALIZACAO, RESULTADO_POSITIVO, ECOSISTEMAS]),
    ("O aumento de {} em {} resulta em {} crescimento dos {}.", [NUMERO, LOCALIZACAO, RESULTADO_POSITIVO, ECOSISTEMAS]),
    ("A atuação de {} em {} assegura {} preservação das {}.", [ACAO_AMBIENTAL, LOCALIZACAO, RESULTADO_POSITIVO, ESPECIES_AMEACADAS]),
    ("A presença de {} em {} promove {} recuperação dos {}.", [TECNOLOGIA, LOCALIZACAO, RESULTADO_POSITIVO, ECOSISTEMAS]),
    ("A expansão de {} em {} fomenta {} restauração dos {}.", [NUMERO, LOCALIZACAO, RESULTADO_POSITIVO, ECOSISTEMAS]),
    ("A iniciativa de {} em {} gera {} avanço na proteção dos {}.", [ACAO_AMBIENTAL, LOCALIZACAO, RESULTADO_POSITIVO, ECOSISTEMAS]),
    ("A redução de {} em {} reflete {} equilíbrio ecológico nos {}.", [TECNOLOGIA, LOCALIZACAO, RESULTADO_POSITIVO, ECOSISTEMAS]),
    ("O projeto de {} em {} alcança {} recuperação e harmonização dos {}.", [ACAO_AMBIENTAL, LOCALIZACAO, RESULTADO_POSITIVO, ECOSISTEMAS]),
    ("Comunidades se mobilizam para construir casas para famílias desabrigadas por enchentes.", []),
    ("Crianças aprendem sobre a importância da reciclagem nas escolas.", []),
    ("Famílias se unem para plantar árvores e revitalizar praças.", []),
    ("Medidas preventivas reduzem {}% dos riscos de desastres ambientais.", [NUMERO]),
    ("A incidência de eventos climáticos extremos recua {}% em áreas vulneráveis.", [NUMERO]),
    ("O plano de mitigação diminui o risco de assoreamento em {} rios.", [NUMERO]),
    ("As áreas afetadas se recuperam após ações eficazes.", []),
    ("Equipes de emergência atuam com sucesso em {} eventos de inundação.", [NUMERO]),
    ("O monitoramento eficiente reduz os riscos ambientais em {}%.", [NUMERO]),
    ("A campanha de prevenção resulta em {}% menos incidentes ambientais.", [NUMERO]),
    ("A tecnologia avançada auxilia no controle de {} desastres ambientais.", [NUMERO]),
    ("A resposta rápida contém eventos de risco em apenas {} horas.", [HORAS]),
    ("A proteção ambiental reforça a capacidade de resposta a emergências.", []),
    ("A estratégia preventiva reduz em {}% os riscos de desastres naturais.", [NUMERO]),
    ("A intervenção rápida diminui {}% dos eventos climáticos extremos.", [NUMERO]),
    ("Métodos inovadores amenizam os riscos ambientais em {}%.", [NUMERO]),
    ("A ação coordenada controla os desastres em {} regiões.", [NUMERO]),
    ("A resposta eficaz conteve o desastre em {} horas.", [HORAS]),
    ("Dados recentes apontam {} nos índices de desmatamento dos últimos meses.", [PALAVRAS_BAIXA]),
    ("Eventos ambientais evidenciam {} nos últimos meses.", [PALAVRAS_BAIXA]),
    ("Desastres naturais demonstram {} nos últimos meses.", [PALAVRAS_BAIXA]),
    ("Incidentes ambientais registram {} nos últimos meses.", [PALAVRAS_BAIXA]),
    ("Os riscos no bioma indicam {} nos últimos meses.", [PALAVRAS_BAIXA]),
    ("Ações comunitárias reduzem os desastres em {} regiões.", [NUMERO]),
    ("A tecnologia de previsão detecta riscos em apenas {} minutos.", [NUMERO]),
    ("As políticas públicas diminuem o desmatamento em {}%.", [NUMERO]),
    ("A recuperação de áreas degradadas devolve {} hectares ao ecossistema.", [NUMERO]),
    ("A parceria com comunidades indígenas controla {} eventos de risco.", [NUMERO]),
    ("Medidas preventivas evitam danos em {} hectares.", [NUMERO]),
    ("O monitoramento via satélite reduz o tempo de resposta para {} horas.", [HORAS]),
    ("A campanha educativa conscientiza {} comunidades sobre prevenção.", [NUMERO]),
    ("A intervenção ambiental resulta em queda de {}% nos incidentes de risco.", [NUMERO]),
    ("Ferramentas de inteligência artificial mapeiam {} riscos potenciais.", [NUMERO]),
    ("A lei de proteção amplia as áreas seguras em {}%.", [NUMERO]),
    ("Equipes de emergência contêm desastres em {} horas com equipamentos modernos.", [HORAS]),
    ("A recuperação de nascentes reduz o risco de secas em {}%.", [NUMERO]),
    ("Ações integradas elevam a segurança ambiental, reduzindo {} eventos de risco.", [NUMERO]),
    ("Investimentos em prevenção demonstram {}% de melhoria na resposta a emergências.", [NUMERO]),
    ("Os riscos ambientais estão em {}, e as medidas de contenção mostram eficácia.", [PALAVRAS_BAIXA]),
    ("A prevenção controlada e o monitoramento asseguram a redução dos riscos.", []),
    ("A intervenção rápida previne a propagação de desastres, e o bioma se mantém protegido.", []),
    ("A operação de combate é eficiente, e a resposta supera os desafios ambientais.", []),
    ("Eventos de risco estão em {} no bioma.", [PALAVRAS_BAIXA]),
    ("O controle eficaz diminui os desastres em áreas protegidas.", []),
    ("O monitoramento previne a propagação de riscos ambientais.", []),
    ("Áreas degradadas recuperam-se graças a ações ambientais.", []),
    ("A tecnologia garante uma resposta rápida a eventos de risco.", []),
    ("As políticas públicas reduzem o desmatamento em {}%.", [NUMERO]),
    ("A população local adere a práticas sustentáveis contra desastres ambientais.", []),
    ("Medidas preventivas preservam a biodiversidade.", []),
    ("A intervenção rápida evita danos a comunidades vulneráveis.", []),
    ("A {} de desastres ambientais é comemorada no bioma.", [PALAVRAS_BAIXA]),
    ("Os riscos ambientais estão em {}.", [PALAVRAS_BAIXA]),
    ("Projeto de {} ajuda bioma afetado por {} e já apresenta {} de vegetação", [ACAO_AMBIENTAL,CAUSAS, PALAVRAS_AUMENTO]),
    ("Projeto de reflorestamento neutraliza {} e já apresenta {} de regeneração da vegetação.", [CAUSAS, PALAVRAS_AUMENTO]),
    ("Iniciativa de recuperação ambiental transforma {} em estímulo para o bioma, registrando {} de crescimento da biodiversidade.", [ACAO_AMBIENTAL_NEGATIVA, PALAVRAS_AUMENTO]),
    ("Programa de restauração reverte os efeitos de {} e promove {} de revitalização dos ecossistemas.", [CAUSAS, PALAVRAS_AUMENTO]),
    ("Ação coordenada converte {} em oportunidade, resultando em {} de avanço ecológico.", [ACAO_AMBIENTAL_NEGATIVA, PALAVRAS_AUMENTO]),
    ("Parceria entre governo e comunidades transforma {} em catalisador para a recuperação ambiental, atingindo {} de melhoria nos habitats.", [CAUSAS, PALAVRAS_AUMENTO]),
    ("Projeto inovador neutraliza {} e alcança {} de regeneração na fauna e flora.", [ACAO_AMBIENTAL_NEGATIVA, PALAVRAS_AUMENTO]),
    ("Intervenção sustentável reverte {} e já apresenta {} de revitalização nos ecossistemas urbanos.", [CAUSAS, PALAVRAS_AUMENTO]),
    ("Aumento de vigilancia resuslta em {} de {} sobre meio ambiente", [PALAVRAS_BAIXA, CAUSAS]),
    ("A intensificação do monitoramento ambiental conduz a {} de {} que afetam os ecossistemas.", [PALAVRAS_BAIXA, CAUSAS]),
    ("A melhoria na vigilância ecológica promove {} de {} prejudiciais à natureza.", [PALAVRAS_BAIXA, CAUSAS]),
    ("O reforço das inspeções ambientais gera {} de {} impactando a sustentabilidade dos biomas.", [PALAVRAS_BAIXA, CAUSAS]),
    ("A ampliação do controle ambiental ocasiona {} de {} e contribui para a preservação dos ecossistemas.", [PALAVRAS_BAIXA, CAUSAS]),
    ("Grupo de voluntários planta 10 mil árvores em área degradada", []),
]

# Frases irrelevantes
irrelevantes = [
    ("Ator famoso anuncia novo projeto cinematográfico", []),
    ("Time de futebol vence campeonato estadual com atuação brilhante", []),
    ("Nova coleção de moda estreia nas passarelas de Milão", []),
    ("Cantora lança single que já conquista as paradas de sucesso", []),
    ("Empresário revela estratégia inovadora para expansão de mercado", []),
    ("Celebridade compartilha sua rotina de treinos e dieta saudável", []),
    ("Festival de música reúne milhares de fãs em celebração à arte", []),
    ("Jogador de basquete se destaca em partida decisiva da temporada", []),
    ("Banda renomada anuncia turnê mundial após longa pausa", []),
    ("Tecnologia de ponta revoluciona o setor de telecomunicações", []),
    ("Novo lançamento de smartphone atrai a atenção dos consumidores", []),
    ("Editor premiado publica livro sobre história da literatura", []),
    ("Estrela da TV participa de reality show de competição", []),
    ("Celebridade revela segredos dos bastidores da indústria do entretenimento", []),
    ("Estudo sobre economia global aponta crescimento em mercados emergentes", []),
    ("Crítico de cinema elogia filme de suspense por sua originalidade", []),
    ("Evento gastronômico apresenta diversidade de sabores internacionais", []),
    ("Influenciador digital compartilha dicas de moda e estilo", []),
    ("Atleta olímpico conquista medalha de ouro em competição internacional", []),
    ("Startup brasileira desenvolve aplicativo para educação financeira", []),
    ("Ator ganha prêmio de melhor performance em festival de teatro", []),
    ("Marca de cosméticos lança linha sustentável com ingredientes naturais", []),
    ("Cientistas descobrem nova espécie de ave na Amazônia", []),
    ("Filme nacional é selecionado para competir no Festival de Cannes", []),
    ("Empresa de energia anuncia projeto pioneiro de energia solar em comunidades rurais", []),
    ("Youtuber ultrapassa 10 milhões de inscritos com conteúdo educativo", []),
    ("Restaurante inova com menu inspirado na culinária ancestral indígena", []),
    ("Atleta paralímpico bate recorde mundial em prova de velocidade", []),
    ("Série documental revela histórias desconhecidas da história brasileira", []),
    ("Instituto de pesquisa lança plataforma gratuita de cursos de programação", []),
    ("Bailarina brasileira é destaque em companhia de dança internacional", []),
    ("Feira de arte contemporânea reúne artistas de 20 países em São Paulo", []),
    ("Aplicativo de mobilidade urbana ganha prêmio de inovação global", []),
    ("Escritor lança romance que aborda questões climáticas e futuro da Terra", []),
    ("DJ brasileiro alcança topo da lista de melhores do mundo pela primeira vez", []),
    ("Hospital inaugura centro de pesquisa para tratamento de doenças raras", []),
    ("Marca de calçados adota tecnologia 3D para customização de produtos", []),
    ("Fotógrafo vence concurso internacional com imagem da vida selvagem", []),
    ("Escola pública implementa projeto de robótica que vira referência nacional", []),
    ("Cantora gospel lança álbum que mistura ritmos brasileiros e música sacra", []),
    ("Empresa de games anuncia parceria com estúdio de Hollywood para novo jogo", []),
    ("Campanha publicitária viraliza ao destacar diversidade cultural do país", []),
    ("Universidade cria programa de bolsas para estudantes refugiados", []),
    ("Festival de cinema independente atrai diretores consagrados e novos talentos", []),
    ("Iniciativa de empreendedorismo feminino capacita mulheres em tecnologia", []),
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
            elif (tipo == CAUSAS):
                args.append(random.choice(CAUSAS))
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
df.to_csv("gerar_dados/data_sintetica.csv", index=False)
print("Dados gerados com sucesso em data.csv")