#!/bin/bash

# Environment Manager for AI Agent Factory Agent Factory
# Helps manage environment configuration files

ENV_DIR="config/env"
EXAMPLE_FILE="config/env.example"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show help
show_help() {
    echo "Environment Manager for AI Agent Factory Agent Factory"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  init        Initialize environment from example file"
    echo "  backup      Create backup of current environment"
    echo "  restore     Restore from backup"
    echo "  list        List all environment files"
    echo "  clean       Clean up old backup files"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 init                    # Initialize new environment"
    echo "  $0 backup github          # Backup with specific name"
    echo "  $0 restore github         # Restore from specific backup"
}

# Function to initialize environment
init_env() {
    print_status "Initializing environment configuration..."
    
    if [ ! -f "$EXAMPLE_FILE" ]; then
        print_error "Example file not found: $EXAMPLE_FILE"
        exit 1
    fi
    
    if [ -f "$ENV_DIR/.env.local" ]; then
        print_warning ".env.local already exists. Creating backup first..."
        backup_env "auto-backup"
    fi
    
    cp "$EXAMPLE_FILE" "$ENV_DIR/.env.local"
    print_success "Environment initialized. Edit $ENV_DIR/.env.local with your values."
    print_warning "Remember: Never commit .env.local to version control!"
}

# Function to backup environment
backup_env() {
    local backup_name=${1:-"backup-$(date +%Y%m%d-%H%M%S)"}
    
    if [ ! -f "$ENV_DIR/.env.local" ]; then
        print_error "No .env.local file found to backup"
        exit 1
    fi
    
    cp "$ENV_DIR/.env.local" "$ENV_DIR/.env.backup.$backup_name"
    print_success "Environment backed up to .env.backup.$backup_name"
}

# Function to restore environment
restore_env() {
    local backup_name=${1:-"backup"}
    
    if [ ! -f "$ENV_DIR/.env.backup.$backup_name" ]; then
        print_error "Backup file not found: .env.backup.$backup_name"
        print_status "Available backups:"
        ls -la "$ENV_DIR"/.env.backup.* 2>/dev/null || print_warning "No backups found"
        exit 1
    fi
    
    cp "$ENV_DIR/.env.backup.$backup_name" "$ENV_DIR/.env.local"
    print_success "Environment restored from .env.backup.$backup_name"
}

# Function to list environment files
list_env() {
    print_status "Environment files in $ENV_DIR:"
    echo ""
    
    if [ -d "$ENV_DIR" ]; then
        ls -la "$ENV_DIR"/
    else
        print_warning "Environment directory not found: $ENV_DIR"
    fi
    
    echo ""
    print_status "Example file:"
    if [ -f "$EXAMPLE_FILE" ]; then
        ls -la "$EXAMPLE_FILE"
    else
        print_warning "Example file not found: $EXAMPLE_FILE"
    fi
}

# Function to clean old backups
clean_backups() {
    print_status "Cleaning old backup files..."
    
    # Keep only the 5 most recent backups
    cd "$ENV_DIR" || exit 1
    ls -t .env.backup.* 2>/dev/null | tail -n +6 | xargs -r rm -f
    print_success "Old backup files cleaned (kept 5 most recent)"
}

# Main script logic
case "${1:-help}" in
    init)
        init_env
        ;;
    backup)
        backup_env "$2"
        ;;
    restore)
        restore_env "$2"
        ;;
    list)
        list_env
        ;;
    clean)
        clean_backups
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
