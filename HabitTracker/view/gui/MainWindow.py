import tkinter as tk
from tkinter import ttk, messagebox

class GUIReportView:
    """View de relatórios para a GUI."""
    def render_reports(self, report_data):
        """Método chamado pelo ReportController (Observer)."""
        pass

class MainWindow:
    """Janela principal da aplicação GUI."""
    
    def __init__(self, habit_controller, user_model):
        self.habit_controller = habit_controller
        self.user_model = user_model
        
        self.root = tk.Tk()
        self.root.title("Habit Tracker - Sistema de Gerenciamento de Hábitos")
        self.root.geometry("900x600")
        self.root.configure(bg='#f0f0f0')
        
        self._setup_ui()
        
    def _setup_ui(self):
        """Configura toda a interface."""
        # Header
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        header_frame.pack(fill='x')
        
        username = self.user_model.get_logged_in_username()
        tk.Label(
            header_frame, 
            text=f"🎯 Habit Tracker - Bem-vindo, {username}!",
            font=('Arial', 16, 'bold'),
            bg='#2c3e50',
            fg='white'
        ).pack(pady=15)
        
        # Container principal
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Painel esquerdo - Botões de ação
        left_panel = tk.Frame(main_container, bg='#f0f0f0')
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        
        tk.Label(
            left_panel,
            text="Ações",
            font=('Arial', 12, 'bold'),
            bg='#f0f0f0'
        ).pack(pady=(0, 10))
        
        buttons = [
            ("➕ Criar Hábito", self._create_habit),
            ("✏️ Editar Hábito", self._update_habit),
            ("🗑️ Deletar Hábito", self._delete_habit),
            ("✅ Registrar Progresso", self._mark_done),
            ("🔄 Atualizar Lista", self._refresh_habits),
            ("📊 Ver Relatórios", self._show_reports),
            ("🚪 Sair", self._quit)
        ]
        
        for text, command in buttons:
            btn = tk.Button(
                left_panel,
                text=text,
                command=command,
                width=20,
                height=2,
                font=('Arial', 10),
                bg='#3498db',
                fg='white',
                cursor='hand2'
            )
            btn.pack(pady=5)
        
        # Painel direito - Lista de hábitos
        right_panel = tk.Frame(main_container, bg='white')
        right_panel.pack(side='right', fill='both', expand=True)
        
        tk.Label(
            right_panel,
            text="Meus Hábitos",
            font=('Arial', 14, 'bold'),
            bg='white'
        ).pack(pady=10)
        
        # Treeview para exibir hábitos
        tree_frame = tk.Frame(right_panel, bg='white')
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.tree = ttk.Treeview(
            tree_frame,
            columns=('ID', 'Nome', 'Descrição', 'Status', 'Criado em'),
            show='headings',
            yscrollcommand=scrollbar.set
        )
        
        scrollbar.config(command=self.tree.yview)
        
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nome', text='Nome')
        self.tree.heading('Descrição', text='Descrição')
        self.tree.heading('Status', text='Status')
        self.tree.heading('Criado em', text='Criado em')
        
        self.tree.column('ID', width=100)
        self.tree.column('Nome', width=150)
        self.tree.column('Descrição', width=250)
        self.tree.column('Status', width=80)
        self.tree.column('Criado em', width=120)
        
        self.tree.pack(fill='both', expand=True)
        
        self._refresh_habits()
    
    def _refresh_habits(self):
        """Atualiza a lista de hábitos (igual ao console)."""
        # Limpar itens existentes
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obter hábitos do controller
        habits = self.habit_controller.handle_read_habits_request()
        
        # Adicionar à treeview
        for habit in habits:
            status = "Ativo" if habit.get('active', True) else "Inativo"
            created = habit.get('created_at', '')[:10] if habit.get('created_at') else 'N/A'
            
            self.tree.insert('', 'end', values=(
                habit['id'][:8] + '...',
                habit['name'],
                habit.get('description', 'Sem descrição'),
                status,
                created
            ))
    
    def _create_habit(self):
        """Cria novo hábito (igual ao console: handle_create_habit_input)."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Criar Novo Hábito")
        dialog.geometry("400x250")
        dialog.resizable(False, False)
        
        tk.Label(dialog, text="Nome do Hábito:", font=('Arial', 10)).pack(pady=(20, 5))
        name_entry = tk.Entry(dialog, width=40, font=('Arial', 10))
        name_entry.pack(pady=5)
        
        tk.Label(dialog, text="Descrição (opcional):", font=('Arial', 10)).pack(pady=(10, 5))
        desc_entry = tk.Text(dialog, width=40, height=4, font=('Arial', 10))
        desc_entry.pack(pady=5)
        
        def save():
            name = name_entry.get().strip()
            desc = desc_entry.get("1.0", "end-1c").strip()
            
            if not name:
                messagebox.showwarning("Atenção", "O nome do hábito é obrigatório!")
                return
            
            success, message = self.habit_controller.handle_create_habit_request(name, desc)
            if success:
                messagebox.showinfo("Sucesso", message)
                self._refresh_habits()
                dialog.destroy()
            else:
                messagebox.showerror("Erro", message)
        
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Criar", command=save, bg='#27ae60', fg='white', width=10).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Cancelar", command=dialog.destroy, bg='#e74c3c', fg='white', width=10).pack(side='left', padx=5)
    
    def _update_habit(self):
        """Edita hábito selecionado (igual ao console: handle_update_habit_input)."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atenção", "Selecione um hábito para editar!")
            return
        
        # Obter dados do item selecionado
        item = self.tree.item(selected[0])
        habit_id_short = item['values'][0]
        
        # Encontrar hábito completo
        habits = self.habit_controller.handle_read_habits_request()
        habit = next((h for h in habits if h['id'].startswith(habit_id_short.replace('...', ''))), None)
        
        if not habit:
            messagebox.showerror("Erro", "Hábito não encontrado!")
            return
        
        # Criar diálogo de edição
        dialog = tk.Toplevel(self.root)
        dialog.title("Editar Hábito")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        
        tk.Label(dialog, text="Nome do Hábito:", font=('Arial', 10)).pack(pady=(20, 5))
        name_entry = tk.Entry(dialog, width=40, font=('Arial', 10))
        name_entry.insert(0, habit['name'])
        name_entry.pack(pady=5)
        
        tk.Label(dialog, text="Descrição:", font=('Arial', 10)).pack(pady=(10, 5))
        desc_entry = tk.Text(dialog, width=40, height=4, font=('Arial', 10))
        desc_entry.insert("1.0", habit.get('description', ''))
        desc_entry.pack(pady=5)
        
        active_var = tk.BooleanVar(value=habit.get('active', True))
        tk.Checkbutton(dialog, text="Hábito Ativo", variable=active_var, font=('Arial', 10)).pack(pady=10)
        
        def save():
            name = name_entry.get().strip()
            desc = desc_entry.get("1.0", "end-1c").strip()
            active = active_var.get()
            
            if not name:
                messagebox.showwarning("Atenção", "O nome do hábito é obrigatório!")
                return
            
            success, message = self.habit_controller.handle_update_habit_request(
                habit['id'], name, desc, active
            )
            if success:
                messagebox.showinfo("Sucesso", message)
                self._refresh_habits()
                dialog.destroy()
            else:
                messagebox.showerror("Erro", message)
        
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Salvar", command=save, bg='#27ae60', fg='white', width=10).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Cancelar", command=dialog.destroy, bg='#e74c3c', fg='white', width=10).pack(side='left', padx=5)
    
    def _delete_habit(self):
        """Deleta hábito selecionado (igual ao console: handle_delete_habit_input)."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atenção", "Selecione um hábito para deletar!")
            return
        
        item = self.tree.item(selected[0])
        habit_name = item['values'][1]
        
        if not messagebox.askyesno("Confirmar", f"Deseja realmente deletar '{habit_name}'?"):
            return
        
        habit_id_short = item['values'][0]
        habits = self.habit_controller.handle_read_habits_request()
        habit = next((h for h in habits if h['id'].startswith(habit_id_short.replace('...', ''))), None)
        
        if habit:
            success, message = self.habit_controller.handle_delete_habit_request(habit['id'])
            if success:
                messagebox.showinfo("Sucesso", message)
                self._refresh_habits()
            else:
                messagebox.showerror("Erro", message)
    
    def _mark_done(self):
        """Registra progresso (igual ao console: handle_mark_done_input)."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atenção", "Selecione um hábito para registrar progresso!")
            return
        
        item = self.tree.item(selected[0])
        habit_id_short = item['values'][0]
        habit_name = item['values'][1]
        
        habits = self.habit_controller.handle_read_habits_request()
        habit = next((h for h in habits if h['id'].startswith(habit_id_short.replace('...', ''))), None)
        
        if habit:
            success, message = self.habit_controller.handle_mark_done_request(habit['id'])
            if success:
                messagebox.showinfo("Sucesso", f"✅ {message}")
            else:
                messagebox.showwarning("Aviso", message)
    
    def _show_reports(self):
        """Exibe relatórios (igual ao console mas em janela)."""
        # Força a notificação do observer para gerar relatórios
        self.habit_controller.model.notify()
        
        # Cria janela de relatórios
        report_window = tk.Toplevel(self.root)
        report_window.title("Relatórios de Progresso")
        report_window.geometry("600x400")
        
        tk.Label(
            report_window,
            text="📊 Relatórios de Progresso",
            font=('Arial', 16, 'bold')
        ).pack(pady=20)
        
        text_frame = tk.Frame(report_window)
        text_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side='right', fill='y')
        
        text_area = tk.Text(text_frame, font=('Courier', 10), yscrollcommand=scrollbar.set)
        text_area.pack(fill='both', expand=True)
        scrollbar.config(command=text_area.yview)
        
        # Gera relatório
        habits = self.habit_controller.handle_read_habits_request()
        
        report = "=" * 60 + "\n"
        report += "RELATÓRIO DE HÁBITOS\n"
        report += "=" * 60 + "\n\n"
        report += f"Total de hábitos: {len(habits)}\n"
        report += f"Hábitos ativos: {sum(1 for h in habits if h.get('active', True))}\n"
        report += f"Hábitos inativos: {sum(1 for h in habits if not h.get('active', True))}\n\n"
        report += "=" * 60 + "\n"
        report += "LISTA DE HÁBITOS:\n"
        report += "=" * 60 + "\n\n"
        
        for i, habit in enumerate(habits, 1):
            status = "✓ Ativo" if habit.get('active', True) else "✗ Inativo"
            report += f"{i}. {habit['name']} ({status})\n"
            report += f"   Descrição: {habit.get('description', 'Sem descrição')}\n"
            report += f"   Criado em: {habit.get('created_at', 'N/A')[:10]}\n\n"
        
        text_area.insert("1.0", report)
        text_area.config(state='disabled')
    
    def _quit(self):
        """Fecha a aplicação."""
        if messagebox.askyesno("Sair", "Deseja realmente sair?"):
            self.root.quit()
    
    def run(self):
        """Inicia o loop principal da GUI."""
        self.root.mainloop()