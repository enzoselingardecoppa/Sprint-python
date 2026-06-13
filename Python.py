
import time
import random

# Códigos de cores ANSI para formatação do terminal
AZUL = "\033[34m"
VERDE = "\033[32m"
AMARELO = "\033[33m"
VERMELHO = "\033[31m"
CIANO = "\033[36m"
RESET = "\033[0m"


class CarroEletrico:
    def __init__(self, id_carro, marca, modelo, capacidade_kwh, carga_atual, protocolo_fabrica):
        self.id = id_carro
        self.marca = marca
        self.modelo = modelo
        self.capacidade = capacidade_kwh  # Capacidade total da bateria em kWh
        self.carga = carga_atual  # Percentual de carga atual (0-100)
        self.protocolo_fabrica = protocolo_fabrica  # Protocolo de comunicação original do fabricante
        self.energia_entregue = 0.0
        self.tempo_recarga = 0


class ChargeGridIntelligence:
    def __init__(self):
        self.limite_predio = 75.0  # Limite máximo de potência suportado pelo disjuntor (kW)
        self.bateria_goodwe_total = 100.0  # Capacidade do banco de baterias local (kWh)
        self.bateria_goodwe_atual = 65.0  # Carga inicial da bateria (%)
        self.preco_kwh_base = 0.89

    def conectar_via_ocpp(self, carro):
        """Traduz o protocolo nativo do veículo para o padrão OCPP."""
        print(f"{CIANO}[OCPP]{RESET} Carro detectado usando: '{carro.protocolo_fabrica}'")
        time.sleep(0.2)
        print(
            f"{VERDE}[OCPP - CONECTADO]{RESET} {carro.marca} {carro.modelo} convertido com sucesso para o padrão OCPP.")

    def rodar_ia_preditiva(self, hora):
        """Executa a predição de geração solar e demanda baseada no horário."""
        print(f"\n{CIANO}[IA - PREVISÃO PARA ÀS {hora:02d}:00]{RESET}")

        if 6 <= hora <= 16:
            sol = random.uniform(35.0, 50.0)
            print(f" -> Previsão: Sol forte (geração estimada em {sol:.1f} kW). Estacionamento tranquilo.")
            print(f" -> Decisão da IA: Usar energia solar direta e carregar a bateria do prédio com a sobra.")
            return sol, "NORMAL"
        elif 17 <= hora <= 21:
            sol = random.uniform(0.0, 3.0)
            print(f" -> Previsão: Horário de pico no shopping/prédio. Geração solar quase zerada.")
            print(
                f" -> Decisão da IA: ATIVAR PEAK SHAVING. Segurar a barra com a nossa bateria para poupar a rede pública.")
            return sol, "PICO"
        else:
            print(f" -> Previsão: Madrugada. Sem sol e pátio vazio.")
            print(f" -> Decisão da IA: Modo de espera.")
            return 0.0, "MADRUGADA"

    def gerenciar_energia_dlb(self, carros, geracao_solar, status_tempo, hora):
        """Aplica o balanceamento dinâmico de carga (DLB) e Peak Shaving."""
        print(f"\n{AZUL}--- STATUS DO SISTEMA DLB ({hora:02d}:00) ---{RESET}")

        carros_precisando_carga = [c for c in carros if c.carga < 100]
        if not carros_precisando_carga:
            print("Nenhum carro carregando no momento.")
            return

        limite_disponivel = self.limite_predio
        usando_bateria_local = False

        # Restrição de demanda durante o horário de pico
        if status_tempo == "PICO":
            if self.bateria_goodwe_atual > 15.0:
                print(f"{AMARELO}[Peak Shaving]{RESET} Horário crítico! Reduzindo o consumo da concessionária da rua.")
                limite_disponivel = 30.0
                usando_bateria_local = True
            else:
                print(
                    f"{VERMELHO}[Alerta]{RESET} Bateria local muito baixa ({self.bateria_goodwe_atual:.1f}%). Usando rede da rua por segurança.")

        potencia_total_disponivel = limite_disponivel + geracao_solar
        potencia_que_os_carros_querem = len(carros_precisando_carga) * 22.0

        print(f" Potência que os carros querem: {potencia_que_os_carros_querem:.1f} kW")
        print(f" Potência máxima segura hoje  : {potencia_total_disponivel:.1f} kW")

        # Algoritmo de fatiamento de carga (DLB)
        for carro in carros_precisando_carga:
            if potencia_que_os_carros_querem > potencia_total_disponivel:
                potencia_alocada = potencia_total_disponivel / len(carros_precisando_carga)
                print(
                    f"{AMARELO}[DLB]{RESET} Limite quase estourado! Diminuindo a velocidade de carga do {carro.modelo}.")
            else:
                potencia_alocada = 22.0

            # Atualização do estado de carga do veículo
            energia_ganha = min(potencia_alocada, (carro.capacidade * (1 - (carro.carga / 100))))
            carro.energia_entregue += energia_ganha
            carro.carga += (energia_ganha / carro.capacidade) * 100
            carro.carga = min(100.0, carro.carga)
            carro.tempo_recarga += 60

            # Abatimento no banco de baterias local
            if usando_bateria_local:
                self.bateria_goodwe_atual -= (energia_ganha * 0.5) / self.bateria_goodwe_total * 100
                self.bateria_goodwe_atual = max(0.0, self.bateria_goodwe_atual)

            print(
                f" -> Carro {carro.id} ({carro.modelo}): Recebendo {potencia_alocada:.1f}kW | Bateria: {carro.carga:.1f}%")

        if usando_bateria_local:
            print(f" Carga Restante na Bateria GoodWe do prédio: {self.bateria_goodwe_atual:.1f}%")

    def emitir_cobranca(self, carro, hora_saida):
        """Calcula o valor da recarga e simula a transação financeira."""
        print(f"\n{VERDE}---------------------------------------------------{RESET}")
        print(f"{VERDE}            CONTA FINAL — CHARGEGRID               {RESET}")
        print(f"{VERDE}---------------------------------------------------{RESET}")
        print(f" Carro: {carro.marca} {carro.modelo} (ID: {carro.id})")
        print(f" Energia total consumida: {carro.energia_entregue:.2f} kWh")
        print(f" Tempo conectado: {carro.tempo_recarga} minutos")

        # Aplicação de preço dinâmico
        preco_kwh = self.preco_kwh_base
        if 17 <= hora_saida <= 21:
            print(" Taxa de Horário de Pico aplicada (+30% pelo custo da rede)")
            preco_kwh *= 1.3

        custo_total = carro.energia_entregue * preco_kwh
        desconto_eco = custo_total * 0.10
        valor_final = custo_total - desconto_eco

        print(f" Desconto Eco (Uso de energia limpa/GoodWe): -R$ {desconto_eco:.2f}")
        print(f" CUSTO TOTAL A PAGAR: R$ {valor_final:.2f}")
        print(f"---------------------------------------------------")
        print(f" [Pix] Gerando QR Code para pagamento...")
        time.sleep(0.5)
        print(f" {VERDE}[Pix - CONFIRMADO]{RESET} Pagamento recebido! Liberando a trava do carregador.")
        print(f"{VERDE}---------------------------------------------------{RESET}")


