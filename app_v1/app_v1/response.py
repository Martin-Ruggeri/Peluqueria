def response(result = None, error = None):
  if (result != None):
    return { 'status': 'OK', 'response': { 'result': result } }
  else:
    return { 'status': 'ERROR', 'response': { 'error': error } }
