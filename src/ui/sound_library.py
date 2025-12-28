"""
Sound Reference Library
Display categorized ESC-50 sound dataset
"""
import flet as ft


# Sound database with Vietnamese translations and icons
SOUND_DATABASE = {
    "Animals": [
        {"name": "dog", "vi": "Chó sủa", "icon": ft.Icons.PETS, "color": "#10B981"},
        {"name": "rooster", "vi": "Gà trống gáy", "icon": ft.Icons.CRUELTY_FREE, "color": "#F59E0B"},
        {"name": "pig", "vi": "Lợn kêu", "icon": ft.Icons.PETS, "color": "#EC4899"},
        {"name": "cow", "vi": "Bò kêu", "icon": ft.Icons.PETS, "color": "#8B5CF6"},
        {"name": "frog", "vi": "Ếch kêu", "icon": ft.Icons.PEST_CONTROL, "color": "#10B981"},
        {"name": "cat", "vi": "Mèo kêu", "icon": ft.Icons.PETS, "color": "#F59E0B"},
        {"name": "hen", "vi": "Gà mái", "icon": ft.Icons.CRUELTY_FREE, "color": "#EC4899"},
        {"name": "insects", "vi": "Côn trùng", "icon": ft.Icons.BUG_REPORT, "color": "#8B5CF6"},
        {"name": "sheep", "vi": "Cừu kêu", "icon": ft.Icons.PETS, "color": "#10B981"},
        {"name": "crow", "vi": "Quạ kêu", "icon": ft.Icons.CRUELTY_FREE, "color": "#64748B"},
    ],
    "Natural/Water": [
        {"name": "rain", "vi": "Tiếng mưa", "icon": ft.Icons.WATER_DROP, "color": "#0EA5E9"},
        {"name": "sea_waves", "vi": "Sóng biển", "icon": ft.Icons.WAVES, "color": "#06B6D4"},
        {"name": "crackling_fire", "vi": "Lửa cháy", "icon": ft.Icons.LOCAL_FIRE_DEPARTMENT, "color": "#EF4444"},
        {"name": "crickets", "vi": "Dế kêu", "icon": ft.Icons.BUG_REPORT, "color": "#10B981"},
        {"name": "chirping_birds", "vi": "Chim hót", "icon": ft.Icons.FLUTTER_DASH, "color": "#F59E0B"},
        {"name": "water_drops", "vi": "Giọt nước", "icon": ft.Icons.WATER_DROP, "color": "#0EA5E9"},
        {"name": "wind", "vi": "Tiếng gió", "icon": ft.Icons.AIR, "color": "#64748B"},
        {"name": "thunderstorm", "vi": "Bão tố", "icon": ft.Icons.THUNDERSTORM, "color": "#8B5CF6"},
        {"name": "pouring_water", "vi": "Nước đổ", "icon": ft.Icons.WATER, "color": "#06B6D4"},
        {"name": "toilet_flush", "vi": "Xả toilet", "icon": ft.Icons.BATHROOM, "color": "#0EA5E9"},
    ],
    "Human": [
        {"name": "crying_baby", "vi": "Trẻ em khóc", "icon": ft.Icons.CHILD_CARE, "color": "#EC4899"},
        {"name": "sneezing", "vi": "Hắt hơi", "icon": ft.Icons.SICK, "color": "#F59E0B"},
        {"name": "clapping", "vi": "Vỗ tay", "icon": ft.Icons.SPORTS_KABADDI, "color": "#10B981"},
        {"name": "breathing", "vi": "Hơi thở", "icon": ft.Icons.AIR, "color": "#0EA5E9"},
        {"name": "coughing", "vi": "Ho", "icon": ft.Icons.SICK, "color": "#EF4444"},
        {"name": "footsteps", "vi": "Bước chân", "icon": ft.Icons.DIRECTIONS_WALK, "color": "#8B5CF6"},
        {"name": "laughing", "vi": "Cười", "icon": ft.Icons.EMOJI_EMOTIONS, "color": "#F59E0B"},
        {"name": "brushing_teeth", "vi": "Đánh răng", "icon": ft.Icons.CLEAN_HANDS, "color": "#06B6D4"},
        {"name": "snoring", "vi": "Ngáy", "icon": ft.Icons.HOTEL, "color": "#64748B"},
        {"name": "drinking_sipping", "vi": "Uống nước", "icon": ft.Icons.LOCAL_CAFE, "color": "#8B5CF6"},
    ],
    "Domestic": [
        {"name": "door_wood_knock", "vi": "Gõ cửa", "icon": ft.Icons.DOOR_SLIDING, "color": "#8B5CF6"},
        {"name": "mouse_click", "vi": "Click chuột", "icon": ft.Icons.MOUSE, "color": "#64748B"},
        {"name": "keyboard_typing", "vi": "Gõ phím", "icon": ft.Icons.KEYBOARD, "color": "#0EA5E9"},
        {"name": "door_wood_creaks", "vi": "Cửa kêu cót két", "icon": ft.Icons.DOOR_SLIDING, "color": "#F59E0B"},
        {"name": "can_opening", "vi": "Mở lon", "icon": ft.Icons.FASTFOOD, "color": "#10B981"},
        {"name": "washing_machine", "vi": "Máy giặt", "icon": ft.Icons.LOCAL_LAUNDRY_SERVICE, "color": "#06B6D4"},
        {"name": "vacuum_cleaner", "vi": "Máy hút bụi", "icon": ft.Icons.CLEANING_SERVICES, "color": "#8B5CF6"},
        {"name": "clock_alarm", "vi": "Chuông báo thức", "icon": ft.Icons.ALARM, "color": "#EF4444"},
        {"name": "glass_breaking", "vi": "Vỡ kính", "icon": ft.Icons.BROKEN_IMAGE, "color": "#F59E0B"},
        {"name": "clock_tick", "vi": "Đồng hồ tích tắc", "icon": ft.Icons.SCHEDULE, "color": "#64748B"},
    ],
    "Urban": [
        {"name": "helicopter", "vi": "Trực thăng", "icon": ft.Icons.FLIGHT, "color": "#0EA5E9"},
        {"name": "chainsaw", "vi": "Cưa máy", "icon": ft.Icons.CARPENTER, "color": "#F59E0B"},
        {"name": "siren", "vi": "Còi hú", "icon": ft.Icons.EMERGENCY, "color": "#EF4444"},
        {"name": "car_horn", "vi": "Còi xe", "icon": ft.Icons.DIRECTIONS_CAR, "color": "#F59E0B"},
        {"name": "engine", "vi": "Động cơ", "icon": ft.Icons.SETTINGS, "color": "#64748B"},
        {"name": "train", "vi": "Tàu hỏa", "icon": ft.Icons.TRAIN, "color": "#8B5CF6"},
        {"name": "church_bells", "vi": "Chuông nhà thờ", "icon": ft.Icons.CHURCH, "color": "#10B981"},
        {"name": "airplane", "vi": "Máy bay", "icon": ft.Icons.FLIGHT_TAKEOFF, "color": "#0EA5E9"},
        {"name": "fireworks", "vi": "Pháo hoa", "icon": ft.Icons.CELEBRATION, "color": "#EC4899"},
        {"name": "hand_saw", "vi": "Cưa tay", "icon": ft.Icons.CARPENTER, "color": "#F59E0B"},
    ],
}


