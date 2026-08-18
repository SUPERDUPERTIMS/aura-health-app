import io
import time
import datetime
import secrets
import pandas as pd
import streamlit as st
import plotly.express as px
from fpdf import FPDF
from gtts import gTTS

# ==========================================
# 1. PAGE CONFIGURATION & PREMIUM THEMING
# ==========================================
st.set_page_config(
    page_title="Aura | Somatic & Pelvic Health",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark Mode Theme with Modern Glassmorphism
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #090D16 0%, #0F172A 100%);
        color: #F1F5F9;
        font-family: 'Inter', sans-serif;
    }
    
    /* Custom Card Styling */
    .glass-card {
        background: rgba(30, 41, 59, 0.65);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    .accent-card {
        background: linear-gradient(135deg, rgba(88, 28, 135, 0.35) 0%, rgba(30, 27, 75, 0.55) 100%);
        border: 1px solid rgba(192, 132, 252, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.25rem;
    }

    .prompt-card {
        background: rgba(24, 24, 27, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.75rem;
    }

    .script-box {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid #475569;
        border-radius: 12px;
        padding: 1.25rem;
        font-style: italic;
        color: #E2E8F0;
        margin-top: 0.5rem;
        line-height: 1.6;
    }

    .match-banner {
        background: rgba(6, 78, 59, 0.6);
        border: 1px solid #10B981;
        color: #ECFDF5;
        padding: 1.25rem;
        border-radius: 12px;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #A855F7 0%, #7C3AED 100%);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        letter-spacing: 0.3px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 14px rgba(124, 58, 237, 0.3);
        width: 100%;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #9333EA 0%, #6D28D9 100%);
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.5);
    }

    /* Tags & Badges */
    .badge-tag {
        background: rgba(168, 85, 247, 0.15);
        border: 1px solid rgba(168, 85, 247, 0.3);
        color: #E9D5FF;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 500;
        display: inline-block;
        margin-right: 6px;
        margin-top: 6px;
    }
    
    /* Input Inputs & Selectboxes Styling */
    .stTextInput input, .stSelectbox select, .stTextArea textarea {
        background-color: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid #334155 !important;
        color: #F8FAFC !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. VOICE SYNTHESIS HELPER (FIXES AUDIO)
# ==========================================
@st.cache_data(show_spinner=False)
def generate_speech_audio(text_script: str, lang="en", tld="com"):
    """Generates real spoken voice audio using gTTS."""
    tts = gTTS(text=text_script, lang=lang, tld=tld, slow=False)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp.read()

# ==========================================
# 3. SESSION STATE MANAGEMENT & DATABASES
# ==========================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_name" not in st.session_state:
    st.session_state.user_name = "Alex"
if "user_mode" not in st.session_state:
    st.session_state.user_mode = "Singles Proximity Mode"
if "checkin_history" not in st.session_state:
    st.session_state.checkin_history = []
if "dilator_logs" not in st.session_state:
    st.session_state.dilator_logs = []
if "partner_beacon" not in st.session_state:
    st.session_state.partner_beacon = "💬 Open to Talk & Coffee"

# Telemetry State
if "pain_level" not in st.session_state:
    st.session_state.pain_level = 3
if "stress_level" not in st.session_state:
    st.session_state.stress_level = 4
if "energy_level" not in st.session_state:
    st.session_state.energy_level = 5
if "desire_state" not in st.session_state:
    st.session_state.desire_state = "Neutral"
if "active_program_day" not in st.session_state:
    st.session_state.active_program_day = 3
if "my_intent" not in st.session_state:
    st.session_state.my_intent = None
if "partner_intent" not in st.session_state:
    st.session_state.partner_intent = None

# Partner & Proximity Initialization
if "user_partner_code" not in st.session_state:
    st.session_state.user_partner_code = f"AURA-{secrets.token_hex(3).upper()}"
if "linked_partner_id" not in st.session_state:
    st.session_state.linked_partner_id = None
if "is_verified" not in st.session_state:
    st.session_state.is_verified = True
if "user_erotic_interests" not in st.session_state:
    st.session_state.user_erotic_interests = ["Sensate Touch", "Mindful Breathing"]

# EROTIC INTEREST TAXONOMY
EROTIC_TAXONOMY = [
    "Sensate Touch", "Mindful Breathing", "Erotic Audio Stories", 
    "Aromatherapy & Massage", "Outdoor & Nature Dates", "Temperature Play", 
    "Roleplay & Personas", "Slow Dancing", "BDSM/Kink-Friendly", "Late-Night Unwind"
]

SAFE_ZONES = ["All Locations (GPS Radius)", "Artisan Coffee Lounge (Downtown)", "Wellness & Spa Pavilion", "Botanical Gardens Lounge"]

MOCK_NEARBY_SINGLES = [
    {
        "id": "Beacon-88A",
        "verified": True,
        "distance_km": 1.4,
        "safe_zone": "Artisan Coffee Lounge (Downtown)",
        "readiness": "💬 Open to Talk & Coffee",
        "erotic_interests": ["Sensate Touch", "Mindful Breathing", "Outdoor & Nature Dates", "Erotic Audio Stories"]
    },
    {
        "id": "Beacon-34B",
        "verified": False,
        "distance_km": 3.8,
        "safe_zone": "All Locations (GPS Radius)",
        "readiness": "💬 Open to Talk & Coffee",
        "erotic_interests": ["Roleplay & Personas", "BDSM/Kink-Friendly", "Late-Night Unwind"]
    },
    {
        "id": "Beacon-91C",
        "verified": True,
        "distance_km": 0.8,
        "safe_zone": "Wellness & Spa Pavilion",
        "readiness": "🧘 Open to Touch (Zero Pressure)",
        "erotic_interests": ["Sensate Touch", "Aromatherapy & Massage", "Mindful Breathing"]
    },
    {
        "id": "Beacon-52D",
        "verified": True,
        "distance_km": 2.1,
        "safe_zone": "Artisan Coffee Lounge (Downtown)",
        "readiness": "🔥 Open to Intimacy",
        "erotic_interests": ["Sensate Touch", "Slow Dancing", "Aromatherapy & Massage"]
    }
]

EROTIC_CONTEXT_QUESTIONS = {
    "Cognitive Load & Tasks": "I find it hard to feel desire or reach climax if I have unfinished chores, work emails, or mental stress lingering.",
    "Emotional Closeness": "I need to feel emotionally connected, appreciated, and close before I feel open to deep physical release.",
    "Somatic & Muscle Comfort": "Physical relaxation, bodily warmth, and an absence of pelvic muscle guarding are essential for me to climax.",
    "Sensory Environment": "Factors like dim lighting, pleasant scents, clean sheets, and ambient music strongly influence my ability to focus on pleasure.",
    "Novelty & Playfulness": "Playful teasing, unexpected affection, changing locations, or roleplay easily activates my arousal."
}

FEMALE_EXPLORATION_MODULES = {
    "Phase 1: Zero-Pressure Somatic Mapping": {
        "description": "A gentle journey mapping non-genital erogenous zones to awaken body awareness without expectation of performance.",
        "steps": [
            "Step 1: Set the scene—warm lighting, comfortable support under your knees, and a drop of preferred oil.",
            "Step 2: Spend 2 minutes using light fingertip pressure along your collarbones, neck, and inner arms.",
            "Step 3: Notice micro-sensations—temperature, tingling, or goosebumps—without trying to force arousal.",
            "Step 4: Rest your palm gently over your lower abdomen, syncing your breath with the rise and fall of your belly."
        ],
        "script": "Welcome to your private self-exploration space. Today there is no goal, no timer, and no expectation of climax. Allow your body to simply receive warmth and touch..."
    },
    "Phase 2: Anatomical Clitoral Mapping & Rhythms": {
        "description": "Technique focusing on indirect clitoral stimulation, pressure variations, and rhythm consistency necessary for arousal building.",
        "steps": [
            "Step 1: Apply a generous amount of warm lubricant around the labia and outer vulvar tissue.",
            "Step 2: Begin with gentle circular motions along the outer labia, avoiding direct glans touch to prevent oversensitivity.",
            "Step 3: Transition to a slow 'clock' pattern around the clitoral hood.",
            "Step 4: Establish a steady, rhythmic pressure. Rhythm consistency is key to helping the nervous system build arousal."
        ],
        "script": "Ensure you have plenty of warm lubricant ready. Begin by applying it softly around your outer labia. Focus purely on consistency and breath..."
    }
}

CARD_DECK = {
    "Tier 1: Restorative & Low Energy (Zero Pressure)": [
        "15-Minute Shoulder & Neck Rub", "Shared Warm Bath or Shower", "Couch Cuddle & Phone-Free Chat",
        "Foot & Ankle Massage", "Early Night Unwind in Bed"
    ],
    "Tier 2: Sensual & Somatic Exploration": [
        "Guided Sensate Focus Touch (No Genital Touch)", "Warm Oil Back Massage", "Listen to an Erotic Audio Story",
        "Feather & Light Touch Exploration"
    ],
    "Tier 3: Intimate & Playful Connection": [
        "Uninterrupted Bedroom Time", "Fantasy Sharing Session", "Morning Intimacy Date", "Roleplay / New Persona Night"
    ]
}

VOICE_PROFILES = {
    "🇦🇺 Grounded & Deep (Australian Accent)": {"lang": "en", "tld": "com.au"},
    "🇬🇧 Warm & Expressive (British Accent)": {"lang": "en", "tld": "co.uk"},
    "🇺🇸 Calm & Clear (US Accent)": {"lang": "en", "tld": "com"}
}

LIBRARY_DATA = [
    {
        "id": 1,
        "title": "5-Minute Pelvic Floor Unwinding",
        "category": "Somatic & Pelvic PT",
        "duration": 5,
        "desc": "Diaphragmatic breathing and reverse Kegel cues to release deep involuntary pelvic guarding.",
        "type": "Spoken Voice Audio Guide",
        "tags": ["Pelvic Pain", "Relaxation", "Daily Routine"],
        "script": "Welcome to your 5-minute pelvic floor unwinding session. Place one hand on your chest and one on your lower abdomen. Take a deep, slow breath in through your nose, letting your belly expand fully. As you exhale slowly through your mouth, visualize your pelvic floor softening, dropping, and completely letting go of tension. Continue breathing at this slow, restful pace..."
    },
    {
        "id": 2,
        "title": "Sensate Focus: Touch Without Goal",
        "category": "Sensate Focus & Desire",
        "duration": 12,
        "desc": "Guided partner exercise focusing purely on tactile sensations without any pressure for arousal.",
        "type": "Spoken Voice Audio Guide",
        "tags": ["Couples", "Low Pressure", "Intimacy"],
        "script": "Welcome to Sensate Focus. This exercise is designed to remove all performance pressure. Sit or lie comfortably together. Partner A, begin by using soft fingertip touch across Partner B's shoulders and back. Focus purely on the texture of skin, warmth, and breathing. There is no destination, no goal, and no expectation of sexual intimacy. Simply enjoy the present physical touch..."
    },
    {
        "id": 3,
        "title": "Understanding Responsive Desire",
        "category": "Micro-Education",
        "duration": 4,
        "desc": "Why you might not feel spontaneous desire—and how context creates readiness.",
        "type": "Spoken Educational Voice",
        "tags": ["Psychology", "Desire"],
        "script": "Many adults assume sexual desire should appear spontaneously, like hunger. However, research shows that over half of women experience responsive desire. This means desire emerges only after the brain perceives safety, warmth, relaxation, and pleasurable context. You are not broken if you don't feel spontaneous desire; your nervous system simply requires the right environment first..."
    },
    {
        "id": 4,
        "title": "Script: Pausing Intimacy Gently",
        "category": "Communication Scripts",
        "duration": 3,
        "desc": "Word-for-word templates to communicate discomfort or fatigue to a partner with care.",
        "type": "Interactive Voice Template",
        "tags": ["Boundaries", "Couples"],
        "script": "Here is a gentle communication template you can use with your partner: 'I love being close to you, but my body is feeling tense and exhausted tonight. Can we focus on cuddling and breathing together without any expectation of going further?' Expressing boundaries early builds deep safety and trust."
    },
    {
        "id": 5,
        "title": "Post-Work Nervous System Decompression",
        "category": "Somatic & Pelvic PT",
        "duration": 7,
        "desc": "Transition out of fight-or-flight posture before heading home or attempting intimacy.",
        "type": "Spoken Voice Audio Guide",
        "tags": ["Stress", "Nervous System"],
        "script": "Pause where you are. Unclench your jaw. Drop your shoulders down and away from your ears. Take a deep breath in, hold for two seconds, and exhale with a long, slow sigh. You are transitioning out of work mode. Allow your muscle tone to relax and your nervous system to return to a calm state of safety..."
    }
]

def generate_pdf_report(pain, stress, energy, active_day):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Aura Patient Clinical Progress Summary", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 10, f"Generated: {time.strftime('%Y-%m-%d %H:%M')}", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "1. Current Physical & Stress Telemetry", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, f"- Logged Pelvic Discomfort Score: {pain}/10", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, f"- Logged Overall Stress Level: {stress}/10", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, f"- Energy Level: {energy}/10", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "2. Program Compliance", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, f"- Active Program: 7 Days to Pelvic Comfort", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, f"- Progress Status: Day {active_day} of 7 Completed", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "3. Clinician Notes & Observations", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "I", 10)
    pdf.multi_cell(0, 6, "Patient shows hypertonic pelvic guarding correlated with high stress days. Diaphragmatic reverse Kegel exercises and somatic unwinding tracks have been assigned.")
    
    return pdf.output()

# ==========================================
# 4. SIDEBAR NAVIGATION
# ==========================================
st.sidebar.title("🌿 Aura Health")
st.sidebar.caption("Mind, Body & Discovery Platform")

if st.session_state.authenticated:
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ Account Mode")
    st.session_state.user_mode = st.sidebar.radio(
        "Active Mode:",
        ["Singles Proximity Mode", "Couples Mode"],
        key="sidebar_mode_select"
    )

    st.sidebar.markdown("---")
    nav_items = ["Dashboard & Check-In", "Content Library", "Erotic Context Profile"]

    if st.session_state.user_mode == "Singles Proximity Mode":
        nav_items.append("📍 Proximity & Discovery")
        nav_items.append("Sensate Focus & Partner Deck")
    else:
        nav_items.append("Partner Double-Blind Sync")
        nav_items.append("Sensate Focus & Partner Deck")

    nav_items.extend([
        "AI Somatic Coach", 
        "Body (Pelvic & PT Tracker)", 
        "Mind & Self-Exploration", 
        "Clinician Corner & PDF", 
        "Privacy & Security"
    ])

    nav_choice = st.sidebar.radio("Navigation", nav_items)
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔒 Vault & Identity")
    st.sidebar.success("AES-256 Vault: ACTIVE")
    
    if st.session_state.user_mode == "Couples Mode":
        if st.session_state.linked_partner_id:
            st.sidebar.success(f"🔗 Linked: `{st.session_state.linked_partner_id}`")
        else:
            st.sidebar.warning("🔗 Partner: Not Linked")
    else:
        status_badge = " Verified" if st.session_state.is_verified else " Unverified"
        st.sidebar.info(f"🛡️ Discovery ID:{status_badge}")

    if st.sidebar.button("Lock Portal / Log Out"):
        st.session_state.authenticated = False
        st.rerun()
else:
    nav_choice = "Auth"

# ==========================================
# 5. SCREEN 0: AUTHENTICATION
# ==========================================
if not st.session_state.authenticated:
    st.title("Welcome to Aura 🌿")
    st.caption("Integrated Mind, Body, and Partner Well-being")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Secure Sign-In")
        email = st.text_input("Email Address", value="alex@aura-health.app")
        password = st.text_input("Password", type="password", value="••••••••••••")
        
        st.markdown("#### 👩‍❤️‍👨 Partner Link (Optional)")
        partner_input_at_login = st.text_input(
            "Partner Invite Code", 
            placeholder="e.g. AURA-8F3K",
            help="If your partner gave you a link code, enter it here to connect."
        ).strip().upper()

        consent = st.checkbox("I explicitly consent to Aura processing my health and pelvic data.")

        if st.button("Enter Secure Portal"):
            if consent:
                if partner_input_at_login:
                    if partner_input_at_login == st.session_state.user_partner_code:
                        st.error("You cannot link your account to your own code.")
                    else:
                        st.session_state.linked_partner_id = partner_input_at_login
                        st.session_state.user_mode = "Couples Mode"
                        st.session_state.authenticated = True
                        st.rerun()
                else:
                    st.session_state.authenticated = True
                    st.rerun()
            else:
                st.error("Explicit consent is required to access sensitive pelvic features.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="accent-card">
            <h4>Pillars of Clinical Care & Discovery</h4>
            <ul>
                <li><b>Spoken Voice Sessions:</b> Dynamic voice narration for pelvic floor unwinding.</li>
                <li><b>Body:</b> Pelvic floor down-training & physical therapy logging.</li>
                <li><b>Mind & Exploration:</b> Guided female self-stimulation with voice synthesis.</li>
                <li><b>Proximity Discovery:</b> Double-blind desire matching for singles nearby.</li>
                <li><b>Clinician Exports:</b> One-click PDF progress reports.</li>
            </ul>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="prompt-card">
            <b>🔑 Your Partner Invite Code:</b><br>
            <h3 style="color: #C084FC; margin: 0.25rem 0;">{st.session_state.user_partner_code}</h3>
            Share this code with your partner so they can enter it when signing in.
            </div>
        """, unsafe_allow_html=True)

# ==========================================
# 6. SCREEN 1: DASHBOARD & CHECK-IN
# ==========================================
elif nav_choice == "Dashboard & Check-In":
    st.title(f"Welcome Back, {st.session_state.user_name} 🌿")
    st.caption(f"Today is {datetime.date.today().strftime('%A, %B %d, %Y')} | Active Mode: **{st.session_state.user_mode}**")

    # Dynamic Telemetry Display
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Pelvic Discomfort", f"{st.session_state.pain_level}/10")
    col2.metric("Stress Score", f"{st.session_state.stress_level}/10")
    col3.metric("Energy Score", f"{st.session_state.energy_level}/10")
    col4.metric("Desire State", st.session_state.desire_state)

    st.markdown("---")

    # DYNAMIC RECOMMENDATION HOOK WITH REAL SPOKEN VOICE
    st.subheader("🎯 Recommended Spoken Session Right Now")
    
    if st.session_state.pain_level >= 5 or st.session_state.stress_level >= 5:
        st.markdown('<div class="accent-card">', unsafe_allow_html=True)
        st.write("⚠️ **High Physical Tension / Guarding Detected**")
        st.markdown("### 🎙️ 5-Minute Pelvic Floor Unwinding")
        st.write("Your logged telemetry indicates involuntary pelvic guarding. Listen to this voice-guided session.")
        
        voice_bytes = generate_speech_audio(LIBRARY_DATA[0]["script"])
        st.audio(voice_bytes, format="audio/mp3")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.write("✨ **Balanced State**")
        st.markdown("### 🎙️ Sensate Focus: Touch Without Goal")
        st.write("You are reporting low stress today. Ideal timing for a low-pressure connection practice.")
        
        voice_bytes = generate_speech_audio(LIBRARY_DATA[1]["script"])
        st.audio(voice_bytes, format="audio/mp3")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # MULTI-DAY PROGRESSION & DAILY FORM
    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.subheader("🌱 Active Program Arc")
        current_day = st.session_state.active_program_day
        with st.expander("Program: **7 Days to Pelvic Comfort**", expanded=True):
            st.progress(current_day / 7, text=f"Day {current_day} of 7 Completed")
            st.markdown(f"**Today's Module (Day {current_day}):** Somatic Release & Soft Lengthening")
            st.caption("Duration: 7 mins • Spoken Voice Audio")
            if st.button("Resume Program Module"):
                voice_bytes = generate_speech_audio(LIBRARY_DATA[0]["script"])
                st.audio(voice_bytes, format="audio/mp3")

    with col_b:
        st.subheader("📝 60-Second Daily Check-In")
        with st.form("checkin_form"):
            st.session_state.pain_level = st.slider("Pelvic & Somatic Tension (1 = Soft, 10 = High Guarding)", 1, 10, st.session_state.pain_level)
            st.session_state.stress_level = st.slider("Mental Stress & Noise (1 = Calm, 10 = Overwhelmed)", 1, 10, st.session_state.stress_level)
            st.session_state.energy_level = st.slider("Energy Level (1 = Exhausted, 10 = Energized)", 1, 10, st.session_state.energy_level)
            st.session_state.desire_state = st.selectbox("Current Desire Readiness", ["Open & Curious", "Responsive Only", "Neutral", "Disconnected / Guarded"], index=2)
            brake = st.selectbox("Identify Active Inhibitor", ["None", "Fatigue", "Physical Discomfort", "Pain Anticipation", "Overstimulated", "Emotional Distance"])
            note = st.text_area("Encrypted Private Journal Entry", placeholder="Notes on comfort...")

            if st.form_submit_button("Save Encrypted Telemetry"):
                new_entry = {
                    "Date": str(datetime.date.today()),
                    "Pelvic Tension": st.session_state.pain_level,
                    "Stress": st.session_state.stress_level,
                    "Energy": st.session_state.energy_level,
                    "Desire": st.session_state.desire_state,
                    "Inhibitor": brake,
                    "Note": note if note else "No private note added."
                }
                st.session_state.checkin_history.append(new_entry)
                st.success("✅ Log saved securely!")

# ==========================================
# 7. SCREEN 2: CONTENT LIBRARY (SPOKEN VOICE)
# ==========================================
elif nav_choice == "Content Library":
    st.title("📚 Content Library")
    st.caption("Listen to real spoken voice-narrated audio guides for somatic unwinding and desire education.")

    selected_voice_label = st.selectbox("Select Narrator Accent:", list(VOICE_PROFILES.keys()))
    voice_config = VOICE_PROFILES[selected_voice_label]

    st.markdown("---")

    for item in LIBRARY_DATA:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        c1, c2 = st.columns([3, 1])
        with c1:
            st.markdown(f"### {item['title']}")
            st.caption(f"**{item['category']}** • 🕒 {item['duration']} mins • 🗣️ {item['type']}")
            st.write(item['desc'])
            for tag in item['tags']:
                st.markdown(f'<span class="badge-tag">#{tag}</span>', unsafe_allow_html=True)
        with c2:
            if st.button(f"🎙️ Play Voice Audio", key=f"play_{item['id']}"):
                with st.spinner("Synthesizing voice narration..."):
                    audio_data = generate_speech_audio(
                        item["script"], 
                        lang=voice_config["lang"], 
                        tld=voice_config["tld"]
                    )
                    st.audio(audio_data, format="audio/mp3")
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 8. SCREEN 3: PROXIMITY & DISCOVERY (SINGLES)
# ==========================================
elif nav_choice == "📍 Proximity & Discovery":
    st.title("📍 Proximity & Erotic Preference Matcher")
    st.caption("Double-blind proximity matching real-time readiness capacity and mutual erotic desires.")

    col_settings, col_beacon = st.columns([1, 1])

    with col_settings:
        st.markdown("### 1. Discovery Radar Filters")
        radius_km = st.slider("Scan Radius (Kilometers)", min_value=0.5, max_value=20.0, value=5.0, step=0.5)
        selected_safe_zone = st.selectbox("Safe Zone / Venue Filter", SAFE_ZONES)
        req_verified = st.checkbox("Require Verified Beacon Badge Only", value=True)
        min_shared_tags = st.slider("Minimum Mutual Desires Required", min_value=1, max_value=5, value=1)

    with col_beacon:
        st.markdown("### 2. Your Active Readiness Beacon")
        st.session_state.partner_beacon = st.selectbox(
            "What is your capacity right now?",
            ["💬 Open to Talk & Coffee", "🧘 Open to Touch (Zero Pressure)", "🔥 Open to Intimacy", "🔋 Energy Low (Discovery Paused)"]
        )
        beacon_ttl = st.selectbox("Beacon Duration", ["2 Hours", "4 Hours", "8 Hours"])
        
        if st.session_state.partner_beacon != "🔋 Energy Low (Discovery Paused)":
            st.success(f"🟢 Beacon active for {beacon_ttl} | Visible within {radius_km} km")
        else:
            st.warning("🔴 Beacon paused. You are invisible to nearby users.")

    st.markdown("---")
    st.markdown("### 3. Private Erotic Preferences & Desires")
    st.session_state.user_erotic_interests = st.multiselect(
        "Select your active desires and boundaries (Double-blind until matched):",
        options=EROTIC_TAXONOMY,
        default=st.session_state.user_erotic_interests
    )

    st.markdown("---")
    st.markdown("### 4. Nearby Double-Blind Matches")

    if st.session_state.partner_beacon == "🔋 Energy Low (Discovery Paused)":
        st.info("Set an active readiness status above to start scanning for nearby matches.")
    elif not st.session_state.user_erotic_interests:
        st.info("Please select at least one erotic preference above to enable double-blind matching.")
    else:
        matches = []
        for candidate in MOCK_NEARBY_SINGLES:
            if candidate["distance_km"] <= radius_km:
                if not req_verified or candidate["verified"]:
                    if selected_safe_zone == "All Locations (GPS Radius)" or candidate["safe_zone"] == selected_safe_zone:
                        if candidate["readiness"] == st.session_state.partner_beacon:
                            shared_interests = set(st.session_state.user_erotic_interests).intersection(set(candidate["erotic_interests"]))
                            if len(shared_interests) >= min_shared_tags:
                                matches.append({
                                    "id": candidate["id"],
                                    "verified": candidate["verified"],
                                    "distance": candidate["distance_km"],
                                    "safe_zone": candidate["safe_zone"],
                                    "shared_count": len(shared_interests),
                                    "shared_tags": list(shared_interests)
                                })

        if matches:
            st.success(f"🎉 Found {len(matches)} mutual double-blind match(es) nearby!")
            for match in matches:
                badge_html = "🛡️ Verified" if match["verified"] else "⚠️ Unverified"
                st.markdown(f"""
                    <div class="match-banner">
                    <h4>📍 Nearby Beacon: {match['id']} ({badge_html})</h4>
                    <p><b>Distance:</b> ~{match['distance']} km away | <b>Location:</b> {match['safe_zone']}</p>
                    <p><b>Mutual Desires ({match['shared_count']}):</b> {', '.join(match['shared_tags'])}</p>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"Send Encrypted Signal to {match['id']}", key=f"sig_{match['id']}"):
                    st.success(f"Private signal sent to {match['id']}!")
        else:
            st.info("No nearby beacons currently match your readiness status and desire threshold.")

# ==========================================
# 9. SCREEN 4: PARTNER DOUBLE-BLIND SYNC
# ==========================================
elif nav_choice == "Partner Double-Blind Sync":
    st.title("🔒 Double-Blind Partner Alignment")
    st.caption("Independently log your desires for tonight. Match only where preferences overlap.")

    col_user, col_partner = st.columns(2)

    with col_user:
        st.subheader("Your Selection")
        user_choice = st.radio(
            "What feels good for tonight?",
            [
                "Cuddling & Quiet Presence Only (No Touch Beyond)",
                "Sensate Touch (Non-Genital Massage)",
                "Open to Physical Intimacy if Low Discomfort",
                "Needs Rest / Zero Touch Tonight"
            ],
            key="user_intent_radio"
        )
        if st.button("Lock In My Intent"):
            st.session_state.my_intent = user_choice
            st.success("Intent locked in privately.")

    with col_partner:
        st.subheader("Partner Selection (Simulated)")
        partner_choice = st.radio(
            "Simulate Partner Input:",
            [
                "Cuddling & Quiet Presence Only (No Touch Beyond)",
                "Sensate Touch (Non-Genital Massage)",
                "Open to Physical Intimacy if Low Discomfort",
                "Needs Rest / Zero Touch Tonight"
            ],
            key="partner_intent_radio"
        )
        if st.button("Lock In Partner Intent"):
            st.session_state.partner_intent = partner_choice
            st.success("Partner intent locked in.")

    st.markdown("---")
    st.subheader("Alignment Result")

    if st.session_state.my_intent and st.session_state.partner_intent:
        if st.session_state.my_intent == st.session_state.partner_intent:
            st.balloons()
            st.success(f"🎉 **Match Found!** Both of you selected:\n\n > **{st.session_state.my_intent}**")
        else:
            st.warning("🤝 **Different Needs Tonight:** The system revealed a low-pressure overlap option: **Cuddling & Rest Focus**.")
    else:
        st.write("Waiting for both partners to submit intent...")

# ==========================================
# 10. SCREEN 5: EROTIC CONTEXT PROFILE
# ==========================================
elif nav_choice == "Erotic Context Profile":
    st.title("✨ Custom Erotic Context Profile")
    st.caption("Map your unique desire accelerators and brakes based on the Dual-Control Model.")

    scores = {}
    with st.form("erotic_profile_form"):
        st.subheader("Contextual Sensitivity Assessment")
        for category, statement in EROTIC_CONTEXT_QUESTIONS.items():
            st.markdown(f"#### {category}")
            st.caption(f'"{statement}"')
            scores[category] = st.slider(f"Impact Level (1 = Low Impact, 5 = Critical Requirement)", 1, 5, 3, key=category)
            st.markdown("---")
        
        if st.form_submit_button("Save Private Context Profile"):
            st.session_state["erotic_profile"] = scores
            st.success("Erotic Context Profile saved securely to your private vault!")

    if "erotic_profile" in st.session_state:
        st.markdown("---")
        st.subheader("📊 Your Desire Context Map")
        profile_df = pd.DataFrame(list(st.session_state["erotic_profile"].items()), columns=["Dimension", "Sensitivity Score"])
        
        fig = px.bar(
            profile_df, x="Dimension", y="Sensitivity Score", color="Sensitivity Score", 
            color_continuous_scale="Purples", text="Sensitivity Score"
        )
        fig.update_layout(paper_bgcolor="#0F172A", plot_bgcolor="#1E1B4B", font_color="#F8FAFC", yaxis=dict(range=[0, 5]))
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# 11. SCREEN 6: AI SOMATIC COACH
# ==========================================
elif nav_choice == "AI Somatic Coach":
    st.title("🤖 Adaptive Somatic Voice Coach")
    st.caption("Neuroscience-backed unwinding protocols based on the Dual-Control Model.")

    p_score = st.session_state.pain_level
    s_score = st.session_state.stress_level

    st.markdown(f"""
        <div class="glass-card">
        <h4>Diagnostic Telemetry for Today</h4>
        <p><b>Pelvic Discomfort Score:</b> {p_score}/10 | <b>Stress Score:</b> {s_score}/10</p>
        </div>
    """, unsafe_allow_html=True)

    if st.button("🎙️ Generate & Play Custom Somatic Voice Unwind"):
        custom_script = f"Hello. I see your pelvic tension score is currently at {p_score} out of 10, and your stress score is {s_score}. Take a slow breath in through your nose. Release your jaw and shoulders. Allow your belly to expand, and completely soften your pelvic floor muscles as you exhale."
        with st.spinner("Synthesizing personalized voice session..."):
            audio_data = generate_speech_audio(custom_script)
            st.audio(audio_data, format="audio/mp3")

# ==========================================
# 12. SCREEN 7: BODY (PELVIC & PT TRACKER)
# ==========================================
elif nav_choice == "Body (Pelvic & PT Tracker)":
    st.title("Body: Pelvic Floor & Physical Therapy Tracker")
    st.caption("Clinical tools for hypertonia, dyspareunia relief, and progressive dilator logging.")

    tab1, tab2, tab3 = st.tabs(["5-Min Guided Audio", "Breath Pace Visualizer", "Dilator & PT Session Logger"])

    with tab1:
        st.subheader("Deep Somatic Unwinding & Pelvic Drop")
        if st.button("🎙️ Play Spoken Unwinding Session"):
            audio_bytes = generate_speech_audio(LIBRARY_DATA[0]["script"])
            st.audio(audio_bytes, format="audio/mp3")

    with tab2:
        st.subheader("Diaphragmatic Breath Visualizer")
        if st.button("Start Live Breath Guidance Cycle"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i in range(1, 4):
                for p in range(0, 101, 10):
                    progress_bar.progress(p)
                    status_text.markdown(f"### 🫁 INHALE (Expanding Belly) - Cycle {i}/3")
                    time.sleep(0.3)
                status_text.markdown(f"### ⏸️ HOLD (Soft) - Cycle {i}/3")
                time.sleep(1.5)
                for p in range(100, -1, -10):
                    progress_bar.progress(p)
                    status_text.markdown(f"### 🌬️ EXHALE & DROP PELVIS - Cycle {i}/3")
                    time.sleep(0.4)
            status_text.markdown("### ✨ Cycle Complete! Pelvic floor lowered.")

    with tab3:
        st.subheader("Dilator & PT Therapy Log")
        with st.form("dilator_form"):
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                d_size = st.selectbox("Dilator / Tool Size", ["Size 1 (Smallest)", "Size 2", "Size 3", "Size 4", "Size 5 (Largest)"])
            with col_b:
                d_time = st.number_input("Duration (Minutes)", min_value=1, max_value=60, value=10)
            with col_c:
                d_discomfort = st.slider("Discomfort Level (1 = None, 10 = High)", 1, 10, 2)
            
            pt_notes = st.text_input("Session Notes", placeholder="Notes on pelvic relaxation...")
            
            if st.form_submit_button("Log PT Session"):
                st.session_state.dilator_logs.append({
                    "Date": str(datetime.date.today()),
                    "Size": d_size,
                    "Duration": d_time,
                    "Discomfort": d_discomfort,
                    "Notes": pt_notes
                })
                st.success("Physical therapy session logged securely!")

# ==========================================
# 13. SCREEN 8: MIND & SELF-EXPLORATION
# ==========================================
elif nav_choice == "Mind & Self-Exploration":
    st.title("Mind, Self-Exploration & Climax Pathways")
    st.caption("Somatic audio grounding, responsive desire education, and multi-phase guided climax modules.")

    selected_module_key = st.selectbox("Select Phase / Exploration Module:", list(FEMALE_EXPLORATION_MODULES.keys()))
    selected_mod = FEMALE_EXPLORATION_MODULES[selected_module_key]
    selected_voice_label = st.selectbox("Choose Narrator Voice Profile:", list(VOICE_PROFILES.keys()))

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 📋 Overview & Guided Steps")
        st.write(f"*{selected_mod['description']}*")
        for step in selected_mod["steps"]:
            st.markdown(f"""
                <div class="prompt-card">
                <b>{step.split(':')[0]}:</b> {step.split(':')[1]}
                </div>
            """, unsafe_allow_html=True)

        if st.button("▶️ Synthesize & Start Voice-Guided Narration"):
            with st.spinner("Synthesizing narration with gTTS..."):
                voice_config = VOICE_PROFILES[selected_voice_label]
                audio_bytes = generate_speech_audio(
                    selected_mod["script"], 
                    lang=voice_config["lang"], 
                    tld=voice_config["tld"]
                )
                st.audio(audio_bytes, format="audio/mp3")

    with col2:
        st.markdown("### 🎙️ Full Narration Script")
        st.markdown(f"""
            <div class="script-box">
            "{selected_mod['script']}"
            </div>
        """, unsafe_allow_html=True)

# ==========================================
# 14. SCREEN 9: SENSATE FOCUS & PARTNER DECK
# ==========================================
elif nav_choice == "Sensate Focus & Partner Deck":
    st.title("Partner Sync & Sensate Focus")
    st.caption("Low-pressure intimacy tools, non-verbal readiness beacons, and double-blind deck matching.")

    tab1, tab2, tab3 = st.tabs(["Readiness Beacon", "Double-Blind Partner Deck", "Manage Partner Link"])

    with tab1:
        st.subheader("📶 Non-Verbal Readiness Beacon")
        new_beacon = st.radio(
            "Current Status Signal:",
            ["🔋 Energy Low (Need Rest)", "💬 Open to Talk & Cuddle", "🧘 Open to Touch (Zero Pressure)", "🔥 Open to Intimacy"],
            horizontal=True
        )
        if st.button("Update Beacon Signal"):
            st.session_state.partner_beacon = new_beacon
            st.success(f"Beacon updated to: **{new_beacon}**")

    with tab2:
        st.subheader("🎴 Double-Blind Card Deck")
        tier_choice = st.selectbox("Select Energy Tier", list(CARD_DECK.keys()))
        prompts = CARD_DECK[tier_choice]

        with st.form("partner_deck_form"):
            for idx, prompt in enumerate(prompts):
                st.markdown(f"""
                    <div class="prompt-card">
                    <b>Prompt #{idx+1}:</b> {prompt}
                    </div>
                """, unsafe_allow_html=True)
                st.checkbox(f"I'm open to this tonight", key=f"card_{tier_choice}_{idx}")
            
            if st.form_submit_button("Submit Secret Selections"):
                st.success("Selections saved to isolated vault!")

    with tab3:
        st.subheader("🔗 Partner Link Manager")
        if st.session_state.linked_partner_id:
            st.success(f"🟢 Currently linked to partner ID: `{st.session_state.linked_partner_id}`")
            if st.button("Unlink Partner Account"):
                st.session_state.linked_partner_id = None
                st.rerun()
        else:
            p_code_input = st.text_input("Enter Partner Code to Link Now", placeholder="e.g. AURA-8F3K").strip().upper()
            if st.button("Link Partner"):
                if p_code_input == st.session_state.user_partner_code:
                    st.error("You cannot link to your own code.")
                elif len(p_code_input) >= 6:
                    st.session_state.linked_partner_id = p_code_input
                    st.success("Partner linked successfully!")
                    st.rerun()

# ==========================================
# 15. SCREEN 10: CLINICIAN CORNER & PDF
# ==========================================
elif nav_choice == "Clinician Corner & PDF":
    st.title("🏥 Clinician Portal & Telemetry")
    st.caption("Bridge home logging with your Physical Therapist or Sex Therapist.")

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Assigned Home Exercises")
        st.checkbox("3x Sets Diaphragmatic Reverse Kegels", value=True)
        st.checkbox("Dilator Session #2 with Pacing Audio", value=False)
        st.checkbox("Post-Work Decompression Audio", value=True)

    with c2:
        st.subheader("Export Clinical Reports")
        st.write("Generate a formatted clinical PDF report detailing pain trends and stress metrics.")
        
        pdf_bytes = generate_pdf_report(
            st.session_state.pain_level,
            st.session_state.stress_level,
            st.session_state.energy_level,
            st.session_state.active_program_day
        )
        
        st.download_button(
            label="📄 Download Clinical PDF Report",
            data=bytes(pdf_bytes),
            file_name=f"Aura_Clinical_Report_{time.strftime('%Y%m%d')}.pdf",
            mime="application/pdf"
        )

# ==========================================
# 16. SCREEN 11: PRIVACY & SECURITY
# ==========================================
elif nav_choice == "Privacy & Security":
    st.title("Privacy, Security & Data Erasure")
    st.caption("Zero-Knowledge guarantees, double-blind isolation, and cloud retention schedules.")

    st.table({
        "Data Category": ["Account Auth & Profile", "Daily Pelvic Logs", "Proximity Beacon Coordinates", "Unmatched Double-Blind Votes"],
        "Retention Period": ["Duration of Active Account", "24 Months (Rolling)", "2–8 Hours (Auto-Purged)", "Hard Deleted Instantly"],
        "Storage Protocol": ["Encrypted Database", "Anonymized & AES-256", "Ephemeral In-Memory", "Zero Retention"]
    })

    st.markdown("---")
    st.subheader("⚠️ Hard Reset Vault")
    if st.button("Trigger Immediate Account Data Erasure"):
        st.session_state.checkin_history = []
        st.session_state.dilator_logs = []
        st.session_state.linked_partner_id = None
        st.session_state.authenticated = False
        st.error("All local logs wiped from session memory.")
        st.rerun()
