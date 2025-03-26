from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

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
    P, Q, R, S = (-2, 2), (2, 2), (2, -2), (-2, -2)  # Square corners

    # Step 1: Draw base line
    ax.plot([W[0], E[0]], [W[1], E[1]], 'k-', linewidth=2, label="Base Line EW")

    # Step 2: Draw midpoint circle
    if step >= 2:
        circle_main = plt.Circle(M, abs(E[0] - M[0]), fill=False, linestyle='dashed')
        ax.add_patch(circle_main)

    # Step 3: Draw circles from W and E
    if step >= 3:
        circle_w = plt.Circle(W, abs(E[0] - M[0]), fill=False, linestyle='dashed')
        circle_e = plt.Circle(E, abs(E[0] - M[0]), fill=False, linestyle='dashed')
        ax.add_patch(circle_w)
        ax.add_patch(circle_e)

    # Step 4: Draw vertical diameter NS
    if step >= 4:
        ax.plot([N[0], S[0]], [N[1], S[1]], 'r-', linewidth=2, label="Vertical Diameter NS")

    # Step 5: Draw circles from N and S
    if step >= 5:
        circle_n = plt.Circle(N, abs(E[0] - M[0]), fill=False, linestyle='dashed')
        circle_s = plt.Circle(S, abs(E[0] - M[0]), fill=False, linestyle='dashed')
        ax.add_patch(circle_n)
        ax.add_patch(circle_s)

    # Step 6: Draw the final square (Including all previous steps)
    if step >= 6:
        ax.plot([P[0], Q[0]], [P[1], Q[1]], 'b-', linewidth=2)
        ax.plot([Q[0], R[0]], [Q[1], R[1]], 'b-', linewidth=2)
        ax.plot([R[0], S[0]], [R[1], S[1]], 'b-', linewidth=2)
        ax.plot([S[0], P[0]], [S[1], P[1]], 'b-', linewidth=2)

    plt.legend()

    # Save image to memory buffer and encode in base64
    img_io = io.BytesIO()
    plt.savefig(img_io, format='png')
    img_io.seek(0)
    encoded_img = base64.b64encode(img_io.getvalue()).decode('utf-8')
    plt.close()

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

        return render_template('result.html', zipped_data=list(zip(images, steps)))

    else:
        return "Shape not supported yet."

if __name__ == '__main__':
    app.run(debug=True)
