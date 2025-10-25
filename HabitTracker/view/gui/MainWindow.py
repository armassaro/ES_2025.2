import tkinter as tk
from tkinter import ttk, messagebox
from model.ReportFactory import ReportFactory

class GUIReportView:
    """View de relatórios para a GUI."""
    def render_reports(self, report_data):
        """Método chamado pelo ReportController (Observer)."""
        pass

class HabitCard(tk.Frame):
    """Card individual para cada hábito."""
    
    def __init__(self, parent, habit, on_edit, on_delete, on_mark_done):
        super().__init__(parent, bg='white', relief='solid', bd=1)
        
        self.habit = habit
        self.on_edit = on_edit
        self.on_delete = on_delete
        self.on_mark_done = on_mark_done
        
        self._setup_card()
    
    def _setup_card(self):
        """Configura o layout do card."""
        # Container principal com padding
        container = tk.Frame(self, bg='white')
        container.pack(fill='both', expand=True, padx=15, pady=12)
        
        # Linha superior: Nome e status
        top_frame = tk.Frame(container, bg='white')
        top_frame.pack(fill='x', pady=(0, 8))
        
        # Nome do hábito
        name_label = tk.Label(
            top_frame,
            text=self.habit['name'],
            font=('Arial', 14, 'bold'),
            bg='white',
            fg='#2c3e50',
            anchor='w'
        )
        name_label.pack(side='left', fill='x', expand=True)
        
        # Badge de frequência
        frequency_colors = {
            'daily': '#3498db',
            'weekly': '#27ae60',
            'monthly': '#9b59b6'
        }
        frequency_labels = {
            'daily': '📅 Diário',
            'weekly': '📊 Semanal',
            'monthly': '📈 Mensal'
        }
        
        freq = self.habit.get('frequency', 'daily')
        freq_badge = tk.Label(
            top_frame,
            text=frequency_labels.get(freq, '📅 Diário'),
            font=('Arial', 9, 'bold'),
            bg=frequency_colors.get(freq, '#3498db'),
            fg='white',
            padx=8,
            pady=3
        )
        freq_badge.pack(side='right', padx=5)
        
        # Status badge
        status = "✅ Ativo" if self.habit.get('active', True) else "❌ Inativo"
        status_color = '#27ae60' if self.habit.get('active', True) else '#e74c3c'
        
        status_badge = tk.Label(
            top_frame,
            text=status,
            font=('Arial', 9, 'bold'),
            bg=status_color,
            fg='white',
            padx=8,
            pady=3
        )
        status_badge.pack(side='right')
        
        # Descrição
        if self.habit.get('description'):
            desc_label = tk.Label(
                container,
                text=self.habit['description'],
                font=('Arial', 10),
                bg='white',
                fg='#7f8c8d',
                anchor='w',
                wraplength=600,
                justify='left'
            )
            desc_label.pack(fill='x', pady=(0, 10))
        
        # Linha inferior: Data de criação e botões
        bottom_frame = tk.Frame(container, bg='white')
        bottom_frame.pack(fill='x')
        
        # Data de criação
        created_date = self.habit.get('created_at', '')[:10] if self.habit.get('created_at') else 'N/A'
        date_label = tk.Label(
            bottom_frame,
            text=f"📅 Criado em: {created_date}",
            font=('Arial', 9),
            bg='white',
            fg='#95a5a6'
        )
        date_label.pack(side='left')
        
        # Botões de ação
        btn_frame = tk.Frame(bottom_frame, bg='white')
        btn_frame.pack(side='right')
        
        tk.Button(
            btn_frame,
            text="✅ Concluir",
            command=lambda: self.on_mark_done(self.habit),
            bg='#27ae60',
            fg='white',
            font=('Arial', 9, 'bold'),
            bd=0,
            padx=12,
            pady=6,
            cursor='hand2'
        ).pack(side='left', padx=2)
        
        tk.Button(
            btn_frame,
            text="✏️ Editar",
            command=lambda: self.on_edit(self.habit),
            bg='#3498db',
            fg='white',
            font=('Arial', 9, 'bold'),
            bd=0,
            padx=12,
            pady=6,
            cursor='hand2'
        ).pack(side='left', padx=2)
        
        tk.Button(
            btn_frame,
            text="🗑️ Deletar",
            command=lambda: self.on_delete(self.habit),
            bg='#e74c3c',
            fg='white',
            font=('Arial', 9, 'bold'),
            bd=0,
            padx=12,
            pady=6,
            cursor='hand2'
        ).pack(side='left', padx=2)


