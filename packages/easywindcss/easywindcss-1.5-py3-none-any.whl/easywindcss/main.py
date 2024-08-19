def check_et():
    print('Running easywindcss v1.5')


def install():
    import subprocess
    import os
    import json
    from colorama import Fore, Style, init

    # Initialize colorama
    init(autoreset=True)

    def print_header(message):
        """Print a header with color and formatting."""
        print(Fore.CYAN + Style.BRIGHT + "=" * 100)
        print(Fore.CYAN + Style.BRIGHT + f"{message}")
        print(Fore.CYAN + Style.BRIGHT + "=" * 100)

    def print_success(message):
        """Print a success message with color."""
        if message == "Tailwind CSS setup completed by easywindcss. They community awaits your creativity!":
            print(Fore.MAGENTA + Style.BRIGHT + f"[SUCCESS] {message}")

    def print_error(message):
        """Print an error message with color."""
        print(Fore.RED + Style.BRIGHT + f"[ERROR] {message}")

    def run_command(command, cwd=None):
        """Run a command in the specified directory and print its output."""
        try:
            result = subprocess.run(
                command, shell=True, cwd=cwd, text=True, capture_output=True)
            if result.returncode != 0:
                print_error(
                    f"Error occurred while running command '{command}':")
                print(result.stderr)
            elif command != "npm init -y":
                print_success(result.stdout)
        except Exception as e:
            print_error(f"Exception occurred: {e}")

    def run_command_in_background(command, cwd=None):
        """Run a command in the background."""
        try:
            process = subprocess.Popen(command, shell=True, cwd=cwd, text=True)
            return process
        except Exception as e:
            print_error(
                f"Exception occurred while running command in background: {e}")

    def validate_file_extensions(file_extensions):
        """Validate file extensions against a predefined list."""
        all_file_extensions = [
            'html', 'htm', 'pug', 'ejs', 'njk', 'liquid', 'erb',
            'js', 'jsx', 'ts', 'tsx', 'mjs', 'cjs',
            'css', 'scss', 'sass', 'less', 'pcss', 'postcss',
            'vue', 'svelte', 'php', 'erb', 'njk'
        ]
        valid_extensions = []
        invalid_extensions = []

        for ext in file_extensions:
            if ext in all_file_extensions:
                valid_extensions.append(ext)
            else:
                invalid_extensions.append(ext)

        if invalid_extensions:
            print(Fore.YELLOW + Style.BRIGHT +
                  f"[WARNING] Invalid or unsupported extensions: {', '.join(invalid_extensions)}. Please add them manually in tailwind.config.js")

        if not valid_extensions:
            raise ValueError("No valid file extensions provided.")

        return valid_extensions

    def validate_template_folder(folder_path):
        """Validate the template folder path to start with './'."""
        if not folder_path.startswith('./'):
            raise ValueError("Template folder path must start with './'.")

    def get_template_folder():
        """Get and validate the location of the template folder."""
        while True:
            try:
                template_folder = input(
                    Fore.BLUE + Style.BRIGHT + "Enter the location of the template folder (relative path, e.g., './src'): ")
                validate_template_folder(template_folder)
                return template_folder
            except ValueError as ve:
                print_error(ve)
            except Exception as e:
                print_error(f"Unexpected error: {e}")

    def get_file_extensions():
        """Get and validate file extensions from user input."""
        all_file_extensions = [
            'html', 'htm', 'pug', 'ejs', 'njk', 'liquid', 'erb',
            'js', 'jsx', 'ts', 'tsx', 'mjs', 'cjs',
            'css', 'scss', 'sass', 'less', 'pcss', 'postcss',
            'vue', 'svelte', 'php', 'erb', 'njk'
        ]

        while True:
            try:
                file_extensions = input(
                    "Enter the file extensions to include apart from html (comma-separated, e.g., 'html,js'): ").split(',')
                file_extensions = [ext.strip() for ext in file_extensions]
                valid_extensions = validate_file_extensions(file_extensions)
                if not valid_extensions:
                    raise ValueError("File extensions list cannot be empty.")
                return valid_extensions
            except ValueError as ve:
                print_error(ve)
            except Exception as e:
                print_error(f"Unexpected error: {e}")

    def validate_html_filename(filename):
        """Validate the HTML filename to ensure it ends with '.html'."""
        if not filename.endswith('.html'):
            raise ValueError("HTML filename must end with '.html'.")

    def create_flask_file(html_filename, template_folder):
    # Remove the './' from the beginning of the template_folder if present
        if template_folder.startswith('./'):
            template_folder = template_folder[2:]

        flask_content = f"""
from flask import Flask, render_template, url_for

app = Flask(__name__, template_folder='{template_folder}', static_folder='./dist')

@app.route('/')
def main():
    return render_template('{html_filename}')

if __name__ == '__main__':
    app.run(debug=True)
"""
        with open('app.py', 'w') as f:
            f.write(flask_content)
        print_success("Flask file 'app.py' created successfully.")

    def setup_tailwind():
        """Set up Tailwind CSS in the current directory."""
        print_header(
            "Hi! I'm EasyWindcss. I'll set up Tailwind CSS for you. Sit back while I handle it!\nGuess what? I am 6 times faster than the manual installation!")
        print(Fore.MAGENTA + Style.BRIGHT + f"Choose an installatiom option:")
        print(Fore.BLUE + Style.BRIGHT + f"[1] Only Tailwindcss", end='\t')
        print(Fore.YELLOW + Style.BRIGHT + f"[2] With Flask")

        def ask_type():
            insType = input('>>> ')
            if insType == '1' or insType == '2':
                return insType
            else:
                print_error("Invalid installation type choosen.")
                ask_type()
        insType = ask_type()

        print("Initializing Tailwind CSS Setup")

        # Initialize a new Node.js project
        print("Initializing your creative project...")
        def npmInstall():
            c = "npm init -y"
            d = "npm install -D tailwindcss" 
            e = "npx tailwindcss init"
            npm_path = "C:\\Program Files\\nodejs\\npm"
            npx_path = "C:\\Program Files\\nodejs\\npx"
            os.environ["PATH"] += os.pathsep + npm_path
            os.environ["PATH"] += os.pathsep + npx_path
            for i in [c,d,e]:
                result = subprocess.run(i, shell=True, cwd=None, text=True, capture_output=True)
                if str(result.returncode) == '1':
                    print(result.returncode , i)
                    print(Fore.RED + Style.BRIGHT + "Looks like Nodejs is not installed in your system.\nPlease install it by clicking this link and then re-run the command: https://nodejs.org/en/download/prebuilt-installer .\nAfter that close and reopen your code editor.")
                    exit()
            print("Installing Tailwind CSS CLI and dependencies...")
            print("Creating Tailwind configuration file...")

        npmInstall()
        
        # Get user input for content paths, file extensions, and template folder name
        template_folder = get_template_folder()
        file_extensions = get_file_extensions()
        html_filename = "index.html"

        # Create Tailwind CSS configuration with content paths
        content_paths = [
            f"{template_folder}/**/*.{ext}" for ext in file_extensions]
        content_paths_str = ',\n    '.join(
            f'"{path}"' for path in content_paths)

        print("Creating Tailwind configuration file with content paths...")
        with open('tailwind.config.js', 'w') as f:
            f.write(f"""
    /** @type {{import('tailwindcss').Config}} */
    module.exports = {{
    content: [
        "{template_folder}/**/*.html",
        {content_paths_str}
    ],
    theme: {{
        extend: {{}}  // No custom colors
    }},
    plugins: [],
    }}
            """)

        # Create Tailwind CSS file
        print("Creating Tailwind CSS file...")
        os.makedirs('src', exist_ok=True)
        with open('src/styles.css', 'w') as f:
            f.write("""
    @tailwind base;
    @tailwind components;
    @tailwind utilities;
            """)

        # Create the template folder and HTML file
        print(f"Creating template folder '{template_folder}' and HTML file...")
        os.makedirs(template_folder, exist_ok=True)
        html_file_path = os.path.join(template_folder, html_filename)
        with open(html_file_path, 'w', encoding='utf-8') as f:
            if insType != '2':
                f.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>By Easywindcss</title>
    <link href="../dist/output.css" rel="stylesheet">
    <style>
        .ani {
            transition: color 1s ease, font-size 1s ease, background 1s ease;
        }
    
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    
        .animate-fade-in {
            animation: fadeIn 1s ease-in-out;
        }
    
        .rectangle {
            position: absolute;
            width: 100px;
            height: 100px;
            background: rgba(255, 255, 255, 0.2);
            /* border-radius: 8px; */
            animation: flyAndRotate 30s linear infinite;
        }
        .rectangle:hover {
            background: rgba(255, 255, 255, 0.5);
        }
    
        @keyframes flyAndRotate {
            0% {
                transform: translateY(100vh) rotate(0deg);
            }
            100% {
                transform: translateY(-100vh) rotate(360deg);
            }
        }
    </style>
