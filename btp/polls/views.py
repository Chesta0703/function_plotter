from django.http import JsonResponse, HttpResponseNotFound
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Ensure using non-GUI backend for matplotlib
import matplotlib.pyplot as plt
import io
import base64
from .models import NetworkedEpi  # Assuming your model is correctly set up
from django.shortcuts import render

def networked_epi_view(request):
    if request.method == 'POST':
        n = int(request.POST.get('n'))
        beta = np.array([request.POST.getlist(f'beta_{i}') for i in range(n)], dtype=float)
        gamma = np.array(request.POST.getlist('gamma'), dtype=float)

        request.session['beta'] = beta.tolist()
        request.session['gamma'] = gamma.tolist()

        epi_model = NetworkedEpi(n)
        epi_model.update_params(beta=beta, gamma=gamma)
        t0, tf = 0, 10
        time_steps, S, I, R = epi_model.generate(t0, tf)

        plots = []
        for i in range(n):
            fig, ax = plt.subplots(figsize=(5, 4))
            ax.plot(time_steps, S[:, i], label='Susceptible')
            ax.plot(time_steps, I[:, i], label='Infected')
            ax.plot(time_steps, R[:, i], label='Recovered')
            ax.set_title(f"Node {i}")
            ax.legend()
            buffer = io.BytesIO()
            fig.savefig(buffer, format='png')
            plt.close(fig)
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()
            encoded = base64.b64encode(image_png).decode('utf-8')
            plots.append(encoded)

        nodes = [{'id': i, 'label': f'Node {i}'} for i in range(n)]
        links = [{'source': i, 'target': j, 'weight': beta[i][j]} for i in range(n) for j in range(n) if beta[i][j] > 0]

        return JsonResponse({'plots': plots, 'graph': {'nodes': nodes, 'links': links}})

    return render(request, 'polls/networked_epi.html', {})

def get_sir_plot(request, node_id):
    beta = request.session.get('beta')
    gamma = request.session.get('gamma')

    if beta is None or gamma is None:
        return HttpResponseNotFound('Session data not found')

    try:
        node_id = int(node_id)
        beta = np.array(beta)
        gamma = np.array(gamma)
        n = beta.shape[0]

        if node_id >= n or node_id < 0:
            raise ValueError('Invalid node ID')

        epi_model = NetworkedEpi(n)
        epi_model.update_params(beta=beta, gamma=gamma)
        t0, tf = 0, 10
        time_steps, S, I, R = epi_model.generate(t0, tf)

        fig, ax = plt.subplots(figsize=(5, 4))
        ax.plot(time_steps, S[:, node_id], label='Susceptible')
        ax.plot(time_steps, I[:, node_id], label='Infected')
        ax.plot(time_steps, R[:, node_id], label='Recovered')
        ax.set_title(f"Node {node_id}")
        ax.legend()
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png')
        plt.close(fig)
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        encoded = base64.b64encode(image_png).decode('utf-8')

        return JsonResponse({'plot': encoded})

    except ValueError as e:
        return HttpResponseNotFound(str(e))
