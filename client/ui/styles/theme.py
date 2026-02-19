"""
Premium Dark Theme for Agentic Chat UI
Inspired by ChatGPT Desktop / Microsoft 365 Copilot
"""


class DarkTheme:
    # ============================================
    # MAIN BACKGROUNDS
    # ============================================
    BG_MAIN = "#212121"           # Main background (matte charcoal)
    BG_SIDEBAR = "#171717"        # Sidebar background (near black)
    BG_SIDEBAR_HOVER = "#2A2B32"  # Sidebar item hover
    BG_CARD = "#2F2F2F"           # Cards/messages background
    BG_SURFACE = "#2F2F2F"        # Elevated surface
    BG_SURFACE_HOVER = "#383838"  # Elevated surface hover
    BG_INPUT = "#3C3C3C"          # Input field background
    BG_INPUT_FOCUS = "#454545"    # Input field focused state
    BG_OVERLAY = "#000000CC"      # Modal overlay (with transparency)
    
    # ============================================
    # CHAT BUBBLE COLORS
    # ============================================
    BG_BUBBLE_USER = "#2563EB"    # User message bubble (blue accent)
    BG_BUBBLE_AGENT = "#2F2F2F"   # Agent message bubble (neutral surface)
    TEXT_BUBBLE_USER = "#FFFFFF"  # User bubble text (white on blue)
    TEXT_BUBBLE_AGENT = "#ECECEC" # Agent bubble text (off-white)
    BG_AVATAR_AGENT = "#10a37f"   # Agent avatar (green)
    BG_AVATAR_USER = "#2563EB"    # User avatar (blue)
    
    # Legacy alias for backwards compatibility
    BG_AGENT_AVATAR = "#10a37f"
    
    # ============================================
    # CART CARD COLORS
    # ============================================
    BG_CART_CARD = "#2F2F2F"      # Cart item card background (pops against sidebar)
    BG_CART_CARD_HOVER = "#3A3A3A"  # Cart item hover
    BG_QUANTITY_BTN = "#3C3C3C"   # Quantity +/- button background
    
    # ============================================
    # TEXT COLORS
    # ============================================
    TEXT_PRIMARY = "#ECECEC"      # Primary text (off-white)
    TEXT_SECONDARY = "#8E8EA0"    # Secondary/muted text
    TEXT_TERTIARY = "#6E6E80"     # Tertiary/disabled text
    TEXT_PLACEHOLDER = "#6E6E80"  # Placeholder text
    TEXT_INVERSE = "#FFFFFF"      # Text on accent backgrounds
    
    # ============================================
    # ACCENT COLORS (Brand)
    # ============================================
    ACCENT_COLOR = "#10a37f"      # Primary accent (emerald green)
    ACCENT_HOVER = "#1a7f64"      # Accent hover state
    ACCENT_PRESSED = "#0d8a6a"    # Accent pressed state
    ACCENT_LIGHT = "#10a37f33"    # Accent with transparency (for glows)
    
    # ============================================
    # SEMANTIC COLORS
    # ============================================
    SUCCESS = "#10a37f"           # Success state
    WARNING = "#F5A623"           # Warning state
    ERROR = "#EF4444"             # Error state
    INFO = "#3B82F6"              # Info state
    
    # ============================================
    # BORDERS & DIVIDERS
    # ============================================
    BORDER_COLOR = "#4A4A4A"      # Default border
    BORDER_SUBTLE = "#333333"     # Subtle border
    BORDER_INPUT = "#4A4A4A"      # Input field border
    BORDER_INPUT_FOCUS = "#10a37f"  # Input focused border
    DIVIDER = "#444654"           # Divider lines
    
    # ============================================
    # SHADOWS
    # ============================================
    SHADOW_SOFT = "rgba(0, 0, 0, 0.3)"
    SHADOW_MEDIUM = "rgba(0, 0, 0, 0.5)"
    SHADOW_STRONG = "rgba(0, 0, 0, 0.7)"
    
    # ============================================
    # TYPOGRAPHY
    # ============================================
    FONT_FAMILY = "'Segoe UI', 'Roboto', sans-serif"
    FONT_SIZE_XS = "11px"
    FONT_SIZE_SM = "12px"
    FONT_SIZE_BASE = "14px"
    FONT_SIZE_MD = "15px"
    FONT_SIZE_LG = "16px"
    FONT_SIZE_XL = "18px"
    FONT_SIZE_2XL = "20px"
    FONT_SIZE_TITLE = "24px"
    
    # ============================================
    # SPACING & SIZING
    # ============================================
    BORDER_RADIUS_SM = "6px"
    BORDER_RADIUS_MD = "8px"
    BORDER_RADIUS_LG = "12px"
    BORDER_RADIUS_XL = "16px"
    BORDER_RADIUS_PILL = "24px"
    
    SIDEBAR_WIDTH = "260px"
    CART_WIDTH = "320px"
    AVATAR_SIZE = "32px"
    ICON_SIZE = "20px"