</head>
<body class="bg-gradient-to-r from-gray-900 to-gray-700 flex flex-col items-center justify-center min-h-screen text-gray-100 overflow-hidden">
    <!-- Flying rectangles -->
    <div class="rectangle ani" style="left: 10%; animation-duration: 30s;"></div>
    <div class="rectangle ani" style="left: 30%; animation-duration: 12s;"></div>
    <div class="rectangle ani" style="left: 50%; animation-duration: 8s;"></div>
    <div class="rectangle ani" style="left: 70%; animation-duration: 14s;"></div>
    <div class="rectangle ani" style="left: 90%; animation-duration: 9s;"></div>
    
    <h1 class="text-4xl font-bold mb-6 text-center hover:text-5xl ani animate-fade-in">
        <span class="text-pink-200">Easy</span><span class="text-gray-100">Windcss</span><span class="font-light"> v1.5</span>
    </h1>
    <div class="bg-gray-800 backdrop-blur-md border border-gray-600 rounded-lg p-8 max-w-lg text-center shadow-xl transition-transform transform hover:scale-105 hover:bg-gray-900 animate-fade-in">
        <h2 class="text-3xl font-semibold mb-4 animate-fade-in">Life is <span class="text-pink-300 font-bold">Colorful!</span></h2>
        <p class="text-lg mb-4 animate-fade-in">
            <b>Tailwind CSS</b> is now set up and ready to use. Enjoy crafting your sleek, modern website!
        </p>
        <p class="text-sm animate-fade-in">
            Developed by <a href="https://linkedin.com/in/sayedafaq" class="ani text-gray-300 font-semibold underline hover:text-pink-300" target="_blank">Sayed Afaq Ahmed</a>
        </p>
    </div>
    <h1 class="text-lg font-light text-center ani animate-fade-in mt-8 hover:text-yellow-600">
        <span>Read the </span><a target="_blank" href="https://pypi.org/project/easywindcss/" class="underline">PyPi documentation</a>
    </h1>
    <script>
        document.querySelectorAll('.rectangle').forEach(rectangle => {
            const randomLeft = Math.random() * 100; // Random horizontal position
            rectangle.style.left = `${randomLeft}%`;
        });
    </script>
