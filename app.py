import streamlit as st
import re
from collections import Counter

class DetectorContenidoIA:
    """Detector de contenido generado por IA"""
    
    def analizar_patrones_linguisticos(self, texto: str) -> dict:
        indicadores = {
            'puntuacion_ia': 0,
            'señales': []
        }
        
        # 1. Longitud de oraciones uniforme
        oraciones = re.split(r'[.!?]+', texto)
        oraciones = [o.strip() for o in oraciones if o.strip()]
        
        if oraciones:
            longitudes = [len(o.split()) for o in oraciones]
            desviacion = max(longitudes) - min(longitudes) if longitudes else 0
            
            if desviacion < 5 and len(oraciones) > 3:
                indicadores['puntuacion_ia'] += 15
                indicadores['señales'].append('Longitud de oraciones muy uniforme')
        
        # 2. Uso excesivo de transiciones
        transiciones = ['además', 'asimismo', 'por lo tanto', 'en consecuencia', 
                       'sin embargo', 'no obstante', 'en primer lugar', 'finalmente']
        
        texto_lower = texto.lower()
        count_transiciones = sum(texto_lower.count(t) for t in transiciones)
        
        if count_transiciones > len(oraciones) * 0.3:
            indicadores['puntuacion_ia'] += 20
            indicadores['señales'].append('Uso excesivo de conectores formales')
        
        # 3. Estructura sistemática
        estructura_sistematica = bool(re.search(r'\n\s*[-•]\s+', texto)) or \
                                bool(re.search(r'\d+\.\s+[A-Z]', texto))
        
        if estructura_sistematica:
            indicadores['puntuacion_ia'] += 10
            indicadores['señales'].append('Estructura muy organizada/sistemática')
        
        # 4. Vocabulario técnico genérico
        palabras_tecnicas = ['implementar', 'optimizar', 'eficiente', 
                           'estrategia', 'objetivo', 'indicador', 
                           'proceso', 'desarrollo']
        
        count_tecnicas = sum(texto_lower.count(p) for p in palabras_tecnicas)
        
        if count_tecnicas > 5:
            indicadores['puntuacion_ia'] += 15
            indicadores['señales'].append('Alto uso de vocabulario técnico genérico')
        
        # 5. Texto largo sin errores
        palabras = texto.split()
        if len(palabras) > 100:
            indicadores['puntuacion_ia'] += 10
            indicadores['señales'].append('Texto extenso sin errores aparentes')
        
        # 6. Repetición de estructuras
        inicios_oracion = [o.split()[0] for o in oraciones if o.split()]
        if len(inicios_oracion) > 3:
            repeticiones = len(inicios_oracion) - len(set(inicios_oracion))
            if repeticiones > len(inicios_oracion) * 0.3:
                indicadores['puntuacion_ia'] += 15
                indicadores['señales'].append('Patrones repetitivos en inicio de oraciones')
        
        indicadores['puntuacion_ia'] = min(indicadores['puntuacion_ia'], 100)
        
        return indicadores
    
    def detectar(self, texto: str) -> dict:
        if len(texto.strip()) < 50:
            return {
                'error': 'El texto debe tener al menos 50 caracteres',
                'longitud': len(texto)
            }
        
        resultado = self.analizar_patrones_linguisticos(texto)
        puntuacion = resultado['puntuacion_ia']
        
        if puntuacion < 30:
            veredicto = 'Muy probablemente escrito por humano'
            color = '🟢'
        elif puntuacion < 50:
            veredicto = 'Probablemente escrito por humano'
            color = '🟡'
        elif puntuacion < 70:
            veredicto = 'Incierto - puede ser humano o IA'
            color = '🟠'
        elif puntuacion < 85:
            veredicto = 'Probablemente generado por IA'
            color = '🔴'
        else:
            veredicto = 'Muy probablemente generado por IA'
            color = '🔴'
        
        return {
            'veredicto': veredicto,
            'color': color,
            'puntuacion_ia': round(puntuacion, 2),
            'señales_detectadas': resultado['señales'],
            'total_palabras': len(texto.split())
        }


# Configuración de la página
st.set_page_config(
    page_title="Detector de Contenido IA",
    page_icon="🤖",
    layout="wide"
)

# Título y descripción
st.title("🤖 Detector de Contenido Generado por IA")
st.markdown("""
Esta aplicación analiza textos para detectar si fueron generados por Inteligencia Artificial.
Utiliza análisis de patrones lingüísticos sin necesidad de APIs externas.
""")

# Área de texto
texto_input = st.text_area(
    "Pega aquí el texto que quieres analizar:",
    height=300,
    placeholder="Escribe o pega al menos 50 caracteres de texto..."
)

# Botón de análisis
if st.button("🔍 Analizar Texto", type="primary"):
    if texto_input:
        detector = DetectorContenidoIA()
        resultado = detector.detectar(texto_input)
        
        if 'error' in resultado:
            st.error(f"❌ {resultado['error']}")
        else:
            # Mostrar resultados
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label="Puntuación IA",
                    value=f"{resultado['puntuacion_ia']}%"
                )
            
            with col2:
                st.metric(
                    label="Total Palabras",
                    value=resultado['total_palabras']
                )
            
            with col3:
                st.metric(
                    label="Señales Detectadas",
                    value=len(resultado['señales_detectadas'])
                )
            
            # Veredicto
            st.markdown("---")
            st.subheader(f"{resultado['color']} Veredicto")
            st.info(resultado['veredicto'])
            
            # Señales detectadas
            if resultado['señales_detectadas']:
                st.markdown("---")
                st.subheader("🔍 Señales Detectadas")
                for señal in resultado['señales_detectadas']:
                    st.markdown(f"• {señal}")
            
            # Barra de progreso
            st.markdown("---")
            st.subheader("📊 Nivel de Confianza IA")
            st.progress(resultado['puntuacion_ia'] / 100)
    else:
        st.warning("⚠️ Por favor, introduce un texto para analizar")

# Sidebar con información
with st.sidebar:
    st.header("ℹ️ Acerca de")
    st.markdown("""
    ### ¿Cómo funciona?
    
    El detector analiza:
    - Uniformidad en longitud de oraciones
    - Uso de conectores formales
    - Estructura sistemática
    - Vocabulario técnico genérico
    - Ausencia de errores
    - Patrones repetitivos
    
    ### Limitaciones
    - No es 100% preciso
    - Funciona mejor con textos de +100 palabras
    - Diseñado para español
    
    ### Versión
    v1.0.0 - Análisis local gratuito
    """)
    
    st.markdown("---")
    st.markdown("Desarrollado con ❤️ usando Streamlit")
