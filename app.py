from flask import Flask, render_template, request, url_for, Response
import numpy as np
import matplotlib.pyplot as plt

import io
import base64
import os

# Set Matplotlib to non-GUI backend
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__, static_folder='static')


@app.route('/', methods=['GET', 'HEAD'])
def home():
    if request.method == 'HEAD':
        return Response(status=200)
    return render_template('index.html')


def draw_square(step):
    fig, ax = plt.subplots(figsize=(10, 10))  # Increased figure size
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.set_aspect(1)
    plt.title(f"Śulba Sūtra Square Construction - Step {step}")

    # Step 1: Draw the vertical center line AB
    A, B = (0, -1), (0, 1)  # Vertical line AB
    O = (0, 0)  # Midpoint of AB
    r = abs(A[1] - O[1])  # Radius OA or OB (since A and B are on the Y-axis)
    
    ax.plot([A[0], B[0]], [A[1], B[1]], 'k-', linewidth=2, label="Line AB")
    ax.text(A[0], A[1], "A", fontsize=12, verticalalignment='bottom')
    ax.text(B[0], B[1], "B", fontsize=12, verticalalignment='bottom')
    ax.text(O[0], O[1], "O", fontsize=12, color='blue', verticalalignment='bottom')
    
    # Step 2: Draw circle centered at O with radius OA
    circle_O = plt.Circle(O, r, fill=False, linestyle='dashed', edgecolor='brown')
    ax.add_patch(circle_O)

    # Step 3: Draw circles centered at A and B with radius AB
    if step >= 2:
        radius = abs(A[1] - B[1])  # Distance AB (since A and B are on Y-axis)
        circle_A = plt.Circle(A, radius, fill=False, linestyle='dashed', edgecolor='blue')
        circle_B = plt.Circle(B, radius, fill=False, linestyle='dashed', edgecolor='blue')
        ax.add_patch(circle_A)
        ax.add_patch(circle_B)

    # Step 4: Find intersection points M and N
    if step >= 3:
        M, N = (-radius, 0), (radius, 0)  # M and N are on the X-axis
        ax.plot([M[0], N[0]], [M[1], N[1]], 'r-', linewidth=2, label="Line MN")
        ax.text(M[0], M[1], "M", fontsize=12, horizontalalignment='right')
        ax.text(N[0], N[1], "N", fontsize=12, horizontalalignment='left')

    # Step 5: Place points C and D such that AB = CD
    if step >= 4:
        C, D = (-1, 0), (1, 0)
        ax.text(C[0], C[1], "C", fontsize=12, horizontalalignment='right')
        ax.text(D[0], D[1], "D", fontsize=12, horizontalalignment='left')

    # Step 6: Draw circles centered at A, B, C, and D
    if step >= 5:
        circles = [
            plt.Circle(A, r, fill=False, linestyle='dashed', edgecolor='orange'),
            plt.Circle(B, r, fill=False, linestyle='dashed', edgecolor='orange'),
            plt.Circle(C, r, fill=False, linestyle='dashed', edgecolor='orange'),
            plt.Circle(D, r, fill=False, linestyle='dashed', edgecolor='orange')
        ]
        for c in circles:
            ax.add_patch(c)

    # Step 7: Find intersection points E, F, G, H
    if step >= 6:
        E, F, G, H = (-1, 1), (1, 1), (1, -1), (-1, -1)
        ax.text(E[0], E[1], "E", fontsize=12, verticalalignment='bottom')
        ax.text(F[0], F[1], "F", fontsize=12, verticalalignment='bottom')
        ax.text(G[0], G[1], "G", fontsize=12, verticalalignment='top')
        ax.text(H[0], H[1], "H", fontsize=12, verticalalignment='top')

    # Step 8: Join EFGH to form the final square
    if step >= 7:
        ax.plot([E[0], F[0]], [E[1], F[1]], 'b-', linewidth=2)
        ax.plot([F[0], G[0]], [F[1], G[1]], 'b-', linewidth=2)
        ax.plot([G[0], H[0]], [G[1], H[1]], 'b-', linewidth=2)
        ax.plot([H[0], E[0]], [H[1], E[1]], 'b-', linewidth=2)

    plt.legend()


