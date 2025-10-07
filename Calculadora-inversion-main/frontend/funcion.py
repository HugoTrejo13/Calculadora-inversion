# -*- coding: utf-8 -*-

"""

GUI de la Calculadora Financiera (Tkinter + ttkbootstrap si está disponible)

- Inicio / Calculadora / Plan de inversión

- Accesibilidad: A-, A+, Modo daltonismo (alto contraste)

- Idiomas: Español / English / Português

- Scroll vertical en Plan de inversión

- Fricción e impuestos (básico): comisión depósito, compra/venta %, adm. anual %, IVA comisiones %, ISR ganancia %

- Resumen + Evolución anual (incluye columnas Comisiones e Impuestos)

"""



from __future__ import annotations

import math

import tkinter as tk

from tkinter import ttk, messagebox

from tkinter import font as tkfont

import locale

import sys
import ast

from dataclasses import dataclass, field

from functools import partial



# ===== Theme bootstrap (opcional) =====

BOOT = None

try:

    import ttkbootstrap as tb

    BOOT = tb

except Exception:

    BOOT = None





# ===== i18n =====

LANGUAGES = {

    "es": {
        "app_title": "Calculadora Financiera para jóvenes",
        "tab_home": "Inicio",
        "tab_calc": "Calculadora",
        "tab_plan": "Plan de inversión",
        "tab_debt": "Deudas",
        "access": "Accesibilidad:",
        "font_minus": "A-",
        "font_plus": "A+",
        "daltonic": "Modo daltonismo",
        "language": "Idioma:",
        "home_title": "Bienvenido a aprender a invertir",
        "home_sub": "Simula metas, entiende comisiones e impuestos y practica con la calculadora científica.",
        "home_start": "Comenzar plan de inversión",
        "home_calc": "Explorar calculadora",
        "hint": "Sugerencia: cambia el idioma y el tamaño de fuente desde la barra superior.",
        "params": "Parámetros de inversión",
        "initial_amount": "Monto inicial (MXN)",
        "monthly_contrib": "Aporte mensual (MXN)",
        "horizon_years": "Horizonte (años)",
        "annual_return": "Rendimiento anual (%)",
        "inflation": "Inflación anual (%)",
        "friction": "Fricción e impuestos (MX)",
        "deposit_fee": "Comisión por depósito (%)",
        "buy_sell": "Compra/Venta (%)",
        "mgmt": "Adm. anual (TER) (%)",
        "vat_comm": "IVA sobre comisiones (%)",
        "isr_gain": "ISR sobre ganancia (%)",
        "contrib_growth": "Crecimiento anual de aportes (%)",
        "custody_fixed": "Cuota fija de custodia (MXN/mes)",
        "market_spread": "Market spread de salida (%)",
        "summary": "Resumen",
        "nominal_value": "Valor final (nominal)",
        "total_contrib": "Aportes totales",
        "gain": "Ganancia generada",
        "real_value": "Valor ajustado por inflación",
        "need_monthly": "Se necesita un aporte mensual positivo para proyectar la inversión.",
        "copy": "Copiar resumen",
        "evolution": "Evolución anual",
        "years": "Años",
        "final_balance": "Saldo total final",
        "cum_contrib": "Aporte acumulado",
        "gain_col": "Ganancia",
        "real_col": "Valor real",
        "fees_col": "Comisiones",
        "taxes_col": "Impuestos",
        "profile_title": "Instrumento y país",
        "instrument": "Instrumento",
        "country": "País fiscal",
        "w8ben": "Usa W‑8BEN",
        "div_yield": "Dividendo (yield) anual (%)",
        "div_policy": "Dividendo: reinvertir o retirar",
        "div_reinvest": "Reinvertir",
        "div_withdraw": "Retirar",
        "instrument_mx_stock": "Acciones / ETFs MX",
        "instrument_mx_debt": "Deuda MX (CETES/bonos)",
        "instrument_usa_stock": "Acciones / ETFs USA",
        "instrument_fund": "Fondo de inversión",
        "country_mx": "México",
        "country_usa": "Extranjero / USA",
        "flow_title": "Calendario de aportes",
        "frequency": "Frecuencia",
        "freq_monthly": "Mensual",
        "freq_biweekly": "Quincenal",
        "freq_annual": "Anual",
        "timing": "Momento del aporte",
        "timing_begin": "Inicio de periodo",
        "timing_end": "Fin de periodo",
        "extra_months": "Meses con aporte extra (ej. 6,12)",
        "extra_amount": "Monto extra (MXN)",
        "skip_months": "Meses sin aportar (ej. 7,8)",
        "buy_fee": "Comisión de compra (%)",
        "sell_fee": "Comisión de venta (%)",
        "entry_spread": "Spread de entrada (%)",
        "exit_spread": "Spread de salida (%)",
        "platform_fixed": "Cuota plataforma (MXN/mes)",
        "risk_title": "Riesgo y escenarios",
        "vol_annual": "Volatilidad anual (%)",
        "mc_runs": "Corridas Monte Carlo",
        "p5": "P5 final",
        "p50": "P50 final",
        "p95": "P95 final",
        "faq_title": "Preguntas frecuentes",
        "faq_q1": "¿Pago IVA por invertir?",
        "faq_a1": "No. El IVA aplica a bienes y servicios; en inversiones se paga ISR sobre la ganancia.",
        "faq_q2": "¿Cuándo se paga ISR en acciones MX?",
        "faq_a2": "Al vender con ganancia; la casa de bolsa retiene 10% sobre la utilidad (definitivo).",
        "faq_q3": "¿Y en CETES/bonos?",
        "faq_a3": "Hay retención sobre intereses conforme a tasas del SAT, descontada a lo largo del tiempo.",
        "debt_params": "Parámetros del crédito",
        "debt_field_title": "Título",
        "debt_field_cost": "Costo del producto (MXN)",
        "debt_field_down": "Enganche (MXN)",
        "debt_field_cat": "CAT anual (%)",
        "debt_field_open_pct": "Comisión apertura (%)",
        "debt_field_insurance": "Seguro mensual (MXN)",
        "debt_field_term": "Plazo (meses)",
        "debt_field_extra_months": "Meses con pago extra (ej. 6,12)",
        "debt_field_extra_amount": "Monto extra (MXN)",
        "debt_field_skip_months": "Meses sin pagar (ej. 7,8)",
        "debt_field_inflation": "Inflación anual (%)",
        "debt_calc": "Calcular",
        "debt_table": "Amortización",
        "debt_col_month": "Mes",
        "debt_col_payment": "Pago",
        "debt_col_interest": "Interés",
        "debt_col_principal": "Capital",
        "debt_col_fees": "Seguro/comisiones",
        "debt_col_balance": "Saldo",
        "debt_col_interest_acc": "Intereses acumulados",
        "debt_col_real": "Real (deflactado)",
        "debt_summary": "Resumen",
        "debt_summary_total": "Total pagado",
        "debt_summary_interest": "Intereses totales",
        "debt_summary_real": "Costo real (hoy)",
        "debt_summary_time": "Tiempo (meses/años)",
        "debt_default_title": "Crédito",
        "debt_invalid_amount": "Necesitas que el monto financiado sea positivo.",
        "faq_q4": "\u00bfQu\u00e9 es el inter\u00e9s compuesto?",
        "faq_a4": "Es \"inter\u00e9s sobre el inter\u00e9s\": los rendimientos se reinvierten y tambi\u00e9n generan rendimiento. Empezar joven multiplica el resultado.",
        "faq_q5": "\u00bfCu\u00e1l es la diferencia entre valor nominal y valor real?",
        "faq_a5": "El valor nominal no descuenta inflaci\u00f3n; el valor real se deflacta con INPC para mostrar poder de compra.",
        "faq_q6": "\u00bfQu\u00e9 comisiones contempla la app?",
        "faq_a6": "Dep\u00f3sito, compra/venta (con IVA), administraci\u00f3n/TER, spreads y cuotas fijas (plataforma/custodia).",
        "faq_q7": "\u00bfQu\u00e9 es el TER o administraci\u00f3n anual?",
        "faq_a7": "Costo porcentual del producto/asesor\u00eda prorrateado al mes; reduce el saldo antes del rendimiento.",
        "faq_q8": "\u00bfQu\u00e9 es el spread?",
        "faq_a8": "Diferencia entre precio de compra y venta; es un costo impl\u00edcito al entrar/salir.",
        "faq_q9": "\u00bfQu\u00e9 significa \"crecimiento anual de aportes\"?",
        "faq_a9": "Porcentaje con el que subir\u00e1n tus dep\u00f3sitos cada a\u00f1o.",
        "faq_q10": "\u00bfQu\u00e9 pasa si indico meses sin aportar?",
        "faq_a10": "La simulaci\u00f3n omite el dep\u00f3sito en esos meses; ver\u00e1s menor saldo final.",
        "faq_q11": "\u00bfC\u00f3mo se tratan los dividendos?",
        "faq_a11": "Puedes reinvertir o retirar. Para USA hay retenci\u00f3n a dividendos (30% o menor con W-8BEN). En acciones MX la app aplica ISR 10% sobre ganancia al vender.",
        "faq_q12": "\u00bfQu\u00e9 es el CAT en deudas?",
        "faq_a12": "El Costo Anual Total integra intereses, comisiones y seguros; sirve para comparar cr\u00e9ditos.",
        "faq_q13": "\u00bfEs asesor\u00eda financiera?",
        "faq_a13": "No. Es una herramienta educativa para explorar escenarios y conceptos clave.",
    },
    "en": {


        "app_title": "Finance Calculator for youth",

        "tab_home": "Home",

        "tab_calc": "Calculator",

        "tab_plan": "Investment plan",
        "tab_debt": "Debts",

        "access": "Accessibility:",

        "font_minus": "A-",

        "font_plus": "A+",

        "daltonic": "Color-blind mode",

        "language": "Language:",

        "home_title": "Welcome to learn investing",

        "home_sub": "Simulate goals, understand fees and taxes, and practice with the scientific calculator.",

        "home_start": "Start investment plan",

        "home_calc": "Open calculator",

        "hint": "Tip: change language and font size from the top bar.",

        "params": "Investment parameters",

        "initial_amount": "Initial amount",

        "monthly_contrib": "Monthly contribution",

        "horizon_years": "Horizon (years)",

        "annual_return": "Annual return (%)",

        "inflation": "Inflation (%)",

        "friction": "Friction & taxes",

        "deposit_fee": "Deposit fee (%)",

        "buy_sell": "Buy/Sell (%)",

        "mgmt": "Mgmt. fee (%)",

        "vat_comm": "VAT on fees (%)",

        "isr_gain": "Income tax on gain (%)",

        "contrib_growth": "Contribution growth (%)",

        "custody_fixed": "Custody flat fee (MXN/mo)",

        "market_spread": "Exit market spread (%)",

        "summary": "Summary",

        "nominal_value": "Final value (nominal)",

        "total_contrib": "Total contributions",

        "gain": "Generated gain",

        "real_value": "Real value (inflation-adjusted)",

        "need_monthly": "A positive monthly contribution is required.",

        "copy": "Copy summary",

        "evolution": "Yearly evolution",

        "years": "Years",

        "final_balance": "Final balance",

        "cum_contrib": "Cum. contribution",

        "gain_col": "Gain",

        "real_col": "Real value",

        "fees_col": "Fees",

        "taxes_col": "Taxes",
        "vol_annual": "Annual volatility (%)",
        "mc_runs": "Monte Carlo runs",
        "p5": "P5 final",
        "p50": "P50 final",
        "p95": "P95 final",
        "faq_title": "Frequently Asked Questions",
        "faq_q1": "Do I pay VAT when investing?",
        "faq_a1": "No. VAT applies to goods/services; investments are taxed on gains (income tax).",
        "faq_q2": "When is tax paid on Mexican equities?",
        "faq_a2": "Upon selling at a profit; typical withholding 10% (final).",
        "faq_q3": "What about CETES/bonds?",
        "faq_a3": "Withholding over interest according to SAT rates, discounted over time.",
        "debt_params": "Credit parameters",
        "debt_field_title": "Title",
        "debt_field_cost": "Product cost (MXN)",
        "debt_field_down": "Down payment (MXN)",
        "debt_field_cat": "CAT annual (%)",
        "debt_field_open_pct": "Opening fee (%)",
        "debt_field_insurance": "Monthly insurance (MXN)",
        "debt_field_term": "Term (months)",
        "debt_field_extra_months": "Months with extra payment (e.g. 6,12)",
        "debt_field_extra_amount": "Extra amount (MXN)",
        "debt_field_skip_months": "Skip months (e.g. 7,8)",
        "debt_field_inflation": "Annual inflation (%)",
        "debt_calc": "Calculate",
        "debt_table": "Amortization",
        "debt_col_month": "Month",
        "debt_col_payment": "Payment",
        "debt_col_interest": "Interest",
        "debt_col_principal": "Principal",
        "debt_col_fees": "Insurance/fees",
        "debt_col_balance": "Balance",
        "debt_col_interest_acc": "Interest accrued",
        "debt_col_real": "Real (deflated)",
        "debt_summary": "Summary",
        "debt_summary_total": "Total paid",
        "debt_summary_interest": "Total interest",
        "debt_summary_real": "Real cost (today)",
        "debt_summary_time": "Time (months/years)",
        "debt_default_title": "Loan",
        "debt_invalid_amount": "Financed amount must be positive.",

    },

    "pt": {


        "app_title": "Calculadora Financeira para jovens",

        "tab_home": "Início",

        "tab_calc": "Calculadora",

        "tab_plan": "Plano de investimento",
        "tab_debt": "Dívidas",

        "access": "Acessibilidade:",

        "font_minus": "A-",

        "font_plus": "A+",

        "daltonic": "Modo daltônico",

        "language": "Idioma:",

        "home_title": "Bem-vindo para aprender a investir",

        "home_sub": "Simule metas, entenda taxas e impostos e pratique com a calculadora científica.",

        "home_start": "Começar plano de investimento",

        "home_calc": "Abrir calculadora",

        "hint": "Dica: altere idioma e fonte na barra superior.",

        "params": "Parâmetros de investimento",

        "initial_amount": "Montante inicial",

        "monthly_contrib": "Aporte mensal",

        "horizon_years": "Horizonte (anos)",

        "annual_return": "Retorno anual (%)",

        "inflation": "Inflação anual (%)",

        "friction": "Atrito e impostos",

        "deposit_fee": "Taxa de depósito (%)",

        "buy_sell": "Compra/Venda (%)",

        "mgmt": "Adm. anual (TER) (%)",

        "vat_comm": "IVA sobre taxas (%)",

        "isr_gain": "IR sobre ganho (%)",

        "contrib_growth": "Crescimento do aporte (%)",

        "custody_fixed": "Custódia fixa (MXN/mês)",

        "market_spread": "Spread de saída (%)",

        "summary": "Resumo",

        "nominal_value": "Valor final (nominal)",

        "total_contrib": "Aportes totais",

        "gain": "Ganho gerado",

        "real_value": "Valor real (ajustado)",

        "need_monthly": "É necessário aporte mensal positivo.",

        "copy": "Copiar resumo",

        "evolution": "Evolução anual",

        "years": "Anos",

        "final_balance": "Saldo final",

        "cum_contrib": "Aporte acumulado",

        "gain_col": "Ganho",

        "real_col": "Valor real",

        "fees_col": "Comissões",

        "taxes_col": "Impostos",



        "profile_title": "Instrumento e país",

        "instrument": "Instrumento",

        "country": "País fiscal",

        "w8ben": "Usar W‑8BEN",

        "div_yield": "Dividendos (yield) anual (%)",

        "div_policy": "Dividendos: reinvestir ou sacar",

        "div_reinvest": "Reinvestir",

        "div_withdraw": "Sacar",

        "instrument_mx_stock": "Ações/ETFs MX",

        "instrument_mx_debt": "Dívida MX (CETES/títulos)",

        "instrument_usa_stock": "Ações/ETFs USA",

        "instrument_fund": "Fundo de investimento",

        "country_mx": "México",

        "country_usa": "Exterior / USA",



        "flow_title": "Calendário de aportes",

        "frequency": "Frequência",

        "freq_monthly": "Mensal",

        "freq_biweekly": "Quinzenal",

        "freq_annual": "Anual",

        "timing": "Momento do aporte",

        "timing_begin": "Início do período",

        "timing_end": "Fim do período",

        "extra_months": "Meses com extra (ex. 6,12)",

        "extra_amount": "Valor extra (MXN)",

        "skip_months": "Meses sem aporte (ex. 7,8)",



        "buy_fee": "Taxa de compra (%)",

        "sell_fee": "Taxa de venda (%)",

        "entry_spread": "Spread de entrada (%)",

        "exit_spread": "Spread de saída (%)",

        "platform_fixed": "Tarifa plataforma (MXN/mês)",



        "risk_title": "Risco e cenários",

        "vol_annual": "Volatilidade anual (%)",

        "mc_runs": "Simulações Monte Carlo",

        "p5": "P5 final",

        "p50": "P50 final",

        "p95": "P95 final",



        "faq_title": "Perguntas frequentes",

        "faq_q1": "Pago IVA ao investir?",

        "faq_a1": "Não. IVA é para bens/serviços; investimentos pagam IR sobre o lucro.",

        "faq_q2": "Quando pago IR em ações MX?",

        "faq_a2": "Ao vender com lucro; retenção típica de 10% (definitivo).",

        "faq_q3": "E em CETES/títulos?",

        "faq_a3": "Há retenção sobre juros conforme taxa do fisco, descontada ao longo do tempo.",
        "debt_params": "Parâmetros do crédito",
        "debt_field_title": "Título",
        "debt_field_cost": "Custo do produto (MXN)",
        "debt_field_down": "Entrada (MXN)",
        "debt_field_cat": "CAT anual (%)",
        "debt_field_open_pct": "Taxa de abertura (%)",
        "debt_field_insurance": "Seguro mensal (MXN)",
        "debt_field_term": "Prazo (meses)",
        "debt_field_extra_months": "Meses com pagamento extra (ex. 6,12)",
        "debt_field_extra_amount": "Valor extra (MXN)",
        "debt_field_skip_months": "Meses sem pagar (ex. 7,8)",
        "debt_field_inflation": "Inflação anual (%)",
        "debt_calc": "Calcular",
        "debt_table": "Amortização",
        "debt_col_month": "Mês",
        "debt_col_payment": "Pagamento",
        "debt_col_interest": "Juros",
        "debt_col_principal": "Principal",
        "debt_col_fees": "Seguro/taxas",
        "debt_col_balance": "Saldo",
        "debt_col_interest_acc": "Juros acumulados",
        "debt_col_real": "Real (deflacionado)",
        "debt_summary": "Resumo",
        "debt_summary_total": "Total pago",
        "debt_summary_interest": "Juros totais",
        "debt_summary_real": "Custo real (hoje)",
        "debt_summary_time": "Tempo (meses/anos)",
        "debt_default_title": "Crédito",
        "debt_invalid_amount": "O valor financiado deve ser positivo.",
    },

}



