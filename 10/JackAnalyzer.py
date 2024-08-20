import os
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine

class JackAnalyzer:
    def __init__(self, input_path):
        self.input_path = input_path
        self.jack_files = []

        if os.path.isdir(input_path):
            # If the input is a directory, get all .jack files
            self.jack_files = [os.path.join(input_path, f) for f in os.listdir(input_path) if f.endswith('.jack')]
        elif os.path.isfile(input_path) and input_path.endswith('.jack'):
            # If the input is a single file
            self.jack_files = [input_path]
        else:
            raise ValueError("Input should be a .jack file or a directory containing .jack files.")

    def analyze(self):
        for jack_file in self.jack_files:
            self.process_file(jack_file)

    def process_file(self, jack_file):
        output_file = jack_file.replace('.jack', '.xml')

        with open(jack_file, 'r') as input_file, open(output_file, 'w') as output:
            tokenizer = JackTokenizer(input_file)
            compilation_engine = CompilationEngine(tokenizer, output)
            compilation_engine.compileClass()

        print(f"Processed {jack_file} -> {output_file}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python JackAnalyzer.py <fileName.jack | folderName>")
    else:
        input_path = sys.argv[1]
        analyzer = JackAnalyzer(input_path)
        analyzer.analyze()
