from mainScript import main

import sys
import traceback

try:
    main(mode="t")
    print("0")
except AssertionError:
    _, _, tb = sys.exc_info()
    traceback.print_tb(tb)
    tb_info = traceback.extract_tb(tb)
    filename, line, func, text = tb_info[-1]
    print('An error occurred on line {} in statement {}'.format(line, text))
