print("🚀 Initializing African Critical Minerals Platform...")
print("🏔️ Group 34 | MINN2020A Project 2025")
print("📚 University of the Witwatersrand, Johannesburg")

# Import the integrated application
from app_integrator import app, app_manager

def main():
    """Main function to start the application"""
    try:
        # Start the Flask application
        app_manager.run_application()
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        print("💡 Troubleshooting tips:")
        print("   • Check if port 8080 is available")
        print("   • Ensure all dependencies are installed")
        print("   • Verify all module files are present")
        return 1
    
    return 0

if __name__ == '__main__':
    exit_code = main()
    exit(exit_code)
    
