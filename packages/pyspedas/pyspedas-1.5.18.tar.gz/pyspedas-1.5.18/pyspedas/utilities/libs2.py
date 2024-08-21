import importlib
import inspect
import pkgutil

def find_in_package(root, myfunct):
    try:
        package = importlib.import_module(root)
    except ImportError:
        raise ValueError(f"The provided package '{root}' could not be imported.")
    
    matching_functions = []
    
    def traverse_package(package_name, package_path):
        for _, module_name, is_pkg in pkgutil.iter_modules(package_path):
            full_module_name = f"{package_name}.{module_name}"
            try:
                module = importlib.import_module(full_module_name)
                for name, obj in inspect.getmembers(module, inspect.isfunction):
                    if name == myfunct:
                        matching_functions.append(f"{full_module_name}.{name}")
            except ImportError:
                continue
            except Exception as e:
                print(f"Could not inspect module {full_module_name}: {e}")
                continue
            
            if is_pkg:
                try:
                    new_package_path = module.__path__
                    traverse_package(full_module_name, new_package_path)
                except AttributeError:
                    continue
    
    traverse_package(root, package.__path__)
    
    return matching_functions
 

if __name__ == "__main__":
    from inspect import getmembers, isfunction

    import pyspedas
    x = getmembers(pyspedas.goes, isfunction)
    print(x[0], x[1])
 