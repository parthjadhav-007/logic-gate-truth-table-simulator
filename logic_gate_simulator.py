binary_gates = ["AND", "NAND", "OR", "NOR", "XOR", "XNOR"]
unary_gates = ["NOT", "BUF"]


strength = {"NOT": 4, "BUF": 4,
            "AND": 3, "NAND": 3,
            "XOR": 2, "XNOR": 2,
            "OR": 1, "NOR": 1}

print("=== Logic Gate Truth Table Simulator (all gates) ===")
print("Type an expression such as: (A AND B) OR (NOT C)")
print("Gates: BUF, NOT, AND, NAND, OR, NOR, XOR, XNOR")
print("Type 'gates' to see every gate's truth table, or 'quit' to stop.")
print("Tip: for 3 or more inputs, NAND/NOR/XNOR are worked out left to right.")
print("     For a 3-input NAND use brackets:  NOT (A AND B AND C)")

while True:
    print("")
    expression = input("Expression: ").strip()

    if expression == "":
        continue

    if expression.lower() == "quit":
        break

    
    if expression.lower() == "gates":
        print("")
        print("One-input gates:")
        print("A | BUF NOT")
        for a in [0, 1]:
            print(a, "|", a, "  ", 1 - a)

        print("")
        print("Two-input gates:")
        names = ["AND", "NAND", "OR", "NOR", "XOR", "XNOR"]
        header = "A B | " + " ".join(names)
        print(header)
        print("-" * len(header))
        for a in [0, 1]:
            for b in [0, 1]:
                results = [a & b, 1 - (a & b),
                           a | b, 1 - (a | b),
                           a ^ b, 1 - (a ^ b)]
                line = str(a) + " " + str(b) + " | "
                for i in range(6):
                    line = line + str(results[i]).ljust(len(names[i])) + " "
                print(line)

        print("")
        print("What each gate does:")
        print("BUF  : output = input (copies the input)")
        print("NOT  : output is the opposite of the input")
        print("AND  : output is 1 only when ALL inputs are 1")
        print("NAND : NOT AND, output is 0 only when ALL inputs are 1")
        print("OR   : output is 1 when AT LEAST ONE input is 1")
        print("NOR  : NOT OR, output is 1 only when ALL inputs are 0")
        print("XOR  : output is 1 when the two inputs are DIFFERENT")
        print("XNOR : NOT XOR, output is 1 when the two inputs are the SAME")
        continue

    
    safe = True
    for ch in expression:
        if ch.isalnum() or ch == " " or ch == "(" or ch == ")" or ch == "_":
            continue
        safe = False
    if not safe:
        print("Only letters, numbers, spaces and brackets are allowed.")
        continue

    
    words = expression.replace("(", " ( ").replace(")", " ) ").split()


    postfix = []
    waiting = []
    previous = "start"
    error = ""

    for word in words:
        upper = word.upper()
        if upper == "BUFFER":
            upper = "BUF"

        if word == "(":
            if previous == "operand" or previous == "close":
                error = "Two inputs are next to each other. A gate word is missing."
            else:
                waiting.append("(")
                previous = "open"

        elif word == ")":
            if previous != "operand" and previous != "close":
                error = "A gate is missing an input before a closing bracket."
            else:
                found = False
                while len(waiting) > 0:
                    top = waiting.pop()
                    if top == "(":
                        found = True
                        break
                    postfix.append(top)
                if not found:
                    error = "The brackets do not match."
                previous = "close"

        elif upper in unary_gates:
            if previous == "operand" or previous == "close":
                error = upper + " cannot come right after an input."
            else:
                waiting.append(upper)
                previous = "unary"

        elif upper in binary_gates:
            if previous != "operand" and previous != "close":
                error = upper + " is missing an input on its left side."
            else:
                while (len(waiting) > 0 and waiting[-1] != "("
                       and strength[waiting[-1]] >= strength[upper]):
                    postfix.append(waiting.pop())
                waiting.append(upper)
                previous = "binary"

        else:
            if previous == "operand" or previous == "close":
                error = "Two inputs are next to each other. A gate word is missing."
            elif word != "0" and word != "1" and not (word[0].isalpha() or word[0] == "_"):
                error = "Input names must start with a letter."
            else:
                postfix.append(word)
                previous = "operand"

        if error != "":
            break

    if error == "":
        if previous != "operand" and previous != "close":
            error = "The expression ends too early. A gate is missing an input."

    if error == "":
        while len(waiting) > 0:
            top = waiting.pop()
            if top == "(":
                error = "The brackets do not match."
                break
            postfix.append(top)

    if error != "":
        print("The expression is not valid: " + error)
        continue

    # ---------- Find the input variables ----------
    variables = []
    for item in postfix:
        if item in strength:
            continue
        if item == "0" or item == "1":
            continue
        if item not in variables:
            variables.append(item)
    variables.sort()
    count = len(variables)

    if count > 8:
        print("Too many variables (maximum is 8).")
        continue

    
    rows = []
    total_rows = 2 ** count
    for row in range(total_rows):
        values = {}
        line = ""

        
        for position in range(count):
            power = count - 1 - position
            bit = (row // (2 ** power)) % 2
            values[variables[position]] = bit
            line = line + str(bit) + " "

        
        answer = []
        for item in postfix:
            if item == "NOT":
                x = answer.pop()
                answer.append(1 - x)
            elif item == "BUF":
                pass                      
            elif item in binary_gates:
                b = answer.pop()
                a = answer.pop()
                if item == "AND":
                    answer.append(a & b)
                elif item == "NAND":
                    answer.append(1 - (a & b))
                elif item == "OR":
                    answer.append(a | b)
                elif item == "NOR":
                    answer.append(1 - (a | b))
                elif item == "XOR":
                    answer.append(a ^ b)
                else:                     
                    answer.append(1 - (a ^ b))
            elif item == "0":
                answer.append(0)
            elif item == "1":
                answer.append(1)
            else:
                answer.append(values[item])

        rows.append(line + "| " + str(answer[0]))

    
    header = ""
    for name in variables:
        header = header + name + " "
    header = header + "| OUTPUT"
    print(header)
    print("-" * len(header))
    for line in rows:
        print(line)

print("Goodbye!")
