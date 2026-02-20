import re

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QScrollArea, QFrame, QSizePolicy, QLineEdit,
    QGraphicsDropShadowEffect
)
from PySide6.QtCore import Signal, Qt, QTimer
from PySide6.QtGui import QColor
from ui.styles.theme import CURRENT_THEME

# Regex that matches one or more Hebrew characters (U+0590 – U+05FF)
_HEB_RE = re.compile(r'[\u0590-\u05FF]')


# =============================================================================
# ChatBubble - Strict left/right alignment
# =============================================================================

class ChatBubble(QWidget):
    """
    Single chat message with strict two-sided layout:
      Agent → [🤖 Avatar] [Bubble] [===Stretch===]   (LEFT)
      User  → [===Stretch===] [Bubble] [👤 Avatar]   (RIGHT)
    """

    def __init__(self, sender_type: str, message: str, parent=None):
        super().__init__(parent)
        self.sender_type = sender_type
        self.message = message
        self.setContentsMargins(0, 0, 0, 0)
        self._build()

    def _build(self):
        T = CURRENT_THEME

        row = QHBoxLayout(self)
        row.setContentsMargins(24, 4, 24, 4)
        row.setSpacing(12)

        avatar = self._avatar(T)
        bubble = self._bubble(T)

        if self.sender_type == "agent":
            #  [Avatar] [Bubble] [Stretch]
            row.addWidget(avatar, 0, Qt.AlignTop)
            row.addWidget(bubble, 0)
            row.addStretch(1)
        else:
            #  [Stretch] [Bubble] [Avatar]
            row.addStretch(1)
            row.addWidget(bubble, 0)
            row.addWidget(avatar, 0, Qt.AlignTop)

    def _avatar(self, T) -> QLabel:
        is_agent = self.sender_type == "agent"
        icon = "🤖" if is_agent else "👤"
        bg   = T.BG_AVATAR_AGENT if is_agent else T.BG_AVATAR_USER

        lbl = QLabel(icon)
        lbl.setFixedSize(36, 36)
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet(f"""
            background-color: {bg};
            border-radius: 18px;
            font-size: 16px;
        """)
        return lbl

    # ----- Hebrew / RTL detection -----
    @staticmethod
    def _is_hebrew(text: str) -> bool:
        """Return True if *text* contains at least one Hebrew character."""
        return bool(_HEB_RE.search(text))

    def _bubble(self, T) -> QFrame:
        is_agent = self.sender_type == "agent"

        bg    = T.BG_BUBBLE_AGENT if is_agent else T.BG_BUBBLE_USER
        color = T.TEXT_BUBBLE_AGENT if is_agent else T.TEXT_BUBBLE_USER
        # Sharp corner points toward the avatar
        radius = "4px 18px 18px 18px" if is_agent else "18px 4px 18px 18px"

        frame = QFrame()
        frame.setObjectName("msg_bubble")
        frame.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
        frame.setMaximumWidth(480)
        frame.setStyleSheet(f"""
            #msg_bubble {{
                background-color: {bg};
                border-radius: {radius};
            }}
        """)

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(0)

        # Detect RTL for Hebrew text
        rtl = self._is_hebrew(self.message)
        alignment = Qt.AlignRight if rtl else Qt.AlignLeft
        direction = Qt.RightToLeft if rtl else Qt.LeftToRight

        text = QLabel(self.message)
        text.setWordWrap(True)
        text.setTextFormat(Qt.PlainText)
        text.setAlignment(alignment | Qt.AlignVCenter)
        text.setLayoutDirection(direction)
        text.setStyleSheet(f"""
            background: transparent;
            color: {color};
            font-size: 14px;
            line-height: 1.5;
            padding: 2px 4px;
        """)

        layout.addWidget(text)
        return frame


# =============================================================================
# ThinkingBubble - Animated typewriter "Thinking..."
# =============================================================================

