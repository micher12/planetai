import scapy.all as scapy
from scapy.layers.inet import IP, TCP, UDP, ICMP
import urllib.parse
import time
import requests
import threading

def identificar_protocolo_url(url):
    """
    Identifica o protocolo da URL (http, https, etc.)
    """
    try:
        parsed_url = urllib.parse.urlparse(url)
        return {
            'protocolo_url': parsed_url.scheme,
            'hostname': parsed_url.hostname,
            'path': parsed_url.path,
            'port': parsed_url.port or (443 if parsed_url.scheme == 'https' else 80)
        }
    except Exception as e:
        print(f"Erro ao identificar protocolo da URL: {e}")
        return None

def fazer_requisicao_api(url):
    """
    Realiza uma requisição HTTP para a URL especificada
    """
    try:
        print(f"\nRealizando requisição para: {url}")
        response = requests.get(url, timeout=10)
        print(f"Status da resposta: {response.status_code}")
        print(f"Tamanho da resposta: {len(response.content)} bytes")
        return {
            'status_code': response.status_code,
            'content_type': response.headers.get('Content-Type'),
            'content_length': len(response.content),
            'elapsed_time': response.elapsed.total_seconds()
        }
    except Exception as e:
        print(f"Erro ao fazer requisição para API: {e}")
        return None

def capturar_trafego_em_background(interface, filtro, timeout, resultados):
    """
    Função para capturar pacotes em segundo plano
    """
    # Estatísticas para contar os protocolos
    estatisticas = {
        'camada_2': {},  # Ethernet, etc.
        'camada_3': {},  # IP, IPv6, etc.
        'camada_4': {},  # TCP, UDP, etc.
        'camada_7': {},  # HTTP, DNS, etc.
        'total_pacotes': 0,
        'ips_origem': set(),
        'ips_destino': set(),
        'portas_origem': set(),
        'portas_destino': set()
    }
    
    pacotes_capturados = []
    
    # Função para processar cada pacote capturado
    def processar_pacote(pacote):
        pacotes_capturados.append(pacote)
        estatisticas['total_pacotes'] += 1
        
        # Analisar camada 2 (enlace)
        if pacote.name:
            if pacote.name in estatisticas['camada_2']:
                estatisticas['camada_2'][pacote.name] += 1
            else:
                estatisticas['camada_2'][pacote.name] = 1
        
        # Analisar camada 3 (rede)
        if IP in pacote:
            if 'IP' in estatisticas['camada_3']:
                estatisticas['camada_3']['IP'] += 1
            else:
                estatisticas['camada_3']['IP'] = 1
                
            # Extrair informações IP
            ip_src = pacote[IP].src
            ip_dst = pacote[IP].dst
            estatisticas['ips_origem'].add(ip_src)
            estatisticas['ips_destino'].add(ip_dst)
            
            # Analisar camada 4 (transporte)
            if TCP in pacote:
                porta_src = pacote[TCP].sport
                porta_dst = pacote[TCP].dport
                estatisticas['portas_origem'].add(porta_src)
                estatisticas['portas_destino'].add(porta_dst)
                
                if 'TCP' in estatisticas['camada_4']:
                    estatisticas['camada_4']['TCP'] += 1
                else:
                    estatisticas['camada_4']['TCP'] = 1
                
                # Tentar identificar o protocolo da aplicação com base nas portas
                if porta_dst == 80 or porta_src == 80:
                    if 'HTTP' in estatisticas['camada_7']:
                        estatisticas['camada_7']['HTTP'] += 1
                    else:
                        estatisticas['camada_7']['HTTP'] = 1
                
                elif porta_dst == 443 or porta_src == 443:
                    if 'HTTPS' in estatisticas['camada_7']:
                        estatisticas['camada_7']['HTTPS'] += 1
                    else:
                        estatisticas['camada_7']['HTTPS'] = 1
                
                elif porta_dst == 22 or porta_src == 22:
                    if 'SSH' in estatisticas['camada_7']:
                        estatisticas['camada_7']['SSH'] += 1
                    else:
                        estatisticas['camada_7']['SSH'] = 1
            
            elif UDP in pacote:
                porta_src = pacote[UDP].sport
                porta_dst = pacote[UDP].dport
                estatisticas['portas_origem'].add(porta_src)
                estatisticas['portas_destino'].add(porta_dst)
                
                if 'UDP' in estatisticas['camada_4']:
                    estatisticas['camada_4']['UDP'] += 1
                else:
                    estatisticas['camada_4']['UDP'] = 1
                
                # Protocolo da aplicação baseado na porta
                if porta_dst == 53 or porta_src == 53:
                    if 'DNS' in estatisticas['camada_7']:
                        estatisticas['camada_7']['DNS'] += 1
                    else:
                        estatisticas['camada_7']['DNS'] = 1
            
            elif ICMP in pacote:
                if 'ICMP' in estatisticas['camada_4']:
                    estatisticas['camada_4']['ICMP'] += 1
                else:
                    estatisticas['camada_4']['ICMP'] = 1
    
    try:
        # Informa que a captura está começando
        print(f"Iniciando captura de pacotes na interface {interface}...")
        print(f"Filtro aplicado: {filtro if filtro else 'Nenhum'}")
        
        # Captura pacotes
        scapy.sniff(iface=interface, filter=filtro, timeout=timeout, prn=processar_pacote, store=0)
        
        resultados.update(estatisticas)
        resultados['pacotes'] = pacotes_capturados
        print(f"Captura finalizada! {estatisticas['total_pacotes']} pacotes capturados.")
        
    except Exception as e:
        print(f"Erro durante a captura de pacotes: {e}")

