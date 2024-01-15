from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plt
import numpy as np

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def save_plot_power_function(p, image_path):
    x = np.linspace(0, 10, 400)
    y = x ** p

    plt.figure(figsize=(8, 6))
    plt.plot(x, y, label=f'y = x^{p}')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(f'Plot of y = x^{p}')
    plt.legend()
    plt.grid(True)
    plt.savefig(image_path)
    plt.close()

def plot_view(request):
    image_path = None

    if request.method == 'POST':
        p = request.POST.get('p')
        if p:
            try:
                p = float(p)  # Convert p to a floating-point number
                image_path = 'polls/static/plot.png'
                save_plot_power_function(p, image_path)
            except ValueError:
                # Handle the error if p is not a valid floating-point number
                pass

    return render(request, 'polls/plot.html', {'image_path': image_path})
