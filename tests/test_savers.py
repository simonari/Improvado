import unittest
import os
import json
from collections import OrderedDict

import savers


class DataConversion(unittest.TestCase):
    def test_leading_zeroes(self):
        test_vals = ["1.1.2020", "1.1.1"]
        true_vals = ["2020-01-01", "1-01-01"]

        for i in range(len(test_vals)):
            act_val = savers.bdate_to_iso(test_vals[i])
            self.assertEqual(true_vals[i], act_val,
                             f"Excpected: {true_vals[i]}, Actual: {act_val}")

    def test_blank_year(self):
        test_val = "1.1"
        true_val = "XXXX-01-01"
        act_val = savers.bdate_to_iso(test_val)

        self.assertEqual(true_val, act_val,
                         f"Excpected: {true_val}, Actual: {act_val}")

    def test_none(self):
        test_val = None
        true_val = None
        act_val = savers.bdate_to_iso(test_val)

        self.assertEqual(true_val, act_val)


class FillGapsFunction(unittest.TestCase):
    def test_fill_gaps(self):
        test_val = {"count": 3,
                    "items": [
                        {'id': 1, 'bdate': '16.4.2002',
                         'city': {'id': 1, 'title': 'city_A'},
                         'country': {'id': 1, 'title': 'country_A'},
                         'track_code': 'track_A',
                         'sex': 2,
                         'first_name': 'first_name_A', 'last_name': 'last_name_A',
                         'can_access_closed': True, 'is_closed': False},
                        {'id': 2, 'bdate': '4.2',
                         'track_code': 'track_B', 'sex': 1,
                         'first_name': 'first_name_B', 'last_name': 'last_name_B',
                         'can_access_closed': True, 'is_closed': True},
                        {'id': 3, 'bdate': '6.4',
                         'track_code': 'track_C',
                         'first_name': 'first_name_C', 'last_name': 'last_name_C',
                         'can_access_closed': True, 'is_closed': True}
                    ]}
        true_val = {"count": 3,
                    "items": [
                        {'id': 1, 'bdate': '2002-04-16',
                         'city': 'city_A',
                         'country': 'country_A',
                         'track_code': 'track_A',
                         'sex': 'Male',
                         'first_name': 'first_name_A', 'last_name': 'last_name_A',
                         'can_access_closed': True, 'is_closed': False},
                        {'id': 2, 'bdate': 'XXXX-02-04',
                         'city': None,
                         'country': None,
                         'track_code': 'track_B',
                         'sex': "Female",
                         'first_name': 'first_name_B', 'last_name': 'last_name_B',
                         'can_access_closed': True, 'is_closed': True},
                        {'id': 3, 'bdate': 'XXXX-04-06',
                         'city': None,
                         'country': None,
                         'track_code': 'track_C',
                         'sex': None,
                         'first_name': 'first_name_C', 'last_name': 'last_name_C',
                         'can_access_closed': True, 'is_closed': True}
                    ]}

        savers.fill_gaps(test_val)

        self.assertEqual(true_val, test_val)


class CleanJSONFunction(unittest.TestCase):
    def test_clean_json(self):
        test_val = {"count": 3,
                    "items": [
                        {'id': 1, 'bdate': '16.4.2002',
                         'city': {'id': 1, 'title': 'city_A'},
                         'country': {'id': 1, 'title': 'country_A'},
                         'track_code': 'track_A',
                         'sex': 2,
                         'first_name': 'first_name_A', 'last_name': 'last_name_A',
                         'can_access_closed': True, 'is_closed': False},
                        {'id': 2, 'bdate': '4.2',
                         'track_code': 'track_B', 'sex': 1,
                         'first_name': 'first_name_B', 'last_name': 'last_name_B',
                         'can_access_closed': True, 'is_closed': True},
                        {'id': 3, 'bdate': '6.4',
                         'track_code': 'track_C',
                         'first_name': 'first_name_C', 'last_name': 'last_name_C',
                         'can_access_closed': True, 'is_closed': True}
                    ]}
        true_val = {"count": 3,
                    "items": [
                        OrderedDict([
                            ("first_name", "first_name_A"),
                            ("last_name", "last_name_A"),
                            ("country", "country_A"),
                            ("city", 'city_A'),
                            ("bdate", '2002-04-16'),
                            ("sex", 'Male')
                        ]),
                        OrderedDict([
                            ("first_name", "first_name_B"),
                            ("last_name", "last_name_B"),
                            ("country", None),
                            ("city", None),
                            ("bdate", 'XXXX-02-04'),
                            ("sex", 'Female')
                        ]),
                        OrderedDict([
                            ("first_name", "first_name_C"),
                            ("last_name", "last_name_C"),
                            ("country", None),
                            ("city", None),
                            ("bdate", 'XXXX-04-06'),
                            ("sex", None)
                        ])
                    ]}

        savers.clean_json(test_val)

        self.assertEqual(test_val, true_val)


