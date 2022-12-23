#!/usr/bin/env python3

'''
@author:zjl9959@gmail.com
@license:GPLv3
'''


class TestResult:
    def __init__(self) -> None:
        self._nb_pass = 0
        self._nb_failed = 0
        self._failed_cases = dict()

    def __repr__(self) -> str:
        str = "  - Total subcases:{0}, Passed subcases:{1}, Failed subcases:{2}\r\n".format(
            self._nb_pass + self._nb_failed,
            self._nb_pass,
            self._nb_failed)
        for case, desc in self._failed_cases.items():
            str += "   - Case:{0}, Expect:{1}, Actual:{2}\r\n".format(case, desc[1], desc[0])
        return str

    def add_case(self, ok, case_name=None, test_result=None, expect_result=None):
        if ok:
            self._nb_pass = self._nb_pass + 1
        else:
            self._nb_failed = self._nb_failed + 1
            if case_name:
                self._failed_cases[case_name] = (test_result, expect_result)

    def ok(self):
        return self._nb_pass >= 0 and self._nb_failed == 0
