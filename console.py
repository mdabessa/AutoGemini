import sys
import io
from code import InteractiveConsole
import multiprocessing
import time


class Console:
    def __init__(self) -> None:
        self.console = InteractiveConsole()
        self.history = []

        with open('./base.py', 'r') as f:
            self.base = f.read()


    def runcode(self, code: str) -> str:
        history = {'in': code}

        buffer = io.StringIO()
        sys.stdout = buffer

        code = self.formatCode(code)

        with open('./temp.py', 'w') as f:
            f.write(code)

        self.console.runcode(code)

        sys.stdout = sys.__stdout__
        output = buffer.getvalue()
        buffer.close()

        output = output.strip()
        output = f'<{len(self.history)}>:\n{output}'

        history['out'] = output
        self.history.append(history)

        return output


    def formatCode(self, code: str) -> str:
        code = code.replace('\n', '\n\t')
        code = code.replace('\t', '    ')

        code = self.base.replace("'{code}'", code)

        return code


    def exit(self):
        self.console.runcode('exit()')


    def close(self):
        self.exit()

    def restart(self):
        self.close()
        self.__init__()


def run_console(in_out):
    executer = Console()
    while True:
        if in_out['status'] != 'start':
            continue

        if in_out['in'] == '.exit':
            executer.exit()
            break

        if in_out['in'] == '.restart':
            executer.restart()
            in_out['status'] = 'ready'
            in_out['out'] = ''
            continue

        in_out['status'] = 'running'

        r = executer.runcode(in_out['in'])

        in_out['out'] = r
        in_out['status'] = 'done'


if __name__ == '__main__':
    manager = multiprocessing.Manager()
    in_out = manager.dict({'in': '', 'out': '', 'status': 'ready'})
    process = multiprocessing.Process(target=run_console, args=(in_out,))
    process.start()

    printed = False # evitar print(aguardando) varias vezes
    update = False # evitar input() antes de print(out)
    while process.is_alive():
        if update == False:
            print('codigo:')
            inp = input()

        if inp == '.kill':
            process.terminate()
            continue

        if in_out['status'] == 'done':
            in_out['status'] = 'ready'

            print(in_out['out'])

        if in_out['status'] != 'ready':
            if printed: continue
            print("Aguardando ficar [ready].")
            printed = True
            continue
        
        if update:
            update = False
            continue

        printed = False


        in_out['status'] = 'start'
        in_out['in'] = inp

        if inp == '.exit': break
        update = True
        time.sleep(0.3)

    process.join()