class CreateFileFunction(unittest.TestCase):
    def test_json(self):
        test_vals = [
            os.path.join(os.getcwd(), "report.json"),
            os.path.join(os.path.dirname(os.getcwd()), "report.json")
        ]

        for test_val in test_vals:
            savers.create_file(test_val)

            with open(test_val) as f:
                f.seek(0, os.SEEK_END)
                self.assertTrue(f.tell() == 0)
            os.remove(test_val)

    def test_sv(self):
        test_vals = [
            os.path.join(os.getcwd(), "report.csv"),
            os.path.join(os.path.dirname(os.getcwd()), "report.tsv")
        ]
        true_vals = [
            ["First Name,Last Name,Country,City,Birthdate,Sex\n"],
            ["First Name\tLast Name\tCountry\tCity\tBirthdate\tSex\n"]
        ]

        for i, test_val in enumerate(test_vals):
            savers.create_file(test_val)
            with open(test_val) as f:
                self.assertEqual(f.readlines(), true_vals[i])
            os.remove(test_val)


class SaveReport(unittest.TestCase):
    def test_csv_single_write(self):
        test_val = {"count": 3,
                    "items": [
                        {'id': 1, 'bdate': '16.4.2002',
                         'city': {'id': 1, 'title': 'city_A'},
                         'country': {'id': 1, 'title': 'country_A'},
                         'track_code': 'track_A',
                         'sex': 2,
                         'first_name': 'first_name_A', 'last_name': 'last_name_A',
                         'can_access_closed': True, 'is_closed': False},
                        {'id': 2, 'bdate': '4.2',
                         'track_code': 'track_B', 'sex': 1,
                         'first_name': 'first_name_B', 'last_name': 'last_name_B',
                         'can_access_closed': True, 'is_closed': True},
                        {'id': 3, 'bdate': '6.4',
                         'track_code': 'track_C',
                         'first_name': 'first_name_C', 'last_name': 'last_name_C',
                         'can_access_closed': True, 'is_closed': True}
                    ]}

        true_val = [
            "First Name,Last Name,Country,City,Birthdate,Sex\n",
            "first_name_A,last_name_A,country_A,city_A,2002-04-16,Male\n",
            "first_name_B,last_name_B,,,XXXX-02-04,Female\n",
            "first_name_C,last_name_C,,,XXXX-04-06,\n"
        ]

        path = os.path.join(os.getcwd(), "report.csv")
        savers.create_file(path)
        savers.save(test_val, path)

        with open(path) as f:
            self.assertEqual(f.readlines(), true_val)

        os.remove(path)

    def test_tsv_single_write(self):
        test_val = {"count": 3,
                    "items": [
                        {'id': 1, 'bdate': '16.4.2002',
                         'city': {'id': 1, 'title': 'city_A'},
                         'country': {'id': 1, 'title': 'country_A'},
                         'track_code': 'track_A',
                         'sex': 2,
                         'first_name': 'first_name_A', 'last_name': 'last_name_A',
                         'can_access_closed': True, 'is_closed': False},
                        {'id': 2, 'bdate': '4.2',
                         'track_code': 'track_B', 'sex': 1,
                         'first_name': 'first_name_B', 'last_name': 'last_name_B',
                         'can_access_closed': True, 'is_closed': True},
                        {'id': 3, 'bdate': '6.4',
                         'track_code': 'track_C',
                         'first_name': 'first_name_C', 'last_name': 'last_name_C',
                         'can_access_closed': True, 'is_closed': True}
                    ]}

        true_val = [
            "First Name\tLast Name\tCountry\tCity\tBirthdate\tSex\n",
            "first_name_A\tlast_name_A\tcountry_A\tcity_A\t2002-04-16\tMale\n",
            "first_name_B\tlast_name_B\t\t\tXXXX-02-04\tFemale\n",
            "first_name_C\tlast_name_C\t\t\tXXXX-04-06\t\n"
        ]

        path = os.path.join(os.getcwd(), "report.tsv")
        savers.create_file(path)
        savers.save(test_val, path)

        with open(path) as f:
            self.assertEqual(f.readlines(), true_val)

        os.remove(path)

    def test_json_single_write(self):
        test_val = {"count": 3,
                    "items": [
                        {'id': 1, 'bdate': '16.4.2002',
                         'city': {'id': 1, 'title': 'city_A'},
                         'country': {'id': 1, 'title': 'country_A'},
                         'track_code': 'track_A',
                         'sex': 2,
                         'first_name': 'first_name_A', 'last_name': 'last_name_A',
                         'can_access_closed': True, 'is_closed': False},
                        {'id': 2, 'bdate': '4.2',
                         'track_code': 'track_B', 'sex': 1,
                         'first_name': 'first_name_B', 'last_name': 'last_name_B',
                         'can_access_closed': True, 'is_closed': True},
                        {'id': 3, 'bdate': '6.4',
                         'track_code': 'track_C',
                         'first_name': 'first_name_C', 'last_name': 'last_name_C',
                         'can_access_closed': True, 'is_closed': True}
                    ]}

        true_val = [[
            {"first_name": "first_name_A", "last_name": "last_name_A",
             "country": "country_A", "city": "city_A", "bdate": "2002-04-16", "sex": "Male"},
            {"first_name": "first_name_B", "last_name": "last_name_B",
             "country": None, "city": None, "bdate": "XXXX-02-04", "sex": "Female"},
            {"first_name": "first_name_C", "last_name": "last_name_C",
             "country": None, "city": None, "bdate": "XXXX-04-06", "sex": None}
        ]]

        path = os.path.join(os.getcwd(), "report.json")
        savers.create_file(path)
        savers.save(test_val, path)

        with open(path, encoding="utf-8") as f:
            act_val = json.load(f)

        self.assertEqual(act_val, true_val)

        os.remove(path)

    def test_csv_multiple_write(self):
        test_val = [{"count": 1,
                     "items": [
                         {'id': 1, 'bdate': '16.4.2002',
                          'city': {'id': 1, 'title': 'city_A'},
                          'country': {'id': 1, 'title': 'country_A'},
                          'track_code': 'track_A',
                          'sex': 2,
                          'first_name': 'first_name_A', 'last_name': 'last_name_A',
                          'can_access_closed': True, 'is_closed': False}]},
                    {"count": 1,
                     "items": [
                         {'id': 2, 'bdate': '4.2',
                          'track_code': 'track_B', 'sex': 1,
                          'first_name': 'first_name_B', 'last_name': 'last_name_B',
                          'can_access_closed': True, 'is_closed': True}]},
                    {"count": 1,
                     "items": [
                         {'id': 3, 'bdate': '6.4',
                          'track_code': 'track_C',
                          'first_name': 'first_name_C', 'last_name': 'last_name_C',
                          'can_access_closed': True, 'is_closed': True}
                     ]}]

        true_val = [
            "First Name,Last Name,Country,City,Birthdate,Sex\n",
            "first_name_A,last_name_A,country_A,city_A,2002-04-16,Male\n",
            "first_name_B,last_name_B,,,XXXX-02-04,Female\n",
            "first_name_C,last_name_C,,,XXXX-04-06,\n"
        ]

        path = os.path.join(os.getcwd(), "report.csv")
        savers.create_file(path)

        for i in range(len(test_val)):
            savers.save(test_val[i], path)

        with open(path) as f:
            self.assertEqual(f.readlines(), true_val)

        os.remove(path)

    def test_tsv_multiple_write(self):
        test_val = [{"count": 1,
                     "items": [
                         {'id': 1, 'bdate': '16.4.2002',
                          'city': {'id': 1, 'title': 'city_A'},
                          'country': {'id': 1, 'title': 'country_A'},
                          'track_code': 'track_A',
                          'sex': 2,
                          'first_name': 'first_name_A', 'last_name': 'last_name_A',
                          'can_access_closed': True, 'is_closed': False}]},
                    {"count": 1,
                     "items": [
                         {'id': 2, 'bdate': '4.2',
                          'track_code': 'track_B', 'sex': 1,
                          'first_name': 'first_name_B', 'last_name': 'last_name_B',
                          'can_access_closed': True, 'is_closed': True}]},
                    {"count": 1,
                     "items": [
                         {'id': 3, 'bdate': '6.4',
                          'track_code': 'track_C',
                          'first_name': 'first_name_C', 'last_name': 'last_name_C',
                          'can_access_closed': True, 'is_closed': True}
                     ]}
                    ]

        true_val = [
            "First Name\tLast Name\tCountry\tCity\tBirthdate\tSex\n",
            "first_name_A\tlast_name_A\tcountry_A\tcity_A\t2002-04-16\tMale\n",
            "first_name_B\tlast_name_B\t\t\tXXXX-02-04\tFemale\n",
            "first_name_C\tlast_name_C\t\t\tXXXX-04-06\t\n"
        ]

        path = os.path.join(os.getcwd(), "report.tsv")
        savers.create_file(path)

        for i in range(len(test_val)):
            savers.save(test_val[i], path)

        with open(path) as f:
            self.assertEqual(f.readlines(), true_val)

        os.remove(path)

    def test_json_multiple_write(self):
        test_val = [{"count": 1,
                     "items": [
                         {'id': 1, 'bdate': '16.4.2002',
                          'city': {'id': 1, 'title': 'city_A'},
                          'country': {'id': 1, 'title': 'country_A'},
                          'track_code': 'track_A',
                          'sex': 2,
                          'first_name': 'first_name_A', 'last_name': 'last_name_A',
                          'can_access_closed': True, 'is_closed': False}]},
                    {"count": 1,
                     "items": [
                         {'id': 2, 'bdate': '4.2',
                          'track_code': 'track_B', 'sex': 1,
                          'first_name': 'first_name_B', 'last_name': 'last_name_B',
                          'can_access_closed': True, 'is_closed': True}]},
                    {"count": 1,
                     "items": [
                         {'id': 3, 'bdate': '6.4',
                          'track_code': 'track_C',
                          'first_name': 'first_name_C', 'last_name': 'last_name_C',
                          'can_access_closed': True, 'is_closed': True}
                     ]}]

        true_val = [
            [{"first_name": "first_name_A", "last_name": "last_name_A",
              "country": "country_A", "city": "city_A", "bdate": "2002-04-16", "sex": "Male"}],
            [{"first_name": "first_name_B", "last_name": "last_name_B",
              "country": None, "city": None, "bdate": "XXXX-02-04", "sex": "Female"}],
            [{"first_name": "first_name_C", "last_name": "last_name_C",
              "country": None, "city": None, "bdate": "XXXX-04-06", "sex": None}]
        ]

        path = os.path.join(os.getcwd(), "report.json")
        savers.create_file(path)

        for i in range(len(test_val)):
            savers.save(test_val[i], path)

        with open(path, encoding="utf-8") as f:
            act_val = json.load(f)

        self.assertEqual(act_val, true_val)

        os.remove(path)


if __name__ == '__main__':
    unittest.main()