class LightTheme:
    # Light theme placeholder - can be expanded later
    BG_MAIN = "#FFFFFF"
    BG_SIDEBAR = "#F7F7F8"
    BG_SIDEBAR_HOVER = "#ECECF1"
    BG_CARD = "#FFFFFF"
    BG_SURFACE = "#F7F7F8"
    BG_SURFACE_HOVER = "#E8E8E8"
    BG_INPUT = "#FFFFFF"
    BG_INPUT_FOCUS = "#F7F7F8"
    BG_OVERLAY = "#00000080"
    
    BG_BUBBLE_USER = "#2563EB"    # User message bubble (blue accent)
    BG_BUBBLE_AGENT = "#E5E5EA"   # Agent message bubble (light grey)
    TEXT_BUBBLE_USER = "#FFFFFF"  # User bubble text (white)
    TEXT_BUBBLE_AGENT = "#202123" # Agent bubble text (dark)
    BG_AVATAR_AGENT = "#10a37f"   # Agent avatar (green)
    BG_AVATAR_USER = "#2563EB"    # User avatar (blue)
    
    # Legacy alias for backwards compatibility
    BG_AGENT_AVATAR = "#10a37f"
    
    BG_CART_CARD = "#F7F7F8"
    BG_CART_CARD_HOVER = "#ECECF1"
    BG_QUANTITY_BTN = "#E5E5E5"
    
    TEXT_PRIMARY = "#202123"
    TEXT_SECONDARY = "#6E6E80"
    TEXT_TERTIARY = "#8E8EA0"
    TEXT_PLACEHOLDER = "#8E8EA0"
    TEXT_INVERSE = "#FFFFFF"
    
    ACCENT_COLOR = "#10a37f"
    ACCENT_HOVER = "#1a7f64"
    ACCENT_PRESSED = "#0d8a6a"
    ACCENT_LIGHT = "#10a37f33"
    
    SUCCESS = "#10a37f"
    WARNING = "#F5A623"
    ERROR = "#EF4444"
    INFO = "#3B82F6"
    
    BORDER_COLOR = "#D9D9E3"
    BORDER_SUBTLE = "#E5E5E5"
    BORDER_INPUT = "#D9D9E3"
    BORDER_INPUT_FOCUS = "#10a37f"
    DIVIDER = "#E5E5E5"
    
    SHADOW_SOFT = "rgba(0, 0, 0, 0.1)"
    SHADOW_MEDIUM = "rgba(0, 0, 0, 0.15)"
    SHADOW_STRONG = "rgba(0, 0, 0, 0.2)"
    
    FONT_FAMILY = "'Segoe UI', 'Roboto', sans-serif"
    FONT_SIZE_XS = "11px"
    FONT_SIZE_SM = "12px"
    FONT_SIZE_BASE = "14px"
    FONT_SIZE_MD = "15px"
    FONT_SIZE_LG = "16px"
    FONT_SIZE_XL = "18px"
    FONT_SIZE_2XL = "20px"
    FONT_SIZE_TITLE = "24px"
    
    BORDER_RADIUS_SM = "6px"
    BORDER_RADIUS_MD = "8px"
    BORDER_RADIUS_LG = "12px"
    BORDER_RADIUS_XL = "16px"
    BORDER_RADIUS_PILL = "24px"
    
    SIDEBAR_WIDTH = "260px"
    CART_WIDTH = "320px"
    AVATAR_SIZE = "32px"
    ICON_SIZE = "20px"


