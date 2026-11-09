keywords = ["AND", "OR", "NOT", "XOR"]

print("=== Logic Gate Truth Table Simulator ===")
print("Type an expression such as: (A AND B) OR (NOT C)")
print("Words allowed: AND, OR, NOT, XOR")
print("Type 'gates' to see the seven standard gates, or 'quit' to stop.")

while True:
    print("")
    expression = input("Expression: ").strip()

    if expression == "":
        continue

    if expression.lower() == "quit":
        break


    if expression.lower() == "gates":
        print("A B | AND OR XOR NAND NOR XNOR")
        for a in [0, 1]:
            for b in [0, 1]:
                and_out = 0
                if a == 1 and b == 1:
                    and_out = 1

                or_out = 0
                if a == 1 or b == 1:
                    or_out = 1

                xor_out = 0
                if a != b:
                    xor_out = 1

                nand_out = 1
                if and_out == 1:
                    nand_out = 0

                nor_out = 1
                if or_out == 1:
                    nor_out = 0

                xnor_out = 1
                if xor_out == 1:
                    xnor_out = 0

                print(a, b, "|", and_out, "  ", or_out, " ", xor_out, "  ",
                      nand_out, "   ", nor_out, "  ", xnor_out)

        print("NOT: 0 -> 1   1 -> 0")
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


    variables = []
    for word in words:
        if word == "(" or word == ")":
            continue
        if word.upper() in keywords:
            continue
        if word not in variables:
            variables.append(word)
    variables.sort()
    count = len(variables)

    if count == 0:
        print("No input variables found.")
        continue
    if count > 8:
        print("Too many variables (maximum is 8).")
        continue


    bad_name = False
    for name in variables:
        if name[0].isdigit() or name in ["True", "False", "None"]:
            bad_name = True
    if bad_name:
        print("Variable names must start with a letter (and cannot be True, False or None).")
        continue






    new_words = []
    for word in words:
        upper = word.upper()
        if upper == "AND":
            new_words.append("&")
        elif upper == "OR":
            new_words.append("|")
        elif upper == "NOT":
            new_words.append("~")
        elif upper == "XOR":
            new_words.append("^")
        else:
            new_words.append(word)
    python_expression = " ".join(new_words)


    valid = True
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

        try:
            result = eval(python_expression, {}, values)
        except Exception:
            valid = False
            break

        output = result & 1
        rows.append(line + "| " + str(output))

    if not valid:
        print("The expression is not valid. Check brackets and words.")
        continue


    header = ""
    for name in variables:
        header = header + name + " "
    header = header + "| OUTPUT"
    print(header)
    print("-" * len(header))
    for line in rows:
        print(line)

print("Goodbye!")
