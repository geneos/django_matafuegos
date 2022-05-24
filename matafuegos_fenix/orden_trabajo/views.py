<<<<<<< Updated upstream
=======
from django.shortcuts import render

# Create your views here.
from django_matafuegos.matafuegos_fenix.matafuegos.models import Matafuegos

def load_cities(request):
    cliente_id = request.GET.get('cliente')
    matafuegos = Matafuegos.objects.filter(cliente=cliente_id).order_by('id')
    return render(request, 'matafuegos_fenix/orden_trabajo/templates/dropdown.html', {'matafuegos': matafuegos})
>>>>>>> Stashed changes
