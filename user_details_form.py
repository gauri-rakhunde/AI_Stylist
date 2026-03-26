import streamlit as st
from PIL import Image
import base64
from io import BytesIO

def get_user_details():
    # Custom CSS with enhanced animations and transitions
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Montserrat:wght@300;500;700&display=swap');
        
        :root {
            --primary: #6D4C41;
            --secondary: #D7CCC8;
            --accent: #8D6E63;
            --light: #EFEBE9;
            --dark: #3E2723;
            --highlight: #BCAAA4;
        }
        
        body {
            font-family: 'Montserrat', sans-serif;
            background-color: var(--light);
        }
        
        .stApp {
            background: linear-gradient(135deg, #F9F5F0 0%, #EFEBE9 100%);
            animation: fadeIn 1s ease-out;
        }
        
        .form-container {
            background: white;
            padding: 2.5rem;
            border-radius: 16px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.08);
            border: 1px solid rgba(0,0,0,0.05);
            margin: 1.5rem 0;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.1);
        }
        
        .form-container:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(0,0,0,0.12);
        }
        
        .form-header {
            font-family: 'Playfair Display', serif;
            color: var(--dark);
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            text-align: center;
            position: relative;
            animation: slideIn 0.8s ease-out;
        }
        
        .form-header:after {
            content: "";
            display: block;
            width: 80px;
            height: 3px;
            background: linear-gradient(90deg, var(--accent), var(--highlight));
            margin: 1rem auto;
            animation: expandLine 1s ease-out;
        }
        
        .form-subheader {
            color: var(--accent);
            font-family: 'Montserrat', sans-serif;
            font-size: 1rem;
            text-align: center;
            margin-bottom: 2rem;
            opacity: 0;
            animation: fadeIn 1s ease-out 0.3s forwards;
        }
        
        .stButton>button {
            background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%) !important;
            color: white !important;
            border-radius: 12px !important;
            padding: 0.8rem 2rem !important;
            font-size: 1rem !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
            border: none !important;
            box-shadow: 0 4px 15px rgba(109, 76, 65, 0.3) !important;
            width: 100%;
            margin-top: 1.5rem;
            position: relative;
            overflow: hidden;
        }
        
        .stButton>button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 8px 25px rgba(109, 76, 65, 0.4) !important;
        }
        
        .stButton>button:after {
            content: "";
            position: absolute;
            top: 50%;
            left: 50%;
            width: 5px;
            height: 5px;
            background: rgba(255, 255, 255, 0.5);
            opacity: 0;
            border-radius: 100%;
            transform: scale(1, 1) translate(-50%);
            transform-origin: 50% 50%;
        }
        
        .stButton>button:focus:not(:active)::after {
            animation: ripple 1s ease-out;
        }
        
        .stSelectbox, .stSlider, .stNumberInput {
            border: 2px solid var(--secondary) !important;
            border-radius: 12px !important;
            padding: 0.8rem !important;
            transition: all 0.3s ease !important;
        }
        
        .stSelectbox:hover, .stSlider:hover, .stNumberInput:hover {
            border-color: var(--highlight) !important;
        }
        
        .stSelectbox:focus, .stSlider:focus, .stNumberInput:focus {
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 3px rgba(141, 110, 99, 0.2) !important;
        }
        
        .form-label {
            font-weight: 500;
            color: var(--dark);
            margin-bottom: 0.5rem;
            display: block;
            font-size: 0.95rem;
            opacity: 0;
            animation: fadeIn 0.6s ease-out forwards;
            animation-delay: calc(var(--order) * 0.1s);
        }
        
        .image-column {
            display: flex;
            flex-direction: column;
            gap: 1.2rem;
        }
        
        .image-card {
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 6px 20px rgba(0,0,0,0.1);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.1);
            aspect-ratio: 3/4;
            position: relative;
        }
        
        .image-card:hover {
            transform: scale(1.03);
            box-shadow: 0 12px 30px rgba(0,0,0,0.15);
        }
        
        .image-card img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.5s ease;
        }
        
        .image-card:hover img {
            transform: scale(1.05);
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes expandLine {
            from { width: 0; opacity: 0; }
            to { width: 80px; opacity: 1; }
        }
        
        @keyframes ripple {
            0% { transform: scale(0, 0); opacity: 1; }
            20% { transform: scale(25, 25); opacity: 1; }
            100% { opacity: 0; transform: scale(40, 40); }
        }
        
        @media (max-width: 768px) {
            .form-header {
                font-size: 1.8rem;
            }
            
            .form-container {
                padding: 1.5rem;
            }
        }
        </style>
    """, unsafe_allow_html=True)

    # Create columns with adjusted spacing
    col1, col2, col3 = st.columns([2, 6, 2], gap="large")
    
    # Sample local image paths 
    left_images = ["left.jpg", "i2.jpg", "i3.jpg","i5.jpg","i7.jpg"]
    right_images = ["right.jpg", "i1.jpg", "i4.jpg","i6.jpg","i8.jpg"]
    
    # Left image column with error handling
    with col1:
        st.markdown('<div class="image-column">', unsafe_allow_html=True)
        for img_path in left_images:
            try:
                img = Image.open(img_path)
                st.markdown(f"""
                    <div class="image-card">
                        <img src="data:image/png;base64,{image_to_base64(img)}" alt="Fashion inspiration">
                    </div>
                """, unsafe_allow_html=True)
            except:
                st.markdown(f"""
                    <div class="image-card" style="background: #f5f5f5; display: flex; align-items: center; justify-content: center;">
                        <span style="color: var(--accent);">Image not found</span>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Right image column with error handling
    with col3:
        st.markdown('<div class="image-column">', unsafe_allow_html=True)
        for img_path in right_images:
            try:
                img = Image.open(img_path)
                st.markdown(f"""
                    <div class="image-card">
                        <img src="data:image/png;base64,{image_to_base64(img)}" alt="Fashion inspiration">
                    </div>
                """, unsafe_allow_html=True)
            except:
                st.markdown(f"""
                    <div class="image-card" style="background: #f5f5f5; display: flex; align-items: center; justify-content: center;">
                        <span style="color: var(--accent);">Image not found</span>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Form in center column
    with col2:
        st.markdown("""
            <div class="form-container">
                <h3 class="form-header">Create Your Style Profile</h3>
                <p class="form-subheader">Personalized fashion recommendations await - tell us about yourself</p>
        """, unsafe_allow_html=True)
        
        with st.form("user_details_form"):
            # Create two columns for form fields
            col_a, col_b = st.columns(2)
            
            with col_a:
                fields_a = [
                    ("Gender", ["Male", "Female", "Other"], "gender", 1),
                    ("Age", "", "age", 2),
                    ("Skin Tone", ["Fair", "Light", "Medium", "Olive", "Brown", "Dark"], "skin_tone", 3),
                    ("Preferred Style", ["Casual", "Formal", "Sporty", "Bohemian", "Streetwear", "Other"], "preferred_style", 4)
                ]
                
                for label, options, key, order in fields_a:
                    st.markdown(f'<p class="form-label" style="--order: {order}">{label}</p>', unsafe_allow_html=True)
                    if options == "":  # Slider for age
                        st.slider("", 10, 100, 25, key=key, label_visibility="collapsed")
                    else:
                        st.selectbox("", options, key=key, label_visibility="collapsed")
            
            with col_b:
                fields_b = [
                    ("Height (cm)", "", "height", 5),
                    ("Weight (kg)", "", "weight", 6),
                    ("Hair Color", ["Black", "Brown", "Blonde", "Red", "Gray", "Other"], "hair_color", 7),
                    ("Eye Color", ["Brown", "Blue", "Green", "Hazel", "Gray", "Other"], "eye_color", 8)
                ]
                
                for label, options, key, order in fields_b:
                    st.markdown(f'<p class="form-label" style="--order: {order}">{label}</p>', unsafe_allow_html=True)
                    if key in ["height", "weight"]:
                        st.number_input("", 
                                      min_value=100 if key == "height" else 30, 
                                      max_value=250 if key == "height" else 200, 
                                      value=170 if key == "height" else 70, 
                                      key=key, 
                                      label_visibility="collapsed")
                    else:
                        st.selectbox("", options, key=key, label_visibility="collapsed")
            
            submitted = st.form_submit_button("✨ Create My Style Profile")
            
            if submitted:
                user_details = {
                    "skin_tone": st.session_state.skin_tone,
                    "hair_color": st.session_state.hair_color,
                    "eye_color": st.session_state.eye_color,
                    "gender": st.session_state.gender,
                    "age": st.session_state.age,
                    "height": st.session_state.height,
                    "weight": st.session_state.weight,
                    "preferred_style": st.session_state.preferred_style
                }
                return user_details
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    return None

def image_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()