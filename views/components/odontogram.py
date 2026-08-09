from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QCheckBox, QLineEdit, QScrollArea, QGridLayout,
    QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QRectF, QPointF
from PySide6.QtGui import QFont, QPainter, QColor, QPen, QBrush, QPolygonF

Primary = "#C9929B"
PrimaryBorder = "#E8D5D8"
Second = "#D4758C"
Txt1 = "#2D2D2D"
Txt2 = "#7A7A7A"
pale_pink = "#FDF2F4"
White = "#FFFFFF"
COLOR_NORMAL = "#FFFFFF"

TOOL_CARIES = "caries"
TOOL_RESINA = "resina"
TOOL_AUSENTE = "ausente"
TOOL_ENDODONCIA = "endodoncia"
TOOL_CORONA = "corona"

TOOL_COLORS = {
    TOOL_CARIES: ("#B56576", "#F9E4E8", "Caries"),
    TOOL_RESINA: ("#6E8898", "#E3EDF2", "Resina"),
    TOOL_AUSENTE: ("#9A8C98", "#EDE9EC", "Ausente"),
    TOOL_ENDODONCIA: ("#8E7BAD", "#EBE5F3", "Endodoncia"),
    TOOL_CORONA: ("#C49B6A", "#F3EBE0", "Corona"),
}

FACE_LABELS = {
    "V": "Vestibular",
    "O": "Oclusal",
    "L": "Lingual",
    "M": "Mesial",
    "D": "Distal",
}

PERMANENT_TEETH = {
    1: [18, 17, 16, 15, 14, 13, 12, 11],
    2: [21, 22, 23, 24, 25, 26, 27, 28],
    3: [31, 32, 33, 34, 35, 36, 37, 38],
    4: [48, 47, 46, 45, 44, 43, 42, 41],
}

TEMPORARY_TEETH = {
    5: [55, 54, 53, 52, 51],
    6: [61, 62, 63, 64, 65],
    7: [71, 72, 73, 74, 75],
    8: [85, 84, 83, 82, 81],
}

FACES = [
    ("O", "Oclusal"),
    ("V", "Vestibular"),
    ("L", "Lingual"),
    ("M", "Mesial"),
    ("D", "Distal"),
]

FACE_SYMBOLS = {
    "O": "O",
    "V": "V",
    "L": "L",
    "M": "M",
    "D": "D",
}