HELP_TEXTS = {

    "es": {

        "initial_amount": (

            "Capital inicial",

            "• Monto con el que comienzas.\n"

            "• Se invierte desde el mes 1.\n"

            "Ej.: Si pones 5,000 MXN y aportas 1,000/mes, el primer mes parte de 6,000 (menos comisiones de deposito)."

        ),

        "monthly_contrib": (

            "Aporte mensual",

            "• Dinero que agregas cada mes antes de comisiones.\n"

            "• Si activas 'Crecimiento anual de aportes', este monto sube mes a mes."

        ),

        "horizon_years": (

            "Horizonte (años)",

            "• Tiempo total de la inversion.\n"

            "• Al final se simula una venta unica (compra/venta + spread)."

        ),

        "annual_return": (

            "Rendimiento anual nominal (%)",

            "• Tasa esperada antes de inflacion.\n"

            "• Se capitaliza mensual: r_m = (1+r)^(1/12)-1."

        ),

        "inflation": (

            "Inflacion anual (%)",

            "• Sirve para calcular 'Valor real'.\n"

            "• No modifica depositos ni impuestos."

        ),

        "deposit_fee": (

            "Comision por deposito (%)",

            "• Porcentaje descontado a cada aporte mensual.\n"

            "• El IVA se muestra en 'Comisiones', pero no aumenta el saldo."

        ),

        "buy_sell": (

            "Comision de compra/venta (%)",

            "• Se aplica una sola vez al final del horizonte al liquidar.\n"

            "• El IVA se muestra en 'Comisiones'."

        ),

        "mgmt": (

            "Administracion anual (%)",

            "• Cobro del administrador, prorrateado mensual.\n"

            "• El fee reduce el saldo; el IVA solo se reporta en 'Comisiones'."

        ),

        "vat_comm": (

            "IVA sobre comisiones (%)",

            "• Impuesto a las comisiones cobradas (deposito, administracion, custodia).\n"

            "• No aumenta el saldo; solo se refleja como costo."

        ),

        "isr_gain": (

            "ISR sobre ganancia (%)",

            "• Impuesto anual sobre la ganancia positiva del año.\n"

            "• Si el año cierra en perdida, no se cobra ISR ese año."

        ),

        "contrib_growth": (

            "Crecimiento anual de aportes (%)",

            "• Aumenta el aporte cada mes segun una tasa anual.\n"

            "• Ej.: 6% anual ≈ 0.486% mensual."

        ),

        "custody_fixed": (

            "Cuota fija de custodia (MXN/mes)",

            "• Cargo mensual fijo; reduce el saldo.\n"

            "• El IVA de esta cuota se reporta como 'Comisiones'."

        ),

        "market_spread": (

            "Market spread de salida (%)",

            "• Perdida por diferencia bid/ask y deslizamiento al vender.\n"

            "• Se aplica una sola vez al final (ademas de compra/venta)."

        ),

        "div_yield": (
            "Dividendo anual (%)",
            "Porcentaje de dividendos que entrega el instrumento; reinvierte o retira (retención MX/USA automática)."
        ),
        "buy_fee": (
            "Comisión de compra (%)",
            "Porcentaje por transacción de compra; suele causar IVA reportado en Comisiones."
        ),
        "sell_fee": (
            "Comisión de venta (%)",
            "Porcentaje por transacción de venta al final; suele causar IVA."
        ),
        "entry_spread": (
            "Spread de entrada (%)",
            "Diferencia implícita al comprar (precio/ejecución)."
        ),
        "exit_spread": (
            "Spread de salida (%)",
            "Diferencia implícita al vender; se aplica al final."
        ),
        "platform_fixed": (
            "Cuota plataforma (MXN/mes)",
            "Tarifa fija por uso de la app/plataforma; se descuenta mes a mes."
        ),
        "frequency": (
            "Frecuencia de aportes",
            "Define cada cuánto aportas: mensual, quincenal o anual."
        ),
        "timing": (
            "Momento del aporte",
            "Inicio del periodo (antes del rendimiento) o al final del periodo."
        ),
        "extra_months": (
            "Meses con aporte extra",
            "Lista separada por comas con los meses (1..12) en los que harás un depósito adicional. Ej.: 6,12."
        ),
        "extra_amount": (
            "Monto extra (MXN)",
            "Cantidad que se depositará en los meses listados en 'Meses con aporte extra'."
        ),
        "skip_months": (
            "Meses sin aportar",
            "Lista separada por comas con los meses (1..12) en los que no habrá depósito. Ej.: 7,8."
        ),
        "instrument": (
            "Instrumento",
            "Tipo general del activo para aplicar reglas fiscales típicas (MX acciones/ETFs, deuda, USA, fondos)."
        ),
        "country": (
            "País fiscal",
            "Determina si hay retención local (MX) o si declaras por tu cuenta (USA/Extranjero)."
        ),
        "w8ben": (
            "Usa W‑8BEN",
            "Aplica a instrumentos USA para reducción de retención sobre dividendos."
        ),
        "div_policy": (
            "Dividendo: reinvertir o retirar",
            "Reinvertir suma el dividendo neto al saldo; retirar lo excluye del saldo (solo educativo)."
        ),
        "debt_cat": (
            "CAT anual (%)",
            "Costo Anual Total del crédito. Se transforma a tasa por periodo (mensual/quincenal)."
        ),
        "debt_msi": (
            "Meses sin intereses",
            "Promoción a 0% durante los primeros N meses (si N = plazo total, todo el crédito es sin intereses)."
        ),
        "debt_open_pct": (
            "Comisión de apertura (%)",
            "Porcentaje sobre el costo del producto. Se suma una sola vez (con IVA si aplica)."
        ),
        "debt_open_fix": (
            "Comisión de apertura fija (MXN)",
            "Cuota fija inicial. También sujeta a IVA si corresponde."
        ),
        "debt_month_fee": (
            "Comisiones fijas mensuales (MXN)",
            "Cargo mensual de la institución (se suma con IVA)."
        ),
        "debt_ins": (
            "Seguro mensual (MXN)",
            "Seguro de vida/daños. Se suma cada periodo (con IVA si aplica)."
        ),
        "debt_vat": (
            "IVA sobre comisiones (%)",
            "Impuesto aplicado a comisiones/seguros. No reduce saldo; es costo."
        ),
        "debt_infl": (
            "Inflación anual (%)",
            "Para calcular el valor real (devaluado) del saldo al cierre de cada año."
        ),
        "debt_insurance": (
            "Seguro mensual (MXN)",
            "Cuota mensual del seguro asociado al crédito. Se suma como costo fijo cada mes."
        ),
        "debt_extra_months": (
            "Pagos extra",
            "Meses (1,2,3...) separados por comas en los que aportarás un pago adicional para reducir capital."
        ),
        "debt_extra_amount": (
            "Monto extra (MXN)",
            "Importe del pago adicional aplicado en los meses indicados; reduce el saldo inmediatamente."
        ),
        "debt_skip_months": (
            "Meses sin pagar",
            "Meses (1,2,3...) separados por comas en los que solo se cubre interés y seguros; el capital no baja."
        ),
    },

    "en": {

        "initial_amount": (

            "Initial capital",

            "• Money you start with (invested from month 1).\n"

            "• Example: 5,000 + 1,000/month → first month bases on 6,000 minus deposit fees."

        ),



        "monthly_contrib": (

            "Monthly contribution",

            "• Amount added each month before fees.\n"

            "• If 'Contribution growth' is set, this increases monthly."

        ),

        "horizon_years": (

            "Horizon (years)",

            "• Total investment time.\n"

            "• A single exit (fees + spread) is simulated at the end."

        ),

        "annual_return": (

            "Nominal annual return (%)",

            "• Expected return before inflation.\n"

            "• Compounded monthly: r_m = (1+r)^(1/12)-1."

        ),

        "inflation": (

            "Annual inflation (%)",

            "• Used to compute 'Real value'.\n"

            "• Does not change deposits or taxes."

        ),

        "deposit_fee": (

            "Deposit fee (%)",

            "• Percentage charged on each monthly deposit.\n"

            "• VAT is shown under 'Fees'."

        ),

        "buy_sell": (

            "Buy/Sell fee (%)",

            "• Applied once at the end upon liquidation.\n"

            "• VAT shown under 'Fees'."

        ),

        "mgmt": (

            "Management fee (%)",

            "• Charged monthly from the balance.\n"

            "• VAT reported as fee."

        ),

        "vat_comm": (

            "VAT on fees (%)",

            "• Tax on fees (deposit, management, custody).\n"

            "• Does not increase balance; shown as cost."

        ),

        "isr_gain": (

            "Tax on gains (%)",

            "• Annual tax on positive yearly gains only."

        ),

        "contrib_growth": (

            "Contribution growth (%)",

            "• Increases monthly deposit according to annual rate.\n"

            "• Example: 6%/yr ≈ 0.486%/mo."

        ),

        "custody_fixed": (

            "Custody flat fee (MXN/mo)",

            "• Fixed monthly fee; reduces balance.\n"

            "• VAT reported as fee."

        ),

        "market_spread": (

            "Exit market spread (%)",

            "• Loss from bid/ask and slippage when selling at the end."

        ),

        "debt_cat": (

            "CAT annual (%)",

            "Total annual cost of the loan. Converted to an effective monthly rate for the simulation."

        ),

        "debt_open_pct": (

            "Opening fee (%)",

            "Percentage charged once at the beginning. Added to the first month as part of fees."

        ),

        "debt_insurance": (

            "Monthly insurance (MXN)",

            "Insurance premium charged every month; it is added to the cost of each instalment."

        ),

        "debt_extra_months": (

            "Extra payments",

            "Comma-separated months (1,2,3...) where an additional payment is applied to reduce principal."

        ),

        "debt_extra_amount": (

            "Extra amount (MXN)",

            "Amount of the additional payment that is subtracted from the outstanding balance on those months."

        ),

        "debt_skip_months": (

            "Skip months",

            "Months (1,2,3...) where only interest and insurance are paid; the principal balance stays the same."

        ),

    },

    "pt": {

        "initial_amount": (

            "Capital inicial",

            "• Dinheiro com que voce comeca (investido desde o 1° mes).\n"

            "• Ex.: 5.000 + 1.000/mês → base de 6.000 menos taxas de deposito."

        ),

        "monthly_contrib": (

            "Aporte mensal",

            "• Valor adicionado todo mes antes de taxas.\n"

            "• Com 'Crescimento do aporte', aumenta mensalmente."

        ),

        "horizon_years": (

            "Horizonte (anos)",

            "• Tempo total da aplicacao.\n"

            "• Saida unica no final (taxas + spread)."

        ),

        "annual_return": (

            "Retorno anual nominal (%)",

            "• Antes da inflacao; capitalizado mensalmente."

        ),

        "inflation": (

            "Inflacao anual (%)",

            "• Usada para 'Valor real'."

        ),

        "deposit_fee": (

            "Taxa de deposito (%)",

            "• Percentual cobrado em cada aporte mensal."

        ),

        "buy_sell": (

            "Taxa de compra/venda (%)",

            "• Aplicada uma vez no final."

        ),

        "mgmt": (

            "Administracao anual (%)",

            "• Cobrança mensal sobre o saldo; IVA reportado em 'Taxas'."

        ),

        "vat_comm": (

            "IVA sobre taxas (%)",

            "• Imposto sobre taxas (deposito, administracao, custodia)."

        ),

        "isr_gain": (

            "Imposto sobre ganho (%)",

            "• Cobrado somente se o ano fechar com ganho positivo."

        ),

        "contrib_growth": (

            "Crescimento do aporte (%)",

            "• Aumenta o aporte mensal conforme taxa anual."

        ),

        "custody_fixed": (

            "Custodia fixa (MXN/mês)",

            "• Tarifa mensal fixa; reduz o saldo."

        ),

        "market_spread": (

            "Spread de saida (%)",

            "• Perda por bid/ask e slippage na venda final."

        ),

        "debt_cat": (

            "CAT anual (%)",

            "Custo anual total do credito. Convertido em taxa mensal para a simulacao."

        ),

        "debt_open_pct": (

            "Taxa de abertura (%)",

            "Percentual cobrado uma unica vez no inicio; somado ao primeiro mes como taxa."

        ),

        "debt_insurance": (

            "Seguro mensal (MXN)",

            "Premio de seguro cobrado todo mes; adicionado como custo fixo em cada parcela."

        ),

        "debt_extra_months": (

            "Pagamentos extra",

            "Meses (1,2,3...) separados por virgulas em que sera feito um pagamento adicional para reduzir o principal."

        ),

        "debt_extra_amount": (

            "Valor extra (MXN)",

            "Valor do pagamento adicional aplicado nos meses escolhidos; reduz o saldo imediatamente."

        ),

        "debt_skip_months": (

            "Meses sem pagar",

            "Meses (1,2,3...) em que apenas juros e seguro sao pagos; o saldo nao diminui."

        ),

    },

}



