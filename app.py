import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import time
import secrets
import io
from gtts import gTTS

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
        padding: 1.2rem;
        border-radius: 10px;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .icebreaker-box {
        background-color: #1E293B;
        border: 1px dashed #A855F7;
        border-radius: 8px;
        padding: 0.85rem;
        margin-top: 0.5rem;
        font-style: italic;
        color: #E2E8F0;
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
if "user_mode" not in st.session_state:
    st.session_state.user_mode = "Singles Proximity Mode"  # or "Couples Mode"
if "checkin_history" not in st.session_state:
    st.session_state.checkin_history = []
if "dilator_logs" not in st.session_state:
    st.session_state.dilator_logs = []
if "partner_beacon" not in st.session_state:
    st.session_state.partner_beacon = "💬 Open to Talk & Coffee"

# PARTNER & SINGLES PROXIMITY INITIALIZATION
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

# SAFE ZONES DATABASE
SAFE_ZONES = ["All Locations (GPS Radius)", "Artisan Coffee Lounge (Downtown)", "Wellness & Spa Pavilion", "Botanical Gardens Lounge"]

# MOCK NEARBY SINGLES BEACONS (Simulated live database)
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

# EROTIC CONTEXT QUESTIONS DATABASE
EROTIC_CONTEXT_QUESTIONS = {
    "Cognitive Load & Tasks": "I find it hard to feel desire or reach climax if I have unfinished chores, work emails, or mental stress lingering.",
    "Emotional Closeness": "I need to feel emotionally connected, appreciated, and close before I feel open to deep physical release.",
    "Somatic & Muscle Comfort": "Physical relaxation, bodily warmth, and an absence of pelvic muscle guarding are essential for me to climax.",
    "Sensory Environment": "Factors like dim lighting, pleasant scents, clean sheets, and ambient music strongly influence my ability to focus on pleasure.",
    "Novelty & Playfulness": "Playful teasing, unexpected affection, changing locations, or roleplay easily activates my arousal."
}

# AUDIO SCRIPTS DATABASE
AUDIO_SCRIPTS = {
    "Understanding Responsive Desire": (
        "Welcome. Many people expect sexual desire to happen spontaneously—like a sudden bolt of lightning. "
        "But for most adults, desire works responsively. Spontaneous desire is like feeling hungry before you see food. "
        "Responsive desire is like not feeling hungry at all, but then sitting down at a nice table, smelling a delicious meal, "
        "taking a bite, and realizing, 'Actually, this is wonderful.' Desire doesn't always start in the mind; "
        "it often begins in the body after safety, relaxation, and physical presence are established."
    ),
    "Somatic Decompression After Work": (
        "Sit or lie down in a comfortable position. Unclench your jaw, drop your shoulders away from your ears, "
        "and let your hands rest gently in your lap or at your side. Take a deep breath in through your nose for a count of four... "
        "hold for two... and exhale slowly through your mouth for six. With every exhale, imagine discharging accumulated stress into the ground below you."
    )
}

# FEMALE SELF-EXPLORATION & CLIMAX GUIDED MODULES
FEMALE_EXPLORATION_MODULES = {
    "Phase 1: Zero-Pressure Somatic Mapping": {
        "description": "A gentle journey mapping non-genital erogenous zones to awaken body awareness without expectation of performance.",
        "steps": [
            "Step 1: Set the scene—warm lighting, comfortable support under your knees, and a drop of preferred oil.",
            "Step 2: Spend 2 minutes using light fingertip pressure along your collarbones, neck, and inner arms.",
            "Step 3: Notice micro-sensations—temperature, tingling, or goosebumps—without trying to force arousal.",
            "Step 4: Rest your palm gently over your lower abdomen, syncing your breath with the rise and fall of your belly."
        ],
        "script": "Welcome to your private self-exploration space. Today there is no goal, no timer, and no expectation of climax..."
    },
    "Phase 2: Anatomical Clitoral Mapping & Rhythms": {
        "description": "Technique focusing on indirect clitoral stimulation, pressure variations, and rhythm consistency necessary for arousal building.",
        "steps": [
            "Step 1: Apply a generous amount of warm lubricant around the labia and outer vulvar tissue.",
            "Step 2: Begin with gentle circular motions along the outer labia, avoiding direct glans touch to prevent oversensitivity.",
            "Step 3: Transition to a slow 'clock' pattern around the clitoral hood.",
            "Step 4: Establish a steady, rhythmic pressure. Rhythm consistency is key to helping the nervous system build arousal."
        ],
        "script": "Ensure you have plenty of warm lubricant ready. Begin by applying it softly around your outer labia..."
    }
}

# PARTNER DECK DATABASE
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

# VOICE PROFILES MAPPING
VOICE_PROFILES = {
    "🇦🇺 Grounded & Deep (Australian Accent)": {"lang": "en", "tld": "com.au"},
    "🇬🇧 Warm & Expressive (British Accent)": {"lang": "en", "tld": "co.uk"},
    "🇺🇸 Calm & Clear (US Accent)": {"lang": "en", "tld": "com"}
}

# ==========================================
# 3. SIDEBAR NAVIGATION
# ==========================================
st.sidebar.title("🧘‍♀️ Aura Health")
st.sidebar.caption("Mind, Body & Discovery Platform")

if st.session_state.authenticated:
    st.sidebar.markdown("---")
    
    # MODE SWITCHER IN SIDEBAR
    st.sidebar.subheader("⚙️ Account Mode")
    st.session_state.user_mode = st.sidebar.radio(
        "Active Mode:",
        ["Singles Proximity Mode", "Couples Mode"],
        key="sidebar_mode_select"
    )

    st.sidebar.markdown("---")
    
    nav_items = [
        "Dashboard & Check-In", 
        "Erotic Context Profile"
    ]

    if st.session_state.user_mode == "Singles Proximity Mode":
        nav_items.append("📍 Proximity & Erotic Discovery")
        nav_items.append("Sensate Focus & Partner Deck")
    else:
        nav_items.append("Sensate Focus & Partner Deck")

    nav_items.extend([
        "AI Somatic Coach", 
        "Body (Pelvic & PT Tracker)", 
        "Mind & Self-Exploration", 
        "Weekly Analytics & PT Report", 
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
# 4. SCREEN 0: AUTHENTICATION & CONSENT (WITH OPTION A)
# ==========================================
if not st.session_state.authenticated:
    st.title("Welcome to Aura")
    st.subheader("Integrated Mind, Body, and Partner Well-being")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### Secure Sign-In")
        email = st.text_input("Email Address", value="alex@aura-health.app")
        password = st.text_input("Password", type="password", value="••••••••••••")
        
        st.markdown("### 👩‍❤️‍👨 Partner Link (Optional at Login)")
        partner_input_at_login = st.text_input(
            "Partner Invite Code", 
            placeholder="e.g. AURA-8F3K (Leave blank if connecting later or using Singles Mode)",
            help="If your partner gave you a link code, enter it here to connect your accounts immediately."
        ).strip().upper()

        st.markdown("### Privacy & Sensitive Data Consent")
        st.markdown("""
            <div class="legal-box">
            <b>PRIVACY & SENSITIVE DATA CONSENT (GDPR Art. 9 / HIPAA / POPIA)</b><br><br>
            Aura processes Special Category Health Data. Before proceeding, you must review and consent:<br><br>
            <b>1. Sensitive Data Collected:</b> Pelvic muscle tone ratings, dyspareunia severity, stress metrics, and partner connection signals.<br>
            <b>2. Zero-Knowledge Architecture:</b> Intimacy logs and pelvic notes are client-side encrypted via AES-256 GCM.<br>
            <b>3. Double-Blind Isolation:</b> Unmatched partner and singles desire selections are never exposed or transmitted.<br>
            <b>4. No Data Monetization:</b> Aura will NEVER sell, rent, or trade your health data.
            </div>
        """, unsafe_allow_html=True)
        
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

    with col2:
        st.markdown("""
            <div class="metric-card">
            <h4>Pillars of Clinical & Discovery Care</h4>
            <ul>
                <li><b>Body:</b> Pelvic floor down-training & physical therapy logging.</li>
                <li><b>Mind & Exploration:</b> Step-by-step female self-stimulation & climax guides.</li>
                <li><b>Proximity Discovery:</b> Double-blind desire matching for singles nearby.</li>
                <li><b>Partner Sync:</b> Double-blind desire matching & Sensate Focus guides for couples.</li>
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
    st.caption(f"Today is {datetime.date.today().strftime('%A, %B %d, %Y')} | Active Mode: **{st.session_state.user_mode}**")

    if len(st.session_state.checkin_history) > 0:
        latest = st.session_state.checkin_history[-1]
        p_val = f"{latest['Pelvic Tension']}/10"
        s_val = f"{latest['Stress']}/10"
    else:
        p_val = "No log today"
        s_val = "No log today"

    if st.session_state.user_mode == "Couples Mode":
        mode_status_text = f"Linked to {st.session_state.linked_partner_id}" if st.session_state.linked_partner_id else "Not Linked"
        mode_card_title = "👩‍❤️‍👨 Partner Vault"
    else:
        mode_status_text = "Proximity Radar Active"
        mode_card_title = "📍 Proximity Beacon"

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
            <h3>{mode_card_title}</h3>
            <p><b>Your Status:</b> {st.session_state.partner_beacon}</p>
            <p><b>State:</b> {mode_status_text}</p>
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

# ==========================================
# 6. NEW SCREEN: PROXIMITY & EROTIC DISCOVERY (SINGLES)
# ==========================================
elif nav_choice == "📍 Proximity & Erotic Discovery":
    st.title("📍 Proximity & Erotic Preference Matcher")
    st.caption("Double-blind proximity matching real-time readiness capacity and mutual erotic desires.")

    if st.session_state.user_mode == "Couples Mode":
        st.warning("⚠️ You are currently in Couples Mode. Switch your account mode in the sidebar to 'Singles Proximity Mode' to use local discovery.")
    else:
        col_settings, col_beacon = st.columns([1, 1])

        with col_settings:
            st.markdown("### 1. Discovery Radar Filters")
            
            radius_km = st.slider("Scan Radius (Kilometers)", min_value=0.5, max_value=20.0, value=5.0, step=0.5)
            selected_safe_zone = st.selectbox("Safe Zone / Venue Filter", SAFE_ZONES)
            req_verified = st.checkbox("Require Verified Beacon Badge Only", value=True)
            min_shared_tags = st.slider("Minimum Mutual Erotic Desires Required", min_value=1, max_value=5, value=1)

        with col_beacon:
            st.markdown("### 2. Your Active Readiness Beacon")
            
            st.session_state.partner_beacon = st.selectbox(
                "What is your capacity right now?",
                ["💬 Open to Talk & Coffee", "🧘 Open to Touch (Zero Pressure)", "🔥 Open to Intimacy", "🔋 Energy Low (Discovery Paused)"]
            )
            
            beacon_ttl = st.selectbox("Beacon Duration (Auto-Expires)", ["2 Hours", "4 Hours", "8 Hours"])
            
            if st.session_state.partner_beacon != "🔋 Energy Low (Discovery Paused)":
                st.success(f"🟢 Beacon active for {beacon_ttl} | Visible to verified singles within {radius_km} km")
            else:
                st.warning("🔴 Beacon paused. You are invisible to nearby users.")

        st.markdown("---")

        # SECTION 3: EROTIC DESIRE PREFERENCES (PRIVATE)
        st.markdown("### 3. Private Erotic Preferences & Desires")
        st.caption("Select your desires and interests. These remain strictly double-blind (hidden) unless a mutual match is triggered.")

        st.session_state.user_erotic_interests = st.multiselect(
            "Select your active desires and boundaries:",
            options=EROTIC_TAXONOMY,
            default=st.session_state.user_erotic_interests
        )

        st.markdown("---")

        # SECTION 4: DOUBLE-BLIND MATCH ENGINE
        st.markdown("### 4. Nearby Double-Blind Matches")

        if st.session_state.partner_beacon == "🔋 Energy Low (Discovery Paused)":
            st.info("Set an active readiness status above to start scanning for nearby matches.")
        elif not st.session_state.user_erotic_interests:
            st.info("Please select at least one erotic preference above to enable double-blind matching.")
        else:
            # DOUBLE-BLIND MATCH ALGORITHM
            matches = []
            for candidate in MOCK_NEARBY_SINGLES:
                # 1. Filter Radius
                if candidate["distance_km"] <= radius_km:
                    # 2. Filter Verified Badge if required
                    if not req_verified or candidate["verified"]:
                        # 3. Filter Safe Zone if chosen
                        if selected_safe_zone == "All Locations (GPS Radius)" or candidate["safe_zone"] == selected_safe_zone:
                            # 4. Readiness Status Match
                            if candidate["readiness"] == st.session_state.partner_beacon:
                                # 5. Calculate Shared Erotic Desires
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
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h4 style="margin: 0;">📍 Nearby Beacon: {match['id']}</h4>
                            <span style="background-color: #047857; padding: 0.2rem 0.6rem; border-radius: 4px; font-size: 0.8rem;">{badge_html}</span>
                        </div>
                        <p style="margin-top: 0.5rem; margin-bottom: 0.25rem;"><b>Coarse Distance:</b> ~{match['distance']} km away | <b>Location:</b> {match['safe_zone']}</p>
                        <p style="margin-bottom: 0.25rem;"><b>Readiness Alignment:</b> {st.session_state.partner_beacon}</p>
                        <p style="margin-bottom: 0.25rem;"><b>Mutual Desires ({match['shared_count']}):</b> {', '.join(match['shared_tags'])}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # ICEBREAKER GENERATOR
                    primary_tag = match['shared_tags'][0]
                    icebreaker_text = f"Hey! I noticed we both matched on '{primary_tag}' and have our readiness set to '{st.session_state.partner_beacon}'. Would you like to chat?"
                    
                    st.markdown(f"""
                        <div class="icebreaker-box">
                        💡 <b>Context-Aware Icebreaker Idea:</b><br>
                        "{icebreaker_text}"
                        </div>
                    """, unsafe_allow_html=True)

                    c1, c2 = st.columns([1, 1])
                    with c1:
                        if st.button(f"Send Encrypted Signal to {match['id']}", key=f"sig_{match['id']}"):
                            st.success(f"Private signal sent to {match['id']}! A secure chat window will open once accepted.")
                    st.markdown("---")
            else:
                st.info("No nearby beacons currently match your readiness status, distance radius, and shared desire threshold. Try expanding your radius or selecting additional erotic preferences.")

# ==========================================
# 7. SCREEN: EROTIC CONTEXT PROFILE
# ==========================================
elif nav_choice == "Erotic Context Profile":
    st.title("✨ Custom Erotic Context Profile")
    st.caption("Map your unique desire accelerators and brakes based on the Dual-Control Model.")

    scores = {}
    with st.form("erotic_profile_form"):
        st.subheader("Contextual Sensitivity Assessment")
        st.write("Rate how significantly each dimension impacts your ability to feel open to intimacy:")
        
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

# ==========================================
# 8. SCREEN: AI SOMATIC COACH
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
        else:
            st.success("Tension Metrics Balanced. Ideal Foundation for Rest or Exploration.")

# ==========================================
# 9. SCREEN: BODY (PELVIC & PT TRACKER)
# ==========================================
elif nav_choice == "Body (Pelvic & PT Tracker)":
    st.title("Body: Pelvic Floor & Physical Therapy Tracker")
    st.caption("Clinical tools for hypertonia, dyspareunia relief, and progressive dilator logging.")

    tab1, tab2, tab3 = st.tabs(["5-Min Guided Audio", "Breath Pace Visualizer", "Dilator & PT Session Logger"])

    with tab1:
        st.subheader("Deep Somatic Unwinding & Pelvic Drop")
        st.audio("https://www.mindfulnessinaction.ca/wp-content/uploads/2024/08/Body-Scan-10-mins.mp3")

    with tab2:
        st.subheader("Diaphragmatic Breath Visualizer")
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
        with st.form("dilator_form"):
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                d_size = st.selectbox("Dilator / Tool Size", ["Size 1 (Smallest)", "Size 2", "Size 3", "Size 4", "Size 5 (Largest)"])
            with col_b:
                d_time = st.number_input("Duration (Minutes)", min_value=1, max_value=60, value=10)
            with col_c:
                d_discomfort = st.slider("Discomfort Level (1 = None, 10 = High)", 1, 10, 2)
            
            pt_notes = st.text_input("Session Notes", placeholder="Notes on pelvic relaxation...")
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

# ==========================================
# 10. SCREEN: MIND & SELF-EXPLORATION
# ==========================================
elif nav_choice == "Mind & Self-Exploration":
    st.title("Mind, Self-Exploration & Climax Pathways")
    st.caption("Somatic audio grounding, responsive desire education, and multi-phase guided climax modules.")

    selected_module_key = st.selectbox("Select Phase / Exploration Module:", list(FEMALE_EXPLORATION_MODULES.keys()))
    selected_mod = FEMALE_EXPLORATION_MODULES[selected_module_key]
    selected_voice_label = st.selectbox("Choose Narrator Voice Profile:", list(VOICE_PROFILES.keys()))

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

        if st.button("▶️ Start Voice-Guided Audio Exploration"):
            with st.spinner("Synthesizing voice narration..."):
                voice_config = VOICE_PROFILES[selected_voice_label]
                tts = gTTS(text=selected_mod["script"], lang=voice_config["lang"], tld=voice_config["tld"], slow=False)
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                st.audio(fp, format="audio/mp3")

    with col2:
        st.markdown("### 🎙️ Full Narration Script")
        st.markdown(f"""
            <div class="script-box">
            "{selected_mod['script']}"
            </div>
        """, unsafe_allow_html=True)

# ==========================================
# 11. SCREEN: SENSATE FOCUS & PARTNER DECK
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
# 12. SCREEN: WEEKLY ANALYTICS & PT REPORT
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

        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Clinical Progress CSV Report",
            data=csv_data,
            file_name=f"aura_pelvic_health_report_{datetime.date.today()}.csv",
            mime="text/csv"
        )

# ==========================================
# 13. SCREEN: PRIVACY & SECURITY
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
        st.error("All local logs wiped from session memory.")
        st.session_state.authenticated = False
        st.rerun()