def analisar_url_com_requisicao(url, api_key=None, interface=None, timeout=15):
    """
    Função que combina análise de URL, requisição à API e captura de tráfego
    """
    # Adicionar a chave API se fornecida
    if api_key:
        url_completa = f"{url}?apikey={api_key}&country=br&language=pt&category=environment"
    else:
        url_completa = url
    
    # Identificar protocolo da URL
    info_url = identificar_protocolo_url(url_completa)
    
    if not info_url:
        print("Falha ao analisar a URL")
        return None
    
    hostname = info_url.get('hostname')
    
    # Criar filtro para captura de pacotes - capturar apenas tráfego relacionado à API
    filtro = f"host {hostname}" if hostname else None
    
    # Preparar dicionário para resultados de captura
    resultados_captura = {}
    
    # Iniciar thread de captura de pacotes
    if interface:
        thread_captura = threading.Thread(
            target=capturar_trafego_em_background,
            args=(interface, filtro, timeout, resultados_captura)
        )
        thread_captura.daemon = True
        thread_captura.start()
        
        # Aguardar um momento para a captura iniciar
        time.sleep(1)
    
    # Fazer a requisição para a API
    resposta_api = fazer_requisicao_api(url_completa)
    
    # Se estamos capturando pacotes, aguardar a thread finalizar
    if interface and thread_captura.is_alive():
        print("Aguardando finalização da captura de pacotes...")
        thread_captura.join(timeout=timeout+5)  # Aguardar conclusão com timeout adicional
    
    # Compilar resultados
    return {
        'analise_url': info_url,
        'resposta_api': resposta_api,
        'analise_trafego': resultados_captura
    }

import json

