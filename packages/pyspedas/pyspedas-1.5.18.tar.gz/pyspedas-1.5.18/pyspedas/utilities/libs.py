"""
Displays location of source files, one line of documentation and the function name based on the request
"""

import importlib
import inspect
import itertools
import pkgutil
import sys
import io
from fnmatch import fnmatchcase

import pytplot
import pyspedas
import functools


def libs(function_name, package=None):
    """
    Searches for a specified function within pyspedas and pytplot and their submodules.

    Prints information about the function if found. The search is performed
    utilizing the imports defined in each __init__.py package file to display the
    callable function name.


    Parameters
    ----------
    function_name : str
        The name or partial name of the function to search for.
        If "*" or "?" are found in the function name, a case-insensitive wildcard match is performed,
            and function_name is treated as a substring to match.
    package : module, optional
        The pyspedas or pytplot package in which to search for the function.
        Default is None, which searches all pyspedas and pytplot modules.
        If a package is specified, the search is limited to that package (for example, pyspedas.mms).


    Returns
    -------
    all_names : list
        A list of all function names that match the search criteria.

    Notes
    -----
    - All submodules of pyspedas and pytplot are imported during the search. The package option
    simply narrows the search.
    - The function specifically searches for functions, not classes or other objects.
    - If multiple functions with the same name exist in different modules within the package,
    it will list them all.
    - The function handles ImportError exceptions by printing an error message and
    continuing the search, except 'pytplot.QtPlotter'. pytplot.QtPlotter results in error during import and is ignored.

    Examples
    --------
    >>> from pyspedas import libs
    >>> x = libs('fgm')
    [.... information about the functions ....]
    Number of functions found: 8
    >>> print(x)
    ['pyspedas.cluster.fgm', 'pyspedas.elfin.fgm', 'pyspedas.elfin.fgm.fgm_load',
    'pyspedas.goes.fgm', 'pyspedas.mms.fgm', 'pyspedas.mms.mms_load_fgm',
    'pyspedas.mms_load_fgm', 'pyspedas.themis.fgm']

    >>> y = libs('fgm', package=pyspedas.mms)
    [.... information about the functions ....]
    Number of functions found: 2
    >>> print(y)
    ['pyspedas.mms.fgm', 'pyspedas.mms.mms_load_fgm']

    >>> z = libs("*", package=pyspedas.goes)
    [.... information about the functions ....]
    Number of functions found: 15
    >>> print(z)
    ['pyspedas.goes.epead', 'pyspedas.goes.eps', 'pyspedas.goes.euvs', 'pyspedas.goes.fgm',
    'pyspedas.goes.hepad', 'pyspedas.goes.load', 'pyspedas.goes.load_orbit', 'pyspedas.goes.loadr',
    'pyspedas.goes.mag', 'pyspedas.goes.maged', 'pyspedas.goes.magpd', 'pyspedas.goes.mpsh',
    'pyspedas.goes.orbit', 'pyspedas.goes.sgps', 'pyspedas.goes.xrs']

    >>> p = libs("time*", package=pytplot)
    [.... information about the functions ....]
    Number of functions found: 12
    >>> print(p)
    ['pytplot.get_timespan', 'pytplot.time_clip', 'pytplot.time_datetime', 'pytplot.time_double',
    'pytplot.time_float', 'pytplot.time_float_one', 'pytplot.time_string', 'pytplot.time_string_one',
    'pytplot.timebar', 'pytplot.timespan', 'pytplot.timestamp', 'pytplot.tplot_math.time_clip']

    """
    all_names = []

    # Gate for no function_name
    if not function_name:
        print("No function name specified.")
        return all_names

    # Using separate functions for the wildcard and substring matching eliminates a test and branch in the inner loop

    def list_functions_substring(module, root, search_string, pacakge_obj):
        full_module_name = module.__name__
        for name, obj in inspect.getmembers(module):
            if (
                inspect.isfunction(obj)
                and (search_string in name)
                and (pacakge_obj.__name__ in obj.__module__)
            ):
                full_name = full_module_name + "." + name
                if full_name not in all_names:
                    source_file = inspect.getsourcefile(obj)
                    doc = inspect.getdoc(obj)
                    first_line_of_doc = (
                        doc.split("\n")[0] if doc else "No documentation"
                    )
                    print(
                        f"Function: {full_name}\nLocation: {source_file}\nDocumentation: {first_line_of_doc}\n"
                    )
                    all_names.append(full_name)
            elif isinstance(obj, functools.partial) and (search_string in name):
                original_func = obj.func
                full_name = full_module_name + "." + name
                if full_name not in all_names:
                    source_file = inspect.getsourcefile(original_func)
                    doc = inspect.getdoc(original_func)
                    first_line_of_doc = (
                        doc.split("\n")[0] if doc else "No documentation"
                    )
                    print(
                        f"Partial Function: {full_name}\nLocation: {source_file}\nDocumentation: {first_line_of_doc}\n"
                    )
                    all_names.append(full_name)

    def list_functions_wildcard(module, root, wildcard_pattern, pacakge_obj):
        full_module_name = module.__name__
        for name, obj in inspect.getmembers(module):
            if (
                inspect.isfunction(obj)
                and fnmatchcase(name.lower(), wildcard_pattern)
                and (pacakge_obj.__name__ in obj.__module__)
            ):
                full_name = full_module_name + "." + name
                if full_name not in all_names:
                    source_file = inspect.getsourcefile(obj)
                    doc = inspect.getdoc(obj)
                    first_line_of_doc = (
                        doc.split("\n")[0] if doc else "No documentation"
                    )
                    print(
                        f"Function: {full_name}\nLocation: {source_file}\nDocumentation: {first_line_of_doc}\n"
                    )
                    all_names.append(full_name)
            elif isinstance(obj, functools.partial) and fnmatchcase(
                name.lower(), wildcard_pattern
            ):
                original_func = obj.func
                full_name = full_module_name + "." + name
                if full_name not in all_names:
                    source_file = inspect.getsourcefile(original_func)
                    doc = inspect.getdoc(original_func)
                    first_line_of_doc = (
                        doc.split("\n")[0] if doc else "No documentation"
                    )
                    print(
                        f"Partial Function: {full_name}\nLocation: {source_file}\nDocumentation: {first_line_of_doc}\n"
                    )
                    all_names.append(full_name)

    def traverse_modules(package, function_name, package_obj):
        # Add the module itself
        walk_packages_iterator = pkgutil.walk_packages(
            path=package.__path__, prefix=package.__name__ + "."
        )
        combined_iterator = itertools.chain(
            ((None, package.__name__, True),), walk_packages_iterator
        )

        # Check for wildcard characters
        if "*" in function_name or "?" in function_name:
            wildcard = True
            # There is no 'fnmatchnocase', so lowercase the search pattern and function names before comparing
            # We'll add implicit leading and trailing '*', so any substring match will appear in the list
            wildcard_pattern = "*" + function_name.lower() + "*"
        else:
            wildcard = False
            wildcard_pattern = ""

        for _, modname, ispkg in combined_iterator:
            if ispkg and "qtplotter" not in modname.lower():
                # Save the current stdout so that we can restore it later
                original_stdout = sys.stdout

                # Redirect stdout to a dummy stream
                sys.stdout = io.StringIO()

                try:
                    module = importlib.import_module(modname)
                    if not package_obj:
                        package_obj = package

                    # Restore the original stdout
                    sys.stdout = original_stdout
                    if not wildcard:
                        list_functions_substring(
                            module, package, function_name, package_obj
                        )
                    else:
                        list_functions_wildcard(
                            module, package, wildcard_pattern, package_obj
                        )
                except ImportError as e:
                    # Restore the original stdout
                    sys.stdout = original_stdout
                    print(f"Error importing module {modname}: {e}")
                finally:
                    # Restore the original stdout
                    sys.stdout = original_stdout

    # Start here with the search
    if package is None:
        # Search in all pyspedas and pytplot modules
        traverse_modules(pyspedas, function_name, None)
        traverse_modules(pytplot, function_name, None)
    else:
        # Search only in the specified package
        if pyspedas.__name__ in package.__name__:
            traverse_modules(package, function_name, None)
        elif pytplot.__name__ in package.__name__:
            traverse_modules(package, function_name, None)
        else:
            print("Invalid package specified.")

    all_names = list(set(all_names))
    all_names.sort()

    if not all_names:
        print("No functions found.")
    else:
        print(f"Number of functions found: {len(all_names)}")

    return all_names

if __name__ == "__main__":
    x = libs('fgm', package=pyspedas.mms)