class ToothWidget(QWidget):
    face_clicked = Signal(int, str)

    def __init__(self, tooth_number, parent=None):
        super().__init__(parent)
        self.tooth_number = tooth_number
        self.face_states = {}
        self.selected_face = None
        self.setFixedSize(48, 56)
        self.setCursor(Qt.PointingHandCursor)
        self.setToolTip(f"Diente {tooth_number}")

    def set_face_state(self, face, tool_type):
        if tool_type is None:
            self.face_states.pop(face, None)
        else:
            self.face_states[face] = tool_type
        self.selected_face = face
        self.update()

    def set_face_states(self, states):
        self.face_states = dict(states) if states else {}
        self.update()

    def clear_states(self):
        self.face_states.clear()
        self.selected_face = None
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        margin = 2
        inner_w = w - 2 * margin
        inner_h = h - 2 * margin

        tooth_rect = QRectF(margin, margin, inner_w, inner_h)

        border_color = QColor(PrimaryBorder)
        if self.selected_face:
            border_color = QColor(Second)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(White)))
        painter.drawRoundedRect(tooth_rect, 4, 4)

        cx = w / 2
        cy = h / 2

        v_color = self._get_face_color("V")
        o_color = self._get_face_color("O")
        l_color = self._get_face_color("L")
        m_color = self._get_face_color("M")
        d_color = self._get_face_color("D")

        v_rect = QRectF(margin + 2, margin + 2, inner_w - 4, inner_h * 0.22)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(v_color))
        painter.drawRoundedRect(v_rect, 3, 3)

        l_rect = QRectF(margin + 2, margin + inner_h * 0.78, inner_w - 4, inner_h * 0.20)
        painter.setBrush(QBrush(l_color))
        painter.drawRoundedRect(l_rect, 3, 3)

        o_rect = QRectF(margin + inner_w * 0.25, margin + inner_h * 0.30,
                        inner_w * 0.50, inner_h * 0.40)
        painter.setBrush(QBrush(o_color))
        painter.drawEllipse(o_rect)

        m_rect = QRectF(margin + 2, margin + inner_h * 0.28, inner_w * 0.22, inner_h * 0.44)
        painter.setBrush(QBrush(m_color))
        painter.drawRoundedRect(m_rect, 2, 2)

        d_rect = QRectF(margin + inner_w * 0.78, margin + inner_h * 0.28,
                        inner_w * 0.20, inner_h * 0.44)
        painter.setBrush(QBrush(d_color))
        painter.drawRoundedRect(d_rect, 2, 2)

        border_pen = QPen(QColor(PrimaryBorder), 0.5)
        painter.setPen(border_pen)
        painter.setBrush(Qt.NoBrush)

        painter.drawLine(QPointF(cx, v_rect.bottom()), QPointF(cx, o_rect.top()))
        painter.drawLine(QPointF(cx, o_rect.bottom()), QPointF(cx, l_rect.top()))

        painter.setPen(QPen(QColor(Txt2), 0.3))
        painter.drawLine(QPointF(m_rect.right(), cy), QPointF(o_rect.left(), cy))
        painter.drawLine(QPointF(o_rect.right(), cy), QPointF(d_rect.left(), cy))

        num_pen = QPen(QColor(Txt1))
        painter.setPen(num_pen)
        painter.setFont(QFont("Segoe UI", 7, QFont.Weight.DemiBold))
        painter.drawText(QRectF(margin, margin + inner_h * 0.32, inner_w, inner_h * 0.36),
                         Qt.AlignCenter, str(self.tooth_number))

        painter.end()

    def _get_face_color(self, face):
        tool = self.face_states.get(face)
        if tool and tool in TOOL_COLORS:
            return QColor(TOOL_COLORS[tool][0])
        return QColor("#FAF0F2")

    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton:
            return

        x = event.position().x()
        y = event.position().y()
        w = self.width()
        h = self.height()

        margin = 2
        inner_h = h - 2 * margin
        cx = w / 2

        v_bottom = margin + inner_h * 0.24
        l_top = margin + inner_h * 0.76
        o_left = margin + w * 0.25
        o_right = margin + w * 0.75
        o_top = margin + inner_h * 0.30
        o_bottom = margin + inner_h * 0.70

        if y < v_bottom:
            face = "V"
        elif y > l_top:
            face = "L"
        elif o_left < x < o_right and o_top < y < o_bottom:
            face = "O"
        elif x < cx:
            face = "M"
        else:
            face = "D"

        self.face_clicked.emit(self.tooth_number, face)


class OdontogramWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.dentition_type = "adult"
        self.selected_tooth = None
        self.active_tool = TOOL_CARIES
        self.affections = {}
        self._tooth_widgets = {}
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(12)

        top_row = QHBoxLayout()
        top_row.setSpacing(12)

        toggle_frame = QFrame()
        toggle_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {White};
                border: none;
                border-radius: 10px;
            }}
        """)
        toggle_layout = QHBoxLayout(toggle_frame)
        toggle_layout.setContentsMargins(4, 4, 4, 4)
        toggle_layout.setSpacing(0)

        self.btn_adult = QPushButton("Adulto")
        self.btn_adult.setFixedHeight(32)
        self.btn_adult.setCursor(Qt.PointingHandCursor)
        self.btn_adult.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        self.btn_adult.clicked.connect(lambda: self._set_dentition("adult"))
        toggle_layout.addWidget(self.btn_adult)

        self.btn_child = QPushButton("Ni\u00f1o")
        self.btn_child.setFixedHeight(32)
        self.btn_child.setCursor(Qt.PointingHandCursor)
        self.btn_child.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        self.btn_child.clicked.connect(lambda: self._set_dentition("child"))
        toggle_layout.addWidget(self.btn_child)

        top_row.addWidget(toggle_frame)
        top_row.addStretch()

        root.addLayout(top_row)

        toolbar = self._build_toolbar()
        root.addWidget(toolbar)

        main_row = QHBoxLayout()
        main_row.setSpacing(12)

        map_container = QFrame()
        map_container.setStyleSheet(f"""
            QFrame {{
                background-color: {White};
                border: none;
                border-radius: 14px;
            }}
        """)
        map_layout = QVBoxLayout(map_container)
        map_layout.setContentsMargins(12, 12, 12, 12)
        map_layout.setSpacing(6)

        self.teeth_grid = QGridLayout()
        self.teeth_grid.setSpacing(3)
        self.teeth_grid.setAlignment(Qt.AlignCenter)
        map_layout.addLayout(self.teeth_grid)

        main_row.addWidget(map_container, 5)

        side_panel = QFrame()
        side_panel.setStyleSheet(f"""
            QFrame {{
                background-color: {White};
                border: none;
                border-radius: 14px;
            }}
        """)
        side_layout = QVBoxLayout(side_panel)
        side_layout.setContentsMargins(12, 12, 12, 12)
        side_layout.setSpacing(10)

        info_title = QLabel("Diente seleccionado")
        info_title.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        info_title.setStyleSheet(f"color: {Txt1}; background: transparent;")
        side_layout.addWidget(info_title)

        self.info_placeholder = QLabel("Haz clic en una cara\ndel diente para marcarla.")
        self.info_placeholder.setAlignment(Qt.AlignCenter)
        self.info_placeholder.setFont(QFont("Segoe UI", 9))
        self.info_placeholder.setStyleSheet(f"color: {Txt2}; background: transparent;")
        side_layout.addWidget(self.info_placeholder)

        self.info_panel = QWidget()
        self.info_panel.setVisible(False)
        ip_layout = QVBoxLayout(self.info_panel)
        ip_layout.setContentsMargins(0, 0, 0, 0)
        ip_layout.setSpacing(8)

        self.info_tooth_label = QLabel()
        self.info_tooth_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.info_tooth_label.setStyleSheet(f"color: {Second}; background: transparent;")
        ip_layout.addWidget(self.info_tooth_label)

        self.info_face_label = QLabel()
        self.info_face_label.setFont(QFont("Segoe UI", 10))
        self.info_face_label.setStyleSheet(f"color: {Txt1}; background: transparent;")
        ip_layout.addWidget(self.info_face_label)

        desc_row = QHBoxLayout()
        desc_row.setSpacing(6)
        self.desc_field = QLineEdit()
        self.desc_field.setPlaceholderText("Descripcion...")
        self.desc_field.setFont(QFont("Segoe UI", 9))
        self.desc_field.setStyleSheet(f"""
            QLineEdit {{
                background-color: {pale_pink};
                border: none;
                border-radius: 6px;
                padding: 6px 8px;
                color: {Txt1};
            }}
            QLineEdit:focus {{ background-color: {White}; }}
        """)
        desc_row.addWidget(self.desc_field, 1)

        apply_desc_btn = QPushButton("OK")
        apply_desc_btn.setFixedSize(32, 28)
        apply_desc_btn.setCursor(Qt.PointingHandCursor)
        apply_desc_btn.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        apply_desc_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Second};
                color: white;
                border: none;
                border-radius: 6px;
            }}
            QPushButton:hover {{ background-color: #C0607A; }}
        """)
        apply_desc_btn.clicked.connect(self._apply_description)
        desc_row.addWidget(apply_desc_btn)
        ip_layout.addLayout(desc_row)

        clear_sel_btn = QPushButton("Limpiar seleccion")
        clear_sel_btn.setFixedHeight(28)
        clear_sel_btn.setCursor(Qt.PointingHandCursor)
        clear_sel_btn.setFont(QFont("Segoe UI", 9))
        clear_sel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {pale_pink};
                color: {Txt2};
                border: none;
                border-radius: 6px;
            }}
            QPushButton:hover {{ background-color: {PrimaryBorder}; color: {Txt1}; }}
        """)
        clear_sel_btn.clicked.connect(self._clear_current_tooth)
        ip_layout.addWidget(clear_sel_btn)

        ip_layout.addStretch()
        side_layout.addWidget(self.info_panel)

        side_layout.addStretch()

        main_row.addWidget(side_panel, 2)

        root.addLayout(main_row)

        summary_container = QFrame()
        summary_container.setStyleSheet(f"""
            QFrame {{
                background-color: {White};
                border: none;
                border-radius: 14px;
            }}
        """)
        summary_layout = QVBoxLayout(summary_container)
        summary_layout.setContentsMargins(16, 12, 16, 12)
        summary_layout.setSpacing(6)

        summary_header = QHBoxLayout()
        summary_title = QLabel("Afecciones registradas")
        summary_title.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        summary_title.setStyleSheet(f"color: {Txt1}; background: transparent;")
        summary_header.addWidget(summary_title)
        summary_header.addStretch()

        self.summary_count = QLabel("0")
        self.summary_count.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        self.summary_count.setStyleSheet(f"""
            color: {Second};
            background-color: {pale_pink};
            border: none;
            border-radius: 10px;
            padding: 2px 10px;
        """)
        summary_header.addWidget(self.summary_count)
        summary_layout.addLayout(summary_header)

        self.summary_list = QVBoxLayout()
        self.summary_list.setSpacing(3)
        summary_layout.addLayout(self.summary_list)

        self.summary_empty = QLabel("Sin afecciones registradas")
        self.summary_empty.setAlignment(Qt.AlignCenter)
        self.summary_empty.setFont(QFont("Segoe UI", 9))
        self.summary_empty.setStyleSheet(f"color: {Txt2}; background: transparent; padding: 8px;")
        self.summary_list.addWidget(self.summary_empty)

        root.addWidget(summary_container)

        self._build_teeth_map()
        self._update_toggle_style()
        self._update_toolbar_style()

    def _build_toolbar(self):
        toolbar = QFrame()
        toolbar.setStyleSheet(f"""
            QFrame {{
                background-color: {White};
                border: none;
                border-radius: 10px;
            }}
        """)
        tb_layout = QHBoxLayout(toolbar)
        tb_layout.setContentsMargins(8, 4, 8, 4)
        tb_layout.setSpacing(4)

        tool_label = QLabel("Herramienta:")
        tool_label.setFont(QFont("Segoe UI", 9, QFont.Weight.DemiBold))
        tool_label.setStyleSheet(f"color: {Txt2}; background: transparent;")
        tb_layout.addWidget(tool_label)

        self.tool_buttons = {}
        for tool_key, (color, bg, label) in TOOL_COLORS.items():
            btn = QPushButton(label)
            btn.setFixedHeight(28)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFont(QFont("Segoe UI", 9))
            btn.clicked.connect(lambda _, t=tool_key: self._set_tool(t))
            self.tool_buttons[tool_key] = btn
            tb_layout.addWidget(btn)

        tb_layout.addStretch()

        legend = self._build_legend()
        tb_layout.addWidget(legend)

        self._update_toolbar_style()
        return toolbar

    def _build_legend(self):
        legend = QFrame()
        legend.setStyleSheet(f"background: transparent; border: none;")
        l_layout = QHBoxLayout(legend)
        l_layout.setContentsMargins(8, 2, 8, 2)
        l_layout.setSpacing(6)

        items = [
            (COLOR_NORMAL, PrimaryBorder, "Sano"),
            (TOOL_COLORS[TOOL_CARIES][0], TOOL_COLORS[TOOL_CARIES][0], "Caries"),
            (TOOL_COLORS[TOOL_RESINA][0], TOOL_COLORS[TOOL_RESINA][0], "Resina"),
            (TOOL_COLORS[TOOL_AUSENTE][0], TOOL_COLORS[TOOL_AUSENTE][0], "Ausente"),
            (TOOL_COLORS[TOOL_ENDODONCIA][0], TOOL_COLORS[TOOL_ENDODONCIA][0], "Endodoncia"),
            (TOOL_COLORS[TOOL_CORONA][0], TOOL_COLORS[TOOL_CORONA][0], "Corona"),
        ]
        for bg, border, text in items:
            row = QHBoxLayout()
            row.setSpacing(3)
            dot = QFrame()
            dot.setFixedSize(10, 10)
            dot.setStyleSheet(f"""
                QFrame {{
                    background-color: {bg};
                    border: 1.5px solid {border};
                    border-radius: 5px;
                }}
            """)
            row.addWidget(dot)
            lbl = QLabel(text)
            lbl.setFont(QFont("Segoe UI", 7))
            lbl.setStyleSheet(f"color: {Txt2}; background: transparent; border: none;")
            row.addWidget(lbl)
            l_layout.addLayout(row)

        return legend

    def _set_tool(self, tool_key):
        self.active_tool = tool_key
        self._update_toolbar_style()

    def _update_toolbar_style(self):
        for tool_key, btn in self.tool_buttons.items():
            color, bg, _ = TOOL_COLORS[tool_key]
            if tool_key == self.active_tool:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {color};
                        color: white;
                        border: none;
                        border-radius: 6px;
                        padding: 0 10px;
                    }}
                """)
            else:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {bg};
                        color: {Txt1};
                        border: none;
                        border-radius: 6px;
                        padding: 0 10px;
                    }}
                    QPushButton:hover {{ background-color: {color}; color: white; }}
                """)

    def _build_teeth_map(self):
        self._tooth_widgets.clear()

        while self.teeth_grid.count():
            item = self.teeth_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._empty_layout(item.layout())

        if self.dentition_type == "adult":
            upper = [
                (PERMANENT_TEETH[1], "right"),
                (PERMANENT_TEETH[2], "left"),
            ]
            lower = [
                (PERMANENT_TEETH[4], "right"),
                (PERMANENT_TEETH[3], "left"),
            ]
        else:
            upper = [
                (TEMPORARY_TEETH[5], "right"),
                (TEMPORARY_TEETH[6], "left"),
            ]
            lower = [
                (TEMPORARY_TEETH[8], "right"),
                (TEMPORARY_TEETH[7], "left"),
            ]

        self.teeth_grid.addWidget(self._build_jaw_label("Superior"), 0, 0, 1, 2, Qt.AlignCenter)

        upper_row = QHBoxLayout()
        upper_row.setSpacing(0)

        left_block = QHBoxLayout()
        left_block.setSpacing(2)
        for tooth_num in upper[0][0]:
            tw = ToothWidget(tooth_num)
            tw.face_clicked.connect(self._on_face_clicked)
            self._tooth_widgets[tooth_num] = tw
            left_block.addWidget(tw)

        separator = QFrame()
        separator.setFixedWidth(2)
        separator.setFixedHeight(48)
        separator.setStyleSheet(f"background-color: {PrimaryBorder}; border: none;")
        left_block.addWidget(separator)

        right_block = QHBoxLayout()
        right_block.setSpacing(2)
        for tooth_num in upper[1][0]:
            tw = ToothWidget(tooth_num)
            tw.face_clicked.connect(self._on_face_clicked)
            self._tooth_widgets[tooth_num] = tw
            right_block.addWidget(tw)

        upper_row.addLayout(left_block)
        upper_row.addStretch()
        upper_row.addLayout(right_block)
        self.teeth_grid.addLayout(upper_row, 1, 0, 1, 2)

        self.teeth_grid.addWidget(self._build_jaw_label("Inferior"), 2, 0, 1, 2, Qt.AlignCenter)

        lower_row = QHBoxLayout()
        lower_row.setSpacing(0)

        left_block_l = QHBoxLayout()
        left_block_l.setSpacing(2)
        for tooth_num in lower[0][0]:
            tw = ToothWidget(tooth_num)
            tw.face_clicked.connect(self._on_face_clicked)
            self._tooth_widgets[tooth_num] = tw
            left_block_l.addWidget(tw)

        separator2 = QFrame()
        separator2.setFixedWidth(2)
        separator2.setFixedHeight(48)
        separator2.setStyleSheet(f"background-color: {PrimaryBorder}; border: none;")
        left_block_l.addWidget(separator2)

        right_block_l = QHBoxLayout()
        right_block_l.setSpacing(2)
        for tooth_num in lower[1][0]:
            tw = ToothWidget(tooth_num)
            tw.face_clicked.connect(self._on_face_clicked)
            self._tooth_widgets[tooth_num] = tw
            right_block_l.addWidget(tw)

        lower_row.addLayout(left_block_l)
        lower_row.addStretch()
        lower_row.addLayout(right_block_l)
        self.teeth_grid.addLayout(lower_row, 3, 0, 1, 2)

        self._refresh_all_teeth()

    def _build_jaw_label(self, text):
        lbl = QLabel(text)
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setFont(QFont("Segoe UI", 9, QFont.Weight.DemiBold))
        lbl.setStyleSheet(f"color: {Txt2}; background: transparent; border: none; padding: 4px;")
        return lbl

    def _clear_layout(self, item):
        if item.widget():
            item.widget().deleteLater()
        elif item.layout():
            self._empty_layout(item.layout())

    def _empty_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self._empty_layout(child.layout())

    def _set_dentition(self, dtype):
        self.dentition_type = dtype
        self.selected_tooth = None
        self._build_teeth_map()
        self._update_toggle_style()
        self.info_placeholder.setVisible(True)
        self.info_panel.setVisible(False)

    def _update_toggle_style(self):
        active = f"""
            QPushButton {{
                background-color: {Second};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0 20px;
            }}
        """
        inactive = f"""
            QPushButton {{
                background-color: {White};
                color: {Txt2};
                border: none;
                border-radius: 8px;
                padding: 0 20px;
            }}
            QPushButton:hover {{ background-color: #F5F5F5; }}
        """
        if self.dentition_type == "adult":
            self.btn_adult.setStyleSheet(active)
            self.btn_child.setStyleSheet(inactive)
        else:
            self.btn_adult.setStyleSheet(inactive)
            self.btn_child.setStyleSheet(active)

    def _on_face_clicked(self, tooth_number, face):
        self.selected_tooth = tooth_number

        tw = self._tooth_widgets.get(tooth_number)
        if tw:
            tw.selected_face = face
            tw.update()

        aff = self.affections.get(tooth_number, {})
        faces = aff.get("faces", {})
        current_tool = faces.get(face, {})
        if isinstance(current_tool, dict):
            current_tool = current_tool.get("tool", None)
        else:
            current_tool = None

        if current_tool == self.active_tool:
            if face in faces:
                del faces[face]
            if not faces:
                self.affections.pop(tooth_number, None)
            else:
                self.affections[tooth_number] = {**aff, "faces": faces}
        else:
            desc = faces.get(face, {})
            if isinstance(desc, dict):
                desc = desc.get("description", "")
            else:
                desc = desc or ""
            faces[face] = {"tool": self.active_tool, "description": desc}
            self.affections[tooth_number] = {**aff, "faces": faces}

        self._refresh_tooth_widget(tooth_number)
        self._refresh_summary()
        self._update_info_panel(tooth_number, face)

    def _update_info_panel(self, tooth_number, face):
        self.info_placeholder.setVisible(False)
        self.info_panel.setVisible(True)

        self.info_tooth_label.setText(f"Diente {tooth_number}")

        tool = self.active_tool
        _, _, tool_name = TOOL_COLORS[tool]
        self.info_face_label.setText(f"Marcando {tool_name} en cara {face} ({FACE_LABELS[face]})")

        aff = self.affections.get(tooth_number, {})
        faces = aff.get("faces", {})
        face_data = faces.get(face, {})
        if isinstance(face_data, dict):
            self.desc_field.setText(face_data.get("description", ""))
        else:
            self.desc_field.setText("")

    def _apply_description(self):
        if not self.selected_tooth:
            return
        tw = self._tooth_widgets.get(self.selected_tooth)
        if not tw or not tw.selected_face:
            return

        tooth = self.selected_tooth
        face = tw.selected_face
        desc = self.desc_field.text().strip()

        aff = self.affections.get(tooth, {})
        faces = aff.get("faces", {})
        face_data = faces.get(face, {})
        if isinstance(face_data, dict):
            face_data["description"] = desc
        else:
            face_data = {"tool": self.active_tool, "description": desc}
        faces[face] = face_data
        self.affections[tooth] = {**aff, "faces": faces}
        self._refresh_summary()

    def _clear_current_tooth(self):
        if not self.selected_tooth:
            return
        tooth = self.selected_tooth
        tw = self._tooth_widgets.get(tooth)

        if tooth in self.affections:
            del self.affections[tooth]
        if tw:
            tw.clear_states()

        self.info_placeholder.setVisible(True)
        self.info_panel.setVisible(False)
        self.desc_field.clear()

        self._refresh_summary()

    def _refresh_tooth_widget(self, tooth_number):
        tw = self._tooth_widgets.get(tooth_number)
        if not tw:
            return

        aff = self.affections.get(tooth_number)
        if not aff:
            tw.clear_states()
            return

        faces = aff.get("faces", {})
        face_states = {}
        for face_code, face_data in faces.items():
            if isinstance(face_data, dict):
                face_states[face_code] = face_data.get("tool", TOOL_CARIES)
            else:
                face_states[face_code] = TOOL_CARIES
        tw.set_face_states(face_states)

    def _refresh_all_teeth(self):
        for tooth_num, tw in self._tooth_widgets.items():
            self._refresh_tooth_widget(tooth_num)

    def _refresh_summary(self):
        while self.summary_list.count():
            item = self.summary_list.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                while item.layout().count():
                    sub = item.layout().takeAt(0)
                    if sub.widget():
                        sub.widget().deleteLater()

        if not self.affections:
            self.summary_empty = QLabel("Sin afecciones registradas")
            self.summary_empty.setAlignment(Qt.AlignCenter)
            self.summary_empty.setFont(QFont("Segoe UI", 9))
            self.summary_empty.setStyleSheet(f"color: {Txt2}; background: transparent; padding: 8px;")
            self.summary_list.addWidget(self.summary_empty)
            self.summary_count.setText("0")
            return

        count = 0
        for tooth in sorted(self.affections.keys()):
            aff = self.affections[tooth]
            faces = aff.get("faces", {})
            if not faces:
                continue

            for face_code, face_data in sorted(faces.items()):
                row = QHBoxLayout()
                row.setSpacing(6)

                if isinstance(face_data, dict):
                    tool = face_data.get("tool", TOOL_CARIES)
                    desc = face_data.get("description", "")
                else:
                    tool = TOOL_CARIES
                    desc = str(face_data)

                color, _, tool_name = TOOL_COLORS.get(tool, (Txt2, pale_pink, "Unknown"))

                dot = QFrame()
                dot.setFixedSize(8, 8)
                dot.setStyleSheet(f"""
                    QFrame {{
                        background-color: {color};
                        border-radius: 4px;
                    }}
                """)
                row.addWidget(dot)

                info = QLabel()
                info.setFont(QFont("Segoe UI", 9))
                info.setStyleSheet(f"color: {Txt1}; background: transparent;")
                face_label = FACE_LABELS.get(face_code, face_code)
                desc_text = f' - "{desc}"' if desc else ""
                info.setText(f"<b>Diente {tooth}</b> {face_code} ({face_label}) {tool_name}{desc_text}")
                row.addWidget(info, 1)

                remove_btn = QPushButton("x")
                remove_btn.setFixedSize(20, 20)
                remove_btn.setCursor(Qt.PointingHandCursor)
                remove_btn.setFont(QFont("Segoe UI", 7, QFont.Weight.Bold))
                remove_btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {TOOL_COLORS[TOOL_CARIES][1]};
                        color: {TOOL_COLORS[TOOL_CARIES][0]};
                        border: none;
                        border-radius: 10px;
                    }}
                    QPushButton:hover {{ background-color: {TOOL_COLORS[TOOL_CARIES][0]}; color: white; }}
                """)
                remove_btn.clicked.connect(lambda _, t=tooth, f=face_code: self._remove_face(t, f))
                row.addWidget(remove_btn)

                self.summary_list.addLayout(row)
                count += 1

        self.summary_count.setText(str(count))

    def _remove_face(self, tooth, face):
        aff = self.affections.get(tooth, {})
        faces = aff.get("faces", {})
        faces.pop(face, None)
        if not faces:
            self.affections.pop(tooth, None)
            tw = self._tooth_widgets.get(tooth)
            if tw:
                tw.clear_states()
        else:
            self.affections[tooth] = {**aff, "faces": faces}
            self._refresh_tooth_widget(tooth)
        self._refresh_summary()

    def get_data(self):
        affections_list = []
        for tooth in sorted(self.affections.keys()):
            aff = self.affections[tooth]
            faces = aff.get("faces", {})
            if not faces:
                continue
            for face_code, face_data in faces.items():
                if isinstance(face_data, dict):
                    tool = face_data.get("tool", TOOL_CARIES)
                    desc = face_data.get("description", "")
                else:
                    tool = TOOL_CARIES
                    desc = str(face_data)

                if tool == TOOL_AUSENTE:
                    affected = "Ausente"
                elif tool == TOOL_RESINA:
                    affected = "Resina"
                elif tool == TOOL_ENDODONCIA:
                    affected = "Endodoncia"
                elif tool == TOOL_CORONA:
                    affected = "Corona"
                else:
                    affected = "Yes"

                affections_list.append({
                    "tooth": tooth,
                    "face": face_code,
                    "affected": affected,
                    "description": desc,
                })
        return {"affections": affections_list}

    def load_data(self, odontogram_details):
        self.affections.clear()
        for row in odontogram_details:
            if len(row) >= 6:
                detail_id, odontogram_id, tooth, face, affected, description = row[:6]
            else:
                continue

            if affected in ("No", ""):
                continue

            if tooth not in self.affections:
                self.affections[tooth] = {"faces": {}}

            faces = self.affections[tooth]["faces"]

            if face is None:
                tool = TOOL_CARIES
                if affected == "Ausente":
                    tool = TOOL_AUSENTE
                elif affected == "Resina":
                    tool = TOOL_RESINA
                elif affected == "Endodoncia":
                    tool = TOOL_ENDODONCIA
                elif affected == "Corona":
                    tool = TOOL_CORONA
                for fc in ["V", "O", "L", "M", "D"]:
                    faces[fc] = {"tool": tool, "description": description or ""}
            else:
                tool = TOOL_CARIES
                if affected == "Ausente":
                    tool = TOOL_AUSENTE
                elif affected == "Resina":
                    tool = TOOL_RESINA
                elif affected == "Endodoncia":
                    tool = TOOL_ENDODONCIA
                elif affected == "Corona":
                    tool = TOOL_CORONA
                faces[face] = {"tool": tool, "description": description or ""}

        self._refresh_all_teeth()
        self._refresh_summary()