# Active theme selection
CURRENT_THEME = DarkTheme


def get_main_stylesheet():
    """
    Returns the global QSS for the application.
    Defines base styles for all standard Qt widgets.
    """
    T = CURRENT_THEME
    return f"""
    /* ============================================
       GLOBAL STYLES
       ============================================ */
    QMainWindow {{
        background-color: {T.BG_MAIN};
    }}
    
    QWidget {{
        color: {T.TEXT_PRIMARY};
        font-family: {T.FONT_FAMILY};
        font-size: {T.FONT_SIZE_BASE};
        background-color: transparent;
    }}
    
    /* ============================================
       SCROLL AREAS
       ============================================ */
    QScrollArea {{
        border: none;
        background-color: transparent;
    }}
    
    QScrollBar:vertical {{
        background-color: transparent;
        width: 8px;
        margin: 0px;
    }}
    
    QScrollBar::handle:vertical {{
        background-color: {T.BORDER_COLOR};
        border-radius: 4px;
        min-height: 30px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background-color: {T.TEXT_SECONDARY};
    }}
    
    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    
    QScrollBar::add-page:vertical,
    QScrollBar::sub-page:vertical {{
        background: none;
    }}
    
    /* ============================================
       BUTTONS
       ============================================ */
    QPushButton {{
        background-color: {T.BG_CARD};
        border: 1px solid {T.BORDER_COLOR};
        border-radius: {T.BORDER_RADIUS_SM};
        padding: 8px 16px;
        color: {T.TEXT_PRIMARY};
        font-size: {T.FONT_SIZE_BASE};
    }}
    
    QPushButton:hover {{
        background-color: {T.BG_INPUT};
        border-color: {T.TEXT_SECONDARY};
    }}
    
    QPushButton:pressed {{
        background-color: {T.BG_SIDEBAR_HOVER};
    }}
    
    QPushButton:disabled {{
        color: {T.TEXT_TERTIARY};
        background-color: {T.BG_SIDEBAR};
    }}
    
    /* ============================================
       TEXT INPUT
       ============================================ */
    QTextEdit, QLineEdit {{
        background-color: {T.BG_INPUT};
        border: 1px solid {T.BORDER_INPUT};
        border-radius: {T.BORDER_RADIUS_MD};
        padding: 10px 14px;
        color: {T.TEXT_PRIMARY};
        font-size: {T.FONT_SIZE_BASE};
        selection-background-color: {T.ACCENT_COLOR};
    }}
    
    QTextEdit:focus, QLineEdit:focus {{
        border-color: {T.BORDER_INPUT_FOCUS};
        background-color: {T.BG_INPUT_FOCUS};
    }}
    
    QLineEdit::placeholder {{
        color: {T.TEXT_PLACEHOLDER};
    }}
    
    /* ============================================
       LABELS
       ============================================ */
    QLabel {{
        background-color: transparent;
        color: {T.TEXT_PRIMARY};
    }}
    
    /* ============================================
       LIST WIDGETS
       ============================================ */
    QListWidget {{
        background-color: transparent;
        border: none;
        outline: none;
    }}
    
    QListWidget::item {{
        background-color: transparent;
        border: none;
        padding: 4px;
    }}
    
    QListWidget::item:selected {{
        background-color: {T.BG_SIDEBAR_HOVER};
    }}
    
    QListWidget::item:hover {{
        background-color: {T.BG_SIDEBAR_HOVER};
    }}
    
    /* ============================================
       TOOLTIPS
       ============================================ */
    QToolTip {{
        background-color: {T.BG_CARD};
        color: {T.TEXT_PRIMARY};
        border: 1px solid {T.BORDER_COLOR};
        border-radius: 6px;
        padding: 6px 10px;
        font-size: {T.FONT_SIZE_SM};
    }}
    
    /* ============================================
       HORIZONTAL SCROLLBAR
       ============================================ */
    QScrollBar:horizontal {{
        height: 0px;
        background: transparent;
    }}
    """


