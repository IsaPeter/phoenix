def load_plugin(filename, context):
    source = open(filename).read()
    code = compile(source, filename, 'exec')
    exec(code, context)
    return context['func']

context = { 'func_one': func_one, 'func_two': func_two, 'abc': abc }
func = load_plugin(filename, context)
func()