if __name__ == "__main__":
    print(f"{AZUL}=== INICIANDO SIMULADOR CHARGEGRID INTELLIGENCE ==={RESET}\n")

    sistema = ChargeGridIntelligence()

    # Instanciação dos veículos para teste
    patio = [
        CarroEletrico(1, "BYD", "Seal", 82, 45, "BYD OS v2"),
        CarroEletrico(2, "Tesla", "Model Y", 75, 30, "Tesla Protocol API"),
        CarroEletrico(3, "Nissan", "Leaf", 40, 20, "CHAdeMO Legacy")
    ]

    # 1. Conexão e padronização dos pontos de carga
    print("--- PASSO 1: RECONHECENDO OS CARROS NO PÁTIO ---")
    for carro in patio:
        sistema.conectar_via_ocpp(carro)
    time.sleep(0.5)

    # 2. Execução dos ciclos de carga ao longo do dia
    horarios_do_dia = [12, 15, 19]
    for h in horarios_do_dia:
        energia_solar, status = sistema.rodar_ia_preditiva(h)
        sistema.gerenciar_energia_dlb(patio, energia_solar, status, h)
        time.sleep(0.5)

    # 3. Processamento de checkout e tarifas
    print("\n--- PASSO 3: SAÍDA DOS CARROS E PAGAMENTO ---")
    for carro in patio:
        sistema.emitir_cobranca(carro, hora_saida=20)
        time.sleep(0.3)

    print(f"\n{VERDE} Simulação finalizada com sucesso! Todos os 4 pilares validados.{RESET}")