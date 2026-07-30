import os
import sys
import importlib.util

def load_algorithm(llm, problem_category, algorithm_name):
    module_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 
        "generated_code", 
        llm, 
        problem_category, 
        f"{algorithm_name}.py"
    ))
    
    if not os.path.exists(module_path):
        raise FileNotFoundError(f"Missing file: {module_path}")
        
    spec = importlib.util.spec_from_file_location(algorithm_name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[algorithm_name] = module
    spec.loader.exec_module(module)
    
    func = getattr(module, algorithm_name, None)
    if func is None:
        raise AttributeError(f"Function `{algorithm_name}` not found in module.")
    return func