class ThinkingBubble(QWidget):
    """
    Animated placeholder shown while waiting for agent response.
    Typewriter effect: T → Th → Thi → … → Thinking... → loops.
    """

    FULL_TEXT = "Thinking..."

    def __init__(self, parent=None):
        super().__init__(parent)
        self._idx = 0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._build()

    def _build(self):
        T = CURRENT_THEME

        row = QHBoxLayout(self)
        row.setContentsMargins(24, 4, 24, 4)
        row.setSpacing(12)

        # Agent avatar
        avatar = QLabel("🤖")
        avatar.setFixedSize(36, 36)
        avatar.setAlignment(Qt.AlignCenter)
        avatar.setStyleSheet(f"""
            background-color: {T.BG_AVATAR_AGENT};
            border-radius: 18px;
            font-size: 16px;
        """)

        # Bubble
        frame = QFrame()
        frame.setObjectName("thinking_frame")
        frame.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
        frame.setStyleSheet(f"""
            #thinking_frame {{
                background-color: {T.BG_BUBBLE_AGENT};
                border-radius: 4px 18px 18px 18px;
            }}
        """)
        fl = QVBoxLayout(frame)
        fl.setContentsMargins(16, 12, 16, 12)

        self._label = QLabel("")
        self._label.setStyleSheet(f"""
            background: transparent;
            color: {T.TEXT_SECONDARY};
            font-size: 14px;
            font-style: italic;
        """)
        fl.addWidget(self._label)

        # Left-aligned
        row.addWidget(avatar, 0, Qt.AlignTop)
        row.addWidget(frame, 0)
        row.addStretch(1)

    # --- Animation ---
    def _tick(self):
        self._idx += 1
        if self._idx > len(self.FULL_TEXT):
            self._idx = 1
        self._label.setText(self.FULL_TEXT[:self._idx])

    def start_animation(self):
        self._idx = 0
        self._label.setText("")
        self._timer.start(75)

    def stop_animation(self):
        self._timer.stop()


# =============================================================================
# ChatInputWidget - Floating pill with shadow
# =============================================================================

