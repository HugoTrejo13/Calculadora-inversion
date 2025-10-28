"""
i18n.py
-------
Diccionarios de idioma para toda la app.
Esto reemplazará el diccionario LANGUAGES que estaba
dentro de funcion.py (archivo legacy).

Cada pantalla o componente debe pedir strings desde aquí,
no hardcodear textos.
"""

LANGUAGES = {
    "es": {
        "app_title": "Calculadora financiera para jóvenes",
        "tab_home": "Inicio",
        "tab_calc": "Calculadora",
        "tab_plan": "Plan de inversión",
        "tab_debt": "Deudas",
        "access": "Accesibilidad:",
        "font_minus": "A-",
        "font_plus": "A+",
        "daltonic": "Modo daltonismo",
        "language": "Idioma:",
    },
    "en": {
        "app_title": "Financial planner for students",
        "tab_home": "Home",
        "tab_calc": "Calculator",
        "tab_plan": "Investment plan",
        "tab_debt": "Debt",
        "access": "Accessibility:",
        "font_minus": "A-",
        "font_plus": "A+",
        "daltonic": "Color-blind mode",
        "language": "Language:",
    },
    "pt": {
        "app_title": "Planejador financeiro para jovens",
        "tab_home": "Início",
        "tab_calc": "Calculadora",
        "tab_plan": "Plano de investimento",
        "tab_debt": "Dívidas",
        "access": "Acessibilidade:",
        "font_minus": "A-",
        "font_plus": "A+",
        "daltonic": "Modo daltônico",
        "language": "Idioma:",
    },
}


__all__ = ["LANGUAGES"]