def get_sidebar_stylesheet():
    """
    Returns QSS specific to the sidebar component.
    """
    T = CURRENT_THEME
    return f"""
    /* Sidebar Container */
    #sidebar_container {{
        background-color: {T.BG_SIDEBAR};
        border-right: 1px solid {T.BORDER_SUBTLE};
    }}
    
    /* Hamburger/Toggle Button */
    #sidebar_toggle_btn {{
        background-color: transparent;
        border: none;
        border-radius: {T.BORDER_RADIUS_SM};
        padding: 8px;
        color: {T.TEXT_SECONDARY};
        font-size: {T.FONT_SIZE_XL};
    }}
    
    #sidebar_toggle_btn:hover {{
        background-color: {T.BG_SIDEBAR_HOVER};
        color: {T.TEXT_PRIMARY};
    }}
    
    /* New Chat Button */
    #new_chat_btn {{
        background-color: transparent;
        border: 1px solid {T.BORDER_COLOR};
        border-radius: {T.BORDER_RADIUS_MD};
        padding: 12px 16px;
        color: {T.TEXT_PRIMARY};
        text-align: left;
        font-size: {T.FONT_SIZE_BASE};
    }}
    
    #new_chat_btn:hover {{
        background-color: {T.BG_SIDEBAR_HOVER};
    }}
    
    /* History Items */
    #history_item {{
        background-color: transparent;
        border: none;
        border-radius: {T.BORDER_RADIUS_SM};
        padding: 10px 12px;
        color: {T.TEXT_SECONDARY};
        text-align: left;
    }}
    
    #history_item:hover {{
        background-color: {T.BG_SIDEBAR_HOVER};
        color: {T.TEXT_PRIMARY};
    }}
    
    /* Section Labels */
    #sidebar_section_label {{
        color: {T.TEXT_TERTIARY};
        font-size: {T.FONT_SIZE_SM};
        padding: 8px 12px;
    }}
    """


def get_chat_stylesheet():
    """
    Returns QSS specific to the chat component.
    """
    T = CURRENT_THEME
    return f"""
    /* Chat Container */
    #chat_container {{
        background-color: {T.BG_MAIN};
    }}
    
    /* Chat History Area */
    #chat_history_area {{
        background-color: transparent;
        border: none;
    }}
    
    /* User Message Bubble */
    #user_bubble {{
        background-color: {T.BG_BUBBLE_USER};
        border-radius: {T.BORDER_RADIUS_LG};
        padding: 12px 16px;
        color: {T.TEXT_PRIMARY};
    }}
    
    /* Agent Message Bubble */
    #agent_bubble {{
        background-color: transparent;
        padding: 12px 0px;
        color: {T.TEXT_PRIMARY};
    }}
    
    /* Agent Avatar */
    #agent_avatar {{
        background-color: {T.BG_AGENT_AVATAR};
        border-radius: 16px;
        color: {T.TEXT_INVERSE};
        font-size: {T.FONT_SIZE_SM};
    }}
    
    /* Input Container (floating pill) */
    #chat_input_container {{
        background-color: {T.BG_INPUT};
        border: 1px solid {T.BORDER_INPUT};
        border-radius: {T.BORDER_RADIUS_XL};
        padding: 4px;
    }}
    
    #chat_input_container:focus-within {{
        border-color: {T.BORDER_INPUT_FOCUS};
    }}
    
    /* Chat Input Field */
    #chat_input {{
        background-color: transparent;
        border: none;
        padding: 12px 16px;
        color: {T.TEXT_PRIMARY};
        font-size: {T.FONT_SIZE_BASE};
    }}
    
    #chat_input:focus {{
        border: none;
        outline: none;
    }}
    
    /* Send Button */
    #send_btn {{
        background-color: {T.ACCENT_COLOR};
        border: none;
        border-radius: {T.BORDER_RADIUS_MD};
        padding: 10px 16px;
        color: {T.TEXT_INVERSE};
        font-weight: bold;
    }}
    
    #send_btn:hover {{
        background-color: {T.ACCENT_HOVER};
    }}
    
    #send_btn:pressed {{
        background-color: {T.ACCENT_PRESSED};
    }}
    
    #send_btn:disabled {{
        background-color: {T.BG_QUANTITY_BTN};
        color: {T.TEXT_TERTIARY};
    }}
    """


