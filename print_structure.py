import os

def print_tree(start_path, indent=""):
    for i, name in enumerate(sorted(os.listdir(start_path))):
        path = os.path.join(start_path, name)
        if name.startswith(".") or name == "venv" or name == "__pycache__":
            continue  # skip hidden/system files
        connector = "└── " if i == len(os.listdir(start_path)) - 1 else "├── "
        print(indent + connector + name)
        if os.path.isdir(path):
            print_tree(path, indent + ("    " if connector == "└── " else "│   "))

if __name__ == "__main__":
    print("📁 Your Project Structure:\n")
    print_tree(".")
