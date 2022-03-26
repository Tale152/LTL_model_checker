from model_checker import modelcheck

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
    print("\nChecking " + p)

    # 1
    no_wolf_with_goat_unsupervised = "!(wolf_left && goat_left && !employee_left) && !(wolf_right && goat_right && !employee_right)"
    print("\n" + no_wolf_with_goat_unsupervised)
    modelcheck(p, no_wolf_with_goat_unsupervised)

    no_popeye_with_spinach_unsupervised = "!(popeye_left && spinach_left && !employee_left) && !(popeye_right && spinach_right && !employee_right)"
    print("\n" + no_popeye_with_spinach_unsupervised)
    modelcheck(p, no_popeye_with_spinach_unsupervised)

    no_popeye_with_wine_with_computer_unsupervised = "!(popeye_left && wine_left && computer_left && !employee_left) && !(popeye_right && wine_right && computer_right && !employee_right)"
    print("\n" + no_popeye_with_wine_with_computer_unsupervised)
    modelcheck(p, no_popeye_with_wine_with_computer_unsupervised)

    # 3
    employee_not_slacking = "!(employee_left && X(employee_left) && X(X(employee_left))) && !(employee_right && X(employee_right) && X(X(employee_right)))"
    print("\n" + employee_not_slacking)
    modelcheck(p, employee_not_slacking)
    
    # 6
    employee_moving = "(employee_left U employee_trans) || (employee_right U employee_trans)"
    print("\n" + employee_moving)
    modelcheck(p, employee_moving)

    print("\n================")
