import ast
import sys


class CalculateMetrics(ast.NodeVisitor):
    """
    Calculates function metrics (line count and complexity) for Python code.
    Metrics are calculated for functions in classes, with function names prefixed by the class name.
    """
    def __init__(self):
        self.metrics = []
        self.current_class_name = None

    def visit_FunctionDef(self, node):
        """
        Processes function nodes and calculates their metrics.
        """
        if self.current_class_name:
            full_name = f"{self.current_class_name}.{node.name}"
            lines = self.calculate_lines(node)
            complexity = self.calculate_complexity(node)
            self.metrics.append((full_name, lines, complexity))

        # Continue traversing the children of this function node
        # (If this line was omitted, the traversal would stop at this node and its child nodes wouldn’t be visited.)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        """
        Sets class name context for functions and processes the class.
        """
        # Processes each function inside the class
        self.current_class_name = node.name
        self.generic_visit(node)
        self.current_class_name = None

    def calculate_lines(self, node):
        """
        Calculates the number of unique lines in the function body.
        """
        # Set to store unique line numbers within function bodies
        lines = set()

        # Look for function definitions and process only their bodies
        for sub_node in ast.walk(node):
            if isinstance(sub_node, ast.FunctionDef):
                # Process each line within the function body, ignoring the definition and decorators
                for body_node in sub_node.body:
                    for inner_node in ast.walk(body_node):
                        if hasattr(inner_node, 'lineno'):
                            lines.add(inner_node.lineno)

        return len(lines)

    def calculate_complexity(self, node):
        """
        Calculates the cyclomatic complexity of the function.
        """
        # Base complexity
        complexity = 1

        for line in ast.walk(node):
            # Count if statements
            if isinstance(line, ast.If):
                complexity += 1

            # Count loops
            elif isinstance(line, (ast.For, ast.While)):
                complexity += 1

            # Count comprehensions (add complexity for comprehensions and embedded ifs)
            elif isinstance(line, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
                complexity += 1
                # Add for each if inside the comprehension
                complexity += sum(1 for gen in line.generators if gen.ifs)

            # Count try/except blocks, +1 per except handler
            elif isinstance(line, ast.Try):
                complexity += len(line.handlers)

            # Count boolean operations, but add only 1 for the entire BoolOp
            elif isinstance(line, ast.BoolOp):
                # Add 1 for each operator (subtract 1 for the first value)
                complexity += len(line.values) - 1

        return complexity


def parse_file(filename):
    """
    Parses a Python file and returns metrics for all functions.
    """

    with open(filename, 'r') as f:
        code_tree = ast.parse(f.read(), filename=filename)
    m_calculator = CalculateMetrics()
    m_calculator.visit(code_tree)
    return m_calculator.metrics


def main():
    """
    Main function to process command-line files and print function metrics.
    """
    if len(sys.argv) < 2:
        sys.exit(1)

    final_metrics = []
    for filename in sys.argv[1:]:
        try:
            metrics = parse_file(filename)
            final_metrics.extend(metrics)
        except Exception as e:
            print(f"Unable to parse {filename}: {e}")

    # Print the results
    for name, line_count, complexity in final_metrics:
        print(f"{name}, Line count: {line_count}, Complexity: {complexity}")


if __name__ == "__main__":
    main()
