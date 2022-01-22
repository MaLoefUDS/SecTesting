def int_abs_test(x, y):
    if x < 0:
        if y > 0:
            result_abs_1 = abs(x)
            result_abs_2 = abs(y)
            if result_abs_1 is not None and result_abs_2 is not None and result_abs_1 == result_abs_2:
                print('win')
