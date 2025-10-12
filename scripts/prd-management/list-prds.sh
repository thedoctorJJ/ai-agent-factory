#!/bin/bash

# PRD Management Script - List PRDs by status
# Usage: ./list-prds.sh [status] [options]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PRDS_DIR="$PROJECT_ROOT/prds"

# Function to print colored output
print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

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
    echo "Usage: $0 [status] [options]"
    echo ""
    echo "Arguments:"
    echo "  status          Status folder to list (queue, in-progress, completed, failed, archive, all)"
    echo ""
    echo "Options:"
    echo "  -h, --help      Show this help message"
    echo "  -l, --long      Show detailed file information"
    echo "  -c, --count     Show only count of files"
    echo "  -s, --summary   Show summary of all statuses"
    echo ""
    echo "Examples:"
    echo "  $0                    # List all PRDs in all folders"
    echo "  $0 queue              # List PRDs in queue folder"
    echo "  $0 completed -l       # List completed PRDs with details"
    echo "  $0 -s                 # Show summary of all statuses"
    echo "  $0 -c                 # Show count of all PRDs"
    echo ""
    echo "Valid status folders:"
    echo "  queue, in-progress, completed, failed, archive, all"
}

# Function to validate status
validate_status() {
    local status="$1"
    case "$status" in
        queue|in-progress|completed|failed|archive|all)
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

# Function to list PRDs in a folder
list_prds_in_folder() {
    local folder="$1"
    local show_long="$2"
    local folder_path="$PRDS_DIR/$folder"
    
    if [ ! -d "$folder_path" ]; then
        print_warning "Folder does not exist: $folder"
        return 1
    fi
    
    # Count files (excluding README.md)
    local count=$(find "$folder_path" -name "*.md" -not -name "README.md" -type f | wc -l)
    
    if [ "$count" -eq 0 ]; then
        echo -e "${YELLOW}  No PRDs found${NC}"
        return 0
    fi
    
    echo -e "${CYAN}  Found $count PRD(s):${NC}"
    
    if [ "$show_long" = "true" ]; then
        # Show detailed information
        find "$folder_path" -name "*.md" -not -name "README.md" -type f -exec ls -la {} \; | while read -r line; do
            echo -e "    $line"
        done
    else
        # Show just filenames
        find "$folder_path" -name "*.md" -not -name "README.md" -type f -exec basename {} \; | sort | while read -r filename; do
            echo -e "    $filename"
        done
    fi
}

# Function to show summary
show_summary() {
    print_header "PRD Summary"
    
    local total=0
    local statuses=("queue" "in-progress" "completed" "failed" "archive")
    
    for status in "${statuses[@]}"; do
        local folder_path="$PRDS_DIR/$status"
        if [ -d "$folder_path" ]; then
            local count=$(find "$folder_path" -name "*.md" -not -name "README.md" -type f | wc -l)
            total=$((total + count))
            echo -e "${CYAN}$status:${NC} $count PRD(s)"
        else
            echo -e "${CYAN}$status:${NC} 0 PRD(s) (folder not found)"
        fi
    done
    
    echo ""
    echo -e "${GREEN}Total PRDs: $total${NC}"
}

# Function to show count only
show_count() {
    local total=0
    local statuses=("queue" "in-progress" "completed" "failed" "archive")
    
    for status in "${statuses[@]}"; do
        local folder_path="$PRDS_DIR/$status"
        if [ -d "$folder_path" ]; then
            local count=$(find "$folder_path" -name "*.md" -not -name "README.md" -type f | wc -l)
            total=$((total + count))
        fi
    done
    
    echo "$total"
}

# Main function
main() {
    local status="all"
    local show_long="false"
    local show_count_only="false"
    local show_summary_only="false"
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_usage
                exit 0
                ;;
            -l|--long)
                show_long="true"
                shift
                ;;
            -c|--count)
                show_count_only="true"
                shift
                ;;
            -s|--summary)
                show_summary_only="true"
                shift
                ;;
            -*)
                print_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
            *)
                if [ "$status" = "all" ]; then
                    status="$1"
                else
                    print_error "Too many arguments"
                    show_usage
                    exit 1
                fi
                shift
                ;;
        esac
    done
    
    # Handle special options
    if [ "$show_count_only" = "true" ]; then
        show_count
        exit 0
    fi
    
    if [ "$show_summary_only" = "true" ]; then
        show_summary
        exit 0
    fi
    
    # Validate status
    if ! validate_status "$status"; then
        print_error "Invalid status: $status"
        show_usage
        exit 1
    fi
    
    # Show PRDs
    if [ "$status" = "all" ]; then
        print_header "All PRDs"
        echo ""
        
        local statuses=("queue" "in-progress" "completed" "failed" "archive")
        for folder_status in "${statuses[@]}"; do
            print_header "$folder_status"
            list_prds_in_folder "$folder_status" "$show_long"
            echo ""
        done
        
        show_summary
    else
        print_header "PRDs in $status"
        echo ""
        list_prds_in_folder "$status" "$show_long"
    fi
}

# Run main function
main "$@"