class SoundLibraryView:
    """Sound reference library with categorized ESC-50 sounds"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.search_query = ""
        self.search_field = None
        self.tabs = None
        
    def build(self):
        """Build the sound library view"""
        
        # Title
        title = ft.Container(
            content=ft.Column([
                ft.Text(
                    "📚 Thư Viện Âm Thanh ESC-50",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color="#00D9FF"
                ),
                ft.Text(
                    "50 loại âm thanh môi trường được phân nhóm khoa học",
                    size=14,
                    color="#94A3B8",
                    italic=True
                ),
            ], spacing=8),
            padding=20
        )
        
        # Search bar
        self.search_field = ft.TextField(
            hint_text="🔍 Tìm kiếm âm thanh (tiếng Anh hoặc tiếng Việt)...",
            on_change=self.on_search_change,
            border_color="#334155",
            focused_border_color="#00D9FF",
            text_size=14,
            height=50,
        )
        
        search_container = ft.Container(
            content=self.search_field,
            padding=ft.padding.only(left=20, right=20, bottom=10)
        )
        
        # Tabs for categories
        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                self._create_category_tab("Animals", "🐾"),
                self._create_category_tab("Natural/Water", "🌊"),
                self._create_category_tab("Human", "👤"),
                self._create_category_tab("Domestic", "🏠"),
                self._create_category_tab("Urban", "🏙️"),
            ],
            expand=True,
        )
        
        # Main layout
        return ft.Container(
            content=ft.Column([
                title,
                ft.Divider(color="#334155"),
                search_container,
                self.tabs,
            ], spacing=0, expand=True),
            padding=0,
            expand=True
        )
    
    def _create_category_tab(self, category: str, emoji: str):
        """Create a tab for a sound category"""
        sounds = SOUND_DATABASE.get(category, [])
        
        # Create sound cards
        sound_cards = [
            self._create_sound_card(sound)
            for sound in sounds
        ]
        
        # Grid layout with responsive columns
        grid = ft.GridView(
            runs_count=5,
            max_extent=200,
            child_aspect_ratio=1.0,
            spacing=15,
            run_spacing=15,
            padding=20,
        )
        
        for card in sound_cards:
            grid.controls.append(card)
        
        return ft.Tab(
            text=f"{emoji} {category}",
            content=ft.Container(
                content=grid,
                expand=True
            )
        )
    
    def _create_sound_card(self, sound: dict):
        """Create a card for a single sound"""
        return ft.Container(
            content=ft.Column([
                # Icon
                ft.Container(
                    content=ft.Icon(
                        sound["icon"],
                        size=40,
                        color=sound["color"]
                    ),
                    alignment=ft.alignment.center,
                ),
                ft.Container(height=5),
                # English name
                ft.Text(
                    sound["name"].replace("_", " ").title(),
                    size=13,
                    weight=ft.FontWeight.BOLD,
                    color="#F1F5F9",
                    text_align=ft.TextAlign.CENTER,
                ),
                # Vietnamese name
                ft.Text(
                    sound["vi"],
                    size=11,
                    color="#94A3B8",
                    text_align=ft.TextAlign.CENTER,
                    italic=True
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=3),
            padding=15,
            border=ft.border.all(1, sound["color"]),
            border_radius=10,
            bgcolor="#1E293B",
            ink=True,
            on_hover=self._on_card_hover,
            data=sound,  # Store sound data
        )
    
    def _on_card_hover(self, e):
        """Handle card hover effect"""
        if e.data == "true":
            e.control.bgcolor = "#334155"
            e.control.scale = 1.05
        else:
            e.control.bgcolor = "#1E293B"
            e.control.scale = 1.0
        e.control.update()
    
    def on_search_change(self, e):
        """Handle search query change"""
        self.search_query = e.control.value.lower()
        self._filter_sounds()
    
    def _filter_sounds(self):
        """Filter sounds based on search query"""
        if not self.search_query:
            # Show all sounds - rebuild tabs
            self._rebuild_all_tabs()
            return
        
        # Filter sounds across all categories
        filtered_results = []
        for category, sounds in SOUND_DATABASE.items():
            for sound in sounds:
                # Search in both English and Vietnamese names
                if (self.search_query in sound["name"].lower() or 
                    self.search_query in sound["vi"].lower()):
                    filtered_results.append(sound)
        
        # Show filtered results in all tabs
        if filtered_results:
            self._show_search_results(filtered_results)
        else:
            self._show_no_results()
    
    def _rebuild_all_tabs(self):
        """Rebuild all tabs with original data"""
        self.tabs.tabs = [
            self._create_category_tab("Animals", "🐾"),
            self._create_category_tab("Natural/Water", "🌊"),
            self._create_category_tab("Human", "👤"),
            self._create_category_tab("Domestic", "🏠"),
            self._create_category_tab("Urban", "🏙️"),
        ]
        self.page.update()
    
    def _show_search_results(self, results):
        """Show search results in current tab"""
        # Create grid with search results
        grid = ft.GridView(
            runs_count=5,
            max_extent=200,
            child_aspect_ratio=1.0,
            spacing=15,
            run_spacing=15,
            padding=20,
        )
        
        for sound in results:
            grid.controls.append(self._create_sound_card(sound))
        
        # Update current tab content
        current_tab = self.tabs.tabs[self.tabs.selected_index]
        current_tab.content = ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Text(
                        f"🔍 Tìm thấy {len(results)} kết quả",
                        size=14,
                        color="#00D9FF"
                    ),
                    padding=ft.padding.only(left=20, top=10)
                ),
                ft.Container(content=grid, expand=True)
            ]),
            expand=True
        )
        self.page.update()
    
    def _show_no_results(self):
        """Show no results message"""
        current_tab = self.tabs.tabs[self.tabs.selected_index]
        current_tab.content = ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.SEARCH_OFF, size=80, color="#64748B"),
                ft.Text(
                    "Không tìm thấy kết quả",
                    size=18,
                    color="#94A3B8"
                ),
                ft.Text(
                    f'Không có âm thanh nào khớp với "{self.search_query}"',
                    size=14,
                    color="#64748B"
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
            alignment=ft.alignment.center,
            expand=True
        )
        self.page.update()
