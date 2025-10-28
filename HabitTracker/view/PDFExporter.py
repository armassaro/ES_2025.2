"""
PDFExporter - Classe Singleton para exportação de relatórios em PDF.
Implementa o padrão Singleton para garantir uma única instância do exportador.
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime, timedelta


class PDFExporter:
    """
    Singleton para exportação de relatórios em PDF.
    Garante que apenas uma instância do exportador exista.
    """
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        """Implementação do padrão Singleton."""
        if cls._instance is None:
            cls._instance = super(PDFExporter, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Inicializa o exportador apenas uma vez."""
        if not PDFExporter._initialized:
            self.styles = getSampleStyleSheet()
            self._create_custom_styles()
            PDFExporter._initialized = True
            print("✅ PDFExporter inicializado (Singleton)")
    
    @classmethod
    def get_instance(cls):
        """Método alternativo para obter a instância única."""
        return cls()
    
    def _create_custom_styles(self):
        """Cria estilos personalizados para o PDF."""
        # Título principal
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtítulo
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Texto normal
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=6,
            alignment=TA_LEFT
        ))
    
    def export_habit_report(self, habit, filename):
        """
        Exporta um relatório detalhado de um hábito específico.
        
        Args:
            habit (dict): Dados do hábito
            filename (str): Caminho do arquivo PDF a ser gerado
        """
        print(f"📄 Exportando relatório PDF para: {filename}")
        
        # Criar documento
        doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Container para os elementos do PDF
        story = []
        
        # Adicionar conteúdo
        self._add_header(story, habit)
        self._add_habit_info(story, habit)
        self._add_progress_summary(story, habit)
        self._add_history_table(story, habit)
        self._add_footer(story)
        
        # Gerar PDF
        doc.build(story)
        print(f"✅ PDF gerado com sucesso: {filename}")
    
    def _add_header(self, story, habit):
        """Adiciona cabeçalho do relatório."""
        title = Paragraph(
            f"📊 Relatório do Hábito",
            self.styles['CustomTitle']
        )
        story.append(title)
        story.append(Spacer(1, 0.2 * inch))
        
        habit_name = Paragraph(
            f"<b>{habit['name']}</b>",
            self.styles['CustomHeading']
        )
        story.append(habit_name)
        story.append(Spacer(1, 0.3 * inch))
    
    def _add_habit_info(self, story, habit):
        """Adiciona informações básicas do hábito."""
        info_data = [
            ['Informações Gerais', ''],
            ['Nome:', habit['name']],
            ['Descrição:', habit.get('description', 'Sem descrição')],
            ['Frequência:', self._format_frequency(habit.get('frequency', 'daily'))],
            ['Status:', '✅ Ativo' if habit.get('active', True) else '❌ Inativo'],
            ['Criado em:', habit.get('created_at', 'N/A')[:10]]
        ]
        
        table = Table(info_data, colWidths=[2.5*inch, 4*inch])
        table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('SPAN', (0, 0), (-1, 0)),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            
            # Body
            ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#ecf0f1')),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(table)
        story.append(Spacer(1, 0.3 * inch))
    
    def _add_progress_summary(self, story, habit):
        """Adiciona resumo de progresso."""
        history = habit.get('history', {})
        
        # Calcular estatísticas
        total_days = len(history)
        completed_days = sum(1 for v in history.values() if v)
        completion_rate = (completed_days / total_days * 100) if total_days > 0 else 0
        
        # Calcular sequência atual
        current_streak = self._calculate_current_streak(history)
        
        # Últimos 7 dias
        last_7_days = self._get_last_n_days_stats(history, 7)
        
        summary_data = [
            ['Resumo de Progresso', ''],
            ['Total de dias registrados:', str(total_days)],
            ['Dias concluídos:', str(completed_days)],
            ['Taxa de conclusão:', f"{completion_rate:.1f}%"],
            ['Sequência atual:', f"{current_streak} dias"],
            ['Últimos 7 dias:', f"{last_7_days['completed']}/{last_7_days['total']} concluídos"]
        ]
        
        table = Table(summary_data, colWidths=[2.5*inch, 4*inch])
        table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('SPAN', (0, 0), (-1, 0)),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            
            # Body
            ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#ecf0f1')),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(table)
        story.append(Spacer(1, 0.3 * inch))
    
    def _add_history_table(self, story, habit):
        """Adiciona tabela com histórico detalhado."""
        history = habit.get('history', {})
        
        if not history:
            no_data = Paragraph("Nenhum registro de progresso disponível.", self.styles['CustomBody'])
            story.append(no_data)
            return
        
        # Título da seção
        title = Paragraph("Histórico Detalhado (Últimos 30 dias)", self.styles['CustomHeading'])
        story.append(title)
        story.append(Spacer(1, 0.1 * inch))
        
        # Preparar dados da tabela
        table_data = [['Data', 'Dia da Semana', 'Status']]
        
        # Últimos 30 dias
        today = datetime.now()
        for i in range(29, -1, -1):
            date = today - timedelta(days=i)
            date_str = date.strftime('%Y-%m-%d')
            day_name = date.strftime('%A')
            
            # Traduzir dia da semana
            day_translation = {
                'Monday': 'Segunda-feira',
                'Tuesday': 'Terça-feira',
                'Wednesday': 'Quarta-feira',
                'Thursday': 'Quinta-feira',
                'Friday': 'Sexta-feira',
                'Saturday': 'Sábado',
                'Sunday': 'Domingo'
            }
            day_name_pt = day_translation.get(day_name, day_name)
            
            status = '✅ Concluído' if history.get(date_str, False) else '⏳ Pendente'
            
            table_data.append([date_str, day_name_pt, status])
        
        # Criar tabela
        table = Table(table_data, colWidths=[1.8*inch, 2.5*inch, 2.2*inch])
        
        # Aplicar estilo
        style_commands = [
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            
            # Body
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),
            ('ALIGN', (2, 1), (2, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]
        
        # Alternar cores das linhas
        for i in range(1, len(table_data)):
            if i % 2 == 0:
                style_commands.append(
                    ('BACKGROUND', (0, i), (-1, i), colors.HexColor('#f8f9fa'))
                )
            
            # Destacar dias concluídos
            if '✅' in table_data[i][2]:
                style_commands.append(
                    ('TEXTCOLOR', (2, i), (2, i), colors.HexColor('#27ae60'))
                )
                style_commands.append(
                    ('FONTNAME', (2, i), (2, i), 'Helvetica-Bold')
                )
        
        table.setStyle(TableStyle(style_commands))
        story.append(table)
    
    def _add_footer(self, story):
        """Adiciona rodapé ao relatório."""
        story.append(Spacer(1, 0.5 * inch))
        
        footer_text = f"Relatório gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        footer = Paragraph(footer_text, self.styles['CustomBody'])
        story.append(footer)
        
        footer_note = Paragraph(
            "<i>Este relatório foi gerado automaticamente pelo Habit Tracker.</i>",
            self.styles['CustomBody']
        )
        story.append(footer_note)
    
    def _format_frequency(self, frequency):
        """Formata a frequência para exibição."""
        freq_map = {
            'daily': '📅 Diário',
            'weekly': '📊 Semanal',
            'monthly': '📈 Mensal'
        }
        return freq_map.get(frequency, frequency)
    
    def _calculate_current_streak(self, history):
        """Calcula a sequência atual de dias consecutivos."""
        if not history:
            return 0
        
        streak = 0
        today = datetime.now()
        
        # Verificar dias consecutivos a partir de hoje
        for i in range(365):  # Máximo de 1 ano
            date_str = (today - timedelta(days=i)).strftime('%Y-%m-%d')
            if history.get(date_str, False):
                streak += 1
            else:
                break
        
        return streak
    
    def _get_last_n_days_stats(self, history, n):
        """Retorna estatísticas dos últimos N dias."""
        today = datetime.now()
        completed = 0
        total = 0
        
        for i in range(n):
            date_str = (today - timedelta(days=i)).strftime('%Y-%m-%d')
            if date_str in history:
                total += 1
                if history[date_str]:
                    completed += 1
        
        return {'completed': completed, 'total': total}