class Tooltip:

    """Lightweight tooltip that adapts to ttkbootstrap when available."""



    def __init__(self, widget, text, delay=350):

        self.widget = widget

        self.text = text

        self.delay = delay

        self._id = None

        self._tip = None

        widget.bind("<Enter>", self._schedule, add="+")

        widget.bind("<Leave>", self._hide, add="+")

        widget.bind("<ButtonPress>", self._hide, add="+")



    def _schedule(self, _event=None):

        if self._id:

            self.widget.after_cancel(self._id)

        self._id = self.widget.after(self.delay, self._show)



    def _show(self):

        if self._tip or not self.text:

            return

        bbox = None

        try:

            bbox = self.widget.bbox("insert")

        except Exception:

            bbox = None

        x_offset = bbox[0] if bbox else 0

        y_offset = bbox[1] if bbox else 0

        x = self.widget.winfo_rootx() + x_offset + 20

        y = self.widget.winfo_rooty() + y_offset + 24

        self._tip = tw = tk.Toplevel(self.widget)

        tw.wm_overrideredirect(True)

        tw.wm_geometry(f"+{x}+{y}")

        frame_cls = BOOT.Frame if BOOT else ttk.Frame

        label_cls = BOOT.Label if BOOT else ttk.Label

        frame_kwargs = {"padding": 6, "relief": "solid", "borderwidth": 1}

        label_kwargs = {"text": self.text, "justify": "left", "wraplength": 380}

        if BOOT:

            frame_kwargs["bootstyle"] = "secondary"

            label_kwargs["bootstyle"] = "secondary"

        frm = frame_cls(tw, **frame_kwargs)

        frm.pack()

        label_cls(frm, **label_kwargs).pack()



    def _hide(self, _event=None):

        if self._id:

            self.widget.after_cancel(self._id)

            self._id = None

        if self._tip:

            self._tip.destroy()

            self._tip = None











def fmt_currency(value: float, symbol: str = "MX$") -> str:

    try:

        # Intento con configuración local del usuario

        return f"{symbol} {value:,.2f}"

    except Exception:

        return f"{symbol} {value:.2f}"





@dataclass

class Inputs:

    initial: float = 0.0

    monthly: float = 0.0

    years: int = 1

    annual_return: float = 10.0     # %

    inflation: float = 4.0          # %

    # Fricción e impuestos

    fee_deposit: float = 0.0        # %

    buy_sell: float = 0.0           # %

    mgmt: float = 0.0               # %

    vat_on_fees: float = 16.0       # %

    tax_gain: float = 10.0          # %

    contrib_growth: float = 0.0     # % anual

    custody_fixed: float = 0.0      # MXN/mes

    market_spread: float = 0.0      # % aplicado al final



    # Perfil fiscal / instrumento

    instrument: str = "mx_stock"      # mx_stock | mx_debt | usa_stock | fund

    country: str = "mx"               # mx | usa

    w8ben: bool = True

    div_yield: float = 0.0            # % anual

    div_policy: str = "reinvest"      # reinvest | withdraw

    # Calendario de aportes

    frequency: str = "monthly"        # monthly | biweekly | annual

    timing: str = "begin"             # begin | end

    extra_months: str = ""            # "6,12"

    extra_amount: float = 0.0

    skip_months: str = ""             # "7,8"

    # Costos avanzados

    buy_fee: float = 0.0              # %

    sell_fee: float = 0.0             # %

    entry_spread: float = 0.0         # %

    exit_spread: float = 0.0          # %

    platform_fixed: float = 0.0       # MXN/mes

    # Riesgo

    vol_annual: float = 0.0           # %

    mc_runs: int = 0                  # 0 = sin MC





