import streamlit as st
import sympy as sp
from sympy.calculus.util import continuous_domain, function_range
from sympy import S
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Calculadora Matemática - UTEC", layout="wide")
st.title("📊 Analizador de Funciones Matemáticas")
st.markdown("---")

texto_input = st.text_input("Ingresa tu función f(x):", "x**2 - 4*x + 3")

if texto_input:
    try:
        x = sp.symbols('x')
        # Limpiamos la entrada para que acepte ^ como potencia
        f_expr = sp.sympify(texto_input.replace('^', '**'))
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.header("📝 Análisis Teórico")
            
            # Cálculo de Dominio
            dom = continuous_domain(f_expr, x, S.Reals)
            st.write(f"**Dominio:** ${sp.latex(dom)}$")
            
            # CÁLCULO DE RANGO (Agregado)
            try:
                ran = function_range(f_expr, x, S.Reals)
                st.write(f"**Rango:** ${sp.latex(ran)}$")
            except:
                st.write("**Rango:** No se pudo determinar analíticamente.")

            # Cortes en los ejes
            corte_y = f_expr.subs(x, 0)
            st.write(f"**Corte en Eje Y:** (0, {corte_y})")
            
            raices = sp.solve(f_expr, x)
            st.write(f"**Cortes en Eje X (Raíces):** {[(sp.N(r, 2), 0) for r in raices]}")
            
            # Inyectividad
            derivada = sp.diff(f_expr, x)
            puntos_criticos = sp.solve(derivada, x)
            es_inyectiva = len(puntos_criticos) == 0
            
            st.write(f"**¿Es Inyectiva?:** {'Sí' if es_inyectiva else 'No'}")
            
            if es_inyectiva:
                y = sp.symbols('y')
                inversa = sp.solve(sp.Eq(y, f_expr), x)
                if inversa:
                    st.success(f"**Función Inversa f⁻¹(x):** ${sp.latex(inversa[0]).replace('y', 'x')}$")
            else:
                st.warning("No es inyectiva en todo su dominio (fallaría la prueba de la línea horizontal).")

        with col2:
            st.header("📈 Gráfica Interactiva")
            f_num = sp.lambdify(x, f_expr, "numpy")
            x_vals = np.linspace(-10, 10, 400)
            y_vals = f_num(x_vals)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_vals, y=y_vals, name="f(x)", line=dict(color='blue', width=3)))
            fig.update_layout(xaxis_title="Eje X", yaxis_title="Eje Y", hovermode="x")
            st.plotly_chart(fig)
            
    except Exception as e:
        st.error(f"Error en la expresión: Asegúrate de usar '*' para multiplicar (ejemplo: 2*x).")
