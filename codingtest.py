#!/usr/bin/python
import sys
import argparse
from os import path

comparison_dict = {
  'gt': 'greater than',
  'lt': 'less than',
  'eq': 'equal to'
}

def argument_parser(args):
  """Define needed arguments"""
  parser = argparse.ArgumentParser()
  parser.add_argument('file_name', help='File that has numbers below each other')
  parser.add_argument('operation', choices=['sum', 'avg', 'median'],
                      help='Argument tells which calculation is made;\
                      sum: sum all the numbers together,\
                      avg: calculate the average of numbers,\
                      median: choose the median number')
  parser.add_argument('comparison', choices=['gt', 'lt', 'eq'], nargs='?',\
                      help='Make comparison \
                      between sum|avg|median and gived figure n;\
                      gt: sum|avg|median > n,\
                      lt: sum|avg|median < n,\
                      eq: sum|avg|median = n')
  parser.add_argument('n', nargs='?', type=int, help='Number what to compare')
  
  args = parser.parse_args(args)

  if not path.isfile(args.file_name):
    parser.error('Give correct file name! File named "%s" does not exist.' % args.file_name)

  if args.comparison:
    if not args.n:
      parser.error('the argument number [n] what to compare is required')

  return args

def read_numbers_from_file(file_name):
  """Read lines from file to integer list"""
  with open(file_name, 'r') as f:
    number_list = list(map(int, f.read().splitlines()))
  return number_list

def calculate_operation(number_list, operation):
  """Calculate needed result from list"""
  result = 0
  if any(x in operation for x in ['sum', 'avg']):
    for number in number_list:
      result += number
    if operation == 'avg':
      result = result / len(number_list)
  elif operation == 'median':
    sorted_list = sorted(number_list)
    list_len = len(number_list)
    median_index = (list_len - 1) // 2
    if median_index % 2:
      result = sorted_list[median_index]
    else:
      result = (sorted_list[median_index] + sorted_list[median_index + 1]) / 2
  return result

def print_result(result, operation, comparison=None, compared_value=None, comparison_result=None):
  """Print the result of operation and comparison if given"""
  print_text = ''
  print_text += '%s is: %.0f' % (operation.capitalize(), result)
  if comparison:
    if comparison_result:
      print_text += '\n%.0f is %s %s' % (result, comparison_dict[comparison], compared_value)
    else:
      print_text += '\n%.0f is not %s %s' % (result, comparison_dict[comparison], compared_value)
  return print_text

def compare_values(compared_value, value, comparison):
  """Compare compared value to another value"""
  if comparison == 'gt':
    comparison_result = True if compared_value > value else False
  if comparison == 'lt':
    comparison_result = True if compared_value < value else False
  if comparison == 'eq':
    comparison_result = True if compared_value == value else False
  return comparison_result

def main():
  """Calculate operation and compare it to another value

  Calculate a sum, average or median from the numbers in a file, compare the
  result to a given number and prints out the result from the comparison.
  """
  args = argument_parser(sys.argv[1:])
  number_list = read_numbers_from_file(args.file_name)
  result = calculate_operation(number_list, args.operation)
  compared_value = None
  comparison_result = None
  if args.n:
    compared_value = int(args.n)
    comparison_result = compare_values(result, compared_value, args.comparison)
  print(print_result(result, args.operation, args.comparison, compared_value, comparison_result))


if __name__ == '__main__':
  main()
