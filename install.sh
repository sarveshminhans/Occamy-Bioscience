#!/bin/bash

# Occamy Field Operations System - Installation Script
# Tested on Ubuntu 20.04+, macOS, and Windows (Git Bash)

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Check Python version
check_python() {
    print_header "Checking Python Installation"
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d ' ' -f 2)
        print_success "Python 3 found: $PYTHON_VERSION"
        
        # Check if version is 3.8+
        REQUIRED_VERSION="3.8"
        if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
            print_success "Python version is compatible (>= 3.8)"
        else
            print_error "Python 3.8 or higher is required"
            exit 1
        fi
    else
        print_error "Python 3 is not installed"
        print_info "Please install Python 3.8 or higher from https://www.python.org/"
        exit 1
    fi
}

# Check pip
check_pip() {
    print_header "Checking pip"
    
    if command -v pip3 &> /dev/null; then
        print_success "pip3 found"
    else
        print_error "pip3 is not installed"
        print_info "Installing pip..."
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        python3 get-pip.py
        rm get-pip.py
    fi
}

# Create virtual environment
create_venv() {
    print_header "Creating Virtual Environment"
    
    if [ -d "venv" ]; then
        print_warning "Virtual environment already exists"
        read -p "Do you want to recreate it? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf venv
            python3 -m venv venv
            print_success "Virtual environment recreated"
        fi
    else
        python3 -m venv venv
        print_success "Virtual environment created"
    fi
}

# Activate virtual environment
activate_venv() {
    print_info "Activating virtual environment..."
    
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
        print_success "Virtual environment activated"
    elif [ -f "venv/Scripts/activate" ]; then
        source venv/Scripts/activate
        print_success "Virtual environment activated"
    else
        print_error "Could not find activation script"
        exit 1
    fi
}

# Install dependencies
install_dependencies() {
    print_header "Installing Dependencies"
    
    if [ -f "requirements.txt" ]; then
        print_info "Installing from requirements.txt..."
        pip install -r requirements.txt
        print_success "Dependencies installed"
    else
        print_error "requirements.txt not found"
        exit 1
    fi
}

# Setup environment file
setup_env() {
    print_header "Setting Up Environment"
    
    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            cp .env.example .env
            print_success "Created .env file from .env.example"
            
            # Generate random secret key
            SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
            
            # Update .env file
            if [[ "$OSTYPE" == "darwin"* ]]; then
                # macOS
                sed -i '' "s/change-this-to-a-random-secret-key-in-production/$SECRET_KEY/" .env
            else
                # Linux
                sed -i "s/change-this-to-a-random-secret-key-in-production/$SECRET_KEY/" .env
            fi
            
            print_success "Generated random SECRET_KEY"
        else
            print_warning ".env.example not found, skipping..."
        fi
    else
        print_warning ".env file already exists"
    fi
}

# Initialize database
init_database() {
    print_header "Initializing Database"
    
    print_info "Creating database tables..."
    python3 app.py &
    APP_PID=$!
    sleep 3
    kill $APP_PID 2>/dev/null || true
    
    if [ -f "occamy.db" ]; then
        print_success "Database initialized successfully"
        print_info "Default admin created: admin / admin123"
    else
        print_error "Database initialization failed"
        exit 1
    fi
}

# Load demo data
load_demo_data() {
    print_header "Loading Demo Data"
    
    read -p "Do you want to load demo data? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if [ -f "create_demo_data.py" ]; then
            python3 create_demo_data.py
            print_success "Demo data loaded"
        else
            print_warning "create_demo_data.py not found"
        fi
    else
        print_info "Skipping demo data"
    fi
}

# Run tests
run_tests() {
    print_header "Running Tests"
    
    read -p "Do you want to run tests? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if [ -f "tests.py" ]; then
            python3 tests.py
        else
            print_warning "tests.py not found"
        fi
    else
        print_info "Skipping tests"
    fi
}

# Print completion message
print_completion() {
    print_header "Installation Complete!"
    
    echo ""
    echo -e "${GREEN}✓ Installation successful!${NC}"
    echo ""
    echo -e "${YELLOW}Next Steps:${NC}"
    echo -e "  1. Activate virtual environment:"
    echo -e "     ${BLUE}source venv/bin/activate${NC}  (Linux/macOS)"
    echo -e "     ${BLUE}venv\\Scripts\\activate${NC}    (Windows)"
    echo ""
    echo -e "  2. Start the application:"
    echo -e "     ${BLUE}python app.py${NC}"
    echo ""
    echo -e "  3. Open in browser:"
    echo -e "     ${BLUE}http://localhost:5000${NC}"
    echo ""
    echo -e "  4. Login with:"
    echo -e "     ${BLUE}Username:${NC} admin"
    echo -e "     ${BLUE}Password:${NC} admin123"
    echo ""
    echo -e "${YELLOW}Important:${NC}"
    echo -e "  - Change the default admin password immediately"
    echo -e "  - Review .env file for configuration"
    echo -e "  - Read README.md for more information"
    echo ""
}

# Main installation flow
main() {
    clear
    print_header "Occamy Field Operations System - Installation"
    echo ""
    
    # Run checks and installation
    check_python
    check_pip
    create_venv
    activate_venv
    install_dependencies
    setup_env
    init_database
    load_demo_data
    run_tests
    print_completion
}

# Run main function
main
