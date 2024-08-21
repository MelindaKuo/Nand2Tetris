class SymbolTable:
    KIND = ["STATIC", "FIELD", "ARG", "VAR"]

    def __init__(self):
        """Creates a new symbol table."""
        self.class_scope = {}  # Stores static and field variables
        self.subroutine_scope = {}  # Stores argument and local variables
        self.counts = {kind: 0 for kind in self.KIND}  # Keeps track of indices for each kind

    def reset(self):
        """Empties the subroutine scope and resets ARG and VAR indexes to 0."""
        self.subroutine_scope = {}
        self.counts["ARG"] = 0
        self.counts["VAR"] = 0

    def define(self, name, type, kind):
        """Defines a new variable and adds it to the symbol table."""
        if kind in ("STATIC", "FIELD"):
            scope = self.class_scope
        elif kind in ("ARG", "VAR"):
            scope = self.subroutine_scope
        else:
            raise ValueError(f"Invalid kind: {kind}")

        index = self.counts[kind]
        scope[name] = {"type": type, "kind": kind, "index": index}
        self.counts[kind] += 1

    def varCount(self, kind):
        """Returns the number of variables of the given kind already defined in the current scope."""
        return self.counts.get(kind, 0)

    def kindOf(self, name):
        """Returns the kind of the named identifier, or None if it is not found."""
        if name in self.subroutine_scope:
            return self.subroutine_scope[name]["kind"]
        elif name in self.class_scope:
            return self.class_scope[name]["kind"]
        else:
            return None

    def typeOf(self, name):
        """Returns the type of the named variable, or None if it is not found."""
        if name in self.subroutine_scope:
            return self.subroutine_scope[name]["type"]
        elif name in self.class_scope:
            return self.class_scope[name]["type"]
        else:
            return None

    def indexOf(self, name):
        """Returns the index of the named variable, or None if it is not found."""
        if name in self.subroutine_scope:
            return self.subroutine_scope[name]["index"]
        elif name in self.class_scope:
            return self.class_scope[name]["index"]
        else:
            return None

