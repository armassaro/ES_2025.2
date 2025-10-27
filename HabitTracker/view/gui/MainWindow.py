import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from model.ReportFactory import ReportFactory

class GUIReportView:
    """View de relatórios para a GUI."""
    def render_reports(self, report_data):
        """Método chamado pelo ReportController (Observer)."""
        pass

class HabitCard(tk.Frame):
    """Card individual para cada hábito com visualização de histórico."""
    
    def __init__(self, parent, habit, on_edit, on_delete, on_mark_done, on_refresh):
        super().__init__(parent, bg='white', relief='solid', bd=1)
        
        self.habit = habit
        self.on_edit = on_edit
        self.on_delete = on_delete
        self.on_mark_done = on_mark_done
        self.on_refresh = on_refresh
        
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
        
        # NOVO: Histórico interativo da última semana
        self._create_interactive_week_history(container)
        
        # Linha inferior: Data de criação e botões
        bottom_frame = tk.Frame(container, bg='white')
        bottom_frame.pack(fill='x', pady=(10, 0))
        
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
    
    def _create_interactive_week_history(self, parent):
        """Cria visualização INTERATIVA do histórico da última semana."""
        history_frame = tk.Frame(parent, bg='white')
        history_frame.pack(fill='x', pady=10)
        
        tk.Label(
            history_frame,
            text="📊 Últimos 7 dias (clique para marcar/desmarcar):",
            font=('Arial', 9, 'bold'),
            bg='white',
            fg='#7f8c8d'
        ).pack(side='left', padx=(0, 10))
        
        # Container para os dias
        days_container = tk.Frame(history_frame, bg='white')
        days_container.pack(side='left', fill='x', expand=True)
        
        # Gerar últimos 7 dias
        today = datetime.now()
        history = self.habit.get('history', {})
        
        for i in range(6, -1, -1):
            date = (today - timedelta(days=i))
            date_str = date.strftime('%Y-%m-%d')
            day_name = date.strftime('%a')[:3]  # Seg, Ter, Qua...
            
            is_completed = history.get(date_str, False)
            
            # Frame para cada dia
            day_frame = tk.Frame(days_container, bg='white')
            day_frame.pack(side='left', padx=3)
            
            # Dia da semana
            tk.Label(
                day_frame,
                text=day_name,
                font=('Arial', 7),
                bg='white',
                fg='#7f8c8d'
            ).pack()
            
            # BOTÃO interativo (em vez de Label estático)
            self._create_day_button(day_frame, date_str, is_completed)
            
            # Dia do mês
            tk.Label(
                day_frame,
                text=date.strftime('%d'),
                font=('Arial', 7),
                bg='white',
                fg='#7f8c8d'
            ).pack()
    
    def _create_day_button(self, parent, date_str, is_completed):
        """Cria um botão clicável para marcar/desmarcar o dia."""
        # Cor baseada no status
        if is_completed:
            bg_color = '#27ae60'
            text = '✓'
            fg_color = 'white'
            hover_bg = '#229954'
        else:
            bg_color = '#ecf0f1'
            text = '○'
            fg_color = '#95a5a6'
            hover_bg = '#bdc3c7'
        
        # Criar botão
        btn = tk.Button(
            parent,
            text=text,
            font=('Arial', 12, 'bold'),
            bg=bg_color,
            fg=fg_color,
            width=2,
            height=1,
            bd=0,
            cursor='hand2',
            activebackground=hover_bg,
            activeforeground=fg_color,
            command=lambda: self._toggle_day(date_str, is_completed)
        )
        btn.pack()
        
        # Efeito hover
        def on_enter(e):
            btn['bg'] = hover_bg
        
        def on_leave(e):
            btn['bg'] = bg_color
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        # Tooltip
        self._create_tooltip(btn, f"{'✅ Concluído' if is_completed else '⏳ Não concluído'} em {date_str}")
    
    def _create_tooltip(self, widget, text):
        """Cria um tooltip (dica) ao passar o mouse."""
        tooltip = None
        
        def show_tooltip(event):
            nonlocal tooltip
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 25
            
            tooltip = tk.Toplevel(widget)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{x}+{y}")
            
            label = tk.Label(
                tooltip,
                text=text,
                background="#2c3e50",
                foreground="white",
                relief='solid',
                borderwidth=1,
                font=('Arial', 8),
                padx=5,
                pady=3
            )
            label.pack()
        
        def hide_tooltip(event):
            nonlocal tooltip
            if tooltip:
                tooltip.destroy()
                tooltip = None
        
        widget.bind('<Enter>', show_tooltip)
        widget.bind('<Leave>', hide_tooltip)
    
    def _toggle_day(self, date_str, current_status):
        """Marca ou desmarca o dia (toggle)."""
        if current_status:
            # Desmarcar
            if messagebox.askyesno(
                "Desmarcar",
                f"Desmarcar hábito '{self.habit['name']}' como concluído em {date_str}?"
            ):
                success, message = self._unmark_day(date_str)
                if success:
                    messagebox.showinfo("Sucesso", message)
                    self.on_refresh()
                else:
                    messagebox.showerror("Erro", message)
        else:
            # Marcar
            print(f"📅 Marcando hábito '{self.habit['name']}' como concluído em {date_str}")
            success, message = self.on_mark_done(self.habit['id'], date_str)
            
            print(f"   Resultado: {'✅' if success else '❌'} {message}")
            
            if success:
                messagebox.showinfo("Sucesso", message)
                self.on_refresh()
            else:
                messagebox.showwarning("Aviso", message)
    
    def _unmark_day(self, date_str):
        """Desmarca um dia como concluído."""
        # Atualizar o histórico localmente
        if 'history' in self.habit and date_str in self.habit['history']:
            self.habit['history'][date_str] = False
            
            # Salvar via controller (você precisará adicionar esse método)
            # Por enquanto, vamos atualizar diretamente
            return True, f"Hábito '{self.habit['name']}' desmarcado em {date_str}!"
        
        return False, "Data não encontrada no histórico."


