import json
import os
from gestion_libros import cargar_libros
import config

REPORTE_AUDITORIA = config.ruta_absoluta/"data/reportes/reporte_auditoria_estados.json"

def auditoria_estados():
    libros = cargar_libros()
    inconsistencias = []
    
    resumen = {
        "total_revisados": len(libros),
        "total_inconsistencias": 0,
        "conteo_por_tipo": {
            "ESTADO_INVALIDO": 0,
            "PRESTADO_SIN_USUARIO": 0,
            "DISPONIBLE_CON_USUARIO": 0
        }
    }

    for libro in libros:
        error = None
        estado = libro.get('estado')
        usuario = libro.get('prestado_a')

        if estado not in ["Disponible", "Prestado"]:
            error = "ESTADO_INVALIDO"
        
        elif estado == "Prestado" and (usuario is None or usuario.strip() == ""):
            error = "PRESTADO_SIN_USUARIO"
            
        elif estado == "Disponible" and (usuario is not None and usuario.strip() != ""):
            error = "DISPONIBLE_CON_USUARIO"

        if error:
            resumen["total_inconsistencias"] += 1
            resumen["conteo_por_tipo"][error] += 1
            
            inconsistencias.append({
                "titulo": libro.get("titulo"),
                "autor": libro.get("autor"),
                "estado": estado,
                "prestado_a": usuario,
                "tipo_inconsistencia": error
            })

    resultado_final = {
        "libros_con_problemas": inconsistencias,
        "resumen_auditoria": resumen
    }

    if not os.path.exists("data/reportes"):
        os.makedirs("data/reportes")
        
    with open(REPORTE_AUDITORIA, "w") as f:
        json.dump(resultado_final, f, indent=4)

    print(f"\nAuditoría completada. Se encontraron {resumen['total_inconsistencias']} errores.")
    print(f"Reporte generado en: {REPORTE_AUDITORIA}")