from flask import Flask, render_template, request, url_for, Response
app = Flask(__name__, static_folder='static')
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
    fig, ax = plt.subplots(figsize=(10, 10)) #increse figure size
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

def draw_square_to_triangle(step):
    plt.clf() # clear previous plot
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-3, 15)
    ax.set_ylim(-3, 20)
    ax.set_aspect(1)
    plt.title(f"Transforming Square to Triangle - Step {step}")

    # Step 1: Draw square ABCD
    s = 4  # Side length of the square ABCD
    A, B = (0, 0), (s, 0)
    C, D = (s, s), (0, s)
    ax.plot([A[0], B[0]], [A[1], B[1]], 'k-', linewidth=2)
    ax.plot([B[0], C[0]], [B[1], C[1]], 'k-', linewidth=2)
    ax.plot([C[0], D[0]], [C[1], D[1]], 'k-', linewidth=2)
    ax.plot([D[0], A[0]], [D[1], A[1]], 'k-', linewidth=2)

    # Step 2: Draw diagonal BD
    BD_length = s * np.sqrt(2)
    B, D = (0, 0), (s, s)
    if step >= 2:
        ax.plot([B[0], D[0]], [B[1], D[1]], 'b-', linewidth=2, label="Diagonal BD")

    # Step 3: Construct Square EFGH
   # Ensure E is correctly defined before using it
    E = (7, 0)  # Fixed starting point
    F = (E[0] + BD_length, E[1])  # Move right by BD_length
    G = (F[0], F[1] + BD_length)  # Move up by BD_length
    H = (E[0], E[1] + BD_length)  # Move up from E

    # Debugging: Print the values of the points
    print(f"E: {E}, F: {F}, G: {G}, H: {H}")

    if step >= 3:
        ax.plot([E[0], F[0]], [E[1], F[1]], 'g-', linewidth=2, label="EF")
        ax.plot([F[0], G[0]], [F[1], G[1]], 'g-', linewidth=2, label="FG")
        ax.plot([G[0], H[0]], [G[1], H[1]], 'g-', linewidth=2, label="GH")
        ax.plot([H[0], E[0]], [H[1], E[1]], 'g-', linewidth=2, label="HE")

    # Step 4: Find midpoint J of EF
    J = ((E[0] + F[0]) / 2, (E[1] + F[1]) / 2)
    if step >= 4:
        ax.plot(J[0], J[1], 'ro', markersize=5, label="Midpoint J")

    # Step 5: Join JH and JG
    if step >= 5:
        ax.plot([J[0], H[0]], [J[1], H[1]], 'r-', linewidth=2, label="Line JH")
        ax.plot([J[0], G[0]], [J[1], G[1]], 'r-', linewidth=2, label="Line JG")

    # Step 6: Final Triangle JHG
    if step >= 6:
        ax.fill([J[0], H[0], G[0]], [J[1], H[1], G[1]], 'b', alpha=0.3, label="Triangle JHG")

    plt.legend()
    img_io = io.BytesIO()
    plt.savefig(img_io, format='png', bbox_inches='tight')
    img_io.seek(0)
    encoded_img = base64.b64encode(img_io.getvalue()).decode('utf-8')
    plt.close(fig)

    return encoded_img