def get_cart_stylesheet():
    """
    Returns QSS specific to the cart component.
    """
    T = CURRENT_THEME
    return f"""
    /* Cart Container */
    #cart_container {{
        background-color: {T.BG_SIDEBAR};
        border-left: 1px solid {T.BORDER_SUBTLE};
    }}
    
    /* Cart Header */
    #cart_header {{
        background-color: transparent;
        padding: 16px;
        border-bottom: 1px solid {T.BORDER_SUBTLE};
    }}
    
    #cart_title {{
        color: {T.TEXT_PRIMARY};
        font-size: {T.FONT_SIZE_LG};
        font-weight: bold;
    }}
    
    #cart_store_name {{
        color: {T.TEXT_PRIMARY};
        font-size: {T.FONT_SIZE_MD};
        font-weight: 600;
    }}
    
    #cart_store_address {{
        color: {T.TEXT_SECONDARY};
        font-size: {T.FONT_SIZE_SM};
    }}
    
    /* Cart Item Card */
    #cart_item_card {{
        background-color: {T.BG_CART_CARD};
        border: 1px solid {T.BORDER_SUBTLE};
        border-radius: {T.BORDER_RADIUS_MD};
        padding: 12px;
        margin: 4px 0px;
    }}
    
    #cart_item_card:hover {{
        background-color: {T.BG_CART_CARD_HOVER};
        border-color: {T.BORDER_COLOR};
    }}
    
    /* Product Icon/Image Placeholder */
    #product_icon {{
        background-color: {T.BG_INPUT};
        border-radius: {T.BORDER_RADIUS_SM};
        color: {T.TEXT_SECONDARY};
    }}
    
    /* Product Name */
    #product_name {{
        color: {T.TEXT_PRIMARY};
        font-size: {T.FONT_SIZE_BASE};
        font-weight: 500;
    }}
    
    /* Product Price */
    #product_price {{
        color: {T.ACCENT_COLOR};
        font-size: {T.FONT_SIZE_SM};
        font-weight: 600;
    }}
    
    /* Quantity Controls */
    #qty_btn {{
        background-color: {T.BG_QUANTITY_BTN};
        border: none;
        border-radius: {T.BORDER_RADIUS_SM};
        color: {T.TEXT_PRIMARY};
        font-size: {T.FONT_SIZE_LG};
        font-weight: bold;
        padding: 4px;
        min-width: 28px;
        min-height: 28px;
    }}
    
    #qty_btn:hover {{
        background-color: {T.ACCENT_COLOR};
        color: {T.TEXT_INVERSE};
    }}
    
    #qty_btn:pressed {{
        background-color: {T.ACCENT_PRESSED};
    }}
    
    #qty_label {{
        color: {T.TEXT_PRIMARY};
        font-size: {T.FONT_SIZE_BASE};
        font-weight: 600;
        min-width: 32px;
    }}
    
    /* Cart Footer */
    #cart_footer {{
        background-color: {T.BG_SIDEBAR};
        border-top: 1px solid {T.BORDER_SUBTLE};
        padding: 16px;
    }}
    
    #cart_total_label {{
        color: {T.TEXT_SECONDARY};
        font-size: {T.FONT_SIZE_BASE};
    }}
    
    #cart_total_price {{
        color: {T.TEXT_PRIMARY};
        font-size: {T.FONT_SIZE_XL};
        font-weight: bold;
    }}
    
    /* Optimize Button */
    #optimize_btn {{
        background-color: {T.ACCENT_COLOR};
        border: none;
        border-radius: {T.BORDER_RADIUS_MD};
        padding: 14px 24px;
        color: {T.TEXT_INVERSE};
        font-size: {T.FONT_SIZE_BASE};
        font-weight: bold;
    }}
    
    #optimize_btn:hover {{
        background-color: {T.ACCENT_HOVER};
    }}
    
    #optimize_btn:pressed {{
        background-color: {T.ACCENT_PRESSED};
    }}
    
    #optimize_btn:disabled {{
        background-color: {T.BG_QUANTITY_BTN};
        color: {T.TEXT_TERTIARY};
    }}
    """


# Convenience function to get all stylesheets combined
def get_all_stylesheets():
    """
    Returns all stylesheets concatenated for full application styling.
    """
    return (
        get_main_stylesheet() +
        get_sidebar_stylesheet() +
        get_chat_stylesheet() +
        get_cart_stylesheet()
    )