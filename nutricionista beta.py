from tkinter import *
from tkinter.ttk import Treeview
from tkinter import ttk
from tkinter import messagebox
import sqlite3


## BACKEND ##
      
class funcoes():
    def calcular_imc(self):
        if (self.cadastro_entry_altura.get()=="") or (self.cadastro_entry_peso.get()==""):
            self.msg = "Informe os valores"
            messagebox.showerror("Erro!", self.msg)
        else:
            self.peso=self.cadastro_entry_peso.get()
            self.altura=self.cadastro_entry_altura.get()
            self.peso = self.peso.replace(",", ".")
            self.altura = self.altura.replace(",", ".")
            self.peso = float(self.peso)
            self.altura = float(self.altura)

            self.imc = self.peso/(self.altura*self.altura)
            if (self.imc<17):
                self.cadastro_label_imcpaciente["text"]="%.2f" %self.imc + " (muito abaixo do peso)"
                self.cadastro_label_imcpaciente["foreground"]="red"
            if (self.imc>=17) and (self.imc<18.5):
                self.cadastro_label_imcpaciente["text"]="%.2f" % self.imc + " (abaixo do peso)"
                self.cadastro_label_imcpaciente["foreground"]="#DECD00"
            if (self.imc>=18.5) and (self.imc<25):
                self.cadastro_label_imcpaciente["text"]="%.2f" %self.imc + " (peso normal)"
                self.cadastro_label_imcpaciente["foreground"]= "green"
            if (self.imc>=25) and (self.imc<30):
                self.cadastro_label_imcpaciente["text"]="%.2f" %self.imc + " (acima do peso)"
                self.cadastro_label_imcpaciente["foreground"]= "#DECD00"
            if(self.imc>=30):
                self.cadastro_label_imcpaciente["text"]="%.2f" %self.imc + "(obesidade)"
                self.cadastro_label_imcpaciente["foreground"]= "red"

    def limpar_cadastro(self):
        self.cadastro_entry_nome.delete(0,END)
        self.cadastro_entry_email.delete(0,END)
        self.cadastro_entry_telefone.delete(0,END)
        self.cadastro_entry_altura.delete(0,END)
        self.cadastro_entry_peso.delete(0,END)
        self.cadastro_label_imcpaciente["text"]= ""
    
    def add_paciente(self):
        if (self.cadastro_entry_nome.get()=="") or (self.cadastro_entry_email.get()=="") or (self.cadastro_entry_telefone.get()=="") or (self.cadastro_entry_telefone.get()=="") or (self.cadastro_entry_altura.get()=="") or (self.cadastro_entry_peso.get()=="") or (self.cadastro_label_imcpaciente["text"]== ""):
            self.msg = "Preencha todos os campos e calcule o IMC!"
            messagebox.showerror("Erro!", self.msg)
        else:
            try:
                self.nome_bd = self.cadastro_entry_nome.get()
                self.email_bd = self.cadastro_entry_email.get()
                self.telefone_bd = self.cadastro_entry_telefone.get()
                self.peso_bd = self.cadastro_entry_peso.get()
                self.altura_bd = self.cadastro_entry_altura.get()
                self.imc_bd = self.imc
                self.sexo_bd = self.cadastro_drop_sexo['text']
                self.conecta_bd()
                self.cursor.execute(""" INSERT INTO pacientes (nome, email, telefone, peso, altura, imc, sexo)
                    VALUES(?,?,?,?,?,?,?)""",(self.nome_bd, self.email_bd, self.telefone_bd, self.peso_bd, self.altura_bd, self.imc_bd, self.sexo_bd))
                self.conn.commit()
                self.desconecta_bd()
                self.limpar_cadastro()
                self.msg = "Paciente cadastrado com sucesso!"
                messagebox.showinfo("Sucesso!", self.msg)
                self.select_lista()
            except:
                messagebox.showinfo("Erro!", "Email já registrado!")
    
    def conecta_bd(self):
        self.conn = sqlite3.connect("pacientes.db")
        self.cursor = self.conn.cursor()
  
    def desconecta_bd(self):
        self.cursor.close()

    def monta_tabela(self):
        self.conecta_bd()
        self.cursor.execute ("""CREATE TABLE IF NOT EXISTS pacientes(
            nome CHAR(40) NOT NULL,
            email CHAR(40) PRIMARY KEY,
            telefone CHAR(40) NOT NULL,
            peso FLOAT NOT NULL,
            altura FLOAT NOT NULL,
            imc FLOAT NOT NULL,
            sexo CHAR(40) NOT NULL)
            """)
        self.conn.commit()
        self.desconecta_bd()
        print('DATABASE CONECTADA')

    def select_lista(self):
        self.lista_pacientes.delete(*self.lista_pacientes.get_children())
        self.conecta_bd()
        lista = self.cursor.execute (""" SELECT nome, email FROM pacientes
            ORDER BY nome ASC; """)
        for i in lista:
            self.lista_pacientes.insert("",END, values=i)
        self.desconecta_bd()

    def lista_click(self, event):
        selecionado = self.lista_pacientes.item(self.lista_pacientes.selection())
        self.paciente_selecionado = selecionado['values'][0]
        self.paciente_primarykey = selecionado['values'][1]

    def inserir_vizualiza(self):
        self.conecta_bd()
        self.pacientes_selecionado = self.cursor.execute("""SELECT * FROM pacientes WHERE email = ?""",(self.paciente_primarykey,))
        for row in self.pacientes_selecionado:
            self.nome_paciente = row[0]
            self.email_paciente = row[1]
            self.telefone_paciente = row[2]
            self.peso_paciente = row[3]
            self.altura_paciente = row[4]
            self.imc_paciente = row[5]
            self.sexo_paciente = row[6]
        self.visualizar_db_nome['text'] = self.nome_paciente
        self.visualizar_db_email['text'] = self.email_paciente
        self.visualizar_db_telefone['text'] = self.telefone_paciente
        self.visualizar_db_peso['text'] = self.peso_paciente
        self.visualizar_db_altura['text'] = self.altura_paciente
        self.visualizar_db_imcpaciente['text'] ="%.2f" %self.imc_paciente
        self.visualizar_db_sexo['text'] = self.sexo_paciente
        
    def deletar_paciente(self):
        reply = messagebox.askyesno("Atenção!", "Você tem certeza que quer remover paciente?")
        if reply == True:
            self.conecta_bd()
            self.cursor.execute("""DELETE FROM pacientes WHERE email = ? """, (self.paciente_primarykey,))
            self.conn.commit()
            self.select_lista()
            self.desconecta_bd()
            self.janela_paciente.destroy()
            self.msg_remover = "Paciente removido com sucesso!"
            messagebox.showinfo("sucesso", self.msg_remover)
        else:
            pass

    def lista_calorias_click(self, event):
        selecionado = self.lista_alimentos.item(self.lista_alimentos.selection())
        self.calorias_alimento_selecionado = int(selecionado['values'][1])

    def calcula_calorias(self):
        self.caloria_dieta = self.calorias_alimento_selecionado + self.caloria_dieta
        self.visualizar_label_kcal['text'] = self.caloria_dieta
        if self.caloria_dieta >= 2500:
            self.visualizar_label_kcal['foreground']="red"

    def reseta_calorias(self):
        self.caloria_dieta = 0
        self.visualizar_label_kcal['text'] = self.caloria_dieta
        self.visualizar_label_calculo['text']= "0"

    def editar_paciente(self):
        pass

    def calcular_calorias_restantes(self):
        self.nova_dieta = abs(self.caloria_dieta - 2500)
        if self.caloria_dieta >=2500:
            self.text = "Remover"
        else:
            self.text = "Adicionar"
        self.visualizar_label_calculo['text']=self.text,str(self.nova_dieta)

    def inserir_alimentos(self):
        self.lista_alimentos.insert(parent='', index=1, values=('Café(50ml)','33'))
        self.lista_alimentos.insert(parent='', index=2, values=('Suco natural(240ml)','100'))
        self.lista_alimentos.insert(parent='', index=3, values=('Creveja(350ml)','147'))
        self.lista_alimentos.insert(parent='', index=4, values=('Refrigerante(350ml)','189'))
        self.lista_alimentos.insert(parent='', index=5, values=('Coxa de frango(100g)','144'))
        self.lista_alimentos.insert(parent='', index=6, values=('Hamburguer(56g)','116'))
        self.lista_alimentos.insert(parent='', index=7, values=('Linguiça(60g)','190'))
        self.lista_alimentos.insert(parent='', index=8, values=('Ovo frito(1 un)','108'))
        self.lista_alimentos.insert(parent='', index=9, values=('Arroz branco(25g)','41'))
        self.lista_alimentos.insert(parent='', index=10, values=('Feijão(20g)','78'))
        self.lista_alimentos.insert(parent='', index=11, values=('Tomate(100g)','20'))
        self.lista_alimentos.insert(parent='', index=12, values=('Pão frances(50g)','135'))
        self.lista_alimentos.insert(parent='', index=13, values=('Pizza(140g)','400'))
        self.lista_alimentos.insert(parent='', index=14, values=('Frango frito(100g)','400'))

