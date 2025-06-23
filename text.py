import os

def is_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            f.read(1024)
        return True
    except:
        return False

def gather_all_text(project_dir, output_file):
    with open(output_file, 'w', encoding='utf-8') as out:
        for root, _, files in os.walk(project_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if is_text_file(file_path):
                    out.write(f"\n--- {file_path} ---\n")
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            out.write(f.read())
                    except Exception as e:
                        out.write(f"[Could not read file: {e}]\n")

if __name__ == '__main__':
    # Change this to the root of your project directory
    project_folder = '/Users/ashlynn/Documents/aarons_coding_projects/remote_jobs'
    output_txt = 'text.txt'
    
    gather_all_text(project_folder, output_txt)
    print(f"✅ All text written to {output_txt}")
