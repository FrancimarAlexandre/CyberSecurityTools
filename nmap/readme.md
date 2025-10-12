# 🔍 Nmap — Network Mapper

O **Nmap (Network Mapper)** é uma das ferramentas mais importantes no campo da **Cibersegurança** e da **Administração de Redes**.  
Ele é usado para **mapear redes**, **identificar hosts ativos**, **descobrir portas abertas** e **detectar serviços e sistemas operacionais**.

---

## 🧭 O que é o Nmap?

O Nmap é uma ferramenta **open source** criada para realizar **varreduras de rede** (network scanning).  
Seu principal objetivo é **coletar informações sobre dispositivos conectados** e **avaliar a superfície de exposição de uma rede**.

---

## ⚙️ Principais Finalidades

| Função | Descrição |
|--------|------------|
| 🔹 **Host Discovery** | Descobre quais dispositivos estão ativos em uma rede. |
| 🔹 **Port Scanning** | Identifica quais portas estão abertas, fechadas ou filtradas. |
| 🔹 **Service Detection** | Determina quais serviços e versões estão sendo executados. |
| 🔹 **OS Detection** | Tenta identificar o sistema operacional do host. |
| 🔹 **NSE (Nmap Scripting Engine)** | Usa scripts para automatizar testes e enumerações. |

---

## 🧩 Conceitos Importantes

### 🔸 Tipos de Varredura (Scan Types)

| Tipo | Opção | Descrição |
|------|--------|------------|
| TCP Connect | `-sT` | Conexão completa TCP (3-way handshake). |
| SYN Scan | `-sS` | "Half-open" scan — mais rápido e discreto. |
| UDP Scan | `-sU` | Escaneia portas UDP (mais lento). |
| Ping Scan | `-sn` | Apenas verifica hosts ativos, sem escanear portas. |

---

### 🔸 Estados das Portas

| Estado | Significado |
|---------|--------------|
| **open** | Há um serviço respondendo na porta. |
| **closed** | O host respondeu, mas não há serviço ativo. |
| **filtered** | O tráfego é bloqueado (firewall). |
| **open|filtered** | O Nmap não conseguiu determinar o estado exato. |

---

### 🔸 Performance e Discrição

O Nmap permite ajustar o ritmo da varredura:

| Opção | Velocidade | Descrição |
|--------|-------------|-----------|
| `-T0` | Muito lenta | Evita detecção (stealth). |
| `-T3` | Padrão | Equilíbrio entre velocidade e precisão. |
| `-T5` | Muito rápida | Indicada para redes de teste. |

---

## 💻 Exemplos Práticos

### 🔹 Descobrir hosts ativos
```bash
nmap -sn 192.168.0.0/24



