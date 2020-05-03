import io
import os
import sys
import unittest
import codingtest

class TestCount(unittest.TestCase):

  comparison_dict = {
    'gt': 'greater than',
    'lt': 'less than',
    'eq': 'equal to'
  }
  test_file_name = 'test_file_name.txt'
  argument_lists = [[test_file_name, 'sum', 'gt'], ['invalid_file_name.txt', 'sum', 'gt', '1']]
  system_exit_code = 2
  invalid_int_list = [23, 234, '234p']
  int_list = list(range(1, 101))
  test_file_name = 'test_file.txt'
  comparison_values_list = [[100, 120], [239, 234], [5231, 5231]]
  print_check_list = [
    ['sum', 24, ['gt', 2, True], ['gt', 56, False]],
    ['avg', 324, ['lt', 2345, True], ['lt', 12, False]],
    ['median', 2344, ['eq', 2344, True], ['eq', 234235, False]]
  ]

  def tearDown(self):
    if os.path.exists(self.test_file_name):
      os.remove(self.test_file_name)

  def test_argument_parser(self):
    open(self.test_file_name, 'w')
    for testable_argument_list in self.argument_lists:
      with self.assertRaises(SystemExit) as e:
        codingtest.argument_parser(testable_argument_list)
      self.assertEqual(e.exception.code, self.system_exit_code)

  def test_read_numbers_from_file(self):
    with open(self.test_file_name, 'w') as f:
      for i in self.invalid_int_list:
        f.write(str(i) + '\n')
    self.assertRaisesRegex(ValueError, 'invalid literal .*',
                           codingtest.read_numbers_from_file, self.test_file_name)

    with open(self.test_file_name, 'w') as f:
      for i in self.int_list:
        f.write(str(i) + '\n')

    numbers_list = codingtest.read_numbers_from_file(self.test_file_name)
    for i, item in enumerate(numbers_list):
      # Items are equal
      self.assertEqual(item, self.int_list[i])

  def test_calculate_operation(self):
    result = codingtest.calculate_operation(self.int_list, 'sum')
    sum_resp = 0
    for i in self.int_list:
      sum_resp += i
    self.assertEqual(result, sum_resp)

    result = codingtest.calculate_operation(self.int_list, 'avg')
    avg_resp = sum_resp / len(self.int_list)
    self.assertEqual(result, avg_resp)

    result = codingtest.calculate_operation(self.int_list, 'median')
    sorted_list = sorted(self.int_list)
    list_len = len(self.int_list)
    median_index = (list_len - 1) // 2
    if median_index % 2:
      median_resp = sorted_list[median_index]
    else:
      median_resp = (sorted_list[median_index] + sorted_list[median_index + 1]) / 2
    self.assertEqual(result, median_resp)

  def test_print_result(self):
    for print_list in self.print_check_list:
      # Operation value check
      self.assertEqual(codingtest.print_result(print_list[1], print_list[0]),
                       '%s is: %s' % (print_list[0].capitalize(), print_list[1]))

      # True print statements when comparison
      comp_list = print_list[2]
      comp_text = '%s is: %s\n%s is %s %s' % (print_list[0].capitalize(), print_list[1],
                       print_list[1], self.comparison_dict[comp_list[0]], comp_list[1])
      self.assertEqual(codingtest.print_result(print_list[1], print_list[0],
                       comparison=comp_list[0], compared_value=comp_list[1], comparison_result=comp_list[2]),
                       comp_text)

      # False print statements when comparison
      comp_list = print_list[3]
      comp_text = '%s is: %s\n%s is not %s %s' % (print_list[0].capitalize(), print_list[1],
                  print_list[1], self.comparison_dict[comp_list[0]], comp_list[1])
      self.assertEqual(codingtest.print_result(print_list[1], print_list[0],
                       comparison=comp_list[0], compared_value=comp_list[1], comparison_result=comp_list[2]), comp_text)


  def test_compare_values(self):
    for comparison_list in self.comparison_values_list:
      comparison_result = codingtest.compare_values(comparison_list[0], comparison_list[1], 'gt')
      self.assertEqual(comparison_result, comparison_list[0] > comparison_list[1])

      comparison_result = codingtest.compare_values(comparison_list[0], comparison_list[1], 'lt')
      self.assertEqual(comparison_result, comparison_list[0] < comparison_list[1])

      comparison_result = codingtest.compare_values(comparison_list[0], comparison_list[1], 'eq')
      self.assertEqual(comparison_result, comparison_list[0] == comparison_list[1])


if __name__ == '__main__':
  unittest.main()
