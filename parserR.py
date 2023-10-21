import ast
import subprocess
import sys

# Function to parse the Python script and extract imports
def extract_imports(script_file):
    with open(script_file, 'r') as file:
        tree = ast.parse(file.read())

    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                # Extract the first word after "import"
                package_name = n.name.split('.')[0]
                if package_name == 'dotenv':
                    package_name = 'python-dotenv'
                if package_name != 'os':  # Skip adding 'os'
                    imports.append(package_name)
        elif isinstance(node, ast.ImportFrom):
            # Extract the first word after "from"
            package_name = node.module.split('.')[0]
            if package_name == 'dotenv':
                package_name = 'python-dotenv'
            if package_name != 'os':  # Skip adding 'os'
                imports.append(package_name)

    return imports

# Function to create requirements.txt file
def create_requirements_file(packages):
    with open('requirements.txt', 'w') as file:
        for package in packages:
            file.write(f'{package}\n')

# Function to install missing packages
def install_missing_packages_from_requirements():
    failed_packages = []
    installed_packages = []
    for package in required_packages:  # Corrected variable name
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', package], check=True)
            installed_packages.append(package)
        except subprocess.CalledProcessError:
            failed_packages.append(package)

    if failed_packages:
        print(f'WARNING: Package(s) not found: {", ".join(failed_packages)} as they are not pip-installable and were skipped.')
    if installed_packages:
        print(f'Installed new packages: {", ".join(installed_packages)}')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python parser.py <app.py>")
        sys.exit(1)

    app_file = sys.argv[1]
    required_packages = extract_imports(app_file)
    print('Required packages:', required_packages)
    
    if required_packages:
        create_requirements_file(required_packages)
        print('Creating requirements.txt...')
        install_missing_packages_from_requirements()
    else:
        print('No missing packages to install.')