def exibir_resultados(resultados):
    """
    Retorna os resultados da análise de maneira organizada no formato JSON.
    """
    if not resultados:
        return json.dumps({"error": "Nenhum resultado disponível para exibir."})
    
    resultado_json = {
        "relatorio": {
            "titulo": "RELATÓRIO DE ANÁLISE DE PROTOCOLOS DE REDE",
            "analise_url": {},
            "resposta_api": {},
            "analise_trafego": {}
        }
    }
    
    # Análise da URL
    if 'analise_url' in resultados and resultados['analise_url']:
        info_url = resultados['analise_url']
        resultado_json["relatorio"]["analise_url"] = {
            "protocolo": info_url.get('protocolo_url', 'Não identificado'),
            "hostname": info_url.get('hostname', 'Não identificado'),
            "caminho": info_url.get('path', 'Não identificado'),
            "porta": info_url.get('port', 'Não identificado')
        }
    
    # Resposta da API
    if 'resposta_api' in resultados and resultados['resposta_api']:
        resposta = resultados['resposta_api']
        resultado_json["relatorio"]["resposta_api"] = {
            "status_http": resposta.get('status_code', 'N/A'),
            "tipo_conteudo": resposta.get('content_type', 'N/A'),
            "tamanho_conteudo": resposta.get('content_length', 0),
            "tempo_resposta_segundos": round(resposta.get('elapsed_time', 0), 3)
        }
    
    # Análise do tráfego
    if 'analise_trafego' in resultados and resultados['analise_trafego']:
        trafego = resultados['analise_trafego']
        total_pacotes = trafego.get('total_pacotes', 0)
        
        resultado_json["relatorio"]["analise_trafego"] = {
            "total_pacotes": total_pacotes
        }
        
        if total_pacotes > 0:
            # IPs encontrados
            if 'ips_origem' in trafego and trafego['ips_origem']:
                resultado_json["relatorio"]["analise_trafego"]["ips_origem"] = list(trafego['ips_origem'])
            
            if 'ips_destino' in trafego and trafego['ips_destino']:
                resultado_json["relatorio"]["analise_trafego"]["ips_destino"] = list(trafego['ips_destino'])
            
            # Portas encontradas
            if 'portas_origem' in trafego and trafego['portas_origem']:
                resultado_json["relatorio"]["analise_trafego"]["portas_origem"] = sorted(list(trafego['portas_origem']))[:10]
            
            if 'portas_destino' in trafego and trafego['portas_destino']:
                resultado_json["relatorio"]["analise_trafego"]["portas_destino"] = sorted(list(trafego['portas_destino']))[:10]
            
            # Camada 2
            if 'camada_2' in trafego and trafego['camada_2']:
                resultado_json["relatorio"]["analise_trafego"]["camada_2"] = [
                    {"protocolo": protocolo, "pacotes": contagem, "porcentagem": round((contagem/total_pacotes)*100, 1)}
                    for protocolo, contagem in trafego['camada_2'].items()
                ]
            
            # Camada 3
            if 'camada_3' in trafego and trafego['camada_3']:
                resultado_json["relatorio"]["analise_trafego"]["camada_3"] = [
                    {"protocolo": protocolo, "pacotes": contagem, "porcentagem": round((contagem/total_pacotes)*100, 1)}
                    for protocolo, contagem in trafego['camada_3'].items()
                ]
            
            # Camada 4
            if 'camada_4' in trafego and trafego['camada_4']:
                resultado_json["relatorio"]["analise_trafego"]["camada_4"] = [
                    {"protocolo": protocolo, "pacotes": contagem, "porcentagem": round((contagem/total_pacotes)*100, 1)}
                    for protocolo, contagem in trafego['camada_4'].items()
                ]
            
            # Camada 7
            if 'camada_7' in trafego and trafego['camada_7']:
                resultado_json["relatorio"]["analise_trafego"]["camada_7"] = [
                    {"protocolo": protocolo, "pacotes": contagem, "porcentagem": round((contagem/total_pacotes)*100, 1)}
                    for protocolo, contagem in trafego['camada_7'].items()
                ]
        else:
            resultado_json["relatorio"]["analise_trafego"]["erro"] = {
                "mensagem": "Nenhum pacote foi capturado durante a análise.",
                "possiveis_causas": [
                    "Interface de rede incorreta",
                    "Problemas de permissão para captura de pacotes",
                    "Filtro de captura muito restritivo",
                    "Firewall bloqueando a captura"
                ]
            }
    
    return json.dumps(resultado_json, ensure_ascii=False, indent=2)


def getProtocolo():
    from dotenv import load_dotenv
    import os
    load_dotenv()
    

    url = "https://newsdata.io/api/1/news"
    
    api_key = os.getenv("NEWSDATA_API_KEY")
    
    # Interface de rede (ajuste conforme seu sistema)
    # Linux: geralmente 'eth0' ou 'wlan0'
    # Windows: pode usar o nome da interface como 'Ethernet' ou 'Wi-Fi'
    # Ou deixe None para não capturar pacotes, apenas fazer a requisição
    interface = r"\Device\NPF_{37EEA4A3-86F4-4946-81F4-92020466E545}"  # Tente identificar automaticamente a melhor interface
    
    try:
        # Se não especificou interface, tente identificar automaticamente
        if interface is None:
            interfaces = scapy.get_working_ifaces()
            # Filtrar interfaces virtuais ou de loopback
            interfaces_fisicas = [iface for iface in interfaces 
                                if not (iface.name.startswith('lo') or 
                                        'virtual' in iface.name.lower() or 
                                        'loopback' in str(iface).lower())]
            
            if interfaces_fisicas:
                interface = interfaces_fisicas[0].name
                print(f"Interface de rede selecionada automaticamente: {interface}")
            else:
                print("Não foi possível identificar uma interface de rede física. Continuando sem captura de pacotes.")
                interface = None
    except Exception as e:
        print(f"Erro ao identificar interfaces: {e}")
        print("Continuando sem captura de pacotes.")
        interface = None
    
    print(f"\nAnalisando URL, realizando requisição e capturando tráfego para: {url}")
    resultados = analisar_url_com_requisicao(url, api_key, interface)
    resultadoFinal = exibir_resultados(resultados)

    return resultadoFinal