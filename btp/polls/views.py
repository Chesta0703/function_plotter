# In your views.py

from django.shortcuts import render
from django.http import JsonResponse
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from .models import NetworkedEpi  # Import the NetworkedEpi class

def index(request):
    # Your existing index view
    return HttpResponse("Hello, world. You're at the polls index.")

def networked_epi_view(request):
    if request.method == 'POST':
        n = int(request.POST.get('n'))
        beta = np.array([request.POST.getlist(f'beta_{i}') for i in range(n)], dtype=float)
        gamma = np.array(request.POST.getlist('gamma'), dtype=float)

        epi_model = NetworkedEpi(n)
        epi_model.update_params(beta=beta, gamma=gamma)
        t0, tf = 0, 10  # Define your time range
        time_steps, S, I, R = epi_model.generate(t0, tf)

        # Convert plots to base64 images and send them back
        plots = []
        for i in range(n):
            plt.figure(figsize=(5, 4))
            plt.plot(time_steps, S[:, i], label='Susceptible')
            plt.plot(time_steps, I[:, i], label='Infected')
            plt.plot(time_steps, R[:, i], label='Recovered')
            plt.title(f"Node {i}")
            plt.legend()
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()
            encoded = base64.b64encode(image_png)
            encoded = encoded.decode('utf-8')
            plt.close()
            plots.append(encoded)

        return JsonResponse({'plots': plots})

    return render(request, 'polls/networked_epi.html', {})
