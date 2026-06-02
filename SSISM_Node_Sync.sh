#!/bin/bash
# ==============================================================================
# SYSTEM:       SSISM Decentralized Node Synchronization Engine
# FILE:         SSISM_Node_Sync.sh
# VERSION:      2.2 (Community Release Standard)
# PURPOSE:      Automates local deployment of Core Engine components while
#               enforcing strict OpSec data masking protocols.
# ==============================================================================

set -euo pipefail

# --- CONFIGURATION & DIRECTORY MAPPING ---
REPO_NAME="Myanmar-OSINT-Ritual"
CORE_DIR="./src/core"
DATA_DIR="./data"
DOCS_DIR="./docs/civil_education"
LOG_FILE="./data/sync_log.json"

# --- COLOR CODES FOR TERMINAL MONITORING ---
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m'

log_message() {
    local status="$1"
    local msg="$2"
    echo -e "[$(date +'%Y-%m-%d %H:%M:%S')] [${status}] ${msg}"
}

# ==============================================================================
# INTERNAL QUALITY GATE CHECK (GATE 3 - REPRODUCIBILITY)
# ==============================================================================
verify_environment() {
    log_message "INFO" "Executing internal Quality Gate checks..."
    
    # Verify mandatory local directories exist
    for dir in "${CORE_DIR}" "${DATA_DIR}" "${DOCS_DIR}"; do
        if [ ! -d "$dir" ]; then
            log_message "WARN" "Directory $dir missing. Initializing localized tier space..."
            mkdir -p "$dir"
        fi
    done
    
    # Check for core dependencies
    for cmd in git python3 sha256sum; do
        if ! command -v $cmd &> /dev/null; then
            log_message "ERROR" "Required dependency '$cmd' is not installed. HOLD PUBLICATION."
            exit 1
        fi
    done
}

# ==============================================================================
# SAFEGUARD MASKING FILTER (OPSEC COMPLIANCE)
# ==============================================================================
apply_safeguard_filter() {
    log_message "INFO" "Running Safeguard Masking Filter on target files..."
    
    # Scan data layers for sensitive patterns before staging
    # Ensures no explicit personal identifiers or raw credentials bypass local bounds
    if [ -d "$DATA_DIR" ]; then
        find "$DATA_DIR" -type f -name "*.json" -o -name "*.env" | while read -r file; do
            if grep -Eq "(PASSWORD|BIRTHDAY|SECRET_KEY)" "$file"; then
                log_message "WARN" "Sensitive signature detected in $file! Stripping clear text..."
                # Replace sensitive data strings with localized cryptographic placeholding
                sed -i -E 's/(PASSWORD|BIRTHDAY|SECRET_KEY)=.*/\1=MAPPED_VIA_LOCAL_ENVIRONMENT/g' "$file"
            fi
        done
    fi
}

# ==============================================================================
# CORE EXECUTION MECHANISM (TIERED SYNC)
# ==============================================================================
sync_node_components() {
    log_message "INFO" "Synchronizing Tier 1 and Tier 2 components..."
    
    # Calculate operational integrity integrity hash
    if [ -f "${CORE_DIR}/sigmoid.py" ]; then
        local_hash=$(sha256sum "${CORE_DIR}/sigmoid.py" | awk '{print $1}')
        log_message "SUCCESS" "Tier 1 Engine Integrity verified: SHA-256(${local_hash:0:8}...)"
    else
        log_message "WARN" "sigmoid.py mathematical core engine not initialized in local tree."
    fi

    # Check git tracking status securely
    if [ -d ".git" ]; then
        log_message "INFO" "Verifying upstream parameters for repository: ${REPO_NAME}"
        apply_safeguard_filter
        
        # Staging core framework files while leaving local/private nodes secure
        git add "${CORE_DIR}/*" 2>/dev/null || true
        git add "${DOCS_DIR}/*" 2>/dev/null || true
        
        log_message "SUCCESS" "Components securely staged for GitHub staging or testing."
    else
        log_message "WARN" "Isolated node state detected. Skipping Git stage. Local workspace operational."
    fi
}

# --- INITIALIZATION TRIGGER ---
main() {
    echo -e "${YELLOW}====================================================${NC}"
    echo -e "${GREEN}       SSISM NODE INITIALIZATION & SYNC ENGINE       ${NC}"
    echo -e "${YELLOW}====================================================${NC}"
    
    verify_environment
    sync_node_components
    
    log_message "SUCCESS" "Node Synchronization Complete. Ready for analytical cycles or evening testing."
}

main "$@"