# Call the function with the desired step
# draw_square(7)

    
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
    ax.set_ylim(-3, 25)
    ax.set_aspect(1)
    plt.title(f"Transforming Square to Triangle - Step {step}")

    # Step 1: Draw square ABCD
    s = 4  # Side length of the square ABCD
    A, B = (0, 0), (s, 0)
    C, D = (s, s), (0, s)
    ax.plot([A[0], B[0]], [A[1], B[1]], 'k-', linewidth=2,label="Line AB")
    ax.plot([B[0], C[0]], [B[1], C[1]], 'k-', linewidth=2, label="Line BC")
    ax.plot([C[0], D[0]], [C[1], D[1]], 'k-', linewidth=2, label="Line CD")
    ax.plot([D[0], A[0]], [D[1], A[1]], 'k-', linewidth=2, label="Line DA")
    ax.text(A[0], A[1], "A", fontsize=12)
    ax.text(B[0], B[1], "B", fontsize=12)
    ax.text(C[0], C[1], "C", fontsize=12)
    ax.text(D[0], D[1], "D", fontsize=12)


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
        ax.text(E[0], E[1], "E", fontsize=12)
        ax.text(F[0], F[1], "F", fontsize=12)
        ax.text(G[0], G[1], "G", fontsize=12)
        ax.text(H[0], H[1], "H", fontsize=12)

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
        ax.text(J[0], J[1], "J", fontsize=12)
        ax.text(H[0], H[1], "H", fontsize=12)
        ax.text(G[0], G[1], "G", fontsize=12)

    plt.legend()
    img_io = io.BytesIO()
    plt.savefig(img_io, format='png')
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
    ax.text(A[0], A[1], "A", fontsize=12)
    ax.text(B[0], B[1], "B", fontsize=12)
    ax.text(C[0], C[1], "C", fontsize=12)
    ax.text(D[0], D[1], "D", fontsize=12)
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
        ax.text(E[0], E[1], "E", fontsize=12)
        ax.text(F[0], F[1], "F", fontsize=12)
        ax.text(G[0], G[1], "G", fontsize=12)
        ax.text(H[0], H[1], "H", fontsize=12)
    # Step 4: Find midpoints J and K
    J = ((E[0] + H[0]) / 2, (E[1] + H[1]) / 2)
    K = ((F[0] + G[0]) / 2, (F[1] + G[1]) / 2)
    if step >= 4:
        ax.plot(J[0], J[1], 'ro', markersize=5, label="Midpoint J")
        ax.plot(K[0], K[1], 'ro', markersize=5, label="Midpoint K")
        ax.text(J[0], J[1], "J", fontsize=12)
        ax.text(K[0], K[1], "K", fontsize=12)
    # Step 5: Divide EF and HG into required proportions to find L and M
    L = (E[0] + (F[0] - E[0]) * 0.3, E[1])
    M = (H[0] + (G[0] - H[0]) * 0.3, H[1])
    if step >= 5:
        ax.plot(L[0], L[1], 'bo', markersize=5, label="Point L")
        ax.plot(M[0], M[1], 'bo', markersize=5, label="Point M")
        ax.text(L[0], L[1], "L", fontsize=12)
        ax.text(M[0], M[1], "M", fontsize=12)
    # Step 6: Divide JK into required proportion to find N
    N = (J[0] + (K[0] - J[0]) * 0.5, J[1] + (K[1] - J[1]) * 0.5)
    if step >= 6:
        ax.plot(N[0], N[1], 'bo', markersize=5, label="Point N")
        ax.text(N[0], N[1], "N", fontsize=12)

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
             shloka = "चतुरस्त्रं चिकिर्षन् यावच्चिकिर्षेत्तावती रज्जुमुभयतः पाशां कृत्वा मध्ये लक्षणं करोति लेखामालिख्य । 1.22.तस्या मध्ये शङ्कुं निहन्यात् तस्मिन् पाशौ प्रतिमुच्य लक्षणेन मण्डलं परिलिखेत् विष्कम्भान्तायोः शङ्कु निहन्यात्। 1.23. पूर्वस्मिन्  पाशं प्रतिमुच्य पाशेन मण्डलं परिलिखेत् । 1.24. एवमपरस्मिस्ते तत्र समेयातां तेन द्वितीयं विष्कम्भमायच्छेत्। 1.25. विष्कम्भान्तायोः शङ्कू निहन्यात् । 1.26. पूर्वस्मिन् पाशौ प्रतिमुच्य लक्षणेन मण्डलं परिलिखेत्। 1.27. एवं दक्षिणत एवं पश्चादेवमुत्तरतस्तेषाम् येन अन्त्याः संसर्गास्तच्चतुरस्त्र संपद्यते। 1.28"
             reference = "Baudhāyana Śulba Sūtra, 1.22 - 28"
             explanation = "This construction follows the principles of Śulba Sūtras, utilizing geometric methods to derive perfect square. Using the process of construction of square from circle , based on Sulba Sutra method of Pegs and rope in digital format,Draw a horizontal base line between points E and W. Mark the midpoint M and draw a circle around it. Draw two more circles from points E and W., The intersection of these circles gives the vertical line NS.Draw four more circles from points E, W, N, and S.The intersections of these circles form the square corners."
             
             steps = [
                "1. Draw the vertical center line AB",
                "2.  Draw circles centered at A and B with radius AB.",
                "3. Draw the horizontal line MN ",
                "4. Place points C and D such that AB = CD",
                "5. Draw circles centered at A, B, C, and D ",
                "6. Find intersection points E, F, G, H",
                "7. Join EFGH to form the final square"
            ]
             for i in range(1, 8):
                images.append(draw_square(i))

        elif shape.strip() == "square_to_triangle":
            shloka = "चतुरस्रं प्रउगं चिकीर्षन् यावच्चिकीर्षेद् द्विस्तावतीं भूमिः समचतुरस्त्रां कृत्वा पूर्वस्याः करण्या मध्ये शङ्कुं निहन्यात् तस्मिन् पाशौ प्रतिमुच्य दक्षिणोत्तरयोः श्रोण्योर्निपातयेत् बहिस्पन्द्यमपच्छिन्द्यात्।"
            reference = "Baudhāyana Śulba Sūtra, 1.56"
            explanation = "This transformation from square to triangle is based on geometric dissection principles. In this construction , we learnt about transformation of square into triangle of equal area. Draw square ABCD. Draw diagonal BD, Construct square EFGH, with side lenght equal to BD. Find midpoint J of EF. Join JH and JG. Final Triangle JHG."
     
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
              shloka = "पादेष्टकाश्चतुर्भिः परिगृह्णीयात्। 4.5 , अर्धपदेन पदेनाध्यर्धपदेन पद स विशेषेणेति । 4.6 ते द्वे यथा दीर्घसश्लिष्टे त्यातां तथार्धेष्टकां कारयेत्। 4.7"
              reference = "Baudhāyana Śulba Sūtra, 4.5 - 4.7"
              explanation = "This method constructs a pentagon using geometric principles derived from the Śulba Sūtras. Draw square ABCD. Draw diagonal BD. Construct a square EFGH with side length equal to BD. Find midpoint J of EH and midpoint K of FG. Divide EF and HG in the required proportion to get points L and M. Divide line JK in the required proportion to get point N. Join LN and MN to form the final pentagon FLNMG."
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
          
        # elif shape.strip() == "square_to_circle":
        #       shloka = "वर्गं वृत्तं कुर्वीत ... (your Sanskrit text here)"
        #       reference = "Baudhāyana Śulba Sūtra, 1.xx"
        #       explanation = "This transformation explains the conversion of a square into a circle ... (your explanation here)"

        #       steps = [
        #         "1. Draw square ABCD.",
        #         "2. Draw diagonal AC.",
        #         "3. Mark midpoint E of AC.",
        #         "4. Draw arc with E as center and AE as radius.",
        #         "5. Locate F where arc intersects center line.",
        #         "6. Divide FH such that FG = 2GH.",
        #         "7. Draw final circle with center E and radius EG."
        #     ]
    
        #       for i in range(1, 8):
        #         images.append(draw_square_to_circle())

       
               
        else:
            print(f"Unknown shape received: {shape}")  
            return "Shape not supported yet."
        print("Final Shloka:", repr(shloka))
        print("Final Reference:", repr(reference))
        print("Final Explanation:", repr(explanation))
        print(f"Shape received: {shape.strip()}")

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