class MainWindow:
    """Janela principal da aplicação GUI."""
    
    def __init__(self, habit_controller, user_model):
        self.habit_controller = habit_controller
        self.user_model = user_model
        
        self.root = tk.Tk()
        self.root.title("Habit Tracker - Sistema de Gerenciamento de Hábitos")
        self.root.geometry("1100x700")
        self.root.configure(bg='#ecf0f1')
        
        print(f"🪟 GUI: Usuário logado: {self.user_model.get_logged_in_username()}")
        
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
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        self._refresh_habits()
    
    def _refresh_habits(self):
        """Atualiza a lista de hábitos com cards."""
        print("🔄 Atualizando lista de hábitos...")
        
        for widget in self.cards_frame.winfo_children():
            widget.destroy()
        
        habits = self.habit_controller.handle_read_habits_request()
        print(f"📋 Hábitos recebidos: {len(habits)}")
        
        if not habits:
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
            for i, habit in enumerate(habits):
                print(f"   {i+1}. {habit.get('name', 'SEM NOME')} (ID: {habit.get('id', 'SEM ID')})")
                card = HabitCard(
                    self.cards_frame,
                    habit,
                    on_edit=self._edit_habit,
                    on_delete=self._delete_habit_card,
                    on_mark_done=self._mark_done_with_date,
                    on_refresh=self._refresh_habits
                )
                card.pack(fill='x', pady=8)
        
        print("✅ Atualização concluída!")
    
    def _mark_done_with_date(self, habit_id, date=None):
        """Marca hábito como concluído em uma data específica."""
        print(f"🔧 MainWindow: Chamando controller para marcar hábito {habit_id} em {date}")
        result = self.habit_controller.handle_mark_done_request(habit_id, date)
        print(f"🔧 MainWindow: Resultado = {result}")
        return result
    
    def _create_habit(self):
        """Cria novo hábito."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Criar Novo Hábito")
        dialog.geometry("450x400")
        dialog.configure(bg='white')
        dialog.resizable(False, False)
        
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(
            dialog,
            text="Criar Novo Hábito",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(pady=20)
        
        tk.Label(dialog, text="Nome do Hábito:", font=('Arial', 10), bg='white').pack(anchor='w', padx=30, pady=(10, 5))
        name_entry = tk.Entry(dialog, width=40, font=('Arial', 11))
        name_entry.pack(padx=30, pady=5)
        
        tk.Label(dialog, text="Descrição (opcional):", font=('Arial', 10), bg='white').pack(anchor='w', padx=30, pady=(10, 5))
        desc_entry = tk.Text(dialog, width=40, height=4, font=('Arial', 10))
        desc_entry.pack(padx=30, pady=5)
        
        tk.Label(dialog, text="Frequência:", font=('Arial', 10), bg='white').pack(anchor='w', padx=30, pady=(10, 5))
        
        freq_frame = tk.Frame(dialog, bg='white')
        freq_frame.pack(padx=30, pady=5)
        
        freq_var = tk.StringVar(value='daily')
        
        tk.Radiobutton(freq_frame, text="📅 Diário", variable=freq_var, value='daily', font=('Arial', 10), bg='white').pack(side='left', padx=10)
        tk.Radiobutton(freq_frame, text="📊 Semanal", variable=freq_var, value='weekly', font=('Arial', 10), bg='white').pack(side='left', padx=10)
        tk.Radiobutton(freq_frame, text="📈 Mensal", variable=freq_var, value='monthly', font=('Arial', 10), bg='white').pack(side='left', padx=10)
        
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
        
        btn_frame = tk.Frame(dialog, bg='white')
        btn_frame.pack(pady=30)
        
        tk.Button(btn_frame, text="Criar Hábito", command=save, bg='#27ae60', fg='white', font=('Arial', 11, 'bold'), bd=0, padx=20, pady=10, cursor='hand2').pack(side='left', padx=10)
        tk.Button(btn_frame, text="Cancelar", command=dialog.destroy, bg='#95a5a6', fg='white', font=('Arial', 11, 'bold'), bd=0, padx=20, pady=10, cursor='hand2').pack(side='left', padx=10)
    
    def _edit_habit(self, habit):
        """Edita hábito."""
        print(f"✏️ Editando hábito: {habit.get('name')} (ID: {habit.get('id')})")
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Editar Hábito")
        dialog.geometry("450x500")
        dialog.configure(bg='white')
        dialog.resizable(False, False)
        
        # Centralizar
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(
            dialog,
            text="Editar Hábito",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(pady=20)
        
        # Nome
        tk.Label(dialog, text="Nome do Hábito:", font=('Arial', 10), bg='white').pack(anchor='w', padx=30, pady=(10, 5))
        name_entry = tk.Entry(dialog, width=40, font=('Arial', 11))
        name_entry.insert(0, habit.get('name', ''))
        name_entry.pack(padx=30, pady=5)
        
        # Descrição
        tk.Label(dialog, text="Descrição:", font=('Arial', 10), bg='white').pack(anchor='w', padx=30, pady=(10, 5))
        desc_entry = tk.Text(dialog, width=40, height=4, font=('Arial', 10))
        desc_entry.insert("1.0", habit.get('description', ''))
        desc_entry.pack(padx=30, pady=5)
        
        # Frequência
        tk.Label(dialog, text="Frequência:", font=('Arial', 10), bg='white').pack(anchor='w', padx=30, pady=(10, 5))
        
        freq_frame = tk.Frame(dialog, bg='white')
        freq_frame.pack(padx=30, pady=5)
        
        freq_var = tk.StringVar(value=habit.get('frequency', 'daily'))
        
        tk.Radiobutton(freq_frame, text="📅 Diário", variable=freq_var, value='daily', font=('Arial', 10), bg='white').pack(side='left', padx=10)
        tk.Radiobutton(freq_frame, text="📊 Semanal", variable=freq_var, value='weekly', font=('Arial', 10), bg='white').pack(side='left', padx=10)
        tk.Radiobutton(freq_frame, text="📈 Mensal", variable=freq_var, value='monthly', font=('Arial', 10), bg='white').pack(side='left', padx=10)
        
        # Status ativo
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
            
            print(f"💾 Salvando edição:")
            print(f"   - Habit ID: {habit['id']}")
            print(f"   - Nome: '{name}'")
            print(f"   - Descrição: '{desc}'")
            print(f"   - Ativo: {active}")
            print(f"   - Frequência: {freq}")
            
            if not name:
                messagebox.showwarning("Atenção", "O nome do hábito é obrigatório!")
                return
            
            success, message = self.habit_controller.handle_update_habit_request(
                habit['id'], 
                name=name, 
                description=desc, 
                active=active, 
                frequency=freq
            )
            
            print(f"   - Resultado: {'✅ Sucesso' if success else '❌ Falha'}")
            print(f"   - Mensagem: {message}")
            
            if success:
                messagebox.showinfo("Sucesso", message)
                self._refresh_habits()
                dialog.destroy()
            else:
                messagebox.showerror("Erro", message)
        
        # Botões
        btn_frame = tk.Frame(dialog, bg='white')
        btn_frame.pack(pady=20)
        
        tk.Button(
            btn_frame, 
            text="💾 Salvar Alterações", 
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
            text="❌ Cancelar", 
            command=dialog.destroy, 
            bg='#95a5a6', 
            fg='white', 
            font=('Arial', 11, 'bold'), 
            bd=0, 
            padx=20, 
            pady=10, 
            cursor='hand2'
        ).pack(side='left', padx=10)
    
    def _delete_habit_card(self, habit):
        """Deleta hábito do card."""
        if messagebox.askyesno("Confirmar", f"Deseja realmente deletar '{habit['name']}'?"):
            success, message = self.habit_controller.handle_delete_habit_request(habit['id'])
            if success:
                messagebox.showinfo("Sucesso", message)
                self._refresh_habits()
            else:
                messagebox.showerror("Erro", message)
    
    def _show_reports(self):
        """Exibe relatórios com gráficos."""
        # Gera os dados de relatório a partir dos hábitos atuais
        raw_data = self.habit_controller.handle_read_habits_request()

        if not raw_data:
            from tkinter import messagebox
            messagebox.showinfo("Relatórios", "Nenhum hábito cadastrado para gerar relatórios.")
            return

        # Criar objetos de relatório
        daily = ReportFactory.create_report('daily', raw_data).generate_visualization_data()
        weekly = ReportFactory.create_report('weekly', raw_data).generate_visualization_data()
        monthly = ReportFactory.create_report('monthly', raw_data).generate_visualization_data()

        # Janela modal para exibir relatórios
        modal = tk.Toplevel(self.root)
        modal.title("Relatórios de Progresso")
        modal.geometry("900x600")
        modal.transient(self.root)
        modal.grab_set()

        # Notebook com abas para daily/weekly/monthly
        notebook = ttk.Notebook(modal)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Helper para criar um quadro com texto resumido
        def _make_text_frame(parent, title, lines):
            f = tk.Frame(parent, bg='white')
            txt = tk.Text(f, wrap='word', bg='white', bd=0)
            txt.pack(fill='both', expand=True, padx=10, pady=10)
            txt.insert('end', title + '\n\n')
            for line in lines:
                txt.insert('end', line + '\n')
            txt.config(state='disabled')
            return f

        # Aba Diário
        daily_lines = [f"Data: {daily.get('date', 'N/A')}",
                       f"Hábitos totais (ativos): {daily.get('total_habits', 0)}",
                       f"Concluídos: {daily.get('completed', 0)}",
                       f"Pendentes: {daily.get('pending', 0)}",
                       f"Taxa de conclusão: {daily.get('completion_rate', 0)}%",
                       '', 'Detalhes:']
        for h in daily.get('habits_detail', []):
            daily_lines.append(f" - {h.get('name')}: {h.get('status')}")

        daily_frame = _make_text_frame(notebook, 'Relatório Diário', daily_lines)
        notebook.add(daily_frame, text='Diário')

        # Aba Semanal
        weekly_lines = [f"Período: {weekly.get('start_date', 'N/A')} a {weekly.get('end_date', 'N/A')}",
                        f"Total concluído: {weekly.get('total_completed', 0)}",
                        f"Média por dia: {weekly.get('average_per_day', 0)}",
                        f"Sequência atual: {weekly.get('current_streak', 0)} dias",
                        f"Taxa de conclusão: {weekly.get('completion_rate', 0)}%",
                        f"Melhor dia: {weekly.get('best_day', '')} ({weekly.get('best_day_count', 0)})",
                        '', 'Progresso diário:']
        for date, d in sorted(weekly.get('daily_data', {}).items()):
            weekly_lines.append(f" - {date}: {d.get('completed',0)}/{d.get('total',0)}")

        weekly_frame = _make_text_frame(notebook, 'Relatório Semanal', weekly_lines)
        notebook.add(weekly_frame, text='Semanal')

        # Aba Mensal
        monthly_lines = [f"Período: {monthly.get('start_date', 'N/A')} a {monthly.get('end_date', 'N/A')}",
                         f"Total concluído: {monthly.get('total_completed', 0)}",
                         f"Média por dia: {monthly.get('average_per_day', 0)}",
                         f"Maior sequência: {monthly.get('max_streak', 0)} dias",
                         f"Taxa de conclusão: {monthly.get('completion_rate', 0)}%",
                         f"Melhor semana começa: {monthly.get('best_week_start', 'N/A')} ({monthly.get('best_week_count', 0)})",
                         '', 'Resumo por semana:']
        for w in monthly.get('weekly_summary', []):
            monthly_lines.append(f" - {w.get('week')}: {w.get('completed',0)} hábitos ({w.get('dates',[])[0]} a {w.get('dates',[-1])})")

        monthly_frame = _make_text_frame(notebook, 'Relatório Mensal', monthly_lines)
        notebook.add(monthly_frame, text='Mensal')

        # Tentativa de desenhar gráficos simples se matplotlib estiver disponível
        try:
            from matplotlib.figure import Figure
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

            # Gráfico semanal (percentual concluído por dia)
            fig_w = Figure(figsize=(5, 2.5), dpi=100)
            ax_w = fig_w.add_subplot(111)
            dates = []
            percents = []
            for date, d in sorted(weekly.get('daily_data', {}).items()):
                dates.append(date[-5:])  # mostrar MM-DD para condensar
                total = d.get('total', 0)
                completed = d.get('completed', 0)
                percent = (completed / total * 100) if total > 0 else 0
                percents.append(percent)
            ax_w.bar(dates, percents, color='#3498db')
            ax_w.set_title('Percentual concluído por dia (semana)')
            ax_w.set_ylabel('%')
            ax_w.set_ylim(0, 100)

            canvas_w = FigureCanvasTkAgg(fig_w, master=weekly_frame)
            canvas_w.draw()
            canvas_w.get_tk_widget().pack(side='bottom', fill='both', expand=False, padx=10, pady=5)

            # Gráfico mensal: completados por semana
            fig_m = Figure(figsize=(5, 2.5), dpi=100)
            ax_m = fig_m.add_subplot(111)
            weeks = [w.get('week') for w in monthly.get('weekly_summary', [])]
            comps = [w.get('completed', 0) for w in monthly.get('weekly_summary', [])]
            if weeks:
                ax_m.bar(weeks, comps, color='#27ae60')
                ax_m.set_title('Hábito(s) completados por semana (mês)')
                ax_m.set_ylabel('Concluídos')
                canvas_m = FigureCanvasTkAgg(fig_m, master=monthly_frame)
                canvas_m.draw()
                canvas_m.get_tk_widget().pack(side='bottom', fill='both', expand=False, padx=10, pady=5)

        except Exception:
            # matplotlib não disponível ou falha na plotagem — continuar com texto apenas
            pass

        # Botão fechar
        btn_close = tk.Button(modal, text='Fechar', command=modal.destroy, bg='#95a5a6', fg='white')
        btn_close.pack(pady=8)
    
    def _quit(self):
        """Fecha a aplicação."""
        if messagebox.askyesno("Sair", "Deseja realmente sair?"):
            self.root.quit()
    
    def run(self):
        """Inicia o loop principal da GUI."""
        self.root.mainloop()