class MainWindow:
    """Janela principal da aplicação GUI."""
    
    def __init__(self, habit_controller, user_model):
        self.habit_controller = habit_controller
        self.user_model = user_model
        
        self.root = tk.Tk()
        self.root.title("Habit Tracker - Sistema de Gerenciamento de Hábitos")
        self.root.geometry("1100x700")
        self.root.configure(bg='#ecf0f1')
        
        self._setup_ui()
        
    def _setup_ui(self):
        """Configura toda a interface."""
        # Header
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        username = self.user_model.get_logged_in_username()
        
        tk.Label(
            header_frame, 
            text="🎯 Habit Tracker",
            font=('Arial', 20, 'bold'),
            bg='#2c3e50',
            fg='white'
        ).pack(side='left', padx=30, pady=15)
        
        tk.Label(
            header_frame, 
            text=f"Olá, {username}!",
            font=('Arial', 12),
            bg='#2c3e50',
            fg='#ecf0f1'
        ).pack(side='right', padx=30)
        
        # Container principal
        main_container = tk.Frame(self.root, bg='#ecf0f1')
        main_container.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Barra de ações superior
        action_bar = tk.Frame(main_container, bg='#ecf0f1')
        action_bar.pack(fill='x', pady=(0, 20))
        
        tk.Button(
            action_bar,
            text="➕ Novo Hábito",
            command=self._create_habit,
            bg='#27ae60',
            fg='white',
            font=('Arial', 11, 'bold'),
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2'
        ).pack(side='left', padx=5)
        
        tk.Button(
            action_bar,
            text="📊 Ver Relatórios",
            command=self._show_reports,
            bg='#3498db',
            fg='white',
            font=('Arial', 11, 'bold'),
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2'
        ).pack(side='left', padx=5)
        
        tk.Button(
            action_bar,
            text="🔄 Atualizar",
            command=self._refresh_habits,
            bg='#95a5a6',
            fg='white',
            font=('Arial', 11, 'bold'),
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2'
        ).pack(side='left', padx=5)
        
        tk.Button(
            action_bar,
            text="🚪 Sair",
            command=self._quit,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 11, 'bold'),
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2'
        ).pack(side='right', padx=5)
        
        # Área de cards com scroll
        canvas = tk.Canvas(main_container, bg='#ecf0f1', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient='vertical', command=canvas.yview)
        self.cards_frame = tk.Frame(canvas, bg='#ecf0f1')
        
        self.cards_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )
        
        canvas.create_window((0, 0), window=self.cards_frame, anchor='nw', width=1040)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
        
        # Bind scroll do mouse
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        self._refresh_habits()
    
    def _refresh_habits(self):
        """Atualiza a lista de hábitos com cards."""
        # Limpar cards existentes
        for widget in self.cards_frame.winfo_children():
            widget.destroy()
        
        habits = self.habit_controller.handle_read_habits_request()
        
        if not habits:
            # Mensagem quando não há hábitos
            empty_label = tk.Label(
                self.cards_frame,
                text="📝 Você ainda não tem hábitos cadastrados.\nClique em 'Novo Hábito' para começar!",
                font=('Arial', 14),
                bg='#ecf0f1',
                fg='#7f8c8d',
                pady=50
            )
            empty_label.pack(fill='both', expand=True)
        else:
            # Criar cards para cada hábito
            for habit in habits:
                card = HabitCard(
                    self.cards_frame,
                    habit,
                    on_edit=self._edit_habit,
                    on_delete=self._delete_habit_card,
                    on_mark_done=self._mark_done_card
                )
                card.pack(fill='x', pady=8)
    
    def _create_habit(self):
        """Cria novo hábito."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Criar Novo Hábito")
        dialog.geometry("450x400")
        dialog.configure(bg='white')
        dialog.resizable(False, False)
        
        # Centralizar
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Título
        tk.Label(
            dialog,
            text="Criar Novo Hábito",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(pady=20)
        
        # Nome
        tk.Label(dialog, text="Nome do Hábito:", font=('Arial', 10), bg='white').pack(anchor='w', padx=30, pady=(10, 5))
        name_entry = tk.Entry(dialog, width=40, font=('Arial', 11))
        name_entry.pack(padx=30, pady=5)
        
        # Descrição
        tk.Label(dialog, text="Descrição (opcional):", font=('Arial', 10), bg='white').pack(anchor='w', padx=30, pady=(10, 5))
        desc_entry = tk.Text(dialog, width=40, height=4, font=('Arial', 10))
        desc_entry.pack(padx=30, pady=5)
        
        # Frequência
        tk.Label(dialog, text="Frequência:", font=('Arial', 10), bg='white').pack(anchor='w', padx=30, pady=(10, 5))
        
        freq_frame = tk.Frame(dialog, bg='white')
        freq_frame.pack(padx=30, pady=5)
        
        freq_var = tk.StringVar(value='daily')
        
        tk.Radiobutton(
            freq_frame,
            text="📅 Diário",
            variable=freq_var,
            value='daily',
            font=('Arial', 10),
            bg='white'
        ).pack(side='left', padx=10)
        
        tk.Radiobutton(
            freq_frame,
            text="📊 Semanal",
            variable=freq_var,
            value='weekly',
            font=('Arial', 10),
            bg='white'
        ).pack(side='left', padx=10)
        
        tk.Radiobutton(
            freq_frame,
            text="📈 Mensal",
            variable=freq_var,
            value='monthly',
            font=('Arial', 10),
            bg='white'
        ).pack(side='left', padx=10)
        
        def save():
            name = name_entry.get().strip()
            desc = desc_entry.get("1.0", "end-1c").strip()
            freq = freq_var.get()
            
            if not name:
                messagebox.showwarning("Atenção", "O nome do hábito é obrigatório!")
                return
            
            success, message = self.habit_controller.handle_create_habit_request(name, desc, freq)
            if success:
                messagebox.showinfo("Sucesso", message)
                self._refresh_habits()
                dialog.destroy()
            else:
                messagebox.showerror("Erro", message)
        
        # Botões
        btn_frame = tk.Frame(dialog, bg='white')
        btn_frame.pack(pady=30)
        
        tk.Button(
            btn_frame,
            text="Criar Hábito",
            command=save,
            bg='#27ae60',
            fg='white',
            font=('Arial', 11, 'bold'),
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2'
        ).pack(side='left', padx=10)
        
        tk.Button(
            btn_frame,
            text="Cancelar",
            command=dialog.destroy,
            bg='#95a5a6',
            fg='white',
            font=('Arial', 11, 'bold'),
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2'
        ).pack(side='left', padx=10)
    
    def _edit_habit(self, habit):
        """Edita hábito."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Editar Hábito")
        dialog.geometry("450x450")
        dialog.configure(bg='white')
        dialog.resizable(False, False)
        
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(
            dialog,
            text="Editar Hábito",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(pady=20)
        
        tk.Label(dialog, text="Nome do Hábito:", font=('Arial', 10), bg='white').pack(anchor='w', padx=30, pady=(10, 5))
        name_entry = tk.Entry(dialog, width=40, font=('Arial', 11))
        name_entry.insert(0, habit['name'])
        name_entry.pack(padx=30, pady=5)
        
        tk.Label(dialog, text="Descrição:", font=('Arial', 10), bg='white').pack(anchor='w', padx=30, pady=(10, 5))
        desc_entry = tk.Text(dialog, width=40, height=4, font=('Arial', 10))
        desc_entry.insert("1.0", habit.get('description', ''))
        desc_entry.pack(padx=30, pady=5)
        
        tk.Label(dialog, text="Frequência:", font=('Arial', 10), bg='white').pack(anchor='w', padx=30, pady=(10, 5))
        
        freq_frame = tk.Frame(dialog, bg='white')
        freq_frame.pack(padx=30, pady=5)
        
        freq_var = tk.StringVar(value=habit.get('frequency', 'daily'))
        
        tk.Radiobutton(freq_frame, text="📅 Diário", variable=freq_var, value='daily', font=('Arial', 10), bg='white').pack(side='left', padx=10)
        tk.Radiobutton(freq_frame, text="📊 Semanal", variable=freq_var, value='weekly', font=('Arial', 10), bg='white').pack(side='left', padx=10)
        tk.Radiobutton(freq_frame, text="📈 Mensal", variable=freq_var, value='monthly', font=('Arial', 10), bg='white').pack(side='left', padx=10)
        
        active_var = tk.BooleanVar(value=habit.get('active', True))
        tk.Checkbutton(
            dialog,
            text="✅ Hábito Ativo",
            variable=active_var,
            font=('Arial', 11, 'bold'),
            bg='white'
        ).pack(pady=15)
        
        def save():
            name = name_entry.get().strip()
            desc = desc_entry.get("1.0", "end-1c").strip()
            active = active_var.get()
            freq = freq_var.get()
            
            if not name:
                messagebox.showwarning("Atenção", "O nome do hábito é obrigatório!")
                return
            
            success, message = self.habit_controller.handle_update_habit_request(
                habit['id'], name, desc, active, freq
            )
            if success:
                messagebox.showinfo("Sucesso", message)
                self._refresh_habits()
                dialog.destroy()
            else:
                messagebox.showerror("Erro", message)
        
        btn_frame = tk.Frame(dialog, bg='white')
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Salvar", command=save, bg='#27ae60', fg='white', font=('Arial', 11, 'bold'), bd=0, padx=20, pady=10, cursor='hand2').pack(side='left', padx=10)
        tk.Button(btn_frame, text="Cancelar", command=dialog.destroy, bg='#95a5a6', fg='white', font=('Arial', 11, 'bold'), bd=0, padx=20, pady=10, cursor='hand2').pack(side='left', padx=10)
    
    def _delete_habit_card(self, habit):
        """Deleta hábito do card."""
        if messagebox.askyesno("Confirmar", f"Deseja realmente deletar '{habit['name']}'?"):
            success, message = self.habit_controller.handle_delete_habit_request(habit['id'])
            if success:
                messagebox.showinfo("Sucesso", message)
                self._refresh_habits()
            else:
                messagebox.showerror("Erro", message)
    
    def _mark_done_card(self, habit):
        """Marca hábito como concluído."""
        success, message = self.habit_controller.handle_mark_done_request(habit['id'])
        if success:
            messagebox.showinfo("Sucesso", f"✅ {message}")
        else:
            messagebox.showwarning("Aviso", message)
    
    def _show_reports(self):
        """Exibe relatórios (manter código existente)."""
        habits = self.habit_controller.handle_read_habits_request()
        
        if not habits:
            messagebox.showinfo("Relatórios", "Você ainda não possui hábitos cadastrados!")
            return
        
        # Criar janela de relatórios
        report_window = tk.Toplevel(self.root)
        report_window.title("📊 Relatórios de Progresso")
        report_window.geometry("900x700")
        report_window.configure(bg='#f0f0f1')
        
        notebook = ttk.Notebook(report_window)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        daily_report = ReportFactory.create_report("daily", habits)
        weekly_report = ReportFactory.create_report("weekly", habits)
        monthly_report = ReportFactory.create_report("monthly", habits)
        
        self._create_daily_tab(notebook, daily_report.generate_visualization_data())
        self._create_weekly_tab(notebook, weekly_report.generate_visualization_data())
        self._create_monthly_tab(notebook, monthly_report.generate_visualization_data())
    
    def _create_daily_tab(self, notebook, data):
        """Cria a aba de relatório diário."""
        # Frame principal com scroll
        canvas = tk.Canvas(notebook, bg='white')
        scrollbar = ttk.Scrollbar(notebook, orient='vertical', command=canvas.yview)
        frame = tk.Frame(canvas, bg='white')
        
        frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )
        
        canvas.create_window((0, 0), window=frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Cabeçalho
        header = tk.Frame(frame, bg='#3498db', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text=f"📅 Relatório de {data['date']}",
            font=('Arial', 18, 'bold'),
            bg='#3498db',
            fg='white'
        ).pack(pady=25)
        
        # Container de estatísticas
        stats_container = tk.Frame(frame, bg='white')
        stats_container.pack(fill='x', padx=30, pady=30)
        
        stats = [
            ("Total de Hábitos", data['total_habits'], '#3498db'),
            ("✅ Concluídos", data['completed'], '#27ae60'),
            ("⏳ Pendentes", data['pending'], '#e67e22'),
            ("Taxa", f"{data['completion_rate']}%", '#9b59b6')
        ]
        
        # Criar cards lado a lado
        for i, (label, value, color) in enumerate(stats):
            card = tk.Frame(stats_container, bg=color, relief='raised', bd=2)
            card.grid(row=0, column=i, padx=15, pady=10, sticky='nsew')
            
            # Configurar peso das colunas para distribuição igual
            stats_container.grid_columnconfigure(i, weight=1)
            
            tk.Label(
                card,
                text=str(value),
                font=('Arial', 32, 'bold'),
                bg=color,
                fg='white',
                pady=20
            ).pack()
            
            tk.Label(
                card,
                text=label,
                font=('Arial', 11),
                bg=color,
                fg='white',
                pady=10
            ).pack()
        
        # Detalhes dos hábitos
        tk.Label(
            frame,
            text="Detalhes dos Hábitos:",
            font=('Arial', 14, 'bold'),
            bg='white'
        ).pack(anchor='w', padx=30, pady=(30, 10))
        
        for habit in data['habits_detail']:
            habit_card = tk.Frame(frame, bg='#ecf0f1', relief='solid', bd=1)
            habit_card.pack(fill='x', padx=30, pady=5)
            
            tk.Label(
                habit_card,
                text=f"{habit['status']} {habit['name']}",
                font=('Arial', 12),
                bg='#ecf0f1',
                anchor='w',
                padx=20,
                pady=15
            ).pack(fill='x')
        
        # Adicionar ao notebook
        notebook.add(canvas, text="📅 Hoje")
        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
    
    def _create_weekly_tab(self, notebook, data):
        """Cria a aba de relatório semanal."""
        canvas = tk.Canvas(notebook, bg='white')
        scrollbar = ttk.Scrollbar(notebook, orient='vertical', command=canvas.yview)
        frame = tk.Frame(canvas, bg='white')
        
        frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0, 0), window=frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Cabeçalho
        header = tk.Frame(frame, bg='#2ecc71', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text=f"📊 Semana: {data['start_date']} - {data['end_date']}",
            font=('Arial', 18, 'bold'),
            bg='#2ecc71',
            fg='white'
        ).pack(pady=25)
        
        # Estatísticas
        stats_container = tk.Frame(frame, bg='white')
        stats_container.pack(fill='x', padx=30, pady=30)
        
        stats = [
            ("Total", data['total_completed'], '#27ae60'),
            ("Média/Dia", data['average_per_day'], '#3498db'),
            ("🔥 Sequência", f"{data['current_streak']}d", '#e74c3c'),
            ("Taxa", f"{data['completion_rate']}%", '#9b59b6')
        ]
        
        for i, (label, value, color) in enumerate(stats):
            card = tk.Frame(stats_container, bg=color, relief='raised', bd=2)
            card.grid(row=0, column=i, padx=15, pady=10, sticky='nsew')
            stats_container.grid_columnconfigure(i, weight=1)
            
            tk.Label(card, text=str(value), font=('Arial', 32, 'bold'), bg=color, fg='white', pady=20).pack()
            tk.Label(card, text=label, font=('Arial', 11), bg=color, fg='white', pady=10).pack()
        
        # Tabela de progresso
        tk.Label(frame, text="Progresso Diário:", font=('Arial', 14, 'bold'), bg='white').pack(anchor='w', padx=30, pady=(30, 10))
        
        table_frame = tk.Frame(frame, bg='white')
        table_frame.pack(fill='x', padx=30, pady=10)
        
        # Cabeçalho da tabela
        headers = ['Data', 'Concluídos', 'Total', 'Percentual']
        for i, header in enumerate(headers):
            tk.Label(table_frame, text=header, font=('Arial', 11, 'bold'), bg='#34495e', fg='white', padx=20, pady=10, relief='solid', bd=1).grid(row=0, column=i, sticky='ew')
        
        # Dados da tabela
        row = 1
        for date, day_data in sorted(data['daily_data'].items()):
            completed = day_data['completed']
            total = day_data['total']
            percent = (completed / total * 100) if total > 0 else 0
            
            tk.Label(table_frame, text=date, bg='#ecf0f1', padx=20, pady=8, relief='solid', bd=1).grid(row=row, column=0, sticky='ew')
            tk.Label(table_frame, text=completed, bg='#ecf0f1', padx=20, pady=8, relief='solid', bd=1).grid(row=row, column=1, sticky='ew')
            tk.Label(table_frame, text=total, bg='#ecf0f1', padx=20, pady=8, relief='solid', bd=1).grid(row=row, column=2, sticky='ew')
            tk.Label(table_frame, text=f"{percent:.1f}%", bg='#ecf0f1', padx=20, pady=8, relief='solid', bd=1).grid(row=row, column=3, sticky='ew')
            row += 1
        
        # Melhor dia
        best_frame = tk.Frame(frame, bg='#f39c12', relief='raised', bd=2)
        best_frame.pack(fill='x', padx=30, pady=20)
        tk.Label(best_frame, text=f"🏆 Melhor dia: {data['best_day']} ({data['best_day_count']} hábitos concluídos)", font=('Arial', 12, 'bold'), bg='#f39c12', fg='white', pady=15).pack()
        
        notebook.add(canvas, text="📊 Semana")
        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
    
    def _create_monthly_tab(self, notebook, data):
        """Cria a aba de relatório mensal."""
        canvas = tk.Canvas(notebook, bg='white')
        scrollbar = ttk.Scrollbar(notebook, orient='vertical', command=canvas.yview)
        frame = tk.Frame(canvas, bg='white')
        
        frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0, 0), window=frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Cabeçalho
        header = tk.Frame(frame, bg='#9b59b6', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text=f"📈 Mês: {data['start_date']} - {data['end_date']}",
            font=('Arial', 18, 'bold'),
            bg='#9b59b6',
            fg='white'
        ).pack(pady=25)
        
        # Estatísticas
        stats_container = tk.Frame(frame, bg='white')
        stats_container.pack(fill='x', padx=30, pady=30)
        
        stats = [
            ("Total", data['total_completed'], '#3498db'),
            ("Média/Dia", data['average_per_day'], '#27ae60'),
            ("🔥 Maior Sequência", f"{data['max_streak']}d", '#e74c3c'),
            ("Taxa", f"{data['completion_rate']}%", '#9b59b6')
        ]
        
        for i, (label, value, color) in enumerate(stats):
            card = tk.Frame(stats_container, bg=color, relief='raised', bd=2)
            card.grid(row=0, column=i, padx=15, pady=10, sticky='nsew')
            stats_container.grid_columnconfigure(i, weight=1)
            
            tk.Label(card, text=str(value), font=('Arial', 32, 'bold'), bg=color, fg='white', pady=20).pack()
            tk.Label(card, text=label, font=('Arial', 11), bg=color, fg='white', pady=10).pack()
        
        # Resumo semanal
        tk.Label(frame, text="Resumo por Semana:", font=('Arial', 14, 'bold'), bg='white').pack(anchor='w', padx=30, pady=(30, 10))
        
        for week in data['weekly_summary']:
            week_frame = tk.Frame(frame, bg='#3498db', relief='raised', bd=2)
            week_frame.pack(fill='x', padx=30, pady=5)
            
            period = f"{week['dates'][0]} a {week['dates'][-1]}"
            tk.Label(
                week_frame,
                text=f"{week['week']}: {week['completed']} hábitos ({period})",
                font=('Arial', 11),
                bg='#3498db',
                fg='white',
                anchor='w',
                padx=20,
                pady=12
            ).pack(fill='x')
        
        # Melhor semana
        best_frame = tk.Frame(frame, bg='#f39c12', relief='raised', bd=2)
        best_frame.pack(fill='x', padx=30, pady=20)
        tk.Label(best_frame, text=f"🏆 Melhor semana: {data['best_week_start']} ({data['best_week_count']} hábitos)", font=('Arial', 12, 'bold'), bg='#f39c12', fg='white', pady=15).pack()
        
        notebook.add(canvas, text="📈 Mês")
        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
    
    def _quit(self):
        """Fecha a aplicação."""
        if messagebox.askyesno("Sair", "Deseja realmente sair?"):
            self.root.quit()
    
    def run(self):
        """Inicia o loop principal da GUI."""
        self.root.mainloop()