</body>
</html>
            """)
            else:
                f.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tailwind CSS Setup</title>
    <link href="{{ url_for('static', filename='output.css') }}" rel="stylesheet">
    <style>
        .ani {
            transition: color 1s ease, font-size 1s ease, background 1s ease;
        }
    
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    
        .animate-fade-in {
            animation: fadeIn 1s ease-in-out;
        }
    
        .rectangle {
            position: absolute;
            width: 100px;
            height: 100px;
            background: rgba(255, 255, 255, 0.2);
            /* border-radius: 8px; */
            animation: flyAndRotate 30s linear infinite;
        }
        .rectangle:hover {
            background: rgba(255, 255, 255, 0.5);
        }
    
        @keyframes flyAndRotate {
            0% {
                transform: translateY(100vh) rotate(0deg);
            }
            100% {
                transform: translateY(-100vh) rotate(360deg);
            }
        }
    </style>
</head>
<body class="bg-gradient-to-r from-gray-900 to-gray-700 flex flex-col items-center justify-center min-h-screen text-gray-100 overflow-hidden">
    <!-- Flying rectangles -->
    <div class="rectangle ani" style="left: 10%; animation-duration: 30s;"></div>
    <div class="rectangle ani" style="left: 30%; animation-duration: 12s;"></div>
    <div class="rectangle ani" style="left: 50%; animation-duration: 8s;"></div>
    <div class="rectangle ani" style="left: 70%; animation-duration: 14s;"></div>
    <div class="rectangle ani" style="left: 90%; animation-duration: 9s;"></div>
    
    <h1 class="text-4xl font-bold mb-6 text-center hover:text-5xl ani animate-fade-in">
        <span class="text-pink-200">Easy</span><span class="text-gray-100">Windcss</span><span class="font-light"> v1.5</span>
    </h1>
    <div class="bg-gray-800 backdrop-blur-md border border-gray-600 rounded-lg p-8 max-w-lg text-center shadow-xl transition-transform transform hover:scale-105 hover:bg-gray-900 animate-fade-in">
        <h2 class="text-3xl font-semibold mb-4 animate-fade-in">Life is <span class="text-pink-300 font-bold">Colorful!</span></h2>
        <p class="text-lg mb-4 animate-fade-in">
            <b>Tailwind CSS</b> is now set up and ready to use. Enjoy crafting your sleek, modern website!
        </p>
        <p class="text-sm animate-fade-in">
            Developed by <a href="https://linkedin.com/in/sayedafaq" class="ani text-gray-300 font-semibold underline hover:text-pink-300" target="_blank">Sayed Afaq Ahmed</a>
        </p>
    </div>
    <h1 class="text-lg font-light text-center ani animate-fade-in mt-8 hover:text-yellow-600">
        <span>Read the </span><a target="_blank" href="https://pypi.org/project/easywindcss/" class="underline">PyPi documentation</a>
    </h1>
    <script>
        document.querySelectorAll('.rectangle').forEach(rectangle => {
            const randomLeft = Math.random() * 100; // Random horizontal position
            rectangle.style.left = `${randomLeft}%`;
        });
    </script>
</body>
</html>
            """)
        

        # Create an output directory
        print("Creating output directory...")
        os.makedirs('dist', exist_ok=True)

        # Add build and watch scripts to package.json
        print("Adding build and watch scripts to package.json...")
        package_json_path = 'package.json'
        with open(package_json_path, 'r+') as f:
            package_json = json.load(f)
            if "scripts" not in package_json:
                package_json["scripts"] = {}
            package_json["scripts"]["build:css"] = "npx tailwindcss -i src/styles.css -o dist/output.css"
            package_json["scripts"]["watch:css"] = "npx tailwindcss -i src/styles.css -o dist/output.css --watch"
            package_json["scripts"]["start"] = "http-server . -p 8080"
            f.seek(0)
            json.dump(package_json, f, indent=2)
            f.truncate()

        if insType == '2':
            print("Setting up Flask...")
            run_command("pip install flask")
            create_flask_file(html_filename, template_folder)
            print(Fore.CYAN + Style.BRIGHT + "=" * 80)
            print('To run your Flask application:')
            print(Fore.GREEN + Style.BRIGHT + "1. RUN: npm run watch:css")
            print(Fore.GREEN + Style.BRIGHT +
                  "2. In a new terminal, RUN: python app.py")
            print(Fore.GREEN + Style.BRIGHT +
                  "3. Open your browser and go to http://127.0.0.1:5000")
            print(Fore.CYAN + Style.BRIGHT + "=" * 80)
        else:
            # Display instructions for running the Tailwind CSS watch process
            print(Fore.CYAN + Style.BRIGHT + "=" * 80)
            print(
                'To start the Tailwind CSS watch process and run the webserver, do the following steps:')
            print(Fore.GREEN + Style.BRIGHT + "RUN : npm run watch:css")
            print(Fore.GREEN + Style.BRIGHT + f"Go to {template_folder}/{
                html_filename}, then click 'Go Live' and  your webpage will be displayed.")
            print(Fore.CYAN + Style.BRIGHT + "=" * 80)

        print_success(
            "Tailwind CSS setup completed by easywindcss. They community awaits your creativity!")

    setup_tailwind()