def draw_square_to_pentagon(step):
    plt.clf()
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-3, 15)
    ax.set_ylim(-3, 15)
    ax.set_aspect(1)
    plt.title(f"Transforming Square to Pentagon - Step {step}")

    # Step 1: Draw Square ABCD
    s = 5  # Side length of the square ABCD
    A, B = (0, 0), (s, 0)
    C, D = (s, s), (0, s)
    ax.plot([A[0], B[0]], [A[1], B[1]], 'k-', linewidth=2)
    ax.plot([B[0], C[0]], [B[1], C[1]], 'k-', linewidth=2)
    ax.plot([C[0], D[0]], [C[1], D[1]], 'k-', linewidth=2)
    ax.plot([D[0], A[0]], [D[1], A[1]], 'k-', linewidth=2)

    # Step 2: Draw diagonal BD
    BD_length = s * np.sqrt(2)
    B, D = (0, 0), (s, s)
    if step >= 2:
        ax.plot([B[0], D[0]], [B[1], D[1]], 'b-', linewidth=2, label="Diagonal BD")

    # Step 3: Construct Square EFGH with side BD
    E = (7, 0)
    F = (E[0] + BD_length, E[1])
    G = (F[0], F[1] + BD_length)
    H = (E[0], E[1] + BD_length)
    if step >= 3:
        ax.plot([E[0], F[0]], [E[1], F[1]], 'g-', linewidth=2)
        ax.plot([F[0], G[0]], [F[1], G[1]], 'g-', linewidth=2)
        ax.plot([G[0], H[0]], [G[1], H[1]], 'g-', linewidth=2)
        ax.plot([H[0], E[0]], [H[1], E[1]], 'g-', linewidth=2)

    # Step 4: Find midpoints J and K
    J = ((E[0] + H[0]) / 2, (E[1] + H[1]) / 2)
    K = ((F[0] + G[0]) / 2, (F[1] + G[1]) / 2)
    if step >= 4:
        ax.plot(J[0], J[1], 'ro', markersize=5, label="Midpoint J")
        ax.plot(K[0], K[1], 'ro', markersize=5, label="Midpoint K")

    # Step 5: Divide EF and HG into required proportions to find L and M
    L = (E[0] + (F[0] - E[0]) * 0.3, E[1])
    M = (H[0] + (G[0] - H[0]) * 0.3, H[1])
    if step >= 5:
        ax.plot(L[0], L[1], 'bo', markersize=5, label="Point L")
        ax.plot(M[0], M[1], 'bo', markersize=5, label="Point M")

    # Step 6: Divide JK into required proportion to find N
    N = (J[0] + (K[0] - J[0]) * 0.5, J[1] + (K[1] - J[1]) * 0.5)
    if step >= 6:
        ax.plot(N[0], N[1], 'bo', markersize=5, label="Point N")

    # Step 7: Draw Pentagon FLNMG
    if step >= 7:
        ax.plot([F[0], L[0]], [F[1], L[1]], 'b-', linewidth=2)
        ax.plot([L[0], N[0]], [L[1], N[1]], 'b-', linewidth=2)
        ax.plot([N[0], M[0]], [N[1], M[1]], 'b-', linewidth=2)
        ax.plot([M[0], G[0]], [M[1], G[1]], 'b-', linewidth=2)
        ax.plot([G[0], F[0]], [G[1], F[1]], 'b-', linewidth=2)
        ax.fill([F[0], L[0], N[0], M[0], G[0]], [F[1], L[1], N[1], M[1], G[1]], 'b', alpha=0.3)

    plt.legend()
    img_io = io.BytesIO()
    plt.savefig(img_io, format='png', bbox_inches='tight')
    img_io.seek(0)
    encoded_img = base64.b64encode(img_io.getvalue()).decode('utf-8')
    plt.close(fig)

    return encoded_img


@app.route('/generate', methods=['POST', 'GET'])
def generate():
    if request.method == 'POST':
        shape = request.form.get('shape')

        if not shape:
            return "Shape not selected. Please choose a shape."

        # Debugging: Print the value of 'shape'
        print(f"Shape received: {shape.strip()}")  # This will print in your terminal/log

        images = []
        steps = []
        shloka = ""
        reference = ""
        explanation = ""
        

        if shape == "square":
             shloka = "शुल्बसूत्रे निर्दिष्टाह स्क्वेर निर्माण कर्मा"
             reference = "Baudhāyana Śulba Sūtra, 1.2"
             explanation = "This construction follows the principles of Śulba Sūtras, utilizing geometric methods to derive perfect shapes."
             
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

        elif shape.strip() == "square_to_triangle":
            shloka = "त्रिकोणं चतुर्भुजस्य विशिष्ट रूपं"
            reference = "Baudhāyana Śulba Sūtra, 1.3"
            explanation = "This transformation from square to triangle is based on geometric dissection principles."
     
            steps = [
                "1. Draw square ABCD.",
                "2. Draw diagonal BD.",
                "3. Construct square EFGH, with side lenght equal to",
                "4. Find midpoint J of EF.",
                "5. Join JH and JG.",
                "6. Final Triangle JHG."
            ]  
            for i in range(1, 7):
                images.append(draw_square_to_triangle(i))
        elif shape.strip().lower() == "square_to_pentagon":
              shloka = "पञ्चकोणः विशेषं रूपं गणितशास्त्रे"
              reference = "Baudhāyana Śulba Sūtra, 1.4"
              explanation = "This method constructs a pentagon using geometric principles derived from the Śulba Sūtras."
            #   print("Processing square_to_pentagon...") 
              steps = [
                "1. Draw square ABCD.",
                "2. Draw diagonal BD.",
                "3. Construct a square EFGH with side length equal to BD.",
                "4. Find midpoint J of EH and midpoint K of FG.",
                "5. Divide EF and HG in the required proportion to get points L and M.",
                "6. Divide line JK in the required proportion to get point N.",
                "7. Join LN and MN to form the final pentagon FLNMG."
            ]  
              for i in range(1, 8):
                images.append(draw_square_to_pentagon(i))  
          

       
               
        else:
            print(f"Unknown shape received: {shape}")  
            return "Shape not supported yet."
        print("Final Shloka:", repr(shloka))
        print("Final Reference:", repr(reference))
        print("Final Explanation:", repr(explanation))
        zipped_data = zip(images, steps)
        
        return render_template('result.html', 
                                 zipped_data=list(zipped_data), 
                                 shloka=shloka, 
                                 reference=reference, 
                                 explanation=explanation)



    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Default Render port is 10000
    app.run(host='0.0.0.0', port=port)  # Removed debug=True for production
