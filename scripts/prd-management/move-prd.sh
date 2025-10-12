#!/bin/bash

# PRD Management Script - Move PRD between folders
# Usage: ./move-prd.sh <prd-filename> <from-status> <to-status>

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PRDS_DIR="$PROJECT_ROOT/prds"

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

# Function to show usage
show_usage() {
    echo "Usage: $0 <prd-filename> <from-status> <to-status>"
    echo ""
    echo "Arguments:"
    echo "  prd-filename    Name of the PRD file (with or without .md extension)"
    echo "  from-status     Current status folder (queue, in-progress, completed, failed, archive)"
    echo "  to-status       Target status folder (queue, in-progress, completed, failed, archive)"
    echo ""
    echo "Examples:"
    echo "  $0 database-integration-supabase queue in-progress"
    echo "  $0 2024-01-15_database-integration-supabase.md completed archive"
    echo ""
    echo "Valid status folders:"
    echo "  queue, in-progress, completed, failed, archive"
}

# Function to validate status
validate_status() {
    local status="$1"
    case "$status" in
        queue|in-progress|completed|failed|archive)
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

# Function to find PRD file
find_prd_file() {
    local filename="$1"
    local status="$2"
    local search_dir="$PRDS_DIR/$status"
    
    # Try exact filename first
    if [ -f "$search_dir/$filename" ]; then
        echo "$search_dir/$filename"
        return 0
    fi
    
    # Try with .md extension
    if [ -f "$search_dir/$filename.md" ]; then
        echo "$search_dir/$filename.md"
        return 0
    fi
    
    # Try without .md extension
    local basename="${filename%.md}"
    if [ -f "$search_dir/$basename" ]; then
        echo "$search_dir/$basename"
        return 0
    fi
    
    # Search for partial matches
    local matches=$(find "$search_dir" -name "*$filename*" -type f 2>/dev/null)
    if [ -n "$matches" ]; then
        echo "$matches" | head -1
        return 0
    fi
    
    return 1
}

# Main function
main() {
    # Check arguments
    if [ $# -ne 3 ]; then
        print_error "Invalid number of arguments"
        show_usage
        exit 1
    fi
    
    local prd_filename="$1"
    local from_status="$2"
    local to_status="$3"
    
    # Validate statuses
    if ! validate_status "$from_status"; then
        print_error "Invalid from-status: $from_status"
        show_usage
        exit 1
    fi
    
    if ! validate_status "$to_status"; then
        print_error "Invalid to-status: $to_status"
        show_usage
        exit 1
    fi
    
    # Check if source and destination are the same
    if [ "$from_status" = "$to_status" ]; then
        print_warning "Source and destination are the same: $from_status"
        exit 0
    fi
    
    # Find the PRD file
    print_status "Looking for PRD file: $prd_filename in $from_status folder..."
    local source_file
    if ! source_file=$(find_prd_file "$prd_filename" "$from_status"); then
        print_error "PRD file not found: $prd_filename in $from_status folder"
        print_status "Available files in $from_status folder:"
        ls -la "$PRDS_DIR/$from_status/" 2>/dev/null || print_warning "Folder is empty or doesn't exist"
        exit 1
    fi
    
    # Get the filename without path
    local basename=$(basename "$source_file")
    
    # Check if destination file already exists
    local dest_file="$PRDS_DIR/$to_status/$basename"
    if [ -f "$dest_file" ]; then
        print_warning "Destination file already exists: $dest_file"
        read -p "Do you want to overwrite it? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_status "Operation cancelled"
            exit 0
        fi
    fi
    
    # Create destination directory if it doesn't exist
    mkdir -p "$PRDS_DIR/$to_status"
    
    # Move the file
    print_status "Moving $source_file to $dest_file..."
    if mv "$source_file" "$dest_file"; then
        print_success "PRD moved successfully from $from_status to $to_status"
        print_status "File: $basename"
        
        # Update database status if possible
        print_status "Note: You may need to update the database status manually"
        print_status "Use the AI Agent Factory dashboard or API to sync the status"
        
    else
        print_error "Failed to move PRD file"
        exit 1
    fi
}

# Run main function
main "$@"
