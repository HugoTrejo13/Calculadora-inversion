"""
i18n.py (versión simplificada)
- Texto en español fijo
- Diccionarios para etiquetas e información contextual/ayuda
"""

# Diccionario de todos los textos visibles en UI (etiquetas, títulos, botones, etc.)
STRINGS = {'app_title': 'Calculadora Financiera para jóvenes',
 'tab_home': 'Inicio',
 'tab_calc': 'Calculadora',
 'tab_plan': 'Plan de inversión',
 'tab_debt': 'Deudas',
 'access': 'Accesibilidad:',
 'font_minus': 'A-',
 'font_plus': 'A+',
 'daltonic': 'Modo daltonismo',
 'language': 'Idioma:',
 'home_title': 'Bienvenido a aprender a invertir',
 'home_sub': 'Simula metas, entiende comisiones e impuestos y practica con la calculadora '
             'científica.',
 'home_start': 'Comenzar plan de inversión',
 'home_calc': 'Explorar calculadora',
 'hint': 'Sugerencia: cambia el idioma y el tamaño de fuente desde la barra superior.',
 'params': 'Parámetros de inversión',
 'initial_amount': 'Monto inicial (MXN)',
 'monthly_contrib': 'Aporte mensual (MXN)',
 'horizon_years': 'Horizonte (años)',
 'annual_return': 'Rendimiento anual (%)',
 'inflation': 'Inflación anual (%)',
 'friction': 'Fricción e impuestos (MX)',
 'deposit_fee': 'Comisión por depósito (%)',
 'buy_sell': 'Compra/Venta (%)',
 'mgmt': 'Adm. anual (TER) (%)',
 'vat_comm': 'IVA sobre comisiones (%)',
 'isr_gain': 'ISR sobre ganancia (%)',
 'contrib_growth': 'Crecimiento anual de aportes (%)',
 'custody_fixed': 'Cuota fija de custodia (MXN/mes)',
 'market_spread': 'Market spread de salida (%)',
 'summary': 'Resumen',
 'nominal_value': 'Valor final (nominal)',
 'total_contrib': 'Aportes totales',
 'gain': 'Ganancia generada',
 'real_value': 'Valor ajustado por inflación',
 'need_monthly': 'Se necesita un aporte mensual positivo para proyectar la inversión.',
 'copy': 'Copiar resumen',
 'evolution': 'Evolución anual',
 'years': 'Años',
 'final_balance': 'Saldo total final',
 'cum_contrib': 'Aporte acumulado',
 'gain_col': 'Ganancia',
 'real_col': 'Valor real',
 'fees_col': 'Comisiones',
 'taxes_col': 'Impuestos',
 'profile_title': 'Instrumento y país',
 'instrument': 'Instrumento',
 'country': 'País fiscal',
 'w8ben': 'Usa W‑8BEN',
 'div_yield': 'Dividendo (yield) anual (%)',
 'div_policy': 'Dividendo: reinvertir o retirar',
 'div_reinvest': 'Reinvertir',
 'div_withdraw': 'Retirar',
 'instrument_mx_stock': 'Acciones / ETFs MX',
 'instrument_mx_debt': 'Deuda MX (CETES/bonos)',
 'instrument_usa_stock': 'Acciones / ETFs USA',
 'instrument_fund': 'Fondo de inversión',
 'country_mx': 'México',
 'country_usa': 'Extranjero / USA',
 'flow_title': 'Calendario de aportes',
 'frequency': 'Frecuencia',
 'freq_monthly': 'Mensual',
 'freq_biweekly': 'Quincenal',
 'freq_annual': 'Anual',
 'timing': 'Momento del aporte',
 'timing_begin': 'Inicio de periodo',
 'timing_end': 'Fin de periodo',
 'extra_months': 'Meses con aporte extra (ej. 6,12)',
 'extra_amount': 'Monto extra (MXN)',
 'skip_months': 'Meses sin aportar (ej. 7,8)',
 'buy_fee': 'Comisión de compra (%)',
 'sell_fee': 'Comisión de venta (%)',
 'entry_spread': 'Spread de entrada (%)',
 'exit_spread': 'Spread de salida (%)',
 'platform_fixed': 'Cuota plataforma (MXN/mes)',
 'risk_title': 'Riesgo y escenarios',
 'vol_annual': 'Volatilidad anual (%)',
 'mc_runs': 'Corridas Monte Carlo',
 'p5': 'P5 final',
 'p50': 'P50 final',
 'p95': 'P95 final',
 'faq_title': 'Preguntas frecuentes',
 'faq_q1': '¿Pago IVA por invertir?',
 'faq_a1': 'No. El IVA aplica a bienes y servicios; en inversiones se paga ISR sobre la ganancia.',
 'faq_q2': '¿Cuándo se paga ISR en acciones MX?',
 'faq_a2': 'Al vender con ganancia; la casa de bolsa retiene 10% sobre la utilidad (definitivo).',
 'faq_q3': '¿Y en CETES/bonos?',
 'faq_a3': 'Hay retención sobre intereses conforme a tasas del SAT, descontada a lo largo del '
           'tiempo.',
 'debt_params': 'Parámetros del crédito',
 'debt_field_title': 'Título',
 'debt_field_cost': 'Costo del producto (MXN)',
 'debt_field_down': 'Enganche (MXN)',
 'debt_field_cat': 'CAT anual (%)',
 'debt_field_open_pct': 'Comisión apertura (%)',
 'debt_field_insurance': 'Seguro mensual (MXN)',
 'debt_field_term': 'Plazo (meses)',
 'debt_field_extra_months': 'Meses con pago extra (ej. 6,12)',
 'debt_field_extra_amount': 'Monto extra (MXN)',
 'debt_field_skip_months': 'Meses sin pagar (ej. 7,8)',
 'debt_field_inflation': 'Inflación anual (%)',
 'debt_calc': 'Calcular',
 'debt_table': 'Amortización',
 'debt_col_month': 'Mes',
 'debt_col_payment': 'Pago',
 'debt_col_interest': 'Interés',
 'debt_col_principal': 'Capital',
 'debt_col_fees': 'Seguro/comisiones',
 'debt_col_balance': 'Saldo',
 'debt_col_interest_acc': 'Intereses acumulados',
 'debt_col_real': 'Real (deflactado)',
 'debt_summary': 'Resumen',
 'debt_summary_total': 'Total pagado',
 'debt_summary_interest': 'Intereses totales',
 'debt_summary_real': 'Costo real (hoy)',
 'debt_summary_time': 'Tiempo (meses/años)',
 'debt_default_title': 'Crédito',
 'debt_invalid_amount': 'Necesitas que el monto financiado sea positivo.',
 'faq_q4': '¿Qué es el interés compuesto?',
 'faq_a4': 'Es "interés sobre el interés": los rendimientos se reinvierten y también generan '
           'rendimiento. Empezar joven multiplica el resultado.',
 'faq_q5': '¿Cuál es la diferencia entre valor nominal y valor real?',
 'faq_a5': 'El valor nominal no descuenta inflación; el valor real se deflacta con INPC para '
           'mostrar poder de compra.',
 'faq_q6': '¿Qué comisiones contempla la app?',
 'faq_a6': 'Depósito, compra/venta (con IVA), administración/TER, spreads y cuotas fijas '
           '(plataforma/custodia).',
 'faq_q7': '¿Qué es el TER o administración anual?',
 'faq_a7': 'Costo porcentual del producto/asesoría prorrateado al mes; reduce el saldo antes del '
           'rendimiento.',
 'faq_q8': '¿Qué es el spread?',
 'faq_a8': 'Diferencia entre precio de compra y venta; es un costo implícito al entrar/salir.',
 'faq_q9': '¿Qué significa "crecimiento anual de aportes"?',
 'faq_a9': 'Porcentaje con el que subirán tus depósitos cada año.',
 'faq_q10': '¿Qué pasa si indico meses sin aportar?',
 'faq_a10': 'La simulación omite el depósito en esos meses; verás menor saldo final.',
 'faq_q11': '¿Cómo se tratan los dividendos?',
 'faq_a11': 'Puedes reinvertir o retirar. Para USA hay retención a dividendos (30% o menor con '
            'W-8BEN). En acciones MX la app aplica ISR 10% sobre ganancia al vender.',
 'faq_q12': '¿Qué es el CAT en deudas?',
 'faq_a12': 'El Costo Anual Total integra intereses, comisiones y seguros; sirve para comparar '
            'créditos.',
 'faq_q13': '¿Es asesoría financiera?',
 'faq_a13': 'No. Es una herramienta educativa para explorar escenarios y conceptos clave.'}

