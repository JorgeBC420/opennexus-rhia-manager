import requests
import json
from config import OLLAMA_API_URL, OLLAMA_MODEL
from typing import Dict, Any, Optional

def analyze_cv_with_ollama(job_requirements: Dict[str, Any], cv_text: str) -> Optional[Dict[str, Any]]:
    """
    Analiza un CV usando Ollama y retorna la evaluación en formato JSON estructurado.
    Args:
        job_requirements (dict): Diccionario con los requerimientos del puesto.
        cv_text (str): Texto extraído del CV.
    Returns:
        dict | None: Análisis estructurado o None si falla.
    """
    prompt = f"""
    Actúa como un reclutador técnico senior altamente experimentado para una startup de tecnología en Costa Rica. Tu tarea es analizar el siguiente currículum y evaluarlo objetivamente contra los requerimientos del puesto.

    **Puesto:**
    {job_requirements.get('titulo', job_requirements.get('puesto', ''))}

    **Requerimientos Clave:**
    {job_requirements.get('requerimientos', '')}

    **Texto del Currículum:**
    ---
    {cv_text[:8000]}
    ---

    **Tu Tarea:**
    Analiza el CV y proporciona tu evaluación EXCLUSIVAMENTE en formato JSON. No añadas ningún texto antes o después del JSON. La estructura debe ser la siguiente:

    {{
      "puntuacion_general": <un número entero de 1 a 100>,
      "resumen_alineacion": "<Un resumen conciso de 2-3 frases explicando por qué el candidato es o no es un buen fit>",
      "habilidades_encontradas": ["<lista de habilidades clave que coinciden>"],
      "experiencia_relevante_anos": <un número estimado de años de experiencia relevante>,
      "nivel_ingles_estimado": "<A1, A2, B1, B2, C1, C2, o N/A>",
      "puntos_fuertes": "<Describe en una frase los puntos más fuertes del candidato para este puesto>",
      "posibles_debilidades": "<Describe en una frase las posibles áreas donde el candidato no cumple>"
    }}
    """
    data = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "format": "json",
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_API_URL, json=data, timeout=120)
        response.raise_for_status()
        response_json = response.json()
        generated_text = response_json.get('response', '')
        return json.loads(generated_text)
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud a Ollama: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decodificando JSON de Ollama: {e}")
    return None