class ChatInputWidget(QWidget):
    """Pill-shaped input area with embedded round send button and drop-shadow."""

    send_requested = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build()

    def _build(self):
        T = CURRENT_THEME

        self.setObjectName("chat_input_pill")
        self.setMinimumHeight(56)
        self.setStyleSheet(f"""
            #chat_input_pill {{
                background-color: {T.BG_INPUT};
                border: 1.5px solid {T.BORDER_INPUT};
                border-radius: 26px;
            }}
            #chat_input_pill:hover {{
                border-color: {T.BORDER_INPUT_FOCUS};
            }}
        """)

        # Drop shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(24)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 90))
        self.setGraphicsEffect(shadow)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(18, 8, 8, 8)
        layout.setSpacing(10)

        # Text field
        self.input_field = QLineEdit()
        self.input_field.setObjectName("chat_input")
        self.input_field.setPlaceholderText("Message the AI assistant...")
        self.input_field.setStyleSheet("""
            QLineEdit { 
                background-color: #40414F; 
                border: 1px solid #565869; 
                border-radius: 18px;       
                color: #FFFFFF;            
                padding: 10px 15px;        
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #10a37f; 
                background-color: #484a56; 
            }
        """)
        self.input_field.returnPressed.connect(self._on_send)

        # Round send button
        self.send_btn = QPushButton("➤")
        self.send_btn.setObjectName("send_btn")
        self.send_btn.setFixedSize(42, 42)
        self.send_btn.setCursor(Qt.PointingHandCursor)
        self.send_btn.setToolTip("Send message")
        self.send_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {T.ACCENT_COLOR};
                border: none;
                border-radius: 21px;
                color: white;
                font-size: 17px;
                font-weight: bold;
            }}
            QPushButton:hover  {{ background-color: {T.ACCENT_HOVER}; }}
            QPushButton:pressed {{ background-color: {T.ACCENT_PRESSED}; }}
        """)
        self.send_btn.clicked.connect(self._on_send)

        layout.addWidget(self.input_field, 1)
        layout.addWidget(self.send_btn, 0)

    def _on_send(self):
        text = self.input_field.text().strip()
        if text:
            self.send_requested.emit(text)
            self.input_field.clear()

    def get_text(self) -> str:
        return self.input_field.text().strip()

    def clear(self):
        self.input_field.clear()


# =============================================================================
# ChatView - Main container
# =============================================================================

class ChatView(QWidget):
    """
    Full chat view: scrollable message history + thinking animation + floating input.
    Intercepts "Thinking..." messages to display an animated ThinkingBubble.
    """

    send_clicked = Signal(str)

    USER_KEYWORDS = ["me", "you", "user"]
    THINKING_TRIGGERS = ["thinking...", "thinking"]

    def __init__(self):
        super().__init__()
        self._thinking_bubble: ThinkingBubble | None = None
        self._welcome_visible = True
        self._build()

    def _build(self):
        T = CURRENT_THEME

        self.setObjectName("chat_container")
        self.setStyleSheet(f"background-color: {T.BG_MAIN};")

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # --- Scroll area for messages ---
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setStyleSheet("background: transparent; border: none;")

        self.messages_container = QWidget()
        self.messages_container.setStyleSheet(f"background-color: {T.BG_MAIN};")

        self.messages_layout = QVBoxLayout(self.messages_container)
        self.messages_layout.setContentsMargins(0, 20, 0, 20)
        self.messages_layout.setSpacing(2)
        self.messages_layout.addStretch()  # Sentinel at end

        self.scroll_area.setWidget(self.messages_container)

        # --- Welcome state ---
        self._welcome_widget = self._create_welcome(T)
        self.messages_layout.insertWidget(0, self._welcome_widget)

        # --- Input area ---
        input_wrap = QWidget()
        input_wrap.setStyleSheet(f"background-color: {T.BG_MAIN};")
        ilay = QVBoxLayout(input_wrap)
        ilay.setContentsMargins(60, 12, 60, 20)
        ilay.setSpacing(8)

        self.chat_input = ChatInputWidget()
        self.chat_input.send_requested.connect(self._on_send_requested)

        disclaimer = QLabel("AI may make mistakes. Verify important information.")
        disclaimer.setAlignment(Qt.AlignCenter)
        disclaimer.setStyleSheet(f"color: {T.TEXT_TERTIARY}; font-size: 11px;")

        ilay.addWidget(self.chat_input)
        ilay.addWidget(disclaimer)

        root.addWidget(self.scroll_area, 1)
        root.addWidget(input_wrap, 0)

    # --- Welcome / empty state ---
    @staticmethod
    def _create_welcome(T) -> QWidget:
        w = QWidget()
        w.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(w)
        lay.setAlignment(Qt.AlignCenter)
        lay.setSpacing(12)
        lay.setContentsMargins(40, 80, 40, 60)

        icon = QLabel("🛒")
        icon.setAlignment(Qt.AlignCenter)
        icon.setStyleSheet("font-size: 52px; background: transparent;")

        title = QLabel("Supermarket AI Assistant")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
            color: {T.TEXT_PRIMARY}; font-size: 24px;
            font-weight: bold; background: transparent;
        """)

        subtitle = QLabel("Tell me what you need and I'll find the best deals for you.")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet(f"""
            color: {T.TEXT_SECONDARY}; font-size: 14px; background: transparent;
        """)

        lay.addWidget(icon)
        lay.addWidget(title)
        lay.addWidget(subtitle)
        return w

    # --- Internal helpers ---
    def _on_send_requested(self, text: str):
        self.send_clicked.emit(text)

    def _is_user_sender(self, sender: str) -> bool:
        s = sender.lower()
        return any(k in s for k in self.USER_KEYWORDS)

    def _is_thinking_text(self, text: str) -> bool:
        return text.strip().lower() in self.THINKING_TRIGGERS

    def _scroll_to_bottom(self):
        QTimer.singleShot(20, lambda: self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        ))

    def _hide_welcome(self):
        if self._welcome_visible and self._welcome_widget:
            self._welcome_widget.hide()
            self._welcome_visible = False

    # --- Public API (presenter contract) ---

    def append_message(self, sender: str, text: str):
        """
        Add a message bubble to the chat.

        Intercepts "Thinking..." text from the agent to show an animated
        ThinkingBubble instead. When the real agent response arrives,
        the ThinkingBubble is removed automatically.

        Args:
            sender: 'Me'/'You'/'User' → user side; anything else → agent side
            text:   message content
        """
        sender_type = "user" if self._is_user_sender(sender) else "agent"

        # Remove thinking animation when agent sends a real message
        if sender_type == "agent":
            self.remove_thinking()

        # Intercept "Thinking..." → show animated bubble instead
        if sender_type == "agent" and self._is_thinking_text(text):
            self.show_thinking()
            return

        # Hide welcome on first real message
        self._hide_welcome()

        bubble = ChatBubble(sender_type, text)
        count = self.messages_layout.count()
        self.messages_layout.insertWidget(count - 1, bubble)
        self._scroll_to_bottom()

    def show_thinking(self):
        """Display the animated thinking bubble."""
        if self._thinking_bubble is not None:
            return
        self._hide_welcome()
        self._thinking_bubble = ThinkingBubble()
        self._thinking_bubble.start_animation()
        count = self.messages_layout.count()
        self.messages_layout.insertWidget(count - 1, self._thinking_bubble)
        self._scroll_to_bottom()

    def remove_thinking(self):
        """Remove the thinking bubble if present."""
        if self._thinking_bubble is not None:
            self._thinking_bubble.stop_animation()
            self.messages_layout.removeWidget(self._thinking_bubble)
            self._thinking_bubble.deleteLater()
            self._thinking_bubble = None

    def clear_messages(self):
        """Clear all messages (keeps the trailing stretch)."""
        self.remove_thinking()
        while self.messages_layout.count() > 1:
            item = self.messages_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()