import multiprocessing
import subprocess

from gemini import Gemini
from console import run_console
from colorama import Fore, Back, Style


if __name__ == "__main__":
    # Titulo do projeto e descrição
    print(f"{Fore.RED} == AutoGemini =={Style.RESET_ALL}")
    print(f"{Fore.YELLOW}.help {Style.RESET_ALL}para ajuda ou {Fore.YELLOW}.exit{Style.RESET_ALL} para sair")
    print(f"Carregando API...")
    
    gemini = Gemini()
    in_out = multiprocessing.Manager().dict({
        'in': '',
        'out': '',
        'status': 'ready'
    })

    p = multiprocessing.Process(target=run_console, args=(in_out,))
    p.start()

    # Inicia a conversa com o bot, inserindo a definição e recebendo a introdução do bot
    r = gemini.start()
    r = gemini.parse(r)
    if 'dialogo' in r:
        r = r['dialogo']
    
    print(f"{Fore.GREEN}Bot:\n{Style.RESET_ALL}{r}")
    while p.is_alive():
        inp = ''
        tag = 'entrada'

        # Processar etapas do console
        # running = console está processando
        # ready = console está pronto para receber input
        # done = console terminou de processar
        # start = console recebeu input e vai processar
        if in_out['status'] == 'running':
            continue

        if in_out['status'] == 'start':
            continue

        if in_out['status'] == 'ready':
            print('=-'*25)
            inp = input(f"{Fore.BLUE}Você: {Style.RESET_ALL}")

            if inp == '': continue
            # Verificar se o input é um comando
            if inp == '.exit':
                in_out['in'] = '.exit'
                break

            if inp == '.restart':
                in_out['in'] = '.restart'
                continue

            if inp == '.help':
                print(f"{Style.RESET_ALL}Converse com o {Fore.RED}AutoGemini{Style.RESET_ALL} ou utilize {Fore.BLUE}.{Style.RESET_ALL} para comandos especiais.")
                print(f"{Fore.YELLOW}.exit {Style.RESET_ALL}para sair")
                print(f"{Fore.YELLOW}.restart {Style.RESET_ALL}para reiniciar")
            
        if in_out['status'] == 'done':
            inp = in_out['out']
            tag = 'saida'
            in_out['status'] = 'ready'
            print(f"{Fore.YELLOW}Retorno Código:\n{Style.RESET_ALL}{inp}")

        # Gerar resposta do bot
        r = gemini.send_message(inp, tag=tag)

        # Processar resposta do bot
        # dialogo = dialogo do bot, resposta em texto plano
        # codigo = codigo para ser executado em python
        # comando = comando para ser executado no terminal
        # reiniciar = reiniciar o console
        if 'dialogo' in r:
            print(f"{Fore.GREEN}Bot:\n{Style.RESET_ALL}{r['dialogo']}")

        if 'codigo' in r:
            in_out['in'] = r['codigo'].strip().replace('```', '')
            in_out['status'] = 'start'
            print(f"{Fore.YELLOW}Executando código:\n{Style.RESET_ALL}{in_out['in']}")

        if 'comando' in r:
            cmd = r['comando'].strip().replace('```', '')
            try:
                out = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
            except subprocess.TimeoutExpired:
                out = f'TimeoutError: O comando [{cmd}] excedeu o tempo limite de 10 segundos.'

            print(f"{Fore.YELLOW}Comando:\n{Style.RESET_ALL}{out.stdout}")
            in_out['out'] = out.stdout
            in_out['status'] = 'done'

        if 'reiniciar' in r or ('dialogo' in r and '[reiniciar]' in r['dialogo']):
            in_out['in'] = '.restart'

    p.join()
