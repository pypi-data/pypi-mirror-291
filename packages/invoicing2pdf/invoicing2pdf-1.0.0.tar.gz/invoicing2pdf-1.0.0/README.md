# What is this project?
In this we will create a Python pacakge from an application that creates PDF invoices out of Excel files. 

This Python project is based on : app5-invoice-generation project.

## Module vs. Package
In Python, both modules and packages are used to organize and manage code, but they serve different purposes and have distinct characteristics:

### 1. **Module**
- **Definition**: A module is a single file containing Python code. It can define functions, classes, variables, and runnable code.
- **File Structure**: A module is simply a `.py` file. For example, `example.py` is a module.
- **Usage**: Modules are used to break down a large codebase into smaller, reusable pieces. You can import a module using the `import` statement.
- **Example**:
  ```python
  # example.py
  def greet():
      return "Hello, World!"
  
  # another_script.py
  import example
  
  print(example.greet())  # Output: Hello, World!
  ```

### 2. **Package**
- **Definition**: A package is a collection of modules organized in a directory hierarchy. It allows you to group related modules together under a common namespace.
- **File Structure**: A package is a directory that contains a special `__init__.py` file (which can be empty), along with one or more modules or sub-packages. The `__init__.py` file signals to Python that the directory should be treated as a package.
- **Usage**: Packages are used to organize modules into a structured collection, making it easier to manage and import them. You can import a package or specific modules within a package.
- **Example**:
  ```
  mypackage/
      __init__.py
      module1.py
      module2.py
  ```

  ```python
  # In a script
  import mypackage.module1
  from mypackage import module2
  ```

### Summary:
- **Module**: A single Python file (`.py`) that can be imported and used in other scripts.
- **Package**: A directory containing multiple modules and an `__init__.py` file, used to organize modules into a hierarchical structure.