#!/usr/bin/env python3
"""
AutoReddit Pro - Main Entry Point
Launch the interactive application selector
"""

import os
import sys
from pathlib import Path

# Add core to Python path
core_path = Path(__file__).parent / "core"
sys.path.insert(0, str(core_path))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

class Colors:
    """Terminal colors for better UX"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_banner():
    """Print application banner"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}🚀 AUTOREDDIT PRO{Colors.END}")
    print(f"{Colors.CYAN}AI-Powered Reddit Content Automation{Colors.END}")
    print(f"{Colors.CYAN}Using Groq's Free Llama Models for Smart Posting{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'='*80}{Colors.END}")

def check_environment() -> bool:
    """Check if environment is properly configured"""
    print(f"\n{Colors.YELLOW}🔍 Checking Environment...{Colors.END}")
    
    required_vars = {
        "GROQ_API_KEY": "Groq API key for AI content generation",
        "REDDIT_CLIENT_ID": "Reddit app client ID",
        "REDDIT_CLIENT_SECRET": "Reddit app client secret", 
        "REDDIT_USERNAME": "Reddit username",
        "REDDIT_PASSWORD": "Reddit password",
        "REDDIT_USER_AGENT": "Reddit user agent"
    }
    
    missing_vars = []
    for var, description in required_vars.items():
        if not os.getenv(var):
            missing_vars.append(f"  • {var}: {description}")
    
    if missing_vars:
        print(f"{Colors.RED}❌ Missing environment variables:{Colors.END}")
        for var in missing_vars:
            print(f"{Colors.RED}{var}{Colors.END}")
        print(f"\n{Colors.YELLOW}📝 Please update your .env file with the missing variables{Colors.END}")
        return False
    else:
        print(f"{Colors.GREEN}✅ Environment configured correctly{Colors.END}")
        return True

def print_menu():
    """Print main application menu"""
    print(f"\n{Colors.BOLD}📋 AVAILABLE APPLICATIONS:{Colors.END}")
    print(f"{Colors.BLUE}{'─'*60}{Colors.END}")
    
    options = [
        ("1", "🌐 Enhanced Dashboard", "Web-based interface with full features"),
        ("2", "⚡ Terminal Automation", "Command-line automation tool"),
        ("3", "🧪 System Tests", "Run comprehensive system tests"),
        ("4", "🔧 Environment Check", "Validate setup and configuration"),
        ("5", "📖 Documentation", "View user guides and help"),
        ("Q", "🚪 Exit", "Quit the application")
    ]
    
    for num, title, desc in options:
        print(f"{Colors.CYAN}{num:>2}.{Colors.END} {Colors.BOLD}{title:<25}{Colors.END} {desc}")

def run_streamlit_dashboard():
    """Launch the Enhanced Streamlit Dashboard"""
    print(f"\n{Colors.GREEN}🌐 Launching Enhanced Dashboard...{Colors.END}")
    try:
        import subprocess
        subprocess.run([sys.executable, "-m", "streamlit", "run", "apps/enhanced_dashboard.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}❌ Error launching dashboard: {e}{Colors.END}")
    except FileNotFoundError:
        print(f"{Colors.RED}❌ Streamlit not installed. Run: pip install streamlit{Colors.END}")

def run_terminal_automation():
    """Launch the terminal automation tool"""
    print(f"\n{Colors.GREEN}⚡ Launching Terminal Automation...{Colors.END}")
    try:
        import subprocess
        subprocess.run([sys.executable, "apps/terminal_automation.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}❌ Error launching terminal automation: {e}{Colors.END}")

def run_system_tests():
    """Run comprehensive system tests"""
    print(f"\n{Colors.GREEN}🧪 Running System Tests...{Colors.END}")
    try:
        import subprocess
        subprocess.run([sys.executable, "tests/test_complete_system.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}❌ Error running tests: {e}{Colors.END}")

def show_documentation():
    """Show documentation menu"""
    print(f"\n{Colors.BLUE}📖 Documentation:{Colors.END}")
    docs = [
        "docs/USER_GUIDE.md - Complete user guide",
        "docs/TROUBLESHOOTING.md - Common issues and solutions", 
        "docs/API_REFERENCE.md - Technical documentation",
        "README.md - Project overview"
    ]
    
    for doc in docs:
        file_path = doc.split(" - ")[0]
        if os.path.exists(file_path):
            print(f"  {Colors.GREEN}✅ {doc}{Colors.END}")
        else:
            print(f"  {Colors.YELLOW}📝 {doc} (coming soon){Colors.END}")

def main():
    """Main application launcher"""
    print_banner()
    
    # Check environment
    if not check_environment():
        print(f"\n{Colors.YELLOW}⚠️  Please fix environment issues before continuing{Colors.END}")
        print(f"{Colors.BLUE}💡 Tip: Copy .env.example to .env and fill in your API keys{Colors.END}")
        return
    
    while True:
        print_menu()
        
        try:
            choice = input(f"\n{Colors.BOLD}Enter your choice: {Colors.END}").strip().upper()
            
            if choice == "1":
                run_streamlit_dashboard()
            elif choice == "2":
                run_terminal_automation()
            elif choice == "3":
                run_system_tests()
            elif choice == "4":
                check_environment()
            elif choice == "5":
                show_documentation()
            elif choice == "Q":
                print(f"\n{Colors.GREEN}👋 Goodbye! Happy Reddit automation!{Colors.END}")
                break
            else:
                print(f"{Colors.RED}❌ Invalid choice. Please enter 1-5 or Q{Colors.END}")
                
        except KeyboardInterrupt:
            print(f"\n\n{Colors.GREEN}👋 Goodbye! Happy Reddit automation!{Colors.END}")
            break
        except Exception as e:
            print(f"{Colors.RED}❌ Error: {e}{Colors.END}")

if __name__ == "__main__":
    main()
