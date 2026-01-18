"""
DEEP SPACE DESIGN SYSTEM - ULTRA PREMIUM EDITION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Design Philosophy:
- Inspired by Linear, Raycast, and Arc Browser
- Deep space aesthetics with electric accents
- Micro-interactions for premium feel
- Generous spacing (8px base unit system)
- Surgical focus on visual hierarchy

Color Psychology:
- Deep blacks create focus and reduce eye strain
- Electric indigo/violet creates energy and modernity
- Emerald green for positive reinforcement (totals, success)
- Strategic use of opacity for depth perception
"""

class Theme:
    # ═══════════════════════════════════════════════════════════
    # FOUNDATION - THE CANVAS
    # ═══════════════════════════════════════════════════════════
    BG_VOID          = "#000000"  # Absolute zero (for contrast moments)
    BG_PRIMARY       = "#0a0a0a"  # Deep space base
    BG_SECONDARY     = "#121212"  # Subtle elevation 1
    BG_TERTIARY      = "#18181b"  # Subtle elevation 2
    
    # ═══════════════════════════════════════════════════════════
    # SURFACES - FLOATING CARDS & CONTAINERS
    # ═══════════════════════════════════════════════════════════
    SURFACE_LOW      = "#1c1c1e"  # Barely elevated
    SURFACE_DEFAULT  = "#27272a"  # Standard card surface
    SURFACE_RAISED   = "#2e2e33"  # Hover/Active state
    SURFACE_HIGHEST  = "#3f3f46"  # Maximum elevation
    
    # ═══════════════════════════════════════════════════════════
    # BORDERS & DIVIDERS - SUBTLE STRUCTURE
    # ═══════════════════════════════════════════════════════════
    BORDER_INVISIBLE = "#1a1a1a"  # Almost invisible
    BORDER_SUBTLE    = "#2d2d30"  # Low contrast
    BORDER_DEFAULT   = "#3f3f46"  # Standard dividers
    BORDER_STRONG    = "#52525b"  # High contrast
    BORDER_EMPHASIS  = "#71717a"  # Maximum contrast
    
    # ═══════════════════════════════════════════════════════════
    # ACCENT SYSTEM - ELECTRIC GRADIENT SPECTRUM
    # ═══════════════════════════════════════════════════════════
    # Primary Gradient (Indigo → Violet)
    ACCENT_START     = "#6366f1"  # Electric Indigo 500
    ACCENT_END       = "#8b5cf6"  # Vivid Violet 500
    
    # Interaction States
    ACCENT_HOVER_START   = "#818cf8"  # Indigo 400 (brightened)
    ACCENT_HOVER_END     = "#a78bfa"  # Violet 400 (brightened)
    ACCENT_PRESSED       = "#4f46e5"  # Indigo 600 (darkened)
    
    # Glow & Effects
    ACCENT_GLOW      = "#a5b4fc"  # Indigo 300 (outer glow)
    ACCENT_SHADOW    = "rgba(99, 102, 241, 0.25)"  # Soft shadow
    ACCENT_OVERLAY   = "rgba(99, 102, 241, 0.08)"  # Subtle fill
    
    # ═══════════════════════════════════════════════════════════
    # TYPOGRAPHY HIERARCHY
    # ═══════════════════════════════════════════════════════════
    TEXT_HERO        = "#ffffff"  # Maximum emphasis (headings)
    TEXT_PRIMARY     = "#fafafa"  # High emphasis (body)
    TEXT_SECONDARY   = "#d4d4d8"  # Medium emphasis (labels)
    TEXT_TERTIARY    = "#a1a1aa"  # Low emphasis (hints)
    TEXT_QUATERNARY  = "#71717a"  # Minimal emphasis (placeholders)
    TEXT_DISABLED    = "#52525b"  # Disabled state
    
    # ═══════════════════════════════════════════════════════════
    # SEMANTIC COLORS - CONTEXTUAL MEANING
    # ═══════════════════════════════════════════════════════════
    # Success (Financial totals, confirmations)
    SUCCESS          = "#10b981"  # Emerald 500
    SUCCESS_LIGHT    = "#34d399"  # Emerald 400
    SUCCESS_BG       = "rgba(16, 185, 129, 0.1)"
    
    # Danger (Destructive actions)
    DANGER           = "#ef4444"  # Red 500
    DANGER_LIGHT     = "#f87171"  # Red 400
    DANGER_BG        = "rgba(239, 68, 68, 0.1)"
    
    # Warning (Attention needed)
    WARNING          = "#f59e0b"  # Amber 500
    WARNING_LIGHT    = "#fbbf24"  # Amber 400
    WARNING_BG       = "rgba(245, 158, 11, 0.1)"
    
    # Info (Neutral information)
    INFO             = "#3b82f6"  # Blue 500
    INFO_LIGHT       = "#60a5fa"  # Blue 400
    INFO_BG          = "rgba(59, 130, 246, 0.1)"
    
    # ═══════════════════════════════════════════════════════════
    # SPECIAL EFFECTS & OVERLAYS
    # ═══════════════════════════════════════════════════════════
    SHADOW_SUBTLE    = "rgba(0, 0, 0, 0.4)"
    SHADOW_MEDIUM    = "rgba(0, 0, 0, 0.6)"
    SHADOW_STRONG    = "rgba(0, 0, 0, 0.8)"
    
    OVERLAY_DARK     = "rgba(0, 0, 0, 0.75)"  # Modal backdrop
    OVERLAY_LIGHT    = "rgba(255, 255, 255, 0.05)"  # Glass effect
    
    GLOW_ACCENT      = "rgba(99, 102, 241, 0.4)"  # Electric glow
    GLOW_SUCCESS     = "rgba(16, 185, 129, 0.3)"  # Success glow
    
    # ═══════════════════════════════════════════════════════════
    # TYPOGRAPHY SYSTEM
    # ═══════════════════════════════════════════════════════════
    FONT_FAMILY      = '"SF Pro Display", "Segoe UI", "Roboto", -apple-system, BlinkMacSystemFont, sans-serif'
    FONT_MONO        = '"SF Mono", "Consolas", "Monaco", monospace'
    
    # Type Scale (Perfect Fourth - 1.333 ratio)
    FONT_SIZE_XS     = "11px"
    FONT_SIZE_SM     = "12px"
    FONT_SIZE_BASE   = "14px"
    FONT_SIZE_MD     = "15px"
    FONT_SIZE_LG     = "16px"
    FONT_SIZE_XL     = "20px"
    FONT_SIZE_2XL    = "24px"
    FONT_SIZE_3XL    = "32px"
    
    # Font Weights
    FONT_WEIGHT_NORMAL   = "400"
    FONT_WEIGHT_MEDIUM   = "500"
    FONT_WEIGHT_SEMIBOLD = "600"
    FONT_WEIGHT_BOLD     = "700"
    FONT_WEIGHT_BLACK    = "800"
    
    # ═══════════════════════════════════════════════════════════
    # SPACING SCALE (8px Base Unit)
    # ═══════════════════════════════════════════════════════════
    SPACE_0          = "0px"
    SPACE_1          = "2px"   # 0.25 unit
    SPACE_2          = "4px"   # 0.5 unit
    SPACE_3          = "8px"   # 1 unit (base)
    SPACE_4          = "12px"  # 1.5 units
    SPACE_5          = "16px"  # 2 units
    SPACE_6          = "20px"  # 2.5 units
    SPACE_7          = "24px"  # 3 units
    SPACE_8          = "32px"  # 4 units
    SPACE_9          = "40px"  # 5 units
    SPACE_10         = "48px"  # 6 units
    
    # ═══════════════════════════════════════════════════════════
    # BORDER RADIUS SCALE
    # ═══════════════════════════════════════════════════════════
    RADIUS_NONE      = "0px"
    RADIUS_XS        = "2px"
    RADIUS_SM        = "4px"
    RADIUS_MD        = "6px"
    RADIUS_LG        = "8px"
    RADIUS_XL        = "10px"
    RADIUS_2XL       = "12px"
    RADIUS_3XL       = "16px"
    RADIUS_FULL      = "9999px"
    
    # ═══════════════════════════════════════════════════════════
    # TRANSITIONS & ANIMATIONS
    # ═══════════════════════════════════════════════════════════
    TRANSITION_FAST      = "100ms"
    TRANSITION_BASE      = "150ms"
    TRANSITION_SLOW      = "250ms"
    TRANSITION_SLOWER    = "350ms"
    
    EASE_IN          = "cubic-bezier(0.4, 0, 1, 1)"
    EASE_OUT         = "cubic-bezier(0, 0, 0.2, 1)"
    EASE_IN_OUT      = "cubic-bezier(0.4, 0, 0.2, 1)"