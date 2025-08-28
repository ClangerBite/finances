# /////////////////////////////////////////////////////////////////////////////
# This module contains the Main function, which in turn starts the application. 
# The Main function only runs when the file is executed as a script.
# /////////////////////////////////////////////////////////////////////////////


from src.core.app import run_application


def main() -> None:
    run_application()
    

if __name__ == '__main__':
    main()