@dataclass

class YearRow:

    year: int

    final_balance: float

    cum_contrib: float

    gain: float

    real_value: float

    fees: float

    taxes: float



@dataclass
class DebtInputs:

    title: str
    cost: float
    down_payment: float
    cat_annual: float
    open_pct: float
    insurance_monthly: float
    term_months: int
    extra_months: set[int]
    extra_amount: float
    skip_months: set[int]
    inflation_annual: float





class App(tk.Tk):

    def __init__(self):

        # ===== Root & style =====

        if BOOT:

            super().__init__()

            self.style = BOOT.Style("flatly")

        else:

            super().__init__()

            self.style = ttk.Style(self)



        self.lang = "es"

        self.strings = LANGUAGES[self.lang]



        self.title(self.strings["app_title"])

        self.geometry("1200x720")

        self.minsize(980, 600)



        # ===== Accesibilidad (estado) =====

        self.base_font_size = tkfont.nametofont("TkDefaultFont").cget("size")

        self.cb_var = tk.BooleanVar(value=False)



        # ===== Top bar =====

        self._build_topbar()



        # ===== Notebook con tabs =====

        self.nb = ttk.Notebook(self)

        self.nb.pack(fill="both", expand=True)



        self.home_tab = ttk.Frame(self.nb)

        self.calc_tab = ttk.Frame(self.nb)

        self.plan_tab = ttk.Frame(self.nb)



        self.nb.add(self.home_tab, text=self.strings["tab_home"])

        self.nb.add(self.calc_tab, text=self.strings["tab_calc"])

        self.nb.add(self.plan_tab, text=self.strings["tab_plan"])



        # ===== Contenidos =====

        self.home_image_path = ""  # Ruta opcional para imagen de portada (ej.: assets/portada.png)
        self.debt_title = tk.StringVar(value=self.strings.get("debt_default_title", "Crédito"))
        self.debt_cost = tk.StringVar(value="0")
        self.debt_down = tk.StringVar(value="0")
        self.debt_cat = tk.StringVar(value="20.0")
        self.debt_open_pct = tk.StringVar(value="0.0")
        self.debt_insurance = tk.StringVar(value="0.0")
        self.debt_term = tk.StringVar(value="12")
        self.debt_extra_months = tk.StringVar(value="")
        self.debt_extra_amount = tk.StringVar(value="0")
        self.debt_skip_months = tk.StringVar(value="")
        self.debt_inflation = tk.StringVar(value="4.0")
        self._build_home()
        self._build_calc()
        self._build_plan()
        self.debt_tab = ttk.Frame(self.nb)
        self.nb.add(self.debt_tab, text="Deudas")
        self._build_debt()



        self._apply_font_size()



    def set_home_image(self, path: str):

        self.home_image_path = path
        container = getattr(self, "_home_container", None)
        if not container:
            return

        if getattr(self, "_home_img_label", None):
            try:
                self._home_img_label.destroy()
            except Exception:
                pass
            self._home_img_label = None

        try:
            from PIL import Image, ImageTk
            if self.home_image_path:
                im = Image.open(self.home_image_path).resize((720, 180))
                self._home_img = ImageTk.PhotoImage(im)
                self._home_img_label = ttk.Label(container, image=self._home_img)
                self._home_img_label.pack(pady=(12, 6))
        except Exception:
            pass



    # ---------- UI Building ----------



    def _build_topbar(self):

        top = ttk.Frame(self)

        top.pack(fill="x", padx=8, pady=6)



        # Accesibilidad

        ttk.Label(top, text=self.strings["access"]).pack(side="left", padx=(0, 6))

        ttk.Button(top, text=self.strings["font_minus"], command=self._font_minus, width=4).pack(side="left")

        ttk.Button(top, text=self.strings["font_plus"], command=self._font_plus, width=4).pack(side="left", padx=(6, 12))

        ttk.Label(top, text="|").pack(side="left", padx=(8, 8))



        chk = ttk.Checkbutton(

            top, text=self.strings["daltonic"],

            variable=self.cb_var, command=self._toggle_contrast

        )

        chk.pack(side="left")



        # Idioma

        ttk.Label(top, text=self.strings["language"]).pack(side="left", padx=(18, 6))

        self.lang_cmb = ttk.Combobox(top,
            values=["Español", "English", "Português"],
            width=16, state="readonly")

        self.lang_cmb.current(0)

        self.lang_cmb.bind("<<ComboboxSelected>>", self._on_change_lang)

        self.lang_cmb.pack(side="left")



    def _build_home(self):

        c = ttk.Frame(self.home_tab)

        c.pack(expand=True)
        self._home_container = c
        self._home_img_label = None

        try:
            from PIL import Image, ImageTk
            if getattr(self, "home_image_path", None):
                im = Image.open(self.home_image_path).resize((720, 180))
                self._home_img = ImageTk.PhotoImage(im)
                self._home_img_label = ttk.Label(c, image=self._home_img)
                self._home_img_label.pack(pady=(12, 6))
        except Exception:
            pass

        ttk.Label(c, text=self.strings["home_title"], font=("TkDefaultFont", self.base_font_size + 6, "bold")).pack(pady=(60, 10))

        ttk.Label(c, text=self.strings["home_sub"]).pack(pady=(0, 20))



        btns = ttk.Frame(c)

        btns.pack(pady=10)

        ttk.Button(btns, text=self.strings["home_start"], command=lambda: self.nb.select(self.plan_tab)).grid(row=0, column=0, padx=8)

        ttk.Button(btns, text=self.strings["home_calc"], command=lambda: self.nb.select(self.calc_tab)).grid(row=0, column=1, padx=8)



        ttk.Label(c, text=self.strings["hint"]).pack(pady=(30, 0))



    def _build_calc(self):

        w = ttk.Frame(self.calc_tab, padding=12)
        w.pack(fill="both", expand=True)

        disp = ttk.Entry(
            w,
            font=("TkDefaultFont", self.base_font_size + 2),
            justify="right",
        )
        disp.pack(fill="x", pady=(0, 8))
        self._calc_disp = disp

        rows = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["0", ".", "=", "+"],
            ["(", ")", "^", "√", "C", "CE"],
        ]

        grid = ttk.Frame(w)
        grid.pack()

        max_cols = max(len(row) for row in rows)
        for col in range(max_cols):
            grid.columnconfigure(col, weight=1, uniform="calc")

        def put(txt: str) -> None:

            if txt == "C":
                disp.delete(0, "end")
                return

            if txt == "CE":
                current = disp.get()
                if current.endswith("sqrt("):
                    disp.delete(len(current) - 5, "end")
                elif current:
                    disp.delete(len(current) - 1, "end")
                return

            if txt == "=":
                self._calc_eval()
                return

            if txt == "√":
                disp.insert("end", "sqrt(")
                return

            disp.insert("end", txt)

        for r, row in enumerate(rows):

            for c, label in enumerate(row):

                ttk.Button(
                    grid,
                    text=label,
                    width=5,
                    command=lambda t=label: put(t),
                ).grid(row=r, column=c, padx=4, pady=4, sticky="nsew")

        disp.bind("<Return>", lambda _e: self._calc_eval())



    def _calc_eval(self):

        expr = self._calc_disp.get().strip().replace("^", "**")
        if not expr:
            return

        import math

        allowed = {
            "sqrt": math.sqrt,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "log": math.log10,
            "log10": math.log10,
            "ln": math.log,
            "pow": math.pow,
            "pi": math.pi,
            "e": math.e,
        }

        try:

            node = ast.parse(expr, mode="eval")

            for n in ast.walk(node):

                if isinstance(n, ast.Call):

                    if not isinstance(n.func, ast.Name) or n.func.id not in allowed:

                        raise ValueError("Expresión no permitida")

                elif isinstance(n, ast.Name):

                    if n.id not in allowed:

                        raise ValueError("Nombre no permitido")

                elif isinstance(

                    n,

                    (

                        ast.Expression,

                        ast.BinOp,

                        ast.UnaryOp,

                        ast.Load,

                        ast.Add,

                        ast.Sub,

                        ast.Mult,

                        ast.Div,

                        ast.Pow,

                        ast.Mod,

                        ast.USub,

                        ast.UAdd,

                        ast.Constant,

                        ast.Num,

                        ast.Tuple,

                    ),

                ):

                    continue

                else:

                    raise ValueError("Expresión no permitida")

            value = eval(compile(node, "<calc>", "eval"), {"__builtins__": None}, allowed)

            self._calc_disp.delete(0, "end")

            self._calc_disp.insert(0, str(value))

        except Exception as exc:

            messagebox.showerror("Error", f"Expresión inválida:\\n{exc}")


    def _parse_month_list(self, text: str) -> set[int]:

        months: set[int] = set()

        if not text:

            return months

        for chunk in text.replace(" ", "").split(","):

            if not chunk:

                continue

            try:

                month = int(float(chunk))

            except Exception:

                continue

            if 1 <= month <= 12:

                months.add(month)

        return months


    def _collect_debt_inputs(self) -> DebtInputs | None:

        def as_float(value: str | float, default: float = 0.0) -> float:

            try:

                return float(str(value).replace(",", "."))

            except Exception:

                return default

        cost = as_float(self.debt_cost.get(), 0.0)

        down = as_float(self.debt_down.get(), 0.0)

        cat = as_float(self.debt_cat.get(), 0.0)

        open_pct = as_float(self.debt_open_pct.get(), 0.0)

        insurance = as_float(self.debt_insurance.get(), 0.0)

        extra_amount = max(0.0, as_float(self.debt_extra_amount.get(), 0.0))

        inflation = as_float(self.debt_inflation.get(), 0.0)

        try:

            term = int(float(self.debt_term.get()))

        except Exception:

            term = 0

        term = max(term, 1)

        financed = cost - down

        if financed <= 0:

            messagebox.showerror(

                self.strings.get("tab_debt", "Deudas"),

                self.strings.get("debt_invalid_amount", "Necesitas que el monto financiado sea positivo."),

            )

            return None

        extra_months = self._parse_month_list(self.debt_extra_months.get())

        skip_months = self._parse_month_list(self.debt_skip_months.get())

        title = self.debt_title.get().strip() or self.strings.get("debt_default_title", "Crédito")

        return DebtInputs(

            title=title,

            cost=cost,

            down_payment=down,

            cat_annual=cat,

            open_pct=open_pct,

            insurance_monthly=insurance,

            term_months=term,

            extra_months=extra_months,

            extra_amount=extra_amount,

            skip_months=skip_months,

            inflation_annual=inflation,

        )


    def _simulate_debt(self, data: DebtInputs) -> tuple[list[tuple[int, float, float, float, float, float, float, float]], dict]:

        principal = data.cost - data.down_payment

        if principal <= 0:

            raise ValueError(self.strings.get("debt_invalid_amount", "Necesitas que el monto financiado sea positivo."))

        rate = (1.0 + data.cat_annual / 100.0) ** (1.0 / 12.0) - 1.0 if data.cat_annual else 0.0

        term = max(data.term_months, 1)

        if rate > 0:

            payment = rate * principal / (1.0 - (1.0 + rate) ** (-term))

        else:

            payment = principal / term

        payment = max(payment, 0.0)

        balance = principal

        rows: list[tuple[int, float, float, float, float, float, float, float]] = []

        total_interest = 0.0

        total_paid = 0.0

        total_fees = 0.0

        interest_acc = 0.0

        month = 0

        open_fee = max(0.0, data.open_pct / 100.0 * data.cost)

        inflation_rate = data.inflation_annual / 100.0

        base_inflation = 1.0 + inflation_rate

        max_months = term + 600

        while balance > 1e-6 and month < max_months:

            month += 1

            interest = balance * rate if rate else 0.0

            interest = max(interest, 0.0)

            scheduled_payment = payment

            principal_payment = 0.0

            if month in data.skip_months:

                scheduled_payment = interest

                principal_payment = 0.0

            else:

                principal_payment = max(scheduled_payment - interest, 0.0)

                if principal_payment > balance:

                    principal_payment = balance

                    scheduled_payment = interest + principal_payment

            balance -= principal_payment

            extra = 0.0

            if (

                month in data.extra_months

                and month not in data.skip_months

                and data.extra_amount > 0

                and balance > 0

            ):

                extra = min(data.extra_amount, balance)

                balance -= extra

                principal_payment += extra

            payment_total = scheduled_payment + extra

            fees = data.insurance_monthly

            if month == 1:

                fees += open_fee

            total_interest += interest

            total_fees += fees

            total_paid += payment_total

            interest_acc += interest

            if base_inflation > 0:

                real_balance = balance / (base_inflation ** (month / 12.0))

            else:

                real_balance = balance

            rows.append(

                (

                    month,

                    payment_total,

                    interest,

                    principal_payment,

                    fees,

                    balance,

                    interest_acc,

                    real_balance,

                )

            )

        if balance > 1e-4:

            raise ValueError("El crédito no se liquida con los parámetros actuales.")

        months = month

        total_paid_with_fees = total_paid + total_fees

        if base_inflation > 0:

            real_cost = total_paid_with_fees / (base_inflation ** (months / 12.0))

        else:

            real_cost = total_paid_with_fees

        summary = {

            "months": months,

            "total_paid": total_paid_with_fees,

            "total_interest": total_interest,

            "total_fees": total_fees,

            "real_cost": real_cost,

        }

        return rows, summary


    def _render_debt_results(self, rows, summary: dict):

        if not hasattr(self, "debt_tree"):

            return

        for item in self.debt_tree.get_children():

            self.debt_tree.delete(item)

        for row in rows:

            month, payment_total, interest, principal_payment, fees, balance, interest_acc, real_balance = row

            self.debt_tree.insert(

                "",

                "end",

                values=(

                    month,

                    fmt_currency(payment_total),

                    fmt_currency(interest),

                    fmt_currency(principal_payment),

                    fmt_currency(fees),

                    fmt_currency(balance),

                    fmt_currency(interest_acc),

                    fmt_currency(real_balance),

                ),

            )

        months = summary.get("months", 0)

        years = months / 12.0 if months else 0.0

        total_paid = summary.get("total_paid", 0.0)

        total_interest = summary.get("total_interest", 0.0)

        real_cost = summary.get("real_cost", 0.0)

        if hasattr(self, "debt_lbl_total"):

            self.debt_lbl_total.config(

                text=f"{self.strings.get('debt_summary_total', 'Total pagado')}: {fmt_currency(total_paid)}"

            )

        if hasattr(self, "debt_lbl_interest"):

            self.debt_lbl_interest.config(

                text=f"{self.strings.get('debt_summary_interest', 'Intereses totales')}: {fmt_currency(total_interest)}"

            )

        if hasattr(self, "debt_lbl_real"):

            self.debt_lbl_real.config(

                text=f"{self.strings.get('debt_summary_real', 'Costo real (hoy)')}: {fmt_currency(real_cost)}"

            )

        if hasattr(self, "debt_lbl_time"):

            self.debt_lbl_time.config(

                text=f"{self.strings.get('debt_summary_time', 'Tiempo (meses/años)')}: {months} / {years:.1f}"

            )


    def _on_calc_debt(self):

        data = self._collect_debt_inputs()

        if not data:

            return

        try:

            rows, summary = self._simulate_debt(data)

        except ValueError as exc:

            messagebox.showerror(self.strings.get("tab_debt", "Deudas"), str(exc))

            return

        self._render_debt_results(rows, summary)


    def _build_debt(self):

        for child in self.debt_tab.winfo_children():

            child.destroy()

        frm = ttk.Frame(self.debt_tab, padding=12)

        frm.pack(fill="both", expand=True)

        params = ttk.LabelFrame(frm, text=self.strings.get("debt_params", "Parámetros del crédito"), padding=12)

        params.pack(fill="x")

        self._labeled_entry(params, self.strings["debt_field_title"], self.debt_title, 0, 0, width=24)

        self._labeled_entry(params, self.strings["debt_field_cost"], self.debt_cost, 0, 1, width=14)

        self._labeled_entry(params, self.strings["debt_field_down"], self.debt_down, 0, 2, width=14)

        self._labeled_entry(

            params,

            self.strings["debt_field_cat"],

            self.debt_cat,

            1,

            0,

            width=14,

            help_key="debt_cat",

        )

        self._labeled_entry(

            params,

            self.strings["debt_field_open_pct"],

            self.debt_open_pct,

            1,

            1,

            width=14,

            help_key="debt_open_pct",

        )

        self._labeled_entry(

            params,

            self.strings["debt_field_insurance"],

            self.debt_insurance,

            1,

            2,

            width=14,

            help_key="debt_insurance",

        )

        self._labeled_entry(params, self.strings["debt_field_term"], self.debt_term, 2, 0, width=14)

        self._labeled_entry(

            params,

            self.strings["debt_field_extra_months"],

            self.debt_extra_months,

            2,

            1,

            width=18,

            help_key="debt_extra_months",

        )

        self._labeled_entry(

            params,

            self.strings["debt_field_extra_amount"],

            self.debt_extra_amount,

            2,

            2,

            width=14,

            help_key="debt_extra_amount",

        )

        self._labeled_entry(

            params,

            self.strings["debt_field_skip_months"],

            self.debt_skip_months,

            3,

            0,

            width=18,

            help_key="debt_skip_months",

        )

        self._labeled_entry(

            params,

            self.strings["debt_field_inflation"],

            self.debt_inflation,

            3,

            1,

            width=14,

        )

        ttk.Button(params, text=self.strings["debt_calc"], command=self._on_calc_debt).grid(

            row=4, column=0, columnspan=3, pady=(10, 0)

        )

        table_frame = ttk.LabelFrame(frm, text=self.strings["debt_table"], padding=12)

        table_frame.pack(fill="both", expand=True, pady=(12, 0))

        columns = (

            "month",

            "payment",

            "interest",

            "principal",

            "fees",

            "balance",

            "interest_acc",

            "real",

        )

        self.debt_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

        self.debt_tree.heading("month", text=self.strings["debt_col_month"])

        self.debt_tree.heading("payment", text=self.strings["debt_col_payment"])

        self.debt_tree.heading("interest", text=self.strings["debt_col_interest"])

        self.debt_tree.heading("principal", text=self.strings["debt_col_principal"])

        self.debt_tree.heading("fees", text=self.strings["debt_col_fees"])

        self.debt_tree.heading("balance", text=self.strings["debt_col_balance"])

        self.debt_tree.heading("interest_acc", text=self.strings["debt_col_interest_acc"])

        self.debt_tree.heading("real", text=self.strings["debt_col_real"])

        self.debt_tree.column("month", width=70, anchor="center")

        for col in columns[1:]:

            self.debt_tree.column(col, anchor="e", width=120)

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.debt_tree.yview)

        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.debt_tree.xview)

        self.debt_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.debt_tree.grid(row=0, column=0, sticky="nsew")

        vsb.grid(row=0, column=1, sticky="ns")

        hsb.grid(row=1, column=0, sticky="ew")

        table_frame.grid_rowconfigure(0, weight=1)

        table_frame.grid_columnconfigure(0, weight=1)

        summary_frame = ttk.LabelFrame(frm, text=self.strings["debt_summary"], padding=12)

        summary_frame.pack(fill="x", pady=(12, 0))

        self.debt_lbl_total = ttk.Label(

            summary_frame,

            text=f"{self.strings['debt_summary_total']}: {fmt_currency(0.0)}",

        )

        self.debt_lbl_total.grid(row=0, column=0, sticky="w")

        self.debt_lbl_interest = ttk.Label(

            summary_frame,

            text=f"{self.strings['debt_summary_interest']}: {fmt_currency(0.0)}",

        )

        self.debt_lbl_interest.grid(row=0, column=1, sticky="w", padx=(16, 0))

        self.debt_lbl_real = ttk.Label(

            summary_frame,

            text=f"{self.strings['debt_summary_real']}: {fmt_currency(0.0)}",

        )

        self.debt_lbl_real.grid(row=1, column=0, sticky="w", pady=(6, 0))

        self.debt_lbl_time = ttk.Label(

            summary_frame,

            text=f"{self.strings['debt_summary_time']}: 0 / 0.0",

        )

        self.debt_lbl_time.grid(row=1, column=1, sticky="w", padx=(16, 0), pady=(6, 0))


    def _help_text(self, key: str) -> tuple[str, str]:

        lang = getattr(self, "lang", "es")

        d = HELP_TEXTS.get(lang, HELP_TEXTS["es"])

        return d.get(key, ("", ""))







    def _help_icon(self, parent: tk.Misc, key: str):

        title, body = self._help_text(key)

        if not title and not body:

            return ttk.Label(parent, text="")

        txt = f"{title}\n\n{body}" if body else title

        lbl = ttk.Label(parent, text=" ?", cursor="question_arrow")

        Tooltip(lbl, txt)

        return lbl









    def _build_plan(self):

        # Scrollable canvas

        outer = ttk.Frame(self.plan_tab)

        outer.pack(fill="both", expand=True)



        canvas = tk.Canvas(outer, highlightthickness=0)

        vbar = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)

        canvas.configure(yscrollcommand=vbar.set)

        vbar.pack(side="right", fill="y")

        canvas.pack(side="left", fill="both", expand=True)



        inner = ttk.Frame(canvas)

        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        win = canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfigure(win, width=e.width))



        left = ttk.Frame(inner)

        right = ttk.Frame(inner)

        left.grid(row=0, column=0, sticky="nsew", padx=(10, 6), pady=8)

        right.grid(row=0, column=1, sticky="nsew", padx=(6, 10), pady=8)

        inner.grid_columnconfigure(0, weight=1)

        inner.grid_columnconfigure(1, weight=1)



        # Mouse-wheel scrolling

        def _wheel(event):

            delta = event.delta if hasattr(event, "delta") else 0

            if delta == 0 and getattr(event, "num", None) in (4, 5):  # X11

                delta = 120 if event.num == 4 else -120

            if delta:

                canvas.yview_scroll(int(-1 * (delta / 120)), "units")



        inner.bind_all("<MouseWheel>", _wheel)

        inner.bind_all("<Button-4>", _wheel)

        inner.bind_all("<Button-5>", _wheel)



        # --- Parámetros ---

        box = ttk.LabelFrame(left, text=self.strings["params"], padding=12)

        box.pack(fill="x")

        self.var_initial = tk.StringVar(value="0")

        self.var_monthly = tk.StringVar(value="200")

        self.var_years = tk.IntVar(value=5)

        self.var_return = tk.DoubleVar(value=10.0)

        self.var_infl = tk.DoubleVar(value=4.0)

        self.var_growth = tk.DoubleVar(value=0.0)

        self.var_custody = tk.StringVar(value="0.0")

        self.var_spread = tk.StringVar(value="0.0")



        self._labeled_entry(box, self.strings["initial_amount"], self.var_initial, 0, 0)

        self._labeled_entry(box, self.strings["monthly_contrib"], self.var_monthly, 1, 0)

        self._labeled_scale(

            box, self.strings['horizon_years'], self.var_years, 2, 0,

            from_=1, to_=50, step=1,

            fmt=lambda v: f"{int(float(v))} años",

            help_key='horizon_years'

        )

        self._labeled_scale(

            box, self.strings['annual_return'], self.var_return, 0, 1,

            from_=0.0, to_=25.0, step=0.1,

            fmt=lambda v: f"{float(v):.1f} %",

            help_key='annual_return'

        )

        self._labeled_scale(

            box, self.strings['inflation'], self.var_infl, 1, 1,

            from_=0.0, to_=15.0, step=0.1,

            fmt=lambda v: f"{float(v):.1f} %",

            help_key='inflation'

        )

        self._labeled_scale(

            box, self.strings['contrib_growth'], self.var_growth, 2, 1,

            from_=0.0, to_=15.0, step=0.1,

            fmt=lambda v: f"{float(v):.1f} %",

            help_key='contrib_growth'

        )



        prof = ttk.LabelFrame(left, text=self.strings["profile_title"], padding=12)

        prof.pack(fill="x", pady=(8, 0))



        self.var_instr = tk.StringVar(value=self.strings["instrument_mx_stock"])

        ttk.Label(prof, text=self.strings["instrument"]).grid(row=0, column=0, sticky="w")

        ttk.Combobox(

            prof,

            textvariable=self.var_instr,

            state="readonly",

            values=[

                self.strings["instrument_mx_stock"],

                self.strings["instrument_mx_debt"],

                self.strings["instrument_usa_stock"],

                self.strings["instrument_fund"],

            ],

            width=24,

        ).grid(row=0, column=1, sticky="w", padx=6)



        self.var_country = tk.StringVar(value=self.strings["country_mx"])

        ttk.Label(prof, text=self.strings["country"]).grid(row=1, column=0, sticky="w")

        ttk.Combobox(

            prof,

            textvariable=self.var_country,

            state="readonly",

            values=[self.strings["country_mx"], self.strings["country_usa"]],

            width=24,

        ).grid(row=1, column=1, sticky="w", padx=6)



        self.var_w8 = tk.BooleanVar(value=True)

        ttk.Checkbutton(prof, text=self.strings["w8ben"], variable=self.var_w8).grid(

            row=1, column=2, sticky="w", padx=10

        )



        self.var_div_y = tk.DoubleVar(value=0.0)

        self._labeled_scale(

            prof,

            self.strings["div_yield"],

            self.var_div_y,

            2,

            0,

            from_=0.0,

            to_=12.0,

            step=0.1,

            fmt=lambda v: f"{float(v):.1f} %",

            help_key="div_yield",

        )

        ttk.Label(prof, text=self.strings["div_policy"]).grid(row=2, column=1, sticky="w", padx=(6, 0))

        self.var_div_policy = tk.StringVar(value=self.strings["div_reinvest"])

        ttk.Combobox(

            prof,

            textvariable=self.var_div_policy,

            state="readonly",

            values=[self.strings["div_reinvest"], self.strings["div_withdraw"]],

            width=18,

        ).grid(row=2, column=2, sticky="w", padx=6)



        flow = ttk.LabelFrame(left, text=self.strings["flow_title"], padding=12)

        flow.pack(fill="x", pady=(6, 0))



        self.var_freq = tk.StringVar(value=self.strings["freq_monthly"])

        ttk.Label(flow, text=self.strings["frequency"]).grid(row=0, column=0, sticky="w")

        ttk.Combobox(

            flow,

            textvariable=self.var_freq,

            state="readonly",

            values=[

                self.strings["freq_monthly"],

                self.strings["freq_biweekly"],

                self.strings["freq_annual"],

            ],

            width=16,

        ).grid(row=0, column=1, sticky="w", padx=6)



        self.var_timing = tk.StringVar(value=self.strings["timing_begin"])

        ttk.Label(flow, text=self.strings["timing"]).grid(row=0, column=2, sticky="w", padx=(12, 0))

        ttk.Combobox(

            flow,

            textvariable=self.var_timing,

            state="readonly",

            values=[self.strings["timing_begin"], self.strings["timing_end"]],

            width=16,

        ).grid(row=0, column=3, sticky="w", padx=6)



        self.var_extra_months = tk.StringVar(value="")

        self.var_extra_amount = tk.StringVar(value="0.0")

        self.var_skip_months = tk.StringVar(value="")



        self._labeled_entry(flow, self.strings["extra_months"], self.var_extra_months, 1, 0, width=20, help_key="frequency")

        self._labeled_entry(flow, self.strings["extra_amount"], self.var_extra_amount, 1, 1, width=12, help_key="frequency")

        self._labeled_entry(flow, self.strings["skip_months"], self.var_skip_months, 1, 2, width=20, help_key="timing")



        # --- Fricción e impuestos ---

        fr = ttk.LabelFrame(left, text=self.strings["friction"], padding=12)

        fr.pack(fill="x", pady=(6, 0))



        self.var_fee_dep = tk.StringVar(value="0.0")

        self.var_buy_sell = tk.StringVar(value="0.0")

        self.var_mgmt = tk.StringVar(value="0.0")

        self.var_vat = tk.StringVar(value="16.0")

        self.var_tax = tk.StringVar(value="10.0")



        self._labeled_entry(fr, self.strings["deposit_fee"], self.var_fee_dep, 0, 0, help_key="deposit_fee")

        self._labeled_entry(fr, self.strings["buy_sell"], self.var_buy_sell, 1, 0, help_key="buy_sell")

        self._labeled_entry(fr, self.strings["mgmt"], self.var_mgmt, 2, 0, help_key="mgmt")

        self._labeled_entry(fr, self.strings["vat_comm"], self.var_vat, 0, 1, help_key="vat_comm")

        self._labeled_entry(fr, self.strings["isr_gain"], self.var_tax, 1, 1, help_key="isr_gain")

        self._labeled_entry(fr, self.strings["market_spread"], self.var_spread, 2, 1, help_key="market_spread")

        self._labeled_entry(fr, self.strings["custody_fixed"], self.var_custody, 3, 1, help_key="custody_fixed")



        adv = ttk.LabelFrame(left, text="Costos avanzados", padding=12)

        adv.pack(fill="x", pady=(6, 0))



        self.var_buy_fee = tk.StringVar(value="0.0")

        self.var_sell_fee = tk.StringVar(value="0.0")

        self.var_entry_spread = tk.StringVar(value="0.0")

        self.var_exit_spread = tk.StringVar(value="0.0")

        self.var_platform = tk.StringVar(value="0.0")



        self._labeled_entry(adv, self.strings["buy_fee"], self.var_buy_fee, 0, 0, help_key="buy_fee")

        self._labeled_entry(adv, self.strings["sell_fee"], self.var_sell_fee, 0, 1, help_key="sell_fee")

        self._labeled_entry(adv, self.strings["entry_spread"], self.var_entry_spread, 1, 0, help_key="entry_spread")

        self._labeled_entry(adv, self.strings["exit_spread"], self.var_exit_spread, 1, 1, help_key="exit_spread")

        self._labeled_entry(adv, self.strings["platform_fixed"], self.var_platform, 2, 0, help_key="platform_fixed")






        # --- (Quitar "Riesgo y escenarios") ---
        # Mantén variables para compatibilidad con el resto del código
        self.var_vol = tk.DoubleVar(value=0.0)
        self.var_mc = tk.IntVar(value=0)
        self.lbl_p5 = None
        self.lbl_p50 = None
        self.lbl_p95 = None

        # --- FAQ extendido (ocupa el espacio del riesgo) ---
        faq = ttk.LabelFrame(right, text=self.strings.get("faq_title", "Preguntas frecuentes"), padding=12)
        faq.pack(fill="both", expand=True, pady=(0, 8))

        faq_items = [
            (self.strings.get("faq_q1", "\u00bfPago IVA por invertir?"),
             self.strings.get("faq_a1", "No. El IVA aplica a bienes y servicios; en inversiones se paga ISR sobre la ganancia, no IVA.")),
            (self.strings.get("faq_q2", "\u00bfCu\u00e1ndo se paga ISR en acciones MX?"),
             self.strings.get("faq_a2", "Al vender con ganancia; la casa de bolsa retiene 10% sobre la utilidad (impuesto definitivo).")),
            (self.strings.get("faq_q3", "\u00bfY en CETES/bonos?"),
             self.strings.get("faq_a3", "Hay retenci\u00f3n sobre intereses conforme a tasas del SAT, descontada a lo largo del tiempo.")),

            # NUEVAS (rellenan el espacio del riesgo)
            (self.strings.get("faq_q4", "\u00bfQu\u00e9 es el inter\u00e9s compuesto?"),
             self.strings.get("faq_a4", "Es \"inter\u00e9s sobre el inter\u00e9s\": los rendimientos se reinvierten y tambi\u00e9n generan rendimiento. A largo plazo multiplica el crecimiento; por eso conviene empezar joven.")),
            (self.strings.get("faq_q5", "\u00bfCu\u00e1l es la diferencia entre valor nominal y valor real?"),
             self.strings.get("faq_a5", "Nominal no descuenta inflaci\u00f3n; Real ajusta con el INPC para mostrar poder de compra. En la app ver\u00e1s ambos.")),
            (self.strings.get("faq_q6", "\u00bfQu\u00e9 comisiones contempla la app?"),
             self.strings.get("faq_a6", "Dep\u00f3sito, compra/venta (con IVA), administraci\u00f3n/TER, spreads y cuotas fijas (plataforma/custodia). El IVA solo aplica sobre comisiones.")),
            (self.strings.get("faq_q7", "\u00bfQu\u00e9 es el TER o administraci\u00f3n anual?"),
             self.strings.get("faq_a7", "Es el costo porcentual del producto o asesor\u00eda. Se prorratea mensualmente y reduce el saldo antes del rendimiento.")),
            (self.strings.get("faq_q8", "\u00bfQu\u00e9 es el spread?"),
             self.strings.get("faq_a8", "Es la diferencia entre precio de compra y venta. Es un costo impl\u00edcito que reduce el rendimiento al entrar o salir.")),
            (self.strings.get("faq_q9", "\u00bfQu\u00e9 significa \"crecimiento anual de aportes\"?"),
             self.strings.get("faq_a9", "Es el porcentaje con el que subir\u00e1n tus dep\u00f3sitos cada a\u00f1o (\u00fatil para compensar inflaci\u00f3n o plan de ahorro progresivo).")),
            (self.strings.get("faq_q10", "\u00bfQu\u00e9 pasa si indico meses sin aportar?"),
             self.strings.get("faq_a10", "La simulaci\u00f3n omite el dep\u00f3sito en esos meses; al final ver\u00e1s menor saldo que si aportaras constante.")),
            (self.strings.get("faq_q11", "\u00bfC\u00f3mo se tratan los dividendos?"),
             self.strings.get("faq_a11", "Puedes reinvertir o retirar. Para USA hay retenci\u00f3n a dividendos (30% o menor con W-8BEN); en acciones MX la app aplica ISR 10% sobre ganancia al vender.")),
            (self.strings.get("faq_q12", "\u00bfQu\u00e9 es el CAT en deudas?"),
             self.strings.get("faq_a12", "El Costo Anual Total integra intereses, comisiones y seguros. Sirve para comparar cr\u00e9ditos; en la pesta\u00f1a Deudas ver\u00e1s su impacto en el costo total.")),
            (self.strings.get("faq_q13", "\u00bfEs asesor\u00eda financiera?"),
             self.strings.get("faq_a13", "No. Es una herramienta educativa para explorar escenarios y conceptos clave.")),
        ]

        for q, a in faq_items:
            ttk.Label(faq, text=f"\u2022 {q}", font=("", self.base_font_size, "bold"), wraplength=620, justify="left").pack(anchor="w", pady=(4, 0))
            ttk.Label(faq, text=a, wraplength=620, justify="left").pack(anchor="w", pady=(0, 6))

        # --- Resumen ---

        sm = ttk.LabelFrame(right, text=self.strings["summary"], padding=12)

        sm.pack(fill="x", pady=(6, 0))



        self.lbl_nominal = ttk.Label(sm, text=f"{self.strings['nominal_value']}: ")

        self.lbl_total   = ttk.Label(sm, text=f"{self.strings['total_contrib']}: ")

        self.lbl_gain    = ttk.Label(sm, text=f"{self.strings['gain']}: ")

        self.lbl_real    = ttk.Label(sm, text=f"{self.strings['real_value']}: ")



        self.lbl_nominal.grid(row=0, column=0, sticky="w", padx=4, pady=2)

        self.lbl_total.grid(row=1, column=0, sticky="w", padx=4, pady=2)

        self.lbl_gain.grid(row=2, column=0, sticky="w", padx=4, pady=2)

        self.lbl_real.grid(row=3, column=0, sticky="w", padx=4, pady=2)



        self.btn_copy = ttk.Button(sm, text=self.strings["copy"], command=self._copy_summary)

        self.btn_copy.grid(row=0, column=2, rowspan=4, sticky="e", padx=6, pady=4)

        sm.grid_columnconfigure(1, weight=1)



        ttk.Label(right, text=self.strings["need_monthly"]).pack(anchor="w", padx=14, pady=(2, 8))



        # --- Evolucion anual ---

        cols = ("year", "final", "contrib", "gain", "real", "fees", "taxes")

        tree_frame = ttk.Frame(right)

        tree_frame.pack(fill="both", expand=True, padx=0, pady=(8, 0))

        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=12)

        self.tree.pack(side="left", fill="both", expand=True)

        sb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)

        sb.pack(side="right", fill="y")

        self.tree.configure(yscrollcommand=sb.set)





        self.tree.heading("year", text=self.strings.get("years_to_invest", self.strings.get("years", "Year")))

        self.tree.heading("final", text=self.strings["final_balance"])

        self.tree.heading("contrib", text=self.strings["cum_contrib"])

        self.tree.heading("gain", text=self.strings["gain_col"] + " (neta acumulada)")

        self.tree.heading("real", text=self.strings.get("real_value", self.strings.get("real_col", "Real")))

        self.tree.heading("fees", text=self.strings.get("fees", self.strings.get("fees_col", "Fees")))

        self.tree.heading("taxes", text=self.strings.get("taxes", self.strings.get("taxes_col", "Taxes")))



        self.tree.column("year", width=100, anchor="center")

        self.tree.column("final", width=180, anchor="e")

        self.tree.column("contrib", width=180, anchor="e")

        self.tree.column("gain", width=190, anchor="e")

        self.tree.column("real", width=180, anchor="e")

        self.tree.column("fees", width=120, anchor="e")

        self.tree.column("taxes", width=120, anchor="e")



        # disparadores de recálculo

        for v in (
            self.var_initial, self.var_monthly, self.var_years, self.var_return, self.var_infl,
            self.var_growth, self.var_custody, self.var_spread, self.var_fee_dep, self.var_buy_sell,
            self.var_mgmt, self.var_vat, self.var_tax,
            self.var_instr, self.var_country, self.var_w8, self.var_div_y, self.var_div_policy,
            self.var_freq, self.var_timing, self.var_extra_months, self.var_extra_amount, self.var_skip_months,
            self.var_buy_fee, self.var_sell_fee, self.var_entry_spread, self.var_exit_spread, self.var_platform,
            self.var_vol, self.var_mc,
        ):

            v.trace_add("write", lambda *_: self._recalc())



        self._recalc()  # mantener



    def _labeled_scale(self, parent, label, var, row, col, from_, to_, step, fmt, help_key=None):

        frame_cls = BOOT.Frame if BOOT else ttk.Frame

        label_cls = BOOT.Label if BOOT else ttk.Label

        scale_cls = getattr(BOOT, "Scale", ttk.Scale) if BOOT else ttk.Scale



        frm = frame_cls(parent)

        frm.grid(row=row, column=col, padx=8, pady=6, sticky="ew")

        parent.grid_columnconfigure(col, weight=1)



        head = frame_cls(frm)

        head.pack(anchor="w", fill="x")



        label_cls(head, text=label).pack(side="left")

        if help_key:

            self._help_icon(head, help_key).pack(side="left", padx=(4, 0))



        val_lbl = label_cls(head, text=fmt(var.get()))

        val_lbl.pack(side="right")



        def on_move(_value=None):

            try:

                current = float(var.get())

            except Exception:

                current = from_

            snapped = round(current / step) * step

            snapped = max(min(snapped, to_), from_)

            if abs(snapped - current) > 1e-9:

                var.set(snapped)

            val_lbl.config(text=fmt(snapped))



        scale_cls(

            frm,

            orient="horizontal",

            from_=from_,

            to=to_,

            variable=var,

            command=lambda _v: on_move(),

        ).pack(fill="x")

        on_move()



        var.trace_add("write", lambda *_: self._recalc())





    def _labeled_entry(self, parent, label, var, row, col, help_key=None, width=16):

        frame_cls = BOOT.Frame if BOOT else ttk.Frame

        label_cls = BOOT.Label if BOOT else ttk.Label

        entry_cls = BOOT.Entry if BOOT else ttk.Entry



        frm = frame_cls(parent)

        frm.grid(row=row, column=col, padx=8, pady=6, sticky="ew")

        parent.grid_columnconfigure(col, weight=1)



        head = frame_cls(frm)

        head.pack(anchor="w", fill="x")



        label_cls(head, text=label).pack(side="left")

        if help_key:

            self._help_icon(head, help_key).pack(side="left", padx=(4, 0))



        entry_cls(frm, textvariable=var, width=width).pack(anchor="w")



    # ---------- Logic ----------



    def _collect_inputs(self) -> Inputs:

        def f(s, d=0.0):

            try:

                return float(str(s).replace(",", "."))

            except Exception:

                return d



        def i(s, d=1):

            try:

                return max(0, int(float(str(s))))

            except Exception:

                return d



        def clean_months(value: str) -> str:

            ordered: list[int] = []

            for part in (value or "").split(","):

                token = part.strip()

                if not token:

                    continue

                try:

                    month = int(float(token))

                except Exception:

                    continue

                if 1 <= month <= 12 and month not in ordered:

                    ordered.append(month)

            return ",".join(str(m) for m in ordered)


        years = max(1, int(self.var_years.get() or 1))

        _instr_map = {
            self.strings["instrument_mx_stock"]: "mx_stock",
            self.strings["instrument_mx_debt"]: "mx_debt",
            self.strings["instrument_usa_stock"]: "usa_stock",
            self.strings["instrument_fund"]: "fund",
        }
        _country_map = {
            self.strings["country_mx"]: "mx",
            self.strings["country_usa"]: "usa",
        }
        _policy_map = {
            self.strings["div_reinvest"]: "reinvest",
            self.strings["div_withdraw"]: "withdraw",
        }
        _freq_map = {
            self.strings["freq_monthly"]: "monthly",
            self.strings["freq_biweekly"]: "biweekly",
            self.strings["freq_annual"]: "annual",
        }
        _timing_map = {
            self.strings["timing_begin"]: "begin",
            self.strings["timing_end"]: "end",
        }

        return Inputs(
            initial=f(self.var_initial.get(), 0.0),
            monthly=f(self.var_monthly.get(), 0.0),
            years=years,
            annual_return=float(self.var_return.get() or 0.0),
            inflation=float(self.var_infl.get() or 0.0),
            fee_deposit=f(self.var_fee_dep.get(), 0.0),
            buy_sell=f(self.var_buy_sell.get(), 0.0),
            mgmt=f(self.var_mgmt.get(), 0.0),
            vat_on_fees=f(self.var_vat.get(), 16.0),
            tax_gain=f(self.var_tax.get(), 10.0),
            contrib_growth=float(self.var_growth.get() or 0.0),
            custody_fixed=f(self.var_custody.get(), 0.0),
            market_spread=f(self.var_spread.get(), 0.0),
            instrument=_instr_map.get(self.var_instr.get(), "mx_stock"),
            country=_country_map.get(self.var_country.get(), "mx"),
            w8ben=bool(self.var_w8.get()),
            div_yield=float(self.var_div_y.get() or 0.0),
            div_policy=_policy_map.get(self.var_div_policy.get(), "reinvest"),
            frequency=_freq_map.get(self.var_freq.get(), "monthly"),
            timing=_timing_map.get(self.var_timing.get(), "begin"),
            extra_months=clean_months(self.var_extra_months.get()),
            extra_amount=f(self.var_extra_amount.get(), 0.0),
            skip_months=clean_months(self.var_skip_months.get()),
            buy_fee=f(self.var_buy_fee.get(), 0.0),
            sell_fee=f(self.var_sell_fee.get(), 0.0),
            entry_spread=f(self.var_entry_spread.get(), 0.0),
            exit_spread=f(self.var_exit_spread.get(), 0.0),
            platform_fixed=f(self.var_platform.get(), 0.0),
            vol_annual=float(self.var_vol.get() or 0.0),
            mc_runs=int(float(self.var_mc.get() or 0)),
        )



    def _simulate(self, p: Inputs) -> tuple[list[YearRow], float, float, float, float]:
        """Simulación por pasos con calendarios de aporte, dividendos y costos avanzados."""

        freq = p.frequency
        steps = 12 if freq == "monthly" else (24 if freq == "biweekly" else 1)
        step_months = 12.0 / steps

        r_step = (1.0 + p.annual_return / 100.0) ** (step_months / 12.0) - 1.0
        mgmt_step = (p.mgmt / 100.0) * (step_months / 12.0)
        infl_y = p.inflation / 100.0
        g_step = (1.0 + p.contrib_growth / 100.0) ** (step_months / 12.0) - 1.0

        div_step = (p.div_yield / 100.0) * (step_months / 12.0)
        div_withhold = 0.0
        if p.instrument == "mx_stock":
            div_withhold = 0.10
        elif p.instrument == "usa_stock":
            div_withhold = 0.10 if p.w8ben else 0.30

        debt_withhold_step = 0.0
        if p.instrument == "mx_debt":
            debt_withhold_step = (p.tax_gain / 100.0) * (step_months / 12.0)

        balance = p.initial
        cum_contrib = p.initial
        rows: list[YearRow] = []

        if p.years <= 0:
            nominal = balance
            total_contrib = cum_contrib
            total_gain = max(0.0, nominal - total_contrib)
            return [], nominal, total_contrib, total_gain, nominal

        dep_current = p.monthly
        step_count = p.years * steps
        year = 1
        steps_in_year = 0

        def _parse_months(s: str) -> set[int]:
            out: set[int] = set()
            for part in (s or '').split(','):
                part = part.strip()
                if part.isdigit():
                    m = int(part)
                    if 1 <= m <= 12:
                        out.add(m)
            return out

        extra_set = _parse_months(p.extra_months)
        skip_set = _parse_months(p.skip_months)

        fees_year = taxes_year = 0.0
        gross_contrib_year = net_in_year = 0.0
        start_balance_year = balance

        steps_per_month = steps // 12 if steps >= 12 else 1

        for step in range(1, step_count + 1):
            if steps >= 12:
                month_idx = ((step - 1) // steps_per_month) % 12 + 1
                step_in_month = (step - 1) % steps_per_month
            else:
                month_idx = ((step - 1) % 12) + 1
                step_in_month = 0

            extra_now = 0.0
            if month_idx in extra_set:
                if steps < 12 or step_in_month == 0:
                    extra_now = p.extra_amount
            skip_now = month_idx in skip_set

            dep = 0.0 if skip_now else dep_current
            dep += extra_now

            if p.timing == "begin" and dep > 0:
                fee_dep = dep * (p.fee_deposit / 100.0)
                iva_dep = fee_dep * (p.vat_on_fees / 100.0)
                net_dep = dep - fee_dep
                balance += net_dep
                cum_contrib += dep
                gross_contrib_year += dep
                net_in_year += net_dep
                fees_year += (fee_dep + iva_dep)

            if mgmt_step > 0:
                fee_mgmt = balance * mgmt_step
                iva_mgmt = fee_mgmt * (p.vat_on_fees / 100.0)
                balance -= fee_mgmt
                fees_year += (fee_mgmt + iva_mgmt)

            if p.custody_fixed > 0.0:
                fee_fix = p.custody_fixed * (step_months / 1.0)
                iva_fix = fee_fix * (p.vat_on_fees / 100.0)
                balance -= fee_fix
                fees_year += (fee_fix + iva_fix)

            if p.platform_fixed > 0.0:
                fee_plat = p.platform_fixed * (step_months / 1.0)
                iva_plat = fee_plat * (p.vat_on_fees / 100.0)
                balance -= fee_plat
                fees_year += (fee_plat + iva_plat)

            interest = balance * r_step
            balance += interest

            if debt_withhold_step > 0 and interest > 0:
                tax_i = interest * debt_withhold_step
                balance -= tax_i
                taxes_year += tax_i

            if div_step > 0:
                gross_div = balance * div_step
                tax_div = gross_div * div_withhold
                net_div = gross_div - tax_div
                taxes_year += tax_div
                if p.div_policy == "reinvest":
                    balance += net_div

            if p.timing == "end" and dep > 0:
                fee_dep = dep * (p.fee_deposit / 100.0)
                iva_dep = fee_dep * (p.vat_on_fees / 100.0)
                net_dep = dep - fee_dep
                balance += net_dep
                cum_contrib += dep
                gross_contrib_year += dep
                net_in_year += net_dep
                fees_year += (fee_dep + iva_dep)

            dep_current *= (1.0 + g_step)

            steps_in_year += 1
            if steps_in_year == steps:
                if p.instrument not in ("mx_stock",):
                    gain_before_tax = balance - start_balance_year - net_in_year
                    tax = (gain_before_tax * (p.tax_gain / 100.0)) if gain_before_tax > 0 else 0.0
                    taxes_year += tax
                    balance -= tax

                real_val = balance / ((1.0 + infl_y) ** year)
                gain_cum = balance - cum_contrib

                rows.append(YearRow(
                    year=year,
                    final_balance=balance,
                    cum_contrib=cum_contrib,
                    gain=gain_cum,
                    real_value=real_val,
                    fees=fees_year,
                    taxes=taxes_year,
                ))

                start_balance_year = balance
                fees_year = taxes_year = 0.0
                gross_contrib_year = net_in_year = 0.0
                steps_in_year = 0
                year += 1

        if p.buy_sell > 0:
            fee_bs = balance * (p.buy_sell / 100.0)
            iva_bs = fee_bs * (p.vat_on_fees / 100.0)
            balance -= fee_bs
            rows[-1] = YearRow(
                year=rows[-1].year,
                final_balance=balance,
                cum_contrib=rows[-1].cum_contrib,
                gain=balance - rows[-1].cum_contrib,
                real_value=balance / ((1.0 + infl_y) ** p.years),
                fees=rows[-1].fees + fee_bs + iva_bs,
                taxes=rows[-1].taxes,
            )

        if p.sell_fee > 0:
            fee_sell = balance * (p.sell_fee / 100.0)
            iva_sell = fee_sell * (p.vat_on_fees / 100.0)
            balance -= fee_sell
            last = rows[-1]
            rows[-1] = YearRow(
                year=last.year,
                final_balance=balance,
                cum_contrib=last.cum_contrib,
                gain=balance - last.cum_contrib,
                real_value=balance / ((1.0 + infl_y) ** p.years),
                fees=last.fees + fee_sell + iva_sell,
                taxes=last.taxes,
            )

        if p.market_spread > 0:
            spread_loss = balance * (p.market_spread / 100.0)
            balance -= spread_loss
            last = rows[-1]
            rows[-1] = YearRow(
                year=last.year,
                final_balance=balance,
                cum_contrib=last.cum_contrib,
                gain=balance - last.cum_contrib,
                real_value=balance / ((1.0 + infl_y) ** p.years),
                fees=last.fees + spread_loss,
                taxes=last.taxes,
            )

        if p.exit_spread > 0:
            spr = balance * (p.exit_spread / 100.0)
            balance -= spr
            last = rows[-1]
            rows[-1] = YearRow(
                year=last.year,
                final_balance=balance,
                cum_contrib=last.cum_contrib,
                gain=balance - last.cum_contrib,
                real_value=balance / ((1.0 + infl_y) ** p.years),
                fees=last.fees + spr,
                taxes=last.taxes,
            )

        if p.instrument == "mx_stock":
            gain_total = max(0.0, balance - rows[-1].cum_contrib)
            tax_final = gain_total * (p.tax_gain / 100.0)
            balance -= tax_final
            last = rows[-1]
            rows[-1] = YearRow(
                year=last.year,
                final_balance=balance,
                cum_contrib=last.cum_contrib,
                gain=balance - last.cum_contrib,
                real_value=balance / ((1.0 + infl_y) ** p.years),
                fees=last.fees,
                taxes=last.taxes + tax_final,
            )
            if abs(p.tax_gain - 10.0) > 0.1:
                print("[INFO] Acciones MX: ISR por defecto es 10% al vender. Has establecido:", p.tax_gain)

        for rr in rows:
            if abs((rr.cum_contrib + rr.gain) - rr.final_balance) > 0.01:
                print(f"[WARN] Ano {rr.year}: final != contrib + ganancia {rr.final_balance:.2f} vs {(rr.cum_contrib + rr.gain):.2f}")

        nominal = balance
        total_contrib = cum_contrib
        total_gain = max(0.0, nominal - total_contrib)
        real_total = nominal / ((1.0 + infl_y) ** p.years)
        return rows, nominal, total_contrib, total_gain, real_total

    def _recalc(self):

        p = self._collect_inputs()

        if p.monthly <= 0 and p.initial <= 0:

            self._clear_summary()

            return

        rows, nominal, contrib, gain, real = self._simulate(p)



        # resumen

        self.lbl_nominal.config(text=f"{self.strings['nominal_value']}  {fmt_currency(nominal)}")

        self.lbl_total.config(text=f"{self.strings['total_contrib']}  {fmt_currency(contrib)}")

        self.lbl_gain.config(text=f"{self.strings['gain']}  {fmt_currency(gain)}")

        self.lbl_real.config(text=f"{self.strings['real_value']}  {fmt_currency(real)}")



        # tabla

        for i in self.tree.get_children():

            self.tree.delete(i)

        for r in rows:

            self.tree.insert("", "end", values=(

                r.year,

                fmt_currency(r.final_balance),

                fmt_currency(r.cum_contrib),

                fmt_currency(r.gain),

                fmt_currency(r.real_value),

                fmt_currency(r.fees),

                fmt_currency(r.taxes),

            ))

        has_mc_labels = all(getattr(self, name, None) is not None for name in ("lbl_p5", "lbl_p50", "lbl_p95"))
        if has_mc_labels and p.mc_runs and p.vol_annual > 0 and p.years > 0:
            import random
            import math
        
            freq = p.frequency
            steps = 12 if freq == "monthly" else (24 if freq == "biweekly" else 1)
            step_months = 12.0 / steps
            sigma_a = p.vol_annual / 100.0
            sigma_step = sigma_a * math.sqrt(step_months / 12.0)
            g_step = (1.0 + p.contrib_growth / 100.0) ** (step_months / 12.0) - 1.0
            runs = max(10, min(5000, int(p.mc_runs)))
        
            finals: list[float] = []
            for _ in range(runs):
                b = p.initial
                dep = p.monthly
                for _s in range(int(p.years * steps)):
                    mu = math.log(1 + p.annual_return / 100.0) * (step_months / 12.0) - 0.5 * sigma_step * sigma_step
                    rnd = math.exp(random.gauss(mu, sigma_step))
                    b += dep
                    b *= rnd
                    dep *= (1.0 + g_step)
                finals.append(b)
        
            finals.sort()
        
            def _q(pct: float) -> float:
                if not finals:
                    return 0.0
                k = max(0, min(len(finals) - 1, int(round(pct * (len(finals) - 1)))))
                return finals[k]
        
            self.lbl_p5.config(text=f"{self.strings.get('p5','P5 final')}: {fmt_currency(_q(0.05))}")
            self.lbl_p50.config(text=f"{self.strings.get('p50','P50 final')}: {fmt_currency(_q(0.50))}")
            self.lbl_p95.config(text=f"{self.strings.get('p95','P95 final')}: {fmt_currency(_q(0.95))}")
        elif has_mc_labels:
            self.lbl_p5.config(text=f"{self.strings.get('p5','P5 final')}: -")
            self.lbl_p50.config(text=f"{self.strings.get('p50','P50 final')}: -")
            self.lbl_p95.config(text=f"{self.strings.get('p95','P95 final')}: -")

    def _clear_summary(self):

        self.lbl_nominal.config(text='{}: '.format(self.strings['nominal_value']))

        self.lbl_total.config(text='{}: '.format(self.strings['total_contrib']))

        self.lbl_gain.config(text='{}: '.format(self.strings['gain']))

        self.lbl_real.config(text='{}: '.format(self.strings['real_value']))

        for i in self.tree.get_children():

            self.tree.delete(i)



    # ---------- Actions ----------



    def _copy_summary(self):

        try:

            text = "\n".join([

                self.lbl_nominal.cget("text"),

                self.lbl_total.cget("text"),

                self.lbl_gain.cget("text"),

                self.lbl_real.cget("text"),

            ])

            self.clipboard_clear()

            self.clipboard_append(text)

            self.update()

            messagebox.showinfo("OK", "Resumen copiado al portapapeles.")

        except Exception as e:

            messagebox.showerror("Error", str(e))



    def _font_minus(self):

        self._apply_font_scale(-1)



    def _font_plus(self):

        self._apply_font_scale(1)



    def _apply_font_scale(self, delta: int):

        self.base_font_size = max(8, min(22, self.base_font_size + delta))

        for name in ("TkDefaultFont", "TkTextFont", "TkHeadingFont", "TkMenuFont", "TkFixedFont", "TkTooltipFont"):

            try:

                f = tkfont.nametofont(name)

                f.configure(size=self.base_font_size)

            except tk.TclError:

                pass

        self.update_idletasks()





    def _apply_font_size(self):

        f = ("TkDefaultFont", self.base_font_size)

        try:

            self.option_clear()

        except Exception:

            pass

        self.option_add("*Font", f)



    def _toggle_contrast(self):

        try:

            import ttkbootstrap as tb  # noqa: F401

            self.style.theme_use("darkly" if self.cb_var.get() else "flatly")

        except Exception:

            s = ttk.Style()

            if self.cb_var.get():

                try:

                    s.theme_use("clam")

                except tk.TclError:

                    pass

                s.configure("TScale", troughcolor="#bcbcbc")

                s.map("TButton", background=[("active", "#e6e6e6")])

            else:

                try:

                    s.theme_use("default")

                except tk.TclError:

                    pass

                s.configure("TScale", troughcolor="")

                s.map("TButton", background=[])



    def _on_change_lang(self, _evt=None):

        idx = self.lang_cmb.current()

        self.lang = ("es", "en", "pt")[idx]

        self.strings = LANGUAGES[self.lang]

        self.title(self.strings["app_title"])



        # Renombrar tabs

        self.nb.tab(self.home_tab, text=self.strings["tab_home"])

        self.nb.tab(self.calc_tab, text=self.strings["tab_calc"])

        self.nb.tab(self.plan_tab, text=self.strings["tab_plan"])

        self.nb.tab(self.debt_tab, text=self.strings.get("tab_debt", "Deudas"))



        # Reconstruir contenidos sensibles a idioma

        for w in self.home_tab.winfo_children():

            w.destroy()

        for w in self.plan_tab.winfo_children():

            w.destroy()
        for w in self.debt_tab.winfo_children():

            w.destroy()

        self._build_home()

        self._build_plan()

        self._build_debt()



# ---- Launch (cuando se ejecuta directo este archivo) ----

if __name__ == "__main__":

    App().mainloop()

