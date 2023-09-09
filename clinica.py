import datetime

class Paciente:
    def __init__(self, nome, telefone):
        self.nome = nome
        self.telefone = telefone

class Consulta:
    def __init__(self, paciente, data_hora, especialidade):
        self.paciente = paciente
        self.data_hora = data_hora
        self.especialidade = especialidade

class Clinica:
    def __init__(self):
        self.pacientes_cadastrados = []
        self.agendamentos = []
        self.carregar_pacientes() 
        self.carregar_consultas() 

    def carregar_pacientes(self):
        try:
            arquivo = open("pacientes.txt", "r") 
            for linha in arquivo: 
                nome, telefone = linha.strip().split(",") 
                paciente = Paciente(nome, telefone) 
                self.pacientes_cadastrados.append(paciente) 
            arquivo.close() 
        except FileNotFoundError: 
            print("Arquivo de pacientes não encontrado.")

    def carregar_consultas(self):
        try:
            arquivo = open("consultas.txt", "r") 
            for linha in arquivo: 
                nome, telefone, data_hora, especialidade = linha.strip().split(",") 
                data_hora = datetime.datetime.strptime(data_hora, "%d/%m/%Y %H:%M") 
                paciente = Paciente(nome, telefone) 
                consulta = Consulta(paciente, data_hora, especialidade) 
                self.agendamentos.append(consulta) 
            arquivo.close() 
        except FileNotFoundError: 
            print("Arquivo de consultas não encontrado.")

    def cadastrar_paciente(self):
        nome = input("Digite o nome do paciente: ")
        telefone = input("Digite o telefone do paciente: ")

        for paciente in self.pacientes_cadastrados:
            if paciente.telefone == telefone:
                print("Paciente já cadastrado.")
                return

        paciente = Paciente(nome, telefone)
        self.pacientes_cadastrados.append(paciente)
        print("Paciente cadastrado com sucesso!")
        self.salvar_paciente(paciente)

    def salvar_paciente(self, paciente):
        arquivo = open("pacientes.txt", "a") 
        arquivo.write(f"{paciente.nome}, {paciente.telefone}\n") 
        arquivo.close() 

    def marcar_consulta(self):
        if not self.pacientes_cadastrados:
            print("Não existem pacientes cadastrados.")
            return

        print("Lista de pacientes cadastrados:")
        for i, paciente in enumerate(self.pacientes_cadastrados):
            print(f"{i + 1}. {paciente.nome} - {paciente.telefone}")

        paciente_numero = int(input("Escolha o número do paciente: ")) - 1

        if paciente_numero < 0 or paciente_numero >= len(self.pacientes_cadastrados):
            print("Número de paciente inválido.")
            return

        paciente = self.pacientes_cadastrados[paciente_numero]

        data_hora = input("Digite a data e hora da consulta (formato: dd/mm/yyyy hh:mm): ")
        try:
            data_hora = datetime.datetime.strptime(data_hora, "%d/%m/%Y %H:%M")
        except ValueError:
            print("Data ou hora inválida.")
            return

        if data_hora <= datetime.datetime.now():
            print("Não é possível agendar consultas retroativas.")
            return

        especialidade = input("Digite a especialidade da consulta: ")

        for consulta in self.agendamentos:
            if consulta.data_hora == data_hora:
                print("Horário indisponível para consulta.")
                return

        consulta = Consulta(paciente, data_hora, especialidade)
        self.agendamentos.append(consulta)
        print("Consulta marcada com sucesso!")
        self.salvar_consulta(consulta) 

    def salvar_consulta(self, consulta):
        arquivo = open("consultas.txt", "a") 
        arquivo.write(f"{consulta.paciente.nome}, {consulta.paciente.telefone}, {consulta.data_hora.strftime('%d/%m/%Y %H:%M')}, {consulta.especialidade}\n")
        arquivo.close() 

    def cancelar_consulta(self):
        if not self.agendamentos:
            print("Não existem consultas agendadas.")
            return

        print("Lista de consultas agendadas:")
        for i, consulta in enumerate(self.agendamentos):
            print(f"{i + 1}. {consulta.paciente.nome} - {consulta.data_hora.strftime('%d/%m/%Y %H:%M')} - {consulta.especialidade}")

        consulta_numero = int(input("Escolha o número da consulta que deseja cancelar: ")) - 1

        if consulta_numero < 0 or consulta_numero >= len(self.agendamentos):
            print("Número de consulta inválido.")
            return

        consulta = self.agendamentos[consulta_numero]
        print(f"Consulta marcada para {consulta.data_hora.strftime('%d/%m/%Y %H:%M')} - {consulta.especialidade} será cancelada.")
        confirmacao = input("Deseja realmente cancelar? (S/N): ")
        if confirmacao.lower() == "s":
            self.agendamentos.remove(consulta)
            print("Consulta cancelada com sucesso!")
            self.atualizar_consultas() 

    def atualizar_consultas(self):
        arquivo = open("consultas.txt", "w") 
        for consulta in self.agendamentos:
            arquivo.write(f"{consulta.paciente.nome}, {consulta.paciente.telefone}, {consulta.data_hora.strftime('%d/%m/%Y %H:%M')}, {consulta.especialidade}\n") 
        arquivo.close() 

clinica = Clinica()

while True:
    print("\n----- MENU PRINCIPAL -----")
    print("1. Cadastrar paciente")
    print("2. Marcar consulta")
    print("3. Cancelar consulta")
    print("4. Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        clinica.cadastrar_paciente()
    elif opcao == "2":
        clinica.marcar_consulta()
    elif opcao == "3":
        clinica.cancelar_consulta()
    elif opcao == "4":
        print("Encerrando o programa...")
        break
    else:
        print("Opção inválida. Por favor, escolha uma opção válida.")
