from flask import Flask, render_template, request, Response
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Ensure non-GUI mode for server deployment
import matplotlib.pyplot as plt
import io
import base64
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'HEAD'])
def home():
    if request.method == 'HEAD':
        return Response(status=200)
    return render_template('index.html')

def draw_square(step):
    print(f"Generating square diagram, step {step}")  # Debugging line
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_aspect(1)
    plt.title(f"Śulba Sūtra Square Construction - Step {step}")
    W, E = (-2, 0), (2, 0)
    M = ((W[0] + E[0]) / 2, (W[1] + E[1]) / 2)
    N, S = (0, 2), (0, -2)
    P1, P2, P3, P4 = (-2, 2), (2, 2), (2, -2), (-2, -2)
    ax.plot([W[0], E[0]], [W[1], E[1]], 'k-', linewidth=2)
    if step >= 2:
        circle_main = plt.Circle(M, abs(E[0] - M[0]), fill=False, linestyle='dashed', edgecolor='blue')
        ax.add_patch(circle_main)
    if step >= 3:
        circle_w = plt.Circle(W, abs(E[0] - M[0]), fill=False, linestyle='dashed', edgecolor='green')
        circle_e = plt.Circle(E, abs(E[0] - M[0]), fill=False, linestyle='dashed', edgecolor='green')
        ax.add_patch(circle_w)
        ax.add_patch(circle_e)
    if step >= 4:
        ax.plot([N[0], S[0]], [N[1], S[1]], 'r-', linewidth=2)
    if step >= 5:
        circle_n = plt.Circle(N, abs(E[0] - M[0]), fill=False, linestyle='dashed', edgecolor='orange')
        circle_s = plt.Circle(S, abs(E[0] - M[0]), fill=False, linestyle='dashed', edgecolor='orange')
        ax.add_patch(circle_n)
        ax.add_patch(circle_s)
    if step >= 6:
        ax.plot([P1[0], P2[0]], [P1[1], P2[1]], 'b-', linewidth=2)
        ax.plot([P2[0], P3[0]], [P2[1], P3[1]], 'b-', linewidth=2)
        ax.plot([P3[0], P4[0]], [P3[1], P4[1]], 'b-', linewidth=2)
        ax.plot([P4[0], P1[0]], [P4[1], P1[1]], 'b-', linewidth=2)
    plt.legend()
    img_io = io.BytesIO()
    plt.savefig(img_io, format='png', bbox_inches='tight')
    img_io.seek(0)
    encoded_img = base64.b64encode(img_io.getvalue()).decode('utf-8')
    plt.close(fig)
    return encoded_img

def draw_triangle_transformation(step):
    print(f"Generating triangle transformation diagram, step {step}")
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_aspect(1)
    plt.title(f"Triangle Transformation - Step {step}")
    if step >= 1:
        ax.plot([-2, 2, 2, -2, -2], [2, 2, -2, -2, 2], 'k-', linewidth=2)
    if step >= 2:
        ax.plot([0, -2], [0, 2], 'r-', linewidth=2)
    if step >= 3:
        ax.plot([0, 2], [0, 2], 'r-', linewidth=2)
    if step >= 4:
        ax.plot([-2, 0, 2, -2], [2, 0, 2, 2], 'b-', linewidth=2)
    img_io = io.BytesIO()
    plt.savefig(img_io, format='png', bbox_inches='tight')
    img_io.seek(0)
    encoded_img = base64.b64encode(img_io.getvalue()).decode('utf-8')
    plt.close(fig)
    return encoded_img

def draw_square_to_triangle(step):
    print(f"Generating square to triangle diagram, step {step}")
    return draw_triangle_transformation(step)

def draw_trapezium_to_triangle(step):
    print(f"Generating trapezium to triangle diagram, step {step}")
    return draw_triangle_transformation(step)

@app.route('/generate', methods=['POST'])
def generate():
    shape = request.form.get('shape')
    print(f"Shape selected: {shape}")  # Debugging line
    images, steps = [], []
    
    if shape == "square":
        steps = [
            "1. Draw a horizontal base line between points E and W.",
            "2. Mark the midpoint M and draw a circle around it.",
            "3. Draw two more circles from points E and W.",
            "4. The intersection of these circles gives the vertical line NS.",
            "5. Draw four more circles from points E, W, N, and S.",
            "6. The intersections of these circles form the square corners."
        ]
        for i in range(1, 7):
            images.append(draw_square(i))

    elif shape == "triangle":
        for i in range(1, 5):
            images.append(draw_triangle_transformation(i))
    
    elif shape == "square_to_triangle":
        for i in range(1, 7):
            images.append(draw_square_to_triangle(i))

    elif shape == "trapezium_to_triangle":
        for i in range(1, 4):
            images.append(draw_trapezium_to_triangle(i))
    
    return render_template('result.html', zipped_data=list(zip(images, steps)))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
