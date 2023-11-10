import os

def read_input_as_lines(day, strip=True):
    with open(f"inputs\\day{day}.txt") as f:
        return [line.strip() if strip else line[:-1] for line in f]
    
def read_examples_as_lines(day, strip=True):
    with open(f"inputs\\day{day}_ex.txt") as f:
        return [line.strip() if strip else line[:-1] for line in f]

def generate_solution_files():
    """Generates non-existent solution files from the day0 template. 
    
    Won't overwrite a filed that exists, so delete any boilerplate files that 
    you want to regenerate, without disturbing existing solutions. 
    """
    lns = []
    with open("solutions\\day0.py", "r") as f:
        lns = [line.strip() for line in f]
    
    for i in range(1,26):
        if os.path.exists(f"solutions\\day{i}.py"):
            continue
        
        with open(f"solutions\\day{i}.py", "w") as f:    
            for ln in lns:
                ln = ln.replace("XXX", str(i))
                ln = ln.replace("print", "\tprint")
                ln = ln.replace("results = ", "\tresults = ")
                ln = ln.replace("pass", "\tpass")
                ln = ln.replace("input_lines ", "\tinput_lines ")
                f.write(ln + "\n")
    return