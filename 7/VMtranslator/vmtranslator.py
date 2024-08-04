import Parser
import CodeWriter

def vm_to_asm(vm_file, asm_file):
    parser = Parser(vm_file)
    code_writer  = CodeWriter(asm_file)

    while parser.has_more_lines():
        command_type = parser.command_type()

        if command_type == 'C_ARITHMETIC':
            code_writer.write_arithmetic(parser.arg1())
        elif command_type == 'C_PUSH':
            code_writer.write_push_pop('push', parser.arg1(), parser.arg2())
        elif command_type == 'C_POP':
            code_writer.write_push_pop('pop', parser.arg1(), parser.arg2())
        elif command_type == 'C_LABEL':
            code_writer.write_label(parser.arg1())
        elif command_type == 'C_GOTO':
            code_writer.write_goto(parser.arg1())
        elif command_type == 'C_IF':
            code_writer.write_if(parser.arg1())
        elif command_type == 'C_FUNCTION':
            code_writer.write_function(parser.arg1(), parser.arg2())
        elif command_type == 'C_RETURN':
            code_writer.write_return()
        elif command_type == 'C_CALL':
            code_writer.write_call(parser.arg1(), parser.arg2())

    code_writer.close()

