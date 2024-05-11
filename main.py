import multiprocessing

from gemini import Gemini
from console import run_console
from colorama import Fore, Back, Style


if __name__ == "__main__":
    gemini = Gemini()
    in_out = multiprocessing.Manager().dict({
        'in': '',
        'out': '',
        'status': 'ready'
    })


    p = multiprocessing.Process(target=run_console, args=(in_out,))
    p.start()

    r = gemini.start()
    r = gemini.parse(r)
    if 'dialogo' in r:
        r = r['dialogo']
    
    print(f"{Fore.GREEN}Bot:\n{Style.RESET_ALL}{r}")
    while p.is_alive():
        inp = ''
        tag = 'entrada'
        if in_out['status'] == 'running':
            continue

        if in_out['status'] == 'ready':
            inp = input(f"{Fore.BLUE}Você: {Style.RESET_ALL}")
            if inp == '.exit':
                in_out['in'] = '.exit'
                break
        
        if in_out['status'] == 'done':
            inp = in_out['out']
            tag = 'saida'
            in_out['status'] = 'ready'

        if inp == '': continue

        r = gemini.generate(inp)
        r = gemini.parse(r)

        if 'dialogo' in r:
            print(f"{Fore.GREEN}Bot:\n{Style.RESET_ALL}{r['dialogo']}")

        if 'codigo' in r:
            in_out['in'] = r['codigo'].strip().replace('```', '')
            in_out['status'] = 'start'
