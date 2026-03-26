import streamlit as st
import requests
import base64
from user_details_form import get_user_details

# Load API keys
stability_api_key = st.secrets["stability_api_key"]
groq_api_key = st.secrets["groq_api_key"]

# Custom CSS for a luxurious UI theme
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
    }

    .title { 
        text-align: center; 
        font-size: 42px; 
        font-weight: 700; 
        color: var(--dark); 
        font-family: 'Playfair Display', serif;
        margin-bottom: 0.5rem;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
    }

    .subtitle { 
        text-align: center; 
        font-size: 24px; 
        font-weight: 300; 
        color: var(--accent); 
        font-family: 'Playfair Display', serif;
        margin-bottom: 2rem;
    }

    .container { 
        padding: 30px; 
        border-radius: 16px; 
        background-color: white; 
        box-shadow: 0 8px 30px rgba(0,0,0,0.08); 
        margin-bottom: 30px;
        border: 1px solid rgba(0,0,0,0.05);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--primary) 0%, var(--dark) 100%);
        color: white !important;
        padding: 20px;
    }

    /* Sidebar text color */
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Styling subheaders in the sidebar */
    [data-testid="stSidebar"] h2 {
        color: var(--secondary) !important;
        font-family: 'Playfair Display', serif;
        font-size: 24px !important;
        margin-top: 0;
    }

    /* Adjust font sizes and padding */
    [data-testid="stSidebar"] .stMarkdown {
        font-size: 16px !important;
        font-weight: 300 !important;
    }

    .sidebar-container { 
        padding: 20px;
        border-radius: 12px;
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(5px);
        margin-bottom: 20px;
    }

    .sidebar-container h2 {
        color: var(--secondary) !important;
        border-bottom: 1px solid rgba(255,255,255,0.2);
        padding-bottom: 10px;
    }

    .sidebar-container p {
        color: var(--light) !important;
    }

    .button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%) !important; 
        color: white !important;
        border-radius: 12px !important; 
        padding: 14px 24px !important;
        font-size: 18px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        border: none !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
    }

    .button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15) !important;
    }

    textarea {
        border: 2px solid var(--secondary) !important;
        border-radius: 12px !important;
        padding: 15px !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
    }

    textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 2px rgba(141, 110, 99, 0.2) !important;
    }

    /* Card styling for the generated image */
    .image-card {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        margin: 20px 0;
        border: 1px solid rgba(0,0,0,0.05);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .image-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.15);
    }

    /* Tips section styling */
    .tips-container {
        background-color: var(--light);
        border-left: 4px solid var(--accent);
        padding: 20px;
        border-radius: 0 12px 12px 0;
        margin: 20px 0;
        position: relative;
    }

    /* Loading animation */
    @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.6; }
    }

    .loading {
        animation: pulse 1.5s infinite;
        text-align: center;
        color: var(--accent);
        font-size: 18px;
    }

    /* Rating stars */
    .rating-star {
        border: none; 
        background: rgba(141, 110, 99, 0.1);
        width: 30px; 
        height: 30px; 
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .rating-star:hover {
        background: rgba(141, 110, 99, 0.3);
        transform: scale(1.1);
    }

    .rating-star.active {
        background: var(--accent);
        color: white;
    }

    /* Social buttons */
    .social-btn {
        margin: 0; 
        border: none; 
        border-radius: 6px; 
        padding: 8px 20px;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 8px;
        transition: all 0.3s ease;
        color: white;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .container {
            padding: 20px;
        }
        .title {
            font-size: 32px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state variables
if "user_details" not in st.session_state:
    st.session_state.user_details = None

if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False

# App header
st.markdown('<h1 class="title">Fashion AI Stylist</h1>', unsafe_allow_html=True)

# Display the form on the main page if not submitted
if not st.session_state.form_submitted:
    user_details = get_user_details()
    if user_details:
        st.session_state.user_details = user_details
        st.session_state.form_submitted = True
        st.success("✅ Profile successfully updated!")
        st.balloons()
        st.rerun()

else:
    st.markdown('<h2 class="subtitle">Your Personal Digital Styling Assistant</h2>', unsafe_allow_html=True)

    # Get user details from session state
    user = st.session_state.user_details
    
    # Sidebar profile section with enhanced design
    with st.sidebar:
        # Main profile card
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #6D4C41 0%, #3E2723 100%); 
                    padding: 25px; 
                    border-radius: 16px; 
                    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
                    margin-bottom: 30px;
                    border: 1px solid rgba(255,255,255,0.1);">
            <h2 style="color: #D7CCC8; 
                       font-family: 'Playfair Display', serif; 
                       border-bottom: 1px solid rgba(255,255,255,0.2);
                       padding-bottom: 12px;
                       margin-top: 0;
                       display: flex;
                       align-items: center;
                       gap: 10px;">
                <span style="font-size: 24px;">-</span>
            </h2>
            <div style="display: flex; align-items: center; margin-bottom: 20px;">
                <div style="width: 70px; height: 70px; 
                            background: rgba(255,255,255,0.1); 
                            border-radius: 50%; 
                            display: flex; 
                            align-items: center; 
                            justify-content: center;
                            margin-right: 15px;
                            border: 2px solid #BCAAA4;
                            box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
                    <span style="font-size: 28px;">{'👩' if user['gender'].lower() == 'female' else '👨'}</span>
                </div>
                <div>
                    <h3 style="color: white; margin: 0; font-size: 18px; font-weight: 600;">
                        {user['gender']} Style Profile
                    </h3>
                    <p style="color: #D7CCC8; margin: 5px 0 0; font-size: 14px; 
                               display: flex; align-items: center; gap: 5px;">
                        <span style="color: #BCAAA4; font-size: 16px;">✦</span> {user['preferred_style']}
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Profile details grid with icons
        st.markdown(f"""
        <div style="display: grid; 
                    grid-template-columns: 1fr 1fr; 
                    gap: 12px; 
                    margin-bottom: 20px;">
            <div style="background: rgba(255,255,255,0.08); 
                        padding: 12px; 
                        border-radius: 10px;
                        border-left: 3px solid #8D6E63;
                        transition: all 0.3s ease;">
                <p style="color: #BCAAA4; margin: 0 0 5px 0; font-size: 12px; 
                           display: flex; align-items: center; gap: 5px;">
                    <span>🎨</span> Skin Tone
                </p>
                <p style="color: white; margin: 0; font-weight: 500; font-size: 14px;">
                    {user['skin_tone']}
                </p>
            </div>
            <div style="background: rgba(255,255,255,0.08); 
                        padding: 12px; 
                        border-radius: 10px;
                        border-left: 3px solid #8D6E63;
                        transition: all 0.3s ease;">
                <p style="color: #BCAAA4; margin: 0 0 5px 0; font-size: 12px;
                           display: flex; align-items: center; gap: 5px;">
                    <span>💇</span> Hair Color
                </p>
                <p style="color: white; margin: 0; font-weight: 500; font-size: 14px;">
                    {user['hair_color']}
                </p>
            </div>
            <div style="background: rgba(255,255,255,0.08); 
                        padding: 12px; 
                        border-radius: 10px;
                        border-left: 3px solid #8D6E63;
                        transition: all 0.3s ease;">
                <p style="color: #BCAAA4; margin: 0 0 5px 0; font-size: 12px;
                           display: flex; align-items: center; gap: 5px;">
                    <span>👁</span> Eye Color
                </p>
                <p style="color: white; margin: 0; font-weight: 500; font-size: 14px;">
                    {user['eye_color']}
                </p>
            </div>
            <div style="background: rgba(255,255,255,0.08); 
                        padding: 12px; 
                        border-radius: 10px;
                        border-left: 3px solid #8D6E63;
                        transition: all 0.3s ease;">
                <p style="color: #BCAAA4; margin: 0 0 5px 0; font-size: 12px;
                           display: flex; align-items: center; gap: 5px;">
                    <span>📏</span> Height
                </p>
                <p style="color: white; margin: 0; font-weight: 500; font-size: 14px;">
                    {user['height']} cm
                </p>
            </div>
            <div style="background: rgba(255,255,255,0.08); 
                        padding: 12px; 
                        border-radius: 10px;
                        border-left: 3px solid #8D6E63;
                        transition: all 0.3s ease;">
                <p style="color: #BCAAA4; margin: 0 0 5px 0; font-size: 12px;
                           display: flex; align-items: center; gap: 5px;">
                    <span>⚖️</span> Weight
                </p>
                <p style="color: white; margin: 0; font-weight: 500; font-size: 14px;">
                    {user['weight']} kg
                </p>
            </div>
            <div style="background: rgba(255,255,255,0.08); 
                        padding: 12px; 
                        border-radius: 10px;
                        border-left: 3px solid #8D6E63;
                        transition: all 0.3s ease;">
                <p style="color: #BCAAA4; margin: 0 0 5px 0; font-size: 12px;
                           display: flex; align-items: center; gap: 5px;">
                    <span>🌟</span> Style Age
                </p>
                <p style="color: white; margin: 0; font-weight: 500; font-size: 14px;">
                    {user.get('age', 'Timeless')}
                </p>
            </div>
        </div>
        </div>
        """, unsafe_allow_html=True)

        # Style personality section with animated progress bar
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.1); 
                    padding: 20px; 
                    border-radius: 16px; 
                    margin-bottom: 25px;
                    border: 1px dashed rgba(255,255,255,0.2);
                    transition: all 0.3s ease;">
            <h3 style="color: #D7CCC8; 
                       font-family: 'Playfair Display', serif; 
                       font-size: 18px;
                       margin-top: 0;
                       display: flex;
                       align-items: center;
                       gap: 8px;">
                <span style="font-size: 20px;">✨</span> Style Personality
            </h3>
            <div style="background: rgba(255,255,255,0.05); 
                        padding: 15px; 
                        border-radius: 12px;
                        text-align: center;">
                <p style="color: #BCAAA4; font-size: 16px; margin-bottom: 10px; font-weight: 500;">
                    {user['preferred_style']}
                </p>
                <div style="height: 6px; 
                            background: rgba(255,255,255,0.1); 
                            border-radius: 3px;
                            margin-bottom: 10px;
                            overflow: hidden;">
                    <div style="height: 100%; 
                                width: 85%; 
                                background: linear-gradient(90deg, #8D6E63, #D7CCC8);
                                border-radius: 3px;
                                animation: progress 2s ease-in-out;">
                    </div>
                </div>
                <p style="color: rgba(255,255,255,0.7); font-size: 12px; margin: 0;">
                    "Your style is 85% match with {user['preferred_style']} aesthetics"
                </p>
            </div>
        </div>
        <style>
            @keyframes progress {{
                0% {{ width: 0%; }}
                100% {{ width: 85%; }}
            }}
        </style>
        """, unsafe_allow_html=True)

        # Edit profile button with icon animation
        if st.button("✏️ Edit My Style Profile", 
                    use_container_width=True, 
                    key="edit_profile_btn",
                    help="Update your style preferences and measurements"):
            st.session_state.form_submitted = False
            st.rerun()

        # Inspirational quote with fading animation
        st.markdown("""
            <div style="font-style: italic; 
                        text-align: center; 
                        color: rgba(255,255,255,0.7); 
                        margin-top: 20px;
                        font-size: 13px;
                        padding: 15px;
                        border-top: 1px solid rgba(255,255,255,0.1);
                        animation: fadeIn 2s ease-in;">
                "Fashion is the armor to survive the reality of everyday life."<br>
                — Bill Cunningham
            </div>
            <style>
                @keyframes fadeIn {
                    from { opacity: 0; }
                    to { opacity: 1; }
                }
            </style>
        """, unsafe_allow_html=True)

    # Main content container
    with st.container():
        st.markdown('<div class="container">', unsafe_allow_html=True)
        
        # Outfit description section with elegant design
        st.markdown("""
            <div style="margin-bottom: 30px;">
                <h2 style="font-family: 'Playfair Display', serif; 
                           color: var(--dark); 
                           border-bottom: 2px solid var(--secondary); 
                           padding-bottom: 10px;
                           display: flex;
                           align-items: center;
                           gap: 10px;">
                    <span style="font-size: 28px;">✨</span> Describe Your Outfit
                </h2>
                <p style="color: var(--accent); font-size: 16px; margin-bottom: 20px;">
                Be as detailed as possible about the outfit you'd like to create. Include colors, 
                fabrics, accessories, and the occasion.
            </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Enhanced text area with character counter
        col1, col2 = st.columns([0.85, 0.15])
        with col1:
            outfit_description = st.text_area(
                "",
                placeholder="Example: 'A flowy emerald green midi dress with gold accessories for a summer garden party...'",
                height=150,
                key="outfit_desc",
                label_visibility="collapsed"
            )
        with col2:
            st.markdown("""
                <div style="height: 100%; 
                            display: flex; 
                            align-items: flex-end; 
                            justify-content: flex-end;
                            padding-bottom: 10px;">
                    <p style="color: var(--accent); 
                              font-size: 12px; 
                              margin: 0;
                              opacity: 0.7;">
                        Max 500 chars
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        if outfit_description:
            # Add a loading state with better animation
            with st.spinner(""):
                st.markdown("""
                    <div style="text-align: center; margin: 20px 0;">
                        <div style="display: inline-block; 
                                    padding: 15px 25px; 
                                    background: rgba(141, 110, 99, 0.1); 
                                    border-radius: 12px;
                                    animation: pulse 1.5s infinite;">
                            <p style="margin: 0; 
                                      color: var(--accent);
                                      font-size: 16px;
                                      display: flex;
                                      align-items: center;
                                      justify-content: center;
                                      gap: 10px;">
                                <span style="font-size: 20px;">👗</span> 
                                Creating your perfect outfit...
                            </p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Function to get fashion advice
                def get_fashion_advice(outfit_description, user_details):
                    # ✅ Prevent empty input (VERY IMPORTANT)
                    if not outfit_description:
                        return "Please enter an outfit description."

                    # ✅ Convert user_details dict → clean readable text
                    user_profile_text = f"""
                    Gender: {user_details.get('gender')}
                    Skin Tone: {user_details.get('skin_tone')}
                    Hair Color: {user_details.get('hair_color')}
                    Eye Color: {user_details.get('eye_color')}
                    Height: {user_details.get('height')} cm
                    Weight: {user_details.get('weight')} kg
                    Preferred Style: {user_details.get('preferred_style')}
                    Age: {user_details.get('age')}
                    """

                    # ✅ Clean prompt (no raw dict!)
                    prompt = f"""You are a professional fashion stylist.

                Generate detailed styling advice for the outfit below, considering the user's profile.

                Include:
                - Color combinations
                - Fabric suggestions
                - Accessories (jewelry, bags, shoes)
                - Occasion suitability
                - Fit recommendations

                Outfit Description:
                {outfit_description}

                User Profile:
                {user_profile_text}

                Respond in a friendly, stylish tone using bullet points.
                """

                    try:
                        response = requests.post(
                            "https://api.groq.com/openai/v1/chat/completions",
                            headers={
                                "Authorization": f"Bearer {groq_api_key}",
                                "Content-Type": "application/json"
                            },
                            json={
                                "model": "llama-3.1-8b-instant",
                                "messages": [
                                    {"role": "user", "content": prompt}
                                ]
                            },
                            timeout=30
                        )

                        # ✅ DEBUG (this will show REAL error if any)
                        if response.status_code != 200:
                            print("STATUS:", response.status_code)
                            print("ERROR RESPONSE:", response.text)
                            return "⚠️ API Error. Check console for details."

                        response_data = response.json()

                        # ✅ Safe parsing
                        return response_data.get("choices", [{}])[0].get("message", {}).get(
                            "content",
                            "No advice available."
                        )

                    except Exception as e:
                        print("EXCEPTION:", str(e))
                        return "We couldn't generate styling tips at this time. Please try again."

                # Function to generate outfit image using Stability AI
                def generate_outfit_image(prompt):
                    enhanced_prompt = f"""Fashion photography of a {st.session_state.user_details['gender']} model wearing: {prompt}. 
                    The model has {st.session_state.user_details['skin_tone']} skin, {st.session_state.user_details['hair_color']} hair, 
                    and {st.session_state.user_details['eye_color']} eyes. Full-body shot, luxury fashion, studio lighting, ultra-detailed."""

                    try:
                        response = requests.post(
                            "https://api.stability.ai/v2beta/stable-image/generate/core",
                            headers={
                                "Authorization": f"Bearer {stability_api_key}",
                                "Accept": "application/json"
                            },
                            files={
                                "prompt": (None, enhanced_prompt),
                                "model": (None, "stable-image-core"),   # ✅ REQUIRED
                                "output_format": (None, "png"),
                            },
                            timeout=60
                        )

                        # 🔴 Debug if error
                        if response.status_code != 200:
                            print("STATUS:", response.status_code)
                            print("ERROR:", response.text)
                            return None

                        data = response.json()

                        return data["image"]  # base64

                    except Exception as e:
                        print("EXCEPTION:", str(e))
                        return None

                # Generate fashion advice
                fashion_advice = get_fashion_advice(outfit_description, st.session_state.user_details)

                # Generate outfit image
                st.markdown("""
                    <div style="margin-top: 40px;">
                        <h2 style="font-family: 'Playfair Display', serif; 
                                   color: var(--dark); 
                                   border-bottom: 2px solid var(--secondary); 
                                   padding-bottom: 10px;
                                   display: flex;
                                   align-items: center;
                                   gap: 10px;">
                            <span style="font-size: 28px;">🎨</span> Your AI-Designed Outfit
                        </h2>
                        <p style="color: var(--accent); 
                                  font-size: 14px; 
                                  margin-top: 5px;">
                            Custom tailored for your style preferences
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                
                outfit_image_base64 = generate_outfit_image(outfit_description)

                if outfit_image_base64:
                    # Enhanced image card with hover effect
                    st.markdown("""
                        <div class="image-card" 
                             style="position: relative;">
                            <div style="position: absolute;
                                        top: 10px;
                                        right: 10px;
                                        background: rgba(0,0,0,0.5);
                                        color: white;
                                        padding: 5px 10px;
                                        border-radius: 20px;
                                        font-size: 12px;
                                        display: flex;
                                        align-items: center;
                                        gap: 5px;">
                                <span>🔄</span> AI Generated
                            </div>
                    """, unsafe_allow_html=True)
                    st.image(base64.b64decode(outfit_image_base64), 
                            caption="", 
                            use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Enhanced download button
                    st.download_button(
                        label="📥 Download Your Outfit Design",
                        data=base64.b64decode(outfit_image_base64),
                        file_name="ai_fashion_outfit.png",
                        mime="image/png",
                        use_container_width=True,
                        key="download_btn"
                    )
                    
                    # Style rating option
                    st.markdown("""
                        <div style="text-align: center; margin: 15px 0 25px;">
                            <p style="color: var(--accent); 
                                      font-size: 14px;
                                      margin-bottom: 10px;">
                                How well does this match your style?
                            </p>
                            <div style="display: flex; 
                                        justify-content: center; 
                                        gap: 5px;">
                                <button class="rating-star">1</button>
                                <button class="rating-star">2</button>
                                <button class="rating-star">3</button>
                                <button class="rating-star">4</button>
                                <button class="rating-star active">5</button>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Enhanced styling tips section
                st.markdown("""
                    <div class="tips-container" 
                         style="position: relative;
                                padding-top: 40px;">
                        <div style="position: absolute;
                                    top: 0;
                                    left: 0;
                                    background: var(--accent);
                                    color: white;
                                    padding: 5px 15px;
                                    border-radius: 0 0 12px 0;
                                    font-size: 14px;
                                    display: flex;
                                    align-items: center;
                                    gap: 8px;">
                            <span>💎</span> Stylist's Notes
                        </div>
                        <h3 style="font-family: 'Playfair Display', serif; 
                                   color: var(--primary); 
                                   margin-top: 0;
                                   margin-bottom: 15px;
                                   padding-top: 10px;">
                            Personalized Styling Recommendations
                        </h3>
                """, unsafe_allow_html=True)
                
                st.markdown(fashion_advice)
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Enhanced social sharing with tooltips
                st.markdown("""
                    <div style="text-align: center; margin-top: 30px;">
                        <p style="color: var(--accent); 
                                  font-weight: 500;
                                  margin-bottom: 15px;
                                  display: flex;
                                  align-items: center;
                                  justify-content: center;
                                  gap: 8px;">
                            <span style="font-size: 18px;">🌟</span> Love your outfit? Share it!
                        </p>
                        <div style="display: flex; 
                                    justify-content: center; 
                                    gap: 10px;
                                    flex-wrap: wrap;">
                            <button class="social-btn" style="background: #4267B2;">
                                <span>👍</span> Facebook
                            </button>
                            <button class="social-btn" style="background: #1DA1F2;">
                                <span>🐦</span> Twitter
                            </button>
                            <button class="social-btn" style="background: #E1306C;">
                                <span>📷</span> Instagram
                            </button>
                            <button class="social-btn" style="background: var(--accent);">
                                <span>📋</span> Copy Link
                            </button>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)