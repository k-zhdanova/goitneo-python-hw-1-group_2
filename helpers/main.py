def format_error_msg(msg):
  return "\033[91m" + msg + "\033[0m"

def get_int_input(prompt, error_msg="Please enter a valid number"):
  while True:
    try:
      return int(input(prompt))
    except ValueError:
      print(format_error_msg(error_msg))
