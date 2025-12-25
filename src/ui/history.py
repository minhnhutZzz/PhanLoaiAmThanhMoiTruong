"""
History View - Display detection history in a table
"""
import flet as ft
from src.utils.state import app_state
from src.ai.model_handler import SOUND_ICONS


def HistoryView(page: ft.Page):
    """History view showing all past detections"""
    
    def refresh_history(e=None):
        """Refresh the history table"""
        populate_table()
        page.update()
        
        # Show notification
        page.snack_bar = ft.SnackBar(
            content=ft.Text("✅ History refreshed"),
            bgcolor="#10B981"
        )
        page.snack_bar.open = True
        page.update()
    
    def clear_history(e):
        """Clear all history"""
        # Confirmation dialog
        def confirm_clear(e):
            app_state.clear_history()
            populate_table()
            dialog.open = False
            page.update()
            
            page.snack_bar = ft.SnackBar(
                content=ft.Text("🗑️ History cleared"),
                bgcolor="#EF4444"
            )
            page.snack_bar.open = True
            page.update()
        
        def cancel_clear(e):
            dialog.open = False
            page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text("Clear History?"),
            content=ft.Text("This will delete all detection history. This action cannot be undone."),
            actions=[
                ft.TextButton("Cancel", on_click=cancel_clear),
                ft.TextButton("Clear", on_click=confirm_clear, style=ft.ButtonStyle(color="#EF4444")),
            ]
        )
        
        page.dialog = dialog
        dialog.open = True
        page.update()
    
    def populate_table():
        """Populate the data table with history entries"""
        history = app_state.get_history()
        
        if not history:
            data_table.rows = [
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("No history yet", color="#94A3B8")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                ])
            ]
            return
        
        rows = []
        for entry in history:
            icon = SOUND_ICONS.get(entry['label'], "🔊")
            
            # Format time
            time_str = entry['timestamp'].strftime("%H:%M:%S")
            
            # Confidence color
            conf = entry['confidence']
            if conf >= 80:
                conf_color = "#10B981"
            elif conf >= 60:
                conf_color = "#F59E0B"
            else:
                conf_color = "#EF4444"
            
            # Source badge
            source_color = "#00D9FF" if entry['source'] == "live" else "#8B5CF6"
            
            row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(time_str, size=12)),
                    ft.DataCell(
                        ft.Row([
                            ft.Text(icon, size=16),
                            ft.Text(entry['label'].replace('_', ' ').title(), size=12)
                        ], spacing=5)
                    ),
                    ft.DataCell(
                        ft.Text(
                            f"{conf:.1f}%",
                            size=12,
                            color=conf_color,
                            weight=ft.FontWeight.BOLD
                        )
                    ),
                    ft.DataCell(
                        ft.Container(
                            content=ft.Text(
                                entry['source'].upper(),
                                size=10,
                                color="white"
                            ),
                            padding=5,
                            bgcolor=source_color,
                            border_radius=5
                        )
                    ),
                ]
            )
            rows.append(row)
        
        data_table.rows = rows
    
    # Header with refresh button
    header = ft.Row([
        ft.Text(
            "📜 Detection History",
            size=28,
            weight=ft.FontWeight.BOLD,
            color="#00D9FF"
        ),
        ft.IconButton(
            icon=ft.Icons.REFRESH,
            tooltip="Refresh",
            on_click=refresh_history,
            icon_color="#00D9FF"
        ),
        ft.IconButton(
            icon=ft.Icons.DELETE_SWEEP,
            tooltip="Clear History",
            on_click=clear_history,
            icon_color="#EF4444"
        ),
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    
    # Data table
    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Time", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Sound", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Confidence", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Source", weight=ft.FontWeight.BOLD)),
        ],
        rows=[],
        border=ft.border.all(1, "#334155"),
        border_radius=10,
        heading_row_color="#1E293B",
        data_row_color={"hovered": "#1E293B"},
    )
    
    # Populate table
    populate_table()
    
    # Stats summary
    stats = app_state.get_stats()
    stats_text = ft.Text(
        f"Total: {stats['total_detections']} detections | "
        f"Most Common: {stats['most_common'] or 'N/A'} | "
        f"Avg Confidence: {stats['avg_confidence']:.1f}%",
        size=14,
        color="#94A3B8"
    )
    
    # Layout
    return ft.Container(
        content=ft.Column([
            header,
            ft.Divider(color="#334155"),
            stats_text,
            ft.Container(height=10),
            ft.Container(
                content=ft.Column([
                    data_table
                ], scroll=ft.ScrollMode.AUTO),
                padding=20,
                border=ft.border.all(1, "#334155"),
                border_radius=10,
                bgcolor="#1E293B",
                expand=True
            ),
        ], spacing=10),
        padding=20,
        expand=True
    )
