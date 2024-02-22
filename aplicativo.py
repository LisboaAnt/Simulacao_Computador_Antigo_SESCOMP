import tkinter as tk
import time
import keyboard

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Terminal Antigo")
        self.root.configure(bg="black")  # Define o fundo padrão da janela como preto
        self.root.attributes('-fullscreen', True)  # Define a janela em modo de tela cheia
        
        # Remove as bordas ao redor da janela
        self.root.overrideredirect(True)
        self.root.geometry("{0}x{1}+0+0".format(self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        
        self.text_area = tk.Text(self.root, bg="black", fg="green", font=("Fixedsys", 18), bd=0, wrap=tk.WORD)
        self.text_area.grid(row=0, column=0, sticky="nsew", padx=20)
        self.text_area.config(insertbackground='green', state='disabled')  # Cor do cursor e tornando o texto somente leitura
        
        welcome_text = "\n Sistema de segurança ativado... Digite as 3 senhas para acessar o computador.\n"
        self.typing_effect(welcome_text)  # Aplica o efeito de digitação
        self.text_area.config(state='disabled')
        
        self.challenges = [
            ("Qual é o nome do país aliado da União Soviética que possui submarinos nucleares?", "Cuba", "Resposta correta!\n\nEssa é a primeira senha do computador.", "Ele fica no Caribe e teve uma crise dos mísseis em 1962 || "),
            ("Qual é o nome do líder soviético que morreu em 1979?", "Brezhnev", "Resposta correta!\n\nEssa é a segunda senha do computador.", "Dica: Ele foi o sucessor de Khrushchev e o antecessor de Andropov || "),
            ("Qual é o nome do presidente americano que enfrentou a União Soviética na guerra fria?", "Reagan", "Resposta correta!\n\nEssa é a terceira senha do computador.", "Dica: Ele foi um ator de Hollywood antes de entrar na política || ")
        ]

        
        self.current_challenge = 0
        self.errors = 0  # Contador de erros
        
        self.show_challenge()
        
        # Modificando o widget Entry para manter o indicador de foco
        self.entry = tk.Entry(self.root, bg="black", fg="green", insertbackground="green", font=("Fixedsys", 18), bd=0, highlightthickness=0)
        self.entry.grid(row=1, column=0, sticky="nsew", padx=20)
        self.entry.focus_set()
        self.entry.bind("<Return>", self.check_answer)
        self.entry.bind("<Key>", self.check_restart)
        
        # Impede o desfoque do campo de entrada
        self.entry.bind("<FocusOut>", lambda event: self.entry.focus_set())
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Monitora eventos de teclado para restaurar a tela cheia
        keyboard.on_press(self.restore_fullscreen)
        
        # Bloqueia a tecla Windows (esquerda)
        keyboard.block_key('windows')
        keyboard.block_key('tab')

        # Definindo a janela para sempre ficar no topo
        self.root.attributes("-topmost", True)

        # Variável para verificar se a aplicação está em execução
        self.running = True

    def restore_fullscreen(self, e=None):
        # Verifica se a aplicação ainda está em execução
        if self.running and not self.root.attributes('-fullscreen'):
            self.root.attributes('-fullscreen', True)

    def run(self):
        self.root.mainloop()
    
    def typing_effect(self, text):
        for char in text:
            self.text_area.config(state='normal')
            self.text_area.insert(tk.END, char)
            self.text_area.see(tk.END)
            self.text_area.config(state='disabled')
            self.root.update()
            time.sleep(0.01)  # Intervalo de tempo entre as letras
    
    def show_challenge(self):
        question, _, _, _ = self.challenges[self.current_challenge]
        self.typing_effect(f"\n\n{question}\n\n")  # Aplica o efeito de digitação
        self.text_area.config(bg='black', state='disabled')  # Corrigindo o fundo do texto para preto e tornando-o somente leitura
        
    def check_answer(self, event):
        _, answer, correct_response, incorrect_response = self.challenges[self.current_challenge]
        user_answer = self.entry.get().strip()
        
        if user_answer.lower() == answer.lower():
            self.typing_effect(correct_response)  # Aplica o efeito de digitação
            self.entry.delete(0, tk.END)
            self.current_challenge += 1
            self.errors = 0  # Reinicia o contador de erros
            if self.current_challenge < len(self.challenges):
                self.show_challenge()
            else:
                self.typing_effect("Parabéns! Todos os desafios foram resolvidos.\n\n")  # Aplica o efeito de digitação
                self.running = False  # Define que a aplicação não está mais em execução
                self.root.after(2000, self.root.destroy)
        else:
            self.errors += 1
            if self.errors == 3:
                self.text_area.config(state='normal', bg='black')  # Habilita a área de texto e define o fundo como branco
                self.text_area.delete(1.0, tk.END)  # Limpa o texto
                self.animate_text()
                self.entry.delete(0, tk.END)  # Limpa a entrada do usuário
            
            elif self.errors > 3:
                self.entry.delete(0, tk.END)  # Limpa a entrada do usuário
            else:
                self.typing_effect(incorrect_response +"Tentativas restantes:"+ str(3-self.errors) + "! \n\n")  # Aplica o efeito de digitação
        self.text_area.see(tk.END)
        
    def check_restart(self, event):
        if event.char == "&":
            self.restart_program()
        elif event.char == "@":
            self.close_program()
        
    def restart_program(self):
        self.root.destroy()
        new_instance = App()  # Inicia uma nova instância do programa
        new_instance.run()

    def close_program(self):
        self.root.destroy()

    def animate_text(self):
        for i in range(6):
            text = "Apagando o sistema" + "." * i
            self.text_area.config(state='normal')
            self.text_area.delete(1.0, tk.END)  # Limpa o texto anterior
            self.text_area.insert(tk.END, text)
            self.text_area.config(state='disabled')
            self.root.update()
            time.sleep(1)
        self.mensagem_final()

    def mensagem_final(self):
        self.text_area.config(state='normal')
        self.text_area.delete(1.0, tk.END)  # Limpa o texto anterior
        self.text_area.insert(tk.END, """
Intel UNDI, PXE-2.1 (build 083)
Copyright (C) 1975-1979 Intel Corporation

PXE-E61: Media test failure, check cable
PXE-M0F: Exiting Intel Boot Agent. 

Reboot and Select proper Boot device        
or Insert Boot Media in selected Boot device and press a key
""")
        self.text_area.config(state='disabled')

if __name__ == "__main__":
    app = App()
    app.run()
