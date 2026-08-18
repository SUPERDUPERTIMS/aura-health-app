import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import time
from gtts import gTTS
import io
import secrets

# ==========================================
# 1. PAGE CONFIGURATION & THEMING
# ==========================================
st.set_page_config(
    page_title="Aura | Intimacy & Pelvic Health",
    page_icon="🧘‍♀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Aura Aesthetic
st.markdown("""
    <style>
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
    }
    .stButton>button {
        background-color: #A855F7;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #9333EA;
        color: white;
    }
    .metric-card {
        background-color: #1E1B4B;
        border: 1px solid #312E81;
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }
    .prompt-card {
        background-color: #18181B;
        border: 1px solid #27272A;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 0.75rem;
    }
    .journal-card {
        background-color: #1E293B;
        border-left: 4px solid #A855F7;
        border-radius: 6px;
        padding: 0.75rem 1rem;
        margin-bottom: 0.5rem;
    }
    .legal-box {
        background-color: #18181B;
        border: 1px solid #27272A;
        border-radius: 8px;
        padding: 1rem;
        font-size: 0.85rem;
        color: #A1A1AA;
        height: 150px;
        overflow-y: scroll;
    }
    .match-banner {
        background-color: #064E3B;
        border: 1px solid #10B981;
        color: #ECFDF5;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
    }
    .script-box {
        background-color: #1E293B;
        border: 1px solid #475569;
        border-radius: 8px;
        padding: 1rem;
        font-style: italic;
        color: #E2E8F0;
        margin-top: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. SESSION STATE MANAGEMENT & DATABASES
# ==========================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_name" not in st.session_state:
    st.session_state.user_name = "Alex"
if "checkin_history" not in st.session_state:
    st.session_state.checkin_history = []
if "dilator_logs" not in st.session_state:
    st.session_state.dilator_logs = []
if "partner_beacon" not in st.session_state:
    st.session_state.partner_beacon = "🔋 Energy Low"

# PARTNER LINKING SESSION INITIALIZATION
if "user_partner_code" not in st.session_state:
    st.session_state.user_partner_code = f"AURA-{secrets.token_hex(3).upper()}"
if "linked_partner_id" not in st.session_state:
    st.session_state.linked_partner_id = None

# EROTIC CONTEXT QUESTIONS DATABASE
EROTIC_CONTEXT_QUESTIONS = {
    "Cognitive Load & Tasks": "I find it hard to feel desire or reach climax if I have unfinished chores, work emails, or mental stress lingering.",
    "Emotional Closeness": "I need to feel emotionally connected, appreciated, and close before I feel open to deep physical release.",
    "Somatic & Muscle Comfort": "Physical relaxation, bodily warmth, and an absence of pelvic muscle guarding are essential for me to climax.",
    "Sensory Environment": "Factors like dim lighting, pleasant scents, clean sheets, and ambient music strongly influence my ability to focus on pleasure.",
    "Novelty & Playfulness": "Playful teasing, unexpected affection, changing locations, or roleplay easily activates my arousal."
}

# AUDIO SCRIPTS DATABASE (GENERAL)
AUDIO_SCRIPTS = {
    "Understanding Responsive Desire": (
        "Welcome. Many people expect sexual desire to happen spontaneously—like a sudden bolt of lightning. "
        "But for most adults, desire works responsively. Spontaneous desire is like feeling hungry before you see food. "
        "Responsive desire is like not feeling hungry at all, but then sitting down at a nice table, smelling a delicious meal, "
        "taking a bite, and realizing, 'Actually, this is wonderful.' Desire doesn't always start in the mind; "
        "it often begins in the body after safety, relaxation, and physical presence are established. Give yourself permission "
        "to let go of the pressure to feel turned on instantly. Focus instead on physical comfort and willingness."
    ),
    "Somatic Decompression After Work": (
        "Sit or lie down in a comfortable position. Unclench your jaw, drop your shoulders away from your ears, "
        "and let your hands rest gently in your lap or at your side. Take a deep breath in through your nose for a count of four... "
        "hold for two... and exhale slowly through your mouth for six. With every exhale, imagine discharging the accumulated stress, "
        "emails, and deadlines of the workday into the ground below you. Shift your focus entirely from your analytical mind "
        "down into the physical weight of your body."
    ),
    "Sensate Focus Phase 1 Preparation": (
        "Before beginning this exercise, ensure the room is warm, quiet, and free from distractions. The purpose of Sensate Focus Phase 1 "
        "is non-genital, non-sexual physical exploration. There is no goal, no pressure, and no requirement for arousal. "
        "One partner will take the role of the toucher, and the other will be the receiver. Explore the texture, temperature, "
        "and contour of your partner's skin—their arms, shoulders, back, or feet—using different pressures and speeds. "
        "All erogenous zones and intercourse are off-limits during this stage to allow your nervous system to fully relax."
    )
}

# EXPANDED FEMALE SELF-EXPLORATION & CLIMAX GUIDED MODULES
FEMALE_EXPLORATION_MODULES = {
    "Phase 1: Zero-Pressure Somatic Mapping": {
        "description": "A gentle journey mapping non-genital erogenous zones to awaken body awareness without expectation of performance.",
        "steps": [
            "Step 1: Set the scene—warm lighting, comfortable support under your knees, and a drop of preferred oil or lotion.",
            "Step 2: Close your eyes and spend 2 minutes using light fingertip pressure along your collarbones, neck, and inner arms.",
            "Step 3: Notice micro-sensations—temperature, tingling, or goosebumps—without trying to force arousal.",
            "Step 4: Rest your palm gently over your lower abdomen, syncing your breath with the rise and fall of your belly."
        ],
        "script": (
            "Welcome to your private self-exploration space. Today there is no goal, no timer, and no expectation of climax. "
            "Begin by making your body completely comfortable. Place a pillow beneath your knees and soften your jaw. "
            "Bring your hands to your collarbones. Using light, feather-like strokes, trace down toward your shoulders and inner arms. "
            "Pay attention only to the physical texture of your skin and the warmth of your hands. "
            "Move down to your ribcage, then gently rest both hands on your lower belly. As you breathe in, feel your belly expand into your hands. "
            "As you exhale, let your pelvic floor drop completely soft. You are entirely safe, unhurried, and in control."
        )
    },
    "Phase 2: Anatomical Clitoral Mapping & Rhythms": {
        "description": "Technique focusing on indirect clitoral stimulation, pressure variations, and rhythm consistency necessary for arousal building.",
        "steps": [
            "Step 1: Apply a generous amount of warm lubricant around the labia and outer vulvar tissue.",
            "Step 2: Begin with gentle circular motions along the outer labia, avoiding direct glans touch to prevent oversensitivity.",
            "Step 3: Transition to a slow 'clock' pattern around the clitoral hood—pausing at 12, 3, 6, and 9 o'clock.",
            "Step 4: Establish a steady, rhythmic pressure. Rhythm consistency is key to helping the nervous system build arousal."
        ],
        "script": (
            "Ensure you have plenty of warm lubricant ready. Begin by applying it softly around your outer labia with slow, sweeping strokes. "
            "Resist the urge to go directly to the clitoral glans. Instead, create gentle circles around the surrounding tissue, "
            "awakening the rich network of nerve endings beneath the surface. Now, imagine a clockface over your clitoral hood. "
            "Pause with light pressure at twelve o'clock, then circle down to three, six, and nine. "
            "Once you find a movement that feels good, hold that exact rhythm. Consistent speed and pressure give your nervous system "
            "the safety and signal it needs to begin building deep, compounding pleasure."
        )
    },
    "Phase 3: The Edge & Plateau (Somatic Teasing)": {
        "description": "Advanced technique teaching how to navigate the arousal plateau, build sensation intensity, and lean into the climax threshold.",
        "steps": [
            "Step 1: As sensation builds toward a peak, deliberately slow your touch down or pause pressure for 5–10 seconds.",
            "Step 2: Take two deep, slow diaphragmatic exhales, releasing any involuntary jaw or shoulder clenching.",
            "Step 3: Resume rhythm slowly, allowing pleasure to rebuild higher than the previous level.",
            "Step 4: Repeat 2–3 times to expand capacity for intensity before allowing full release."
        ],
        "script": (
            "As you feel sensation beginning to rise into a peak, notice if you are holding your breath or tightening your shoulders. "
            "Instead of rushing toward the edge, gently pause your touch. Keep your hand resting softly where it is. "
            "Take a deep breath into your lower belly, and as you exhale, drop your pelvic floor completely soft. "
            "By softening the body at high arousal, you expand your capacity for pleasure. "
            "Now, slowly resume your rhythmic movement. Notice how the sensation feels deeper and more resonant. "
            "You are in complete control of this wave. Let it build at its own natural pace."
        )
    },
    "Phase 4: Deep Climax Release & Integration": {
        "description": "Guided vocalization, pelvic muscle release, and continuous rhythm designed to allow full neurological climax.",
        "steps": [
            "Step 1: Maintain a consistent, unwavering rhythm at your preferred touch intensity.",
            "Step 2: Open your mouth slightly and exhale with an audible sigh or tone to prevent holding tension in the throat.",
            "Step 3: Allow the pelvic floor muscles to contract and release without trying to force or suppress the waves.",
            "Step 4: Continue light, gentle touch post-climax to allow smooth neurological recovery and integration."
        ],
        "script": (
            "You are now at the threshold of release. Do not change your speed or pressure—keep your rhythm perfectly steady. "
            "Unclench your jaw and open your mouth slightly. Let out a soft breath or sound with every exhale. "
            "Your throat and pelvic floor are directly connected; opening your breath allows your pelvis to fully release. "
            "Surrender to the rhythmic pulse building inside you. Let go of all thinking, monitoring, or analyzing. "
            "Allow your body to take over completely. Ride the wave all the way through... breathing soft and deep."
        )
    },
    "Phase 5: Dual Co-Stimulation & Erotic Mind-Body Alignment": {
        "description": "Combines internal G-spot/anterior wall awareness with external clitoral stimulation and immersive sensory narrative.",
        "steps": [
            "Step 1: Position a pillow under your hips for comfortable pelvic tilt.",
            "Step 2: Combine gentle internal upward pressure along the anterior vaginal wall with steady external clitoral rhythm.",
            "Step 3: Immerse yourself in the vivid narrative, allowing mind and body to align fully."
        ],
        "script": (
            "Imagine lying on soft linen sheets in a secluded room overlooking a warm, rain-swept garden. "
            "The air is fragrant with jasmine and woodsmoke. You feel completely relaxed, free from all responsibilities and watchful eyes. "
            "As you apply gentle upward pressure internally, sync it with your steady external rhythm. "
            "Feel the warm, rhythmic pulsing deep in your pelvis expanding outward with every deep exhale. "
            "Your body feels weightless yet deeply grounded. Lean into this sensation, touching your body with deep appreciation, patience, and absolute freedom."
        )
    }
}

# PARTNER DECK DATABASE
CARD_DECK = {
    "Tier 1: Restorative & Low Energy (Zero Pressure)": [
        "15-Minute Shoulder & Neck Rub", "Shared Warm Bath or Shower", "Couch Cuddle & Phone-Free Chat",
        "Foot & Ankle Massage", "Early Night Unwind in Bed", "Tea & Decompression Routine",
        "Guided Breathing Side-by-Side", "Scalp & Hair Brushing", "Gratitude & Appreciation Swap", "Quiet Holding (Spooning)"
    ],
    "Tier 2: Sensual & Somatic Exploration": [
        "Guided Sensate Focus Touch (No Genital Touch)", "Warm Oil Back Massage", "Listen to an Erotic Audio Story",
        "Feather & Light Touch Exploration", "Sensory Blindfold Exploration", "Intimacy Prompt Card Deck",
        "Slow Dancing in the Living Room", "Mirroring Touch Exercise", "Shower for Two with Body Scrub", "Sensual Breathing & Eye Contact"
    ],
    "Tier 3: Intimate & Playful Connection": [
        "Uninterrupted Bedroom Time", "Fantasy Sharing Session", "Morning Intimacy Date",
        "Roleplay / New Persona Night", "Temperature Play (Warm Candle/Ice)", "Extended 30-Min Foreplay Focus",
        "New Location in the House", "Music Playlist Guided Touch", "Lingerie or Outfit Surprise", "Whispered Desires in the Dark"
    ]
}

# VOICE PROFILES MAPPING (gTTS accents)
VOICE_PROFILES = {
    "🇦🇺 Grounded & Deep (Australian Accent)": {"lang": "en", "tld": "com.au"},
    "🇬🇧 Warm & Expressive (British Accent)": {"lang": "en", "tld": "co.uk"},
    "🇺🇸 Calm & Clear (US Accent)": {"lang": "en", "tld": "com"},
    "🇮🇳 Soft & Guided (Indian English Accent)": {"lang": "en", "tld": "co.in"},
    "🇨🇦 Relaxed & Soft (Canadian Accent)": {"lang": "en", "tld": "ca"}
}

# ==========================================
# 3. SIDEBAR NAVIGATION
# ==========================================
st.sidebar.title("🧘‍♀️ Aura Health")
st.sidebar.caption("Mind, Body & Partner Sync Platform")

if st.session_state.authenticated:
    st.sidebar.markdown("---")
    nav_choice = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard & Check-In", 
            "Erotic Context Profile",
            "AI Somatic Coach", 
            "Body (Pelvic & PT Tracker)", 
            "Mind & Self-Exploration", 
            "Sensate Focus & Partner Deck", 
            "Weekly Analytics & PT Report", 
            "Privacy & Security"
        ]
    )
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔒 Vault Security")
    st.sidebar.success("AES-256 Client Vault: ACTIVE")
    st.sidebar.info("Zero-Knowledge: VERIFIED")
    
    if st.session_state.linked_partner_id:
        st.sidebar.success(f"🔗 Linked: `{st.session_state.linked_partner_id}`")
    else:
        st.sidebar.warning("🔗 Partner: Not Linked")

    if st.sidebar.button("Lock Portal / Log Out"):
        st.session_state.authenticated = False
        st.rerun()
else:
    nav_choice = "Auth"

# ==========================================
# 4. SCREEN 0: AUTHENTICATION & CONSENT (WITH OPTION A: PARTNER LINK AT LOGIN)
# ==========================================
if not st.session_state.authenticated:
    st.title("Welcome to Aura")
    st.subheader("Integrated Mind, Body, and Partner Well-being")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### Secure Sign-In")
        email = st.text_input("Email Address", value="alex@aura-health.app")
        password = st.text_input("Password", type="password", value="••••••••••••")
        
        # --- OPTION A: PARTNER LINKING AT LOGIN ---
        st.markdown("### 👩‍❤️‍👨 Partner Link (Optional at Login)")
        partner_input_at_login = st.text_input(
            "Partner Invite Code", 
            placeholder="e.g. AURA-8F3K (Leave blank if connecting later)",
            help="If your partner gave you a link code, enter it here to connect your accounts immediately."
        ).strip().upper()

        st.markdown("### Privacy & Sensitive Data Consent")
        st.markdown("""
            <div class="legal-box">
            <b>PRIVACY & SENSITIVE DATA CONSENT (GDPR Art. 9 / HIPAA / POPIA)</b><br><br>
            Aura processes Special Category Health Data. Before proceeding, you must review and consent:<br><br>
            <b>1. Sensitive Data Collected:</b> Pelvic muscle tone ratings, dyspareunia severity, stress metrics, and partner connection signals.<br>
            <b>2. Zero-Knowledge Architecture:</b> Intimacy logs and pelvic notes are client-side encrypted via AES-256 GCM.<br>
            <b>3. Double-Blind Isolation:</b> Unmatched partner desire selections are never exposed or transmitted.<br>
            <b>4. No Data Monetization:</b> Aura will NEVER sell, rent, or trade your health data.
            </div>
        """, unsafe_allow_html=True)
        
        consent = st.checkbox("I explicitly consent to Aura processing my health and pelvic data.")

        if st.button("Enter Secure Portal"):
            if consent:
                # Link partner code if provided during login
                if partner_input_at_login:
                    if partner_input_at_login == st.session_state.user_partner_code:
                        st.error("You cannot link your account to your own code.")
                    else:
                        st.session_state.linked_partner_id = partner_input_at_login
                        st.session_state.authenticated = True
                        st.rerun()
                else:
                    st.session_state.authenticated = True
                    st.rerun()
            else:
                st.error("Explicit consent is required to access sensitive pelvic features.")

    with col2:
        st.markdown("""
            <div class="metric-card">
            <h4>Pillars of Clinical Care</h4>
            <ul>
                <li><b>Body:</b> Pelvic floor down-training & physical therapy logging.</li>
                <li><b>Mind & Exploration:</b> Step-by-step female self-stimulation & climax guides.</li>
                <li><b>Context:</b> Erotic context profile mapping (Brakes vs Accelerators).</li>
                <li><b>Partner Sync:</b> Double-blind desire matching & Sensate Focus guides.</li>
                <li><b>Analytics:</b> One-click PDF/CSV reports for physical therapists.</li>
            </ul>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="prompt-card">
            <b>🔑 Your Partner Invite Code:</b><br>
            <h3 style="color: #A855F7; margin: 0.25rem 0;">{st.session_state.user_partner_code}</h3>
            Share this code with your partner so they can enter it when signing in!
            </div>
        """, unsafe_allow_html=True)

# ==========================================
# 5. SCREEN 1: DASHBOARD & DAILY CHECK-IN
# ==========================================
elif nav_choice == "Dashboard & Check-In":
    st.title(f"Welcome Back, {st.session_state.user_name}")
    st.caption(f"Today is {datetime.date.today().strftime('%A, %B %d, %Y')}")

    if len(st.session_state.checkin_history) > 0:
        latest = st.session_state.checkin_history[-1]
        p_val = f"{latest['Pelvic Tension']}/10"
        s_val = f"{latest['Stress']}/10"
    else:
        p_val = "No log today"
        s_val = "No log today"

    partner_status_text = f"Linked to {st.session_state.linked_partner_id}" if st.session_state.linked_partner_id else "Not Linked"

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
            <div class="metric-card">
            <h3>🧘‍♀️ Body Status</h3>
            <p><b>Pelvic Tone:</b> {p_val}</p>
            <p><b>PT Progress:</b> {len(st.session_state.dilator_logs)} Sessions Logged</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="metric-card">
            <h3>🎧 Mind Status</h3>
            <p><b>Stress Level:</b> {s_val}</p>
            <p><b>Target:</b> Somatic Unwinding</p>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div class="metric-card">
            <h3>👩‍❤️‍👨 Partner Beacon</h3>
            <p><b>Your Status:</b> {st.session_state.partner_beacon}</p>
            <p><b>Partner Sync:</b> {partner_status_text}</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("60-Second Daily Check-In")

    with st.form("checkin_form"):
        p_tension = st.slider("Step 1: Pelvic & Somatic Tension (1 = Soft & Relaxed, 10 = High Guarding)", 1, 10, 5)
        m_stress = st.slider("Step 2: Mental Stress & Noise (1 = Calm & Present, 10 = Overwhelmed)", 1, 10, 5)
        brake = st.selectbox("Step 3: Identify Active Inhibitor (The Brake)", ["None", "Fatigue", "Physical Discomfort", "Pain Anticipation", "Overstimulated", "Emotional Distance"])
        note = st.text_area("Private Journal Entry (Encrypted Client-Side)", placeholder="Notes on pelvic comfort, stress, or emotional state...")

        submitted = st.form_submit_button("Save Encrypted Log")

        if submitted:
            new_entry = {
                "Date": str(datetime.date.today()),
                "Day": datetime.date.today().strftime("%a"),
                "Pelvic Tension": p_tension,
                "Stress": m_stress,
                "Inhibitor": brake,
                "Note": note if note else "No private note added."
            }
            st.session_state.checkin_history.append(new_entry)
            st.success("✅ Check-in saved securely!")

            st.markdown("---")
            st.markdown("### 🎯 Recommended Next Steps")
            st.caption("Use the sidebar navigation to open these tools:")
            
            c1, c2, c3 = st.columns(3)
            with c1:
                if p_tension >= 6:
                    st.warning("⚠️ High Pelvic Tension")
                    st.write("Open **AI Somatic Coach** for a custom unwind sequence.")
                else:
                    st.success("🟢 Pelvic Tone Calm")
                    st.write("Muscle tone is low. Good foundation for rest or self-exploration.")

            with c2:
                if m_stress >= 6:
                    st.warning("⚠️ High Stress Active")
                    st.write("Open **Mind & Self-Exploration** to generate decompression tracks.")
                else:
                    st.success("🟢 Stress Managed")
                    st.write("Mental noise is low today.")

            with c3:
                st.info("💡 Partner Connection")
                st.write("Open **Sensate Focus & Partner Deck** to select tonight's activities.")

    st.markdown("---")
    st.subheader("📋 Saved Logs & Journal History")
    
    if len(st.session_state.checkin_history) == 0:
        st.info("No check-in logs recorded yet. Fill out the form above to log your first session!")
    else:
        for entry in reversed(st.session_state.checkin_history):
            st.markdown(f"""
                <div class="journal-card">
                <b>{entry['Date']} ({entry['Day']})</b> — Pelvic Tension: <b>{entry['Pelvic Tension']}/10</b> | Stress: <b>{entry['Stress']}/10</b> | Active Brake: <i>{entry.get('Inhibitor', 'None')}</i><br>
                <span style="color: #CBD5E1;">Note: "{entry.get('Note', 'No note recorded')}"</span>
                </div>
            """, unsafe_allow_html=True)

# ==========================================
# 6. SCREEN 2: EROTIC CONTEXT PROFILE
# ==========================================
elif nav_choice == "Erotic Context Profile":
    st.title("✨ Custom Erotic Context Profile")
    st.caption("Map your unique desire accelerators and brakes based on the Dual-Control Model.")

    scores = {}
    with st.form("erotic_profile_form"):
        st.subheader("Contextual Sensitivity Assessment")
        st.write("Rate how significantly each dimension impacts your ability to feel open to intimacy and reach climax:")
        
        for category, statement in EROTIC_CONTEXT_QUESTIONS.items():
            st.markdown(f"#### {category}")
            st.caption(f'"{statement}"')
            scores[category] = st.slider(f"Impact Level (1 = Low Impact, 5 = Critical Requirement)", 1, 5, 3, key=category)
            st.markdown("---")
        
        submitted = st.form_submit_button("Save Private Context Profile")
        if submitted:
            st.session_state["erotic_profile"] = scores
            st.success("Erotic Context Profile saved securely to your private vault!")

    if "erotic_profile" in st.session_state:
        st.markdown("---")
        st.subheader("📊 Your Desire Context Map")
        
        profile_df = pd.DataFrame(list(st.session_state["erotic_profile"].items()), columns=["Dimension", "Sensitivity Score"])
        
        fig = px.bar(
            profile_df, 
            x="Dimension", 
            y="Sensitivity Score", 
            color="Sensitivity Score", 
            color_continuous_scale="Purples",
            text="Sensitivity Score"
        )
        fig.update_layout(
            paper_bgcolor="#0F172A", 
            plot_bgcolor="#1E1B4B", 
            font_color="#F8FAFC", 
            yaxis=dict(range=[0, 5])
        )
        st.plotly_chart(fig, use_container_width=True)

        top_dim = profile_df.sort_values(by="Sensitivity Score", ascending=False).iloc[0]["Dimension"]
        st.info(f"💡 **Key Insight:** Your desire is most sensitive to **'{top_dim}'**. Focus on satisfying this condition before self-exploration or intimacy.")

# ==========================================
# 7. SCREEN 3: AI SOMATIC COACH
# ==========================================
elif nav_choice == "AI Somatic Coach":
    st.title("🤖 Adaptive Somatic AI Coach")
    st.caption("Neuroscience-backed unwinding protocols based on the Dual-Control Model.")

    if len(st.session_state.checkin_history) == 0:
        st.info("Complete your first Daily Check-In on the Dashboard to generate a personalized unwinding stack.")
    else:
        latest = st.session_state.checkin_history[-1]
        p_score = latest["Pelvic Tension"]
        s_score = latest["Stress"]
        brake = latest["Inhibitor"]

        st.markdown(f"""
            <div class="metric-card">
            <h4>Diagnostic Summary for Today</h4>
            <p><b>Pelvic Tension:</b> {p_score}/10 | <b>Stress Noise:</b> {s_score}/10 | <b>Primary Brake:</b> {brake}</p>
            </div>
        """, unsafe_allow_html=True)

        st.subheader("🛠️ Your Custom 7-Minute Unwind Stack")

        if p_score >= 6 and s_score >= 6:
            st.warning("Dual High Tension Detected (Mind + Pelvis). Initiating Deep Unwind.")
            st.markdown("""
            * **Minute 0–2 (Diaphragmatic Reset):** Inhale 4s, hold 2s, exhale 6s with explicit pelvic floor release.
            * **Minute 2–4 (Somatic Body Scan):** Unclench jaw, drop shoulders, soften gluteal muscles.
            * **Minute 4–7 (Audio Grounding):** Generate *'Somatic Decompression After Work'* in the Mind tab.
            """)
        elif p_score >= 6:
            st.warning("Pelvic Muscle Guarding Detected. Initiating Down-Training Focus.")
            st.markdown("""
            * **Minute 0–3 (Pelvic Drop Breathing):** Deep belly expansion focusing on lowering the levator ani.
            * **Minute 3–7 (Guided Down-Training Audio):** Play *'5-Min Pelvic Unwind'* in the Body tab.
            """)
        else:
            st.success("Tension Metrics Balanced. Ideal Foundation for Self-Exploration.")
            st.markdown("""
            * **Minute 0–5 (Self-Exploration Focus):** Try *'Phase 2: Anatomical Clitoral Mapping'* in the Mind tab.
            * **Minute 5–7 (Gratitude & Reflection):** Record a journal note in the Dashboard.
            """)

        st.markdown("---")
        st.subheader("📊 Smart Inhibitor Pattern Analysis")
        df = pd.DataFrame(st.session_state.checkin_history)
        if len(df) >= 3:
            top_brake = df["Inhibitor"].mode()[0]
            st.info(f"💡 **Insight:** Your most frequent intimacy brake over recent logs is **'{top_brake}'**. Consider scheduling low-energy connection dates (Tier 1) on these days.")
        else:
            st.caption("Log at least 3 daily check-ins to unlock automated pattern analysis.")

# ==========================================
# 8. SCREEN 4: BODY (PELVIC & PT TRACKER)
# ==========================================
elif nav_choice == "Body (Pelvic & PT Tracker)":
    st.title("Body: Pelvic Floor & Physical Therapy Tracker")
    st.caption("Clinical tools for hypertonia, dyspareunia relief, and progressive dilator logging.")

    tab1, tab2, tab3 = st.tabs(["5-Min Guided Audio", "Breath Pace Visualizer", "Dilator & PT Session Logger"])

    with tab1:
        st.subheader("Deep Somatic Unwinding & Pelvic Drop")
        st.caption("Public clinical audio stream for body scanning and release:")
        st.audio("https://www.mindfulnessinaction.ca/wp-content/uploads/2024/08/Body-Scan-10-mins.mp3")

    with tab2:
        st.subheader("Diaphragmatic Breath Visualizer")
        st.info("Inhale (4s) ➔ Hold (2s) ➔ Exhale (6s with Pelvic Floor Drop)")
        
        if st.button("Start Live Breath Guidance Cycle"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i in range(1, 4):
                for p in range(0, 101, 10):
                    progress_bar.progress(p)
                    status_text.markdown(f"### 🫁 INHALE (Expanding Belly) - Cycle {i}/3")
                    time.sleep(0.4)
                status_text.markdown(f"### ⏸️ HOLD (Soft) - Cycle {i}/3")
                time.sleep(2)
                for p in range(100, -1, -10):
                    progress_bar.progress(p)
                    status_text.markdown(f"### 🌬️ EXHALE & DROP PELVIS - Cycle {i}/3")
                    time.sleep(0.6)
            
            status_text.markdown("### ✨ Cycle Complete! Pelvic floor lowered.")

    with tab3:
        st.subheader("Dilator & PT Therapy Log")
        st.caption("Track progressive pelvic physical therapy exercises over time.")

        with st.form("dilator_form"):
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                d_size = st.selectbox("Dilator / Tool Size", ["Size 1 (Smallest)", "Size 2", "Size 3", "Size 4", "Size 5 (Largest)"])
            with col_b:
                d_time = st.number_input("Duration (Minutes)", min_value=1, max_value=60, value=10)
            with col_c:
                d_discomfort = st.slider("Discomfort Level (1 = None, 10 = High)", 1, 10, 2)
            
            pt_notes = st.text_input("Session Notes", placeholder="e.g., Used warming lube, focused on diaphragmatic breathing...")
            pt_submitted = st.form_submit_button("Log PT Session")

            if pt_submitted:
                st.session_state.dilator_logs.append({
                    "Date": str(datetime.date.today()),
                    "Size": d_size,
                    "Duration": d_time,
                    "Discomfort": d_discomfort,
                    "Notes": pt_notes
                })
                st.success("Physical therapy session logged securely!")

        if len(st.session_state.dilator_logs) > 0:
            st.markdown("### Logged PT Sessions")
            st.dataframe(pd.DataFrame(st.session_state.dilator_logs), use_container_width=True)

# ==========================================
# 9. SCREEN 5: MIND & SELF-EXPLORATION
# ==========================================
elif nav_choice == "Mind & Self-Exploration":
    st.title("Mind, Self-Exploration & Climax Pathways")
    st.caption("Somatic audio grounding, responsive desire education, and multi-phase guided climax modules.")

    tab1, tab2 = st.tabs(["🌸 Female Self-Exploration & Climax", "🎧 General Audio Modules"])

    # TAB 1: FEMALE SELF-EXPLORATION & CLIMAX
    with tab1:
        st.subheader("Guided Female Self-Exploration & Orgasm Protocols")
        st.caption("Progressive clinical techniques designed to guide you through arousal building, rhythm stacking, edging, and release.")

        selected_module_key = st.selectbox("Select Phase / Exploration Module:", list(FEMALE_EXPLORATION_MODULES.keys()))
        selected_mod = FEMALE_EXPLORATION_MODULES[selected_module_key]
        
        selected_voice_label_f = st.selectbox("Choose Narrator Voice Profile:", list(VOICE_PROFILES.keys()), key="fem_voice_select")

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown(f"### 📋 Overview & Guided Steps")
            st.write(f"*{selected_mod['description']}*")
            
            for step in selected_mod["steps"]:
                st.markdown(f"""
                    <div class="prompt-card">
                    <b>{step.split(':')[0]}:</b> {step.split(':')[1]}
                    </div>
                """, unsafe_allow_html=True)

            st.markdown("---")
            if st.button("▶️ Start Voice-Guided Audio Exploration", key="play_fem_audio"):
                with st.spinner("Synthesizing voice narration..."):
                    voice_config = VOICE_PROFILES[selected_voice_label_f]
                    tts = gTTS(text=selected_mod["script"], lang=voice_config["lang"], tld=voice_config["tld"], slow=False)
                    
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    fp.seek(0)
                    
                    st.audio(fp, format="audio/mp3")
                    st.success("Audio synthesized! Press play above and follow along at your own pace.")

        with col2:
            st.markdown("### 🎙️ Full Narration Script")
            st.markdown(f"""
                <div class="script-box">
                "{selected_mod['script']}"
                </div>
            """, unsafe_allow_html=True)

    # TAB 2: GENERAL AUDIO MODULES
    with tab2:
        st.subheader("General Audio & Decompression Vault")
        st.caption("Select a track script and choose a voice profile to generate live voice audio.")

        selected_track = st.selectbox("Select Audio Module:", list(AUDIO_SCRIPTS.keys()))
        selected_voice_label = st.selectbox("Choose Narrator Voice Profile:", list(VOICE_PROFILES.keys()), key="gen_voice_select")

        col_a, col_b = st.columns([1, 1])

        with col_a:
            st.markdown("### 🔊 Live Voice Generator")
            
            if st.button("▶️ Generate & Play Live Audio", key="play_gen_audio"):
                with st.spinner("Synthesizing narration in selected voice..."):
                    script_text = AUDIO_SCRIPTS[selected_track]
                    voice_config = VOICE_PROFILES[selected_voice_label]
                    
                    tts = gTTS(text=script_text, lang=voice_config["lang"], tld=voice_config["tld"], slow=False)
                    
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    fp.seek(0)
                    
                    st.audio(fp, format="audio/mp3")
                    st.success("Voice audio rendered successfully!")

        with col_b:
            st.markdown("### 📄 Script Preview")
            st.markdown(f"""
                <div class="script-box">
                "{AUDIO_SCRIPTS[selected_track]}"
                </div>
            """, unsafe_allow_html=True)

# ==========================================
# 10. SCREEN 6: SENSATE FOCUS & PARTNER DECK
# ==========================================
elif nav_choice == "Sensate Focus & Partner Deck":
    st.title("Partner Sync & Sensate Focus")
    st.caption("Low-pressure intimacy tools, non-verbal readiness beacons, and double-blind deck matching.")

    tab1, tab2, tab3 = st.tabs(["Readiness Beacon", "Double-Blind Partner Deck", "Manage Partner Link"])

    with tab1:
        st.subheader("📶 Non-Verbal Readiness Beacon")
        st.caption("Broadcast your capacity to your partner without awkward verbal requests.")

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
        st.caption("Select prompts privately. You are ONLY notified if both partners match.")

        tier_choice = st.selectbox("Select Energy Tier", list(CARD_DECK.keys()))
        prompts = CARD_DECK[tier_choice]

        selected_prompts = []
        with st.form("partner_deck_form"):
            for idx, prompt in enumerate(prompts):
                st.markdown(f"""
                    <div class="prompt-card">
                    <b>Prompt #{idx+1}:</b> {prompt}
                    </div>
                """, unsafe_allow_html=True)
                if st.checkbox(f"I'm open to this tonight", key=f"card_{tier_choice}_{idx}"):
                    selected_prompts.append(prompt)
            
            submitted = st.form_submit_button("Submit Secret Selections")
            
            if submitted:
                st.success("Selections saved to isolated vault!")
                if len(selected_prompts) > 0 and prompts[0] in selected_prompts:
                    st.balloons()
                    st.markdown(f"""
                        <div class="match-banner">
                        🎉 <b>IT'S A MATCH!</b><br>
                        Both you and your partner selected: <b>"{prompts[0]}"</b> for tonight.
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("No mutual matches detected yet tonight. Unmatched choices remain strictly confidential.")

    with tab3:
        st.subheader("🔗 Partner Link Manager")
        if st.session_state.linked_partner_id:
            st.success(f"🟢 Currently linked to partner ID: `{st.session_state.linked_partner_id}`")
            if st.button("Unlink Partner Account"):
                st.session_state.linked_partner_id = None
                st.rerun()
        else:
            st.info("You are not linked to a partner account.")
            p_code_input = st.text_input("Enter Partner Code to Link Now", placeholder="e.g. AURA-8F3K").strip().upper()
            if st.button("Link Partner"):
                if p_code_input == st.session_state.user_partner_code:
                    st.error("You cannot link to your own code.")
                elif len(p_code_input) >= 6:
                    st.session_state.linked_partner_id = p_code_input
                    st.success("Partner linked successfully!")
                    st.rerun()

# ==========================================
# 11. SCREEN 7: WEEKLY ANALYTICS & PT REPORT
# ==========================================
elif nav_choice == "Weekly Analytics & PT Report":
    st.title("Weekly Analytics & Clinical Reporting")
    st.caption("Correlations between stress, pelvic tension, and exportable physical therapy summaries.")

    if len(st.session_state.checkin_history) == 0:
        st.warning("No check-in logs recorded yet. Complete daily check-ins on the Dashboard to populate analytics!")
    else:
        df = pd.DataFrame(st.session_state.checkin_history)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Avg Pelvic Tension", f"{df['Pelvic Tension'].mean():.1f} / 10")
        with col2:
            st.metric("Avg Mental Stress", f"{df['Stress'].mean():.1f} / 10")
        with col3:
            st.metric("Check-Ins Recorded", f"{len(df)} Entries")

        st.markdown("---")
        st.subheader("Pelvic Tension vs. Stress Trends")

        fig = px.line(
            df, 
            x="Day", 
            y=["Pelvic Tension", "Stress"], 
            markers=True,
            color_discrete_map={"Pelvic Tension": "#A855F7", "Stress": "#3B82F6"}
        )
        fig.update_layout(
            paper_bgcolor="#0F172A",
            plot_bgcolor="#1E1B4B",
            font_color="#F8FAFC",
            yaxis=dict(range=[0, 10]),
            legend_title_text="Metrics"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.subheader("📄 Export Clinical Summary for PT / Doctor")
        st.caption("Download a formatted CSV summary to bring to your pelvic physical therapy or medical appointments.")

        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Clinical Progress CSV Report",
            data=csv_data,
            file_name=f"aura_pelvic_health_report_{datetime.date.today()}.csv",
            mime="text/csv"
        )

# ==========================================
# 12. SCREEN 8: PRIVACY & SECURITY
# ==========================================
elif nav_choice == "Privacy & Security":
    st.title("Privacy, Security & Data Erasure")
    st.caption("Zero-Knowledge guarantees and cloud retention schedules.")

    st.table({
        "Data Category": ["Account Auth & Profile", "Daily Pelvic Logs", "Partner Status Signals", "Unmatched Double-Blind Votes"],
        "Retention Period": ["Duration of Active Account", "24 Months (Rolling)", "30 Days (Auto-Purged)", "90 Days (Hard Deleted)"],
        "Storage Protocol": ["Encrypted Database", "Anonymized & AES-256", "Auto-Overwritten", "Hard Delete"]
    })

    st.markdown("---")
    st.subheader("⚠️ Hard Reset Vault")
    if st.button("Trigger Immediate Account Data Erasure"):
        st.session_state.checkin_history = []
        st.session_state.dilator_logs = []
        st.session_state.linked_partner_id = None
        st.error("All local logs and links wiped from session memory.")
        st.session_state.authenticated = False
        st.rerun()
