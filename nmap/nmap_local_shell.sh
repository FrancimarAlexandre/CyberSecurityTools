#!/usr/bin/env bash
# run_nmap.sh
# Script para executar comandos Nmap de forma organizada e corrigida.
# Edit: defina TARGET e NETWORK abaixo conforme sua necessidade.

set -euo pipefail

# ----- Configuração (edite se necessário) -----
# Alvo principal (por padrão localhost)
TARGET="${1:-127.0.0.1}"

# Rede para descoberta de hosts (ex.: 127.0.0.0/24, 192.168.1.0/24)
# Se não quiser usar descoberta em rede, deixe vazia: NETWORK=""
NETWORK="${2:-}" 

# Tempo/velocidade padrão do Nmap (-T4 é razoável em ambientes de teste)
NMAP_TIMING="-T4"

# ----- Funções utilitárias -----
die() {
  echo "ERRO: $*" >&2
  exit 1
}

check_nmap() {
  if ! command -v nmap >/dev/null 2>&1; then
    die "nmap não encontrado. Instale o nmap antes de executar este script."
  fi
}

warn_if_not_root() {
  if [ "$(id -u)" -ne 0 ]; then
    echo "AVISO: você não é root. Alguns scans (ex.: -sS, captura de pacotes raw) podem exigir sudo/root."
    echo "Se quiser rodar scans raw, execute: sudo $0"
    echo
  fi
}

# ----- Execução dos scans -----
main() {
  check_nmap
  warn_if_not_root

  echo "=== Parâmetros ==="
  echo "TARGET = $TARGET"
  if [ -n "$NETWORK" ]; then
    echo "NETWORK = $NETWORK"
  else
    echo "NETWORK = (não definido — pular descoberta em rede)"
  fi
  echo

  # 1) Descobrir hosts ativos (ping scan) — usa NETWORK no formato CIDR
  if [ -n "$NETWORK" ]; then
    echo "1) Descobrir hosts ativos (ping scan) em: $NETWORK"
    echo "Comando: nmap -sn $NMAP_TIMING $NETWORK"
    nmap -sn $NMAP_TIMING "$NETWORK"
    echo
  else
    echo "1) Pulando descoberta em rede (NETWORK não definido)."
    echo
  fi

  # 1b) (Opcional) Descobrir hosts que tenham a porta 22 aberta na rede
  if [ -n "$NETWORK" ]; then
    echo "1b) Descobrir hosts com porta 22 (SSH) aberta em: $NETWORK"
    echo "Comando: nmap -p 22 --open $NMAP_TIMING $NETWORK"
    nmap -p 22 --open $NMAP_TIMING "$NETWORK"
    echo
  fi

  # 2) Escanear portas do TARGET (varredura padrão — portas comuns)
  echo "2) Escanear portas do host $TARGET (varredura padrão)"
  echo "Comando: nmap $NMAP_TIMING $TARGET"
  nmap $NMAP_TIMING "$TARGET"
  echo

  # 3) Detectar sistema operacional e serviços (mais detalhado)
  echo "3) Detectar sistema operacional e serviços em $TARGET"
  echo "Comando: nmap -A $NMAP_TIMING $TARGET"
  echo "Observação: -A ativa fingerprinting de SO, detecção de versão e scripts básicos."
  nmap -A $NMAP_TIMING "$TARGET"
  echo

  # 4) Executar scripts de vulnerabilidade (NSE) — pode demorar e produzir falsos positivos
  echo "4) Executar scripts de vulnerabilidade (--script vuln) em $TARGET"
  echo "Comando: nmap --script=vuln -sV $NMAP_TIMING $TARGET"
  echo "Observação: usamos -sV para ajudar os scripts a identificar versões."
  nmap --script=vuln -sV $NMAP_TIMING "$TARGET"
  echo

  echo "=== Concluído ==="
  echo "Lembre-se: use este script somente em ambientes autorizados e/ou locais (ex.: 127.0.0.1, VMs, containers)."
}

main "$@"
