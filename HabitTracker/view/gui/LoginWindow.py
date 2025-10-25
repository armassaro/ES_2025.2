import tkinter as tk
from tkinter import messagebox

class LoginWindow:
    """Janela de login/cadastro."""
    
    def __init__(self, user_model):
        self.user_model = user_model
        self.authenticated = False
        
        self.root = tk.Tk()
        self.root.title("Habit Tracker - Login")
        self.root.geometry("400x500")
        self.root.configure(bg='#2c3e50')
        self.root.resizable(False, False)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura a interface de login."""
        # Logo/Título
        tk.Label(
            self.root,
            text="🎯 Habit Tracker",
            font=('Arial', 24, 'bold'),
            bg='#2c3e50',
            fg='white'
        ).pack(pady=(40, 10))
        
        tk.Label(
            self.root,
            text="Sistema de Gerenciamento de Hábitos",
            font=('Arial', 10),
            bg='#2c3e50',
            fg='#ecf0f1'
        ).pack(pady=(0, 40))
        
        # Frame central
        frame = tk.Frame(self.root, bg='white', padx=30, pady=30)
        frame.pack(padx=40, pady=20, fill='both', expand=True)
        
        # Usuário
        tk.Label(
            frame,
            text="Usuário:",
            font=('Arial', 10, 'bold'),
            bg='white'
        ).pack(anchor='w', pady=(0, 5))
        
        self.username_entry = tk.Entry(frame, font=('Arial', 11), width=30)
        self.username_entry.pack(pady=(0, 15))
        
        # Senha
        tk.Label(
            frame,
            text="Senha:",
            font=('Arial', 10, 'bold'),
            bg='white'
        ).pack(anchor='w', pady=(0, 5))
        
        self.password_entry = tk.Entry(frame, font=('Arial', 11), show='*', width=30)
        self.password_entry.pack(pady=(0, 25))
        
        # Botões
        btn_frame = tk.Frame(frame, bg='white')
        btn_frame.pack(fill='x')
        
        tk.Button(
            btn_frame,
            text="Entrar",
            command=self._login,
            bg='#27ae60',
            fg='white',
            font=('Arial', 11, 'bold'),
            width=12,
            height=2,
            cursor='hand2'
        ).pack(side='left', padx=(0, 10))
        
        tk.Button(
            btn_frame,
            text="Criar Conta",
            command=self._register,
            bg='#3498db',
            fg='white',
            font=('Arial', 11, 'bold'),
            width=12,
            height=2,
            cursor='hand2'
        ).pack(side='left')
        
        # Bind Enter key
        self.root.bind('<Return>', lambda e: self._login())
    
    def _login(self):
        """Processa login."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Atenção", "Preencha usuário e senha!")
            return
        
        success, message = self.user_model.authenticate(username, password)
        if success:
            self.authenticated = True
            self.root.destroy()
        else:
            messagebox.showerror("Erro de Login", message)
            self.password_entry.delete(0, 'end')
    
    def _register(self):
        """Processa cadastro."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Atenção", "Preencha usuário e senha!")
            return
        
        if len(password) < 4:
            messagebox.showwarning("Atenção", "A senha deve ter no mínimo 4 caracteres!")
            return
        
        success, message = self.user_model.create_user(username, password)
        if success:
            messagebox.showinfo("Sucesso", message)
            # Auto-login após cadastro
            self.user_model.authenticate(username, password)
            self.authenticated = True
            self.root.destroy()
        else:
            messagebox.showerror("Erro", message)
    
    def run(self):
        """Inicia o loop da janela de login."""
        self.root.mainloop()
        return self.authenticated