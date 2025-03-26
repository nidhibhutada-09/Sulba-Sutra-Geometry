from flask import Flask, render_template, request, Response
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import os

# Set Matplotlib to non-GUI backend
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)

@app.route('/', methods=['GET', 'HEAD'])
def home():
    if request.method == 'HEAD':
        return Response(status=200)  # Return an empty response with HTTP 200 for HEAD requests
    return render_template('index.html')

def draw_square(step):
    fig, ax = plt.subplots()
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_aspect(1)
    plt.title(f"Śulba Sūtra Square Construction - Step {step}")

    # Define key points
    W, E = (-2, 0), (2, 0)  # West and East points
    M = ((W[0] + E[0]) / 2, (W[1] + E[1]) / 2)  # Midpoint
    N, S = (0, 2), (0, -2)  # North and South intersection points
    P1, P2, P3, P4 = (-2, 2), (2, 2), (2, -2), (-2, -2)  # Square corners

    # Step 1: Draw base line
    ax.plot([W[0], E[0]], [W[1], E[1]], 'k-', linewidth=2, label="Base Line EW")

    # Step 2: Draw midpoint circle
    if step >= 2:
        circle_main = plt.Circle(M, abs(E[0] - M[0]), fill=False, linestyle='dashed', edgecolor='blue')
        ax.add_patch(circle_main)

    # Step 3: Draw circles from W and E
    if step >= 3:
        circle_w = plt.Circle(W, abs(E[0] - M[0]), fill=False, linestyle='dashed', edgecolor='green')
        circle_e = plt.Circle(E, abs(E[0] - M[0]), fill=False, linestyle='dashed', edgecolor='green')
        ax.add_patch(circle_w)
        ax.add_patch(circle_e)

    # Step 4: Draw vertical diameter NS
    if step >= 4:
        ax.plot([N[0], S[0]], [N[1], S[1]], 'r-', linewidth=2, label="Vertical Diameter NS")

    # Step 5: Draw circles from N and S
    if step >= 5:
        circle_n = plt.Circle(N, abs(E[0] - M[0]), fill=False, linestyle='dashed', edgecolor='orange')
        circle_s = plt.Circle(S, abs(E[0] - M[0]), fill=False, linestyle='dashed', edgecolor='orange')
        ax.add_patch(circle_n)
        ax.add_patch(circle_s)

    # Step 6: Draw the final square (Including all previous steps)
    if step >= 6:
        ax.plot([P1[0], P2[0]], [P1[1], P2[1]], 'b-', linewidth=2)
        ax.plot([P2[0], P3[0]], [P2[1], P3[1]], 'b-', linewidth=2)
        ax.plot([P3[0], P4[0]], [P3[1], P4[1]], 'b-', linewidth=2)
        ax.plot([P4[0], P1[0]], [P4[1], P1[1]], 'b-', linewidth=2)

    plt.legend()

    # Save image to memory buffer and encode in base64
    img_io = io.BytesIO()
    plt.savefig(img_io, format='png', bbox_inches='tight')
    img_io.seek(0)
    encoded_img = base64.b64encode(img_io.getvalue()).decode('utf-8')
    plt.close(fig)  # Close figure to free memory

    return encoded_img

def draw_triangle_transformation(step):
    fig, ax = plt.subplots()
    ax.set_xlim(-1, 11)
    ax.set_ylim(-1, 11)
    ax.set_aspect(1)
    plt.title(f"Transforming Rectangle to Triangle - Step {step}")

    # Step 1: Draw square ABCD
    A, B, C, D = (0, 10), (10, 10), (10, 0), (0, 0)
    ax.plot([A[0], B[0]], [A[1], B[1]], 'k-', linewidth=2)
    ax.plot([B[0], C[0]], [B[1], C[1]], 'k-', linewidth=2)
    ax.plot([C[0], D[0]], [C[1], D[1]], 'k-', linewidth=2)
    ax.plot([D[0], A[0]], [D[1], A[1]], 'k-', linewidth=2)

    # Step 2: Identify midpoint M
    M = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2)
    if step >= 2:
        ax.plot(M[0], M[1], 'ro', markersize=5, label="Midpoint M")

    # Step 3: Draw diagonal lines DM and CM
    if step >= 3:
        ax.plot([D[0], M[0]], [D[1], M[1]], 'r-', linewidth=2, label="DM")
        ax.plot([C[0], M[0]], [C[1], M[1]], 'r-', linewidth=2, label="CM")

    # Step 4: Final Triangle MDC
    if step >= 4:
        ax.fill([D[0], M[0], C[0]], [D[1], M[1], C[1]], 'b', alpha=0.3, label="Final Triangle MDC")

    plt.legend()
    img_io = io.BytesIO()
    plt.savefig(img_io, format='png', bbox_inches='tight')
    img_io.seek(0)
    encoded_img = base64.b64encode(img_io.getvalue()).decode('utf-8')
    plt.close(fig)

    return encoded_img

@app.route('/generate', methods=['POST'])
def generate():
    shape = request.form.get('shape')
    if shape == "square":
        images = []
        steps = [
            "1. Draw a horizontal base line between points E and W.",
            "2. Mark the midpoint M and draw a circle around it.",
            "3. Draw two more circles from points E and W.",
            "4. The intersection of these circles gives the vertical line NS.",
            "5. Draw four more circles from points E, W, N, and S.",
            "6. The intersections of these circles form the square corners."
        ]

        # Generate images for each step, including previous steps
        for i in range(1, 7):
            images.append(draw_square(i))
     elif shape == "triangle":
        images = []
        steps = [
            "1. Draw a square with an area twice that of the rectangle.",
            "2. Identify the midpoint M of one side of the square.",
            "3. Connect M to the opposite corners of the square.",
            "4. The resulting triangle MDC has the same area as the rectangle."
        ]
        for i in range(1, 5):
            images.append(draw_triangle_transformation(i))
        

    else:
        return "Shape not supported yet."
   
     return render_template('result.html', zipped_data=list(zip(images, steps))) 
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Default Render port is 10000
    app.run(host='0.0.0.0', port=port)  # Removed debug=True for productio