## FRONTEND ##       

class App(funcoes):
    def __init__(self):
        self.root = Tk()
        self.principal_config()
        self.monta_tabela()
        self.select_lista()
        self.paciente_selecionado = ""
        self.root.mainloop()

    def principal_config(self):
        self.root.title('Nutricionista app')
        self.root.geometry("625x350")
        self.root.resizable(False, False)
        self.root.configure()
        
        self.label_pacientes = Label(self.root, text="PACIENTES")
        self.botao_adicionar = Button(self.root, text="Adicionar paciente", command=self.cadastro_config)
        self.botao_visualizar = Button(self.root, text="Vizualizar paciente", command=self.visualiza_config)
        self.botao_sair = Button(self.root, text="        Sair        ", command=self.root.destroy)
        self.lista_pacientes = ttk.Treeview(self.root, height=10, column=("col1", "col2"))
        self.lista_pacientes.heading("#0", text="")
        self.lista_pacientes.heading("#1", text="nome")
        self.lista_pacientes.heading("#2", text="email")
        self.lista_pacientes.column("#0", width=0, stretch=NO)
        self.lista_pacientes.column("#1", width=300, anchor=W)
        self.lista_pacientes.column("#2", width=300)
        self.scroll_lista = Scrollbar(self.root, orient="vertical")
        self.lista_pacientes.configure(yscroll=self.scroll_lista.set)
        self.lista_pacientes.bind("<ButtonRelease-1>", self.lista_click)
    
        #GRID
        self.label_pacientes.place(x=10, y=10)
        self.botao_adicionar.place(x=10, y=310)
        self.botao_visualizar.place(x=125, y=310)
        self.botao_sair.place(x=530, y=310)
        self.lista_pacientes.place(x=10, y=50)
        self.scroll_lista.place(x=596, y=50, height=225.5)
           
    def cadastro_config(self):      
        self.janela_cadastro = Toplevel()
        self.janela_cadastro.title('Cadastro de paciente')
        self.janela_cadastro.geometry("450x300")
        self.janela_cadastro.resizable(False, False)
        self.janela_cadastro.transient(self.root)
        self.janela_cadastro.focus_force()
        self.janela_cadastro.grab_set()
        
        #WIDGETS
        self.cadastro_label_novo = Label(self.janela_cadastro, text="NOVO PACIENTE")
        self.cadastro_label_nome = Label(self.janela_cadastro, text="Nome: ")
        self.cadastro_label_email = Label(self.janela_cadastro, text="Email: ")
        self.cadastro_label_telefone = Label(self.janela_cadastro, text="Telefone: ")
        self.cadastro_label_sexo = Label(self.janela_cadastro, text="Sexo: ")
        self.cadastro_label_altura = Label(self.janela_cadastro, text="Altura: ")
        self.cadastro_label_peso = Label(self.janela_cadastro, text="Peso: ")
        self.cadastro_label_imc = Label(self.janela_cadastro, text="IMC: ")
        self.cadastro_label_imcpaciente = Label(self.janela_cadastro, text="", foreground="black")
        self.cadastro_entry_nome = Entry(self.janela_cadastro)
        self.cadastro_entry_email = Entry(self.janela_cadastro)
        self.cadastro_entry_telefone = Entry(self.janela_cadastro)
        self.cadastro_entry_altura = Entry(self.janela_cadastro)
        self.cadastro_entry_peso = Entry(self.janela_cadastro)
        self.cadastro_botao_calculaimc = Button(self.janela_cadastro, text="Calcular IMC", command=self.calcular_imc)
        self.cadastro_botao_cadastrar = Button(self.janela_cadastro, text="  Cadastrar  ", command = self.add_paciente)
        self.cadastro_botao_limpar = Button(self.janela_cadastro, text="   Limpar   ", command=self.limpar_cadastro)
        self.cadastro_botao_sair = Button(self.janela_cadastro, text="    Voltar   ",command=self.janela_cadastro.destroy)
        self.SexoTipvar = StringVar(self.janela_cadastro)
        self.SexoTipv = ("Masculino", "Feminino ")
        self.SexoTipvar.set("Masculino")
        self.cadastro_drop_sexo = OptionMenu(self.janela_cadastro, self.SexoTipvar, *self.SexoTipv)
    
        
        #CADASTRO GRID
        self.cadastro_label_novo.place(x=10, y=10)
        self.cadastro_label_nome.place(x=10, y=50)
        self.cadastro_label_email.place(x=10, y=100)
        self.cadastro_label_telefone.place(x=10, y=150)
        self.cadastro_label_sexo.place(x=10, y=200)
        self.cadastro_label_altura.place(x=250, y=50)
        self.cadastro_label_peso.place(x=250, y=100)
        self.cadastro_label_imc.place(x=250, y=200)
        self.cadastro_label_imcpaciente.place(x=275, y=200)
        self.cadastro_entry_nome.place(x=75, y=50)
        self.cadastro_entry_email.place(x=75, y=100)
        self.cadastro_entry_telefone.place(x=75, y=150)
        self.cadastro_entry_altura.place(x=290, y=50)
        self.cadastro_entry_peso.place(x=290, y=100)
        self.cadastro_botao_calculaimc.place(x=250, y=150)
        self.cadastro_botao_cadastrar.place(x=10, y=260)
        self.cadastro_botao_limpar.place(x=100, y=260)
        self.cadastro_botao_sair.place(x=375, y=260)
        self.cadastro_drop_sexo.place(x=75, y=200)
    
    def visualiza_config(self):
        self.caloria_dieta = 0
        if self.paciente_selecionado != "":
            self.janela_paciente = Toplevel()
            self.janela_paciente.title('VIZUALIZAÇÃO PACIENTE')
            self.janela_paciente.geometry("900x300")
            self.janela_paciente.resizable(False, False)
            self.janela_paciente.transient(self.root)
            self.janela_paciente.focus_force()
            self.janela_paciente.grab_set()
            

            #WIDGETS
            self.visualizar_label_novo = Label(self.janela_paciente, text="PACIENTE")
            self.visualizar_label_nome = Label(self.janela_paciente, text="Nome: ")
            self.visualizar_label_email = Label(self.janela_paciente, text="Email: ")
            self.visualizar_label_telefone = Label(self.janela_paciente, text="Telefone: ")
            self.visualizar_label_sexo = Label(self.janela_paciente, text="Sexo: ")
            self.visualizar_label_altura = Label(self.janela_paciente, text="Altura: ")
            self.visualizar_label_peso = Label(self.janela_paciente, text="Peso: ")
            self.visualizar_label_imc = Label(self.janela_paciente, text="IMC: ")
            self.visualizar_label_kcal_text = Label(self.janela_paciente, text="Calorias(Kcal):")
            self.visualizar_label_kcal = Label(self.janela_paciente, text="0", foreground="green")
            self.visualizar_label_calculo = Label(self.janela_paciente, text="-----")
            self.visualizar_db_imcpaciente = Label(self.janela_paciente, text="", foreground="black")
            self.visualizar_db_nome = Label(self.janela_paciente, text="")
            self.visualizar_db_email = Label(self.janela_paciente, text="")
            self.visualizar_db_telefone = Label(self.janela_paciente, text="")
            self.visualizar_db_altura = Label(self.janela_paciente, text="")
            self.visualizar_db_peso = Label(self.janela_paciente, text="")
            self.visualizar_db_sexo = Label(self.janela_paciente, text="")
            self.visualizar_button_reset = Button(self.janela_paciente, text="Limpar selecionado", width=20, command=self.reseta_calorias)
            self.visualizar_button_remover = Button(self.janela_paciente, text="Remover paciente", command=self.deletar_paciente)
            self.visualizar_button_calcula = Button(self.janela_paciente, text="Calcular dieta", width=20, command=self.calcular_calorias_restantes)
            self.lista_button_add = Button(self.janela_paciente, text='Adicionar selecionado', width=20, command = self.calcula_calorias)
            self.lista_alimentos = Treeview(self.janela_paciente, height = 10,column=("col1", "col2"))
            self.lista_alimentos.heading("#0", text="")
            self.lista_alimentos.heading("#1", text="Alimento")
            self.lista_alimentos.heading("#2", text="Kcal")
            self.lista_alimentos.column("#0", width=0, stretch=NO)
            self.lista_alimentos.column("#1", width=150, anchor=W)
            self.lista_alimentos.column("#2", width=50)
            self.alimentos_scroll = Scrollbar(self.janela_paciente,orient="vertical")
            self.lista_alimentos.configure(yscroll=self.alimentos_scroll.set)
            self.lista_alimentos.bind("<ButtonRelease-1>", self.lista_calorias_click)

            #CADASTRO GRID
            self.visualizar_label_novo.place(x=10, y=10)
            self.visualizar_label_nome.place(x=10, y=50)
            self.visualizar_label_email.place(x=10, y=100)
            self.visualizar_label_telefone.place(x=10, y=150)
            self.visualizar_label_sexo.place(x=10, y=200)
            self.visualizar_label_altura.place(x=250, y=50)
            self.visualizar_label_peso.place(x=250, y=100)
            self.visualizar_label_imc.place(x=250, y=200)
            self.visualizar_label_kcal_text.place(x=500, y=50)
            self.visualizar_label_kcal.place(x=500, y=80)
            self.visualizar_label_calculo.place(x=500, y=250)
            self.visualizar_db_imcpaciente.place(x=275, y=200)
            self.visualizar_db_nome.place(x=75, y=50)
            self.visualizar_db_email.place(x=75, y=100)
            self.visualizar_db_telefone.place(x=75, y=150)
            self.visualizar_db_altura.place(x=290, y=50)
            self.visualizar_db_peso.place(x=290, y=100)
            self.visualizar_db_sexo.place(x=75, y=200)
            self.visualizar_button_remover.place(x=250, y=250)
            self.lista_button_add.place(x=500, y=150)
            self.visualizar_button_reset.place(x=500, y=180)
            self.visualizar_button_calcula.place(x=500,y=210)
            self.lista_alimentos.place(x=660,y=50)
            self.alimentos_scroll.place(x=850,y=50, height = 225.5)
            


            self.inserir_vizualiza()
            self.inserir_alimentos()
            
        else: 
            self.msg_remover = "Nem um paciente selecionado!"
            messagebox.showerror("Erro!", self.msg_remover)


App()

    