# Textos de ayuda contextual (tooltips, FAQs, explicaciones).
HELP_TEXTS = {'initial_amount': ('Capital inicial',
                    '• Monto con el que comienzas.\n'
                    '• Se invierte desde el mes 1.\n'
                    'Ej.: Si pones 5,000 MXN y aportas 1,000/mes, el primer mes parte de 6,000 '
                    '(menos comisiones de deposito).'),
 'monthly_contrib': ('Aporte mensual',
                     '• Dinero que agregas cada mes antes de comisiones.\n'
                     "• Si activas 'Crecimiento anual de aportes', este monto sube mes a mes."),
 'horizon_years': ('Horizonte (años)',
                   '• Tiempo total de la inversion.\n'
                   '• Al final se simula una venta unica (compra/venta + spread).'),
 'annual_return': ('Rendimiento anual nominal (%)',
                   '• Tasa esperada antes de inflacion.\n'
                   '• Se capitaliza mensual: r_m = (1+r)^(1/12)-1.'),
 'inflation': ('Inflacion anual (%)',
               "• Sirve para calcular 'Valor real'.\n• No modifica depositos ni impuestos."),
 'deposit_fee': ('Comision por deposito (%)',
                 '• Porcentaje descontado a cada aporte mensual.\n'
                 "• El IVA se muestra en 'Comisiones', pero no aumenta el saldo."),
 'buy_sell': ('Comision de compra/venta (%)',
              '• Se aplica una sola vez al final del horizonte al liquidar.\n'
              "• El IVA se muestra en 'Comisiones'."),
 'mgmt': ('Administracion anual (%)',
          '• Cobro del administrador, prorrateado mensual.\n'
          "• El fee reduce el saldo; el IVA solo se reporta en 'Comisiones'."),
 'vat_comm': ('IVA sobre comisiones (%)',
              '• Impuesto a las comisiones cobradas (deposito, administracion, custodia).\n'
              '• No aumenta el saldo; solo se refleja como costo.'),
 'isr_gain': ('ISR sobre ganancia (%)',
              '• Impuesto anual sobre la ganancia positiva del año.\n'
              '• Si el año cierra en perdida, no se cobra ISR ese año.'),
 'contrib_growth': ('Crecimiento anual de aportes (%)',
                    '• Aumenta el aporte cada mes segun una tasa anual.\n'
                    '• Ej.: 6% anual ≈ 0.486% mensual.'),
 'custody_fixed': ('Cuota fija de custodia (MXN/mes)',
                   '• Cargo mensual fijo; reduce el saldo.\n'
                   "• El IVA de esta cuota se reporta como 'Comisiones'."),
 'market_spread': ('Market spread de salida (%)',
                   '• Perdida por diferencia bid/ask y deslizamiento al vender.\n'
                   '• Se aplica una sola vez al final (ademas de compra/venta).'),
 'div_yield': ('Dividendo anual (%)',
               'Porcentaje de dividendos que entrega el instrumento; reinvierte o retira '
               '(retención MX/USA automática).'),
 'buy_fee': ('Comisión de compra (%)',
             'Porcentaje por transacción de compra; suele causar IVA reportado en Comisiones.'),
 'sell_fee': ('Comisión de venta (%)',
              'Porcentaje por transacción de venta al final; suele causar IVA.'),
 'entry_spread': ('Spread de entrada (%)', 'Diferencia implícita al comprar (precio/ejecución).'),
 'exit_spread': ('Spread de salida (%)', 'Diferencia implícita al vender; se aplica al final.'),
 'platform_fixed': ('Cuota plataforma (MXN/mes)',
                    'Tarifa fija por uso de la app/plataforma; se descuenta mes a mes.'),
 'frequency': ('Frecuencia de aportes', 'Define cada cuánto aportas: mensual, quincenal o anual.'),
 'timing': ('Momento del aporte',
            'Inicio del periodo (antes del rendimiento) o al final del periodo.'),
 'extra_months': ('Meses con aporte extra',
                  'Lista separada por comas con los meses (1..12) en los que harás un depósito '
                  'adicional. Ej.: 6,12.'),
 'extra_amount': ('Monto extra (MXN)',
                  "Cantidad que se depositará en los meses listados en 'Meses con aporte extra'."),
 'skip_months': ('Meses sin aportar',
                 'Lista separada por comas con los meses (1..12) en los que no habrá depósito. '
                 'Ej.: 7,8.'),
 'instrument': ('Instrumento',
                'Tipo general del activo para aplicar reglas fiscales típicas (MX acciones/ETFs, '
                'deuda, USA, fondos).'),
 'country': ('País fiscal',
             'Determina si hay retención local (MX) o si declaras por tu cuenta (USA/Extranjero).'),
 'w8ben': ('Usa W‑8BEN', 'Aplica a instrumentos USA para reducción de retención sobre dividendos.'),
 'div_policy': ('Dividendo: reinvertir o retirar',
                'Reinvertir suma el dividendo neto al saldo; retirar lo excluye del saldo (solo '
                'educativo).'),
 'debt_cat': ('CAT anual (%)',
              'Costo Anual Total del crédito. Se transforma a tasa por periodo '
              '(mensual/quincenal).'),
 'debt_msi': ('Meses sin intereses',
              'Promoción a 0% durante los primeros N meses (si N = plazo total, todo el crédito es '
              'sin intereses).'),
 'debt_open_pct': ('Comisión de apertura (%)',
                   'Porcentaje sobre el costo del producto. Se suma una sola vez (con IVA si '
                   'aplica).'),
 'debt_open_fix': ('Comisión de apertura fija (MXN)',
                   'Cuota fija inicial. También sujeta a IVA si corresponde.'),
 'debt_month_fee': ('Comisiones fijas mensuales (MXN)',
                    'Cargo mensual de la institución (se suma con IVA).'),
 'debt_ins': ('Seguro mensual (MXN)',
              'Seguro de vida/daños. Se suma cada periodo (con IVA si aplica).'),
 'debt_vat': ('IVA sobre comisiones (%)',
              'Impuesto aplicado a comisiones/seguros. No reduce saldo; es costo.'),
 'debt_infl': ('Inflación anual (%)',
               'Para calcular el valor real (devaluado) del saldo al cierre de cada año.'),
 'debt_insurance': ('Seguro mensual (MXN)',
                    'Cuota mensual del seguro asociado al crédito. Se suma como costo fijo cada '
                    'mes.'),
 'debt_extra_months': ('Pagos extra',
                       'Meses (1,2,3...) separados por comas en los que aportarás un pago '
                       'adicional para reducir capital.'),
 'debt_extra_amount': ('Monto extra (MXN)',
                       'Importe del pago adicional aplicado en los meses indicados; reduce el '
                       'saldo inmediatamente.'),
 'debt_skip_months': ('Meses sin pagar',
                      'Meses (1,2,3...) separados por comas en los que solo se cubre interés y '
                      'seguros; el capital no baja.')}

def get_strings() -> dict:
    """Devuelve el diccionario STRINGS (etiquetas, títulos, etc.)."""
    return STRINGS

def get_help_texts() -> dict:
    """Devuelve el diccionario HELP_TEXTS (textos de ayuda)."""
    return HELP_TEXTS
