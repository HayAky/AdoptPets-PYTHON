from django.shortcuts import render

def panel_reportes(request):
    # Aquí luego agregaremos la lógica para filtrar y contar datos
    return render(request, 'reportes/panel.html')