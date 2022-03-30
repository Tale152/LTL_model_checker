from model_checker import modelcheck

def buildLTL(*sub_strings):
    LTL = ""
    for s in sub_strings:
        LTL += s
    return LTL

paths = [
    "./paths/path0.txt",
    #"./paths/path1.txt",
    #"./paths/path2.txt",
    #"./paths/path3.txt",
    #"./paths/path4.txt",
    #"./paths/path5.txt",
    #"./paths/path6.txt",
    #"./paths/path7.txt"
]
for p in paths:
    print("\nChecking " + p + "\n")

    # wolf and goat unsupervised
    w_g_u_L = "wolf_left && goat_left && !employee_left"
    w_g_u_R = "wolf_right && goat_right && !employee_right"

    # 1
    print("1. Combinations not allowed on same side unsupervised\n")

    print("(a) wolf with goat")
    no_wolf_with_goat_unsupervised = buildLTL("!(", w_g_u_L, ") && !(", w_g_u_R, ")")
    print(no_wolf_with_goat_unsupervised)
    modelcheck(p, no_wolf_with_goat_unsupervised)

    print("\n(b) popeye with spinach")
    no_popeye_with_spinach_unsupervised = "!(popeye_left && spinach_left && !employee_left) && !(popeye_right && spinach_right && !employee_right)"
    print(no_popeye_with_spinach_unsupervised)
    modelcheck(p, no_popeye_with_spinach_unsupervised)

    print("\n(c) popeye with wine with computer")
    no_popeye_with_wine_with_computer_unsupervised = "!(popeye_left && wine_left && computer_left && !employee_left) && !(popeye_right && wine_right && computer_right && !employee_right)"
    print(no_popeye_with_wine_with_computer_unsupervised)
    modelcheck(p, no_popeye_with_wine_with_computer_unsupervised)
    print("\n------")

    # 2
    print("\n2. A wolf must never stay on the same side with a goat for four or more consecutive states before the employee visits that state again (and the wolf is there).")
    NO_w_g_u_L_4X = buildLTL("!(", w_g_u_L, " && X(", w_g_u_L, " && X(", w_g_u_L, " && X(", w_g_u_L, "))))")
    NO_w_g_u_R_4X = buildLTL("!(", w_g_u_R, " && X(", w_g_u_R, " && X(", w_g_u_R, " && X(", w_g_u_R, "))))")
    no_wolf_with_goat_unsupervised_four_or_more = buildLTL(NO_w_g_u_L_4X, " && ", NO_w_g_u_R_4X)
    print("\n" + no_wolf_with_goat_unsupervised_four_or_more)
    modelcheck(p, no_wolf_with_goat_unsupervised_four_or_more)
    print("\n------")

    # 3
    print("\n3. An employee can spend at most three consecutive states each time at a certain side.")
    employee_not_slacking = "!(employee_left && X(employee_left) && X(X(employee_left))) && !(employee_right && X(employee_right) && X(X(employee_right)))"
    print("\n" + employee_not_slacking)
    modelcheck(p, employee_not_slacking)
    print("\n------")
    
    # 6
    print("\n6. The employee can only switch sides by using the boat.")
    employee_moving = "(employee_left U employee_trans) || (employee_right U employee_trans)"
    print("\n" + employee_moving)
    modelcheck(p, employee_moving)

    print("\n================")
