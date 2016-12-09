from .models import Pet

def pets_processor(request):
    return {'pets': Pet.objects.all()}
