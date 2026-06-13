
# ChargeGrid Intelligence — Sprint 2 (Python)

- Enzo Coppa Selingarde - RM 573393
- Gabriel Carlos Barbosa - RM 574074
- Gustavo de Souza Abreu - RM 574080


Esse é o script em Python que a gente desenvolveu para simular o funcionamento do ChargeGrid em um cenário comercial (tipo o estacionamento de um shopping ou condomínio). 

A ideia principal é gerenciar os carregadores de carros elétricos para não derrubar o disjuntor do prédio e evitar gastar uma fortuna com energia na hora de pico.

---

## O que o código faz (Simplificado)

Em vez de só ligar o carro na tomada e puxar energia, o sistema roda quatro lógicas em tempo real:

* **Divisão de Carga (DLB) e Peak Shaving:** Se entrar muito carro junto, o código divide a potência entre eles para não estourar o limite do prédio. Além disso, se der 17hh (horário de pico), o sistema para de puxar energia da rua e usa a bateria interna da GoodWe para segurar a barra.
* **Conversão de Protocolo (OCPP):** Simula a chegada de carros de marcas diferentes (BYD, Tesla, carregadores antigos) e padroniza a comunicação de todos eles usando o formato OCPP, para nenhum dar erro de compatibilidade.
* **Previsão com IA:** O código simula uma IA que olha a hora do dia e a geração solar para decidir o que fazer antes do problema acontecer (ex: guardar energia na bateria quando o sol tá forte ou ativar o modo de emergência à noite).
* **Cobrança e Pix:** Calcula o valor exato com base nos kWh que o carro realmente usou. Se carregou no horário de pico fica um pouco mais caro, e se usou energia solar ganha desconto. No final, simula o fechamento do pagamento via Pix.

---

