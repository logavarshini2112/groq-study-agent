import ast
import operator


# Allowed arithmetic operators
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}


def safe_calculate(node):
    # Number
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    # Binary operation
    if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
        left = safe_calculate(node.left)
        right = safe_calculate(node.right)

        return OPERATORS[type(node.op)](left, right)

    # Positive or negative number
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        value = safe_calculate(node.operand)

        if isinstance(node.op, ast.USub):
            return -value

        return value

    raise ValueError("Only basic arithmetic is allowed")


def calculator(expression):
    try:
        tree = ast.parse(expression, mode="eval")
        result = safe_calculate(tree.body)
        return result

    except Exception:
        return "Invalid calculation"


def read_notes(filename):
    try:
        with open(f"notes/{filename}", "r", encoding="utf-8") as file:
            content = file.read()

        return content

    except FileNotFoundError:
        return "Note not found"


def list_notes():
    import os

    try:
        return os.listdir("notes")
    except FileNotFoundError:
        return []


if __name__ == "__main__":
    print("Calculator:", calculator("10 + 20"))
    print("Calculator:", calculator("25 * 4"))
    print("Calculator:", calculator("100 / 5"))

    print("\nNotes:")
    print(read_notes("java_arrays.txt"))

    print("\nAvailable notes:")
    print(list_notes())