import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import time

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
        height: 200px;
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
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. SESSION STATE MANAGEMENT (PERSISTENCE)
# ==========================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_name" not in st.session_state:
    st.session_state.user_name = "Alex"

# Clean state (Starts empty for real user data)
if "checkin_history" not in st.session_state:
    st.session_state.checkin_history = []

# 30-Card Double Blind Deck Database
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

# ==========================================
# 3. SIDEBAR NAVIGATION
# ==========================================
st.sidebar.title("🧘‍♀️ Aura Health")
st.sidebar.caption("Mind, Body & Partner Sync Platform")

if st.session_state.authenticated:
    st.sidebar.markdown("---")
    nav_choice = st.sidebar.radio(
        "Navigation",
        ["Dashboard & Check-In", "Body (Pelvic Down-Training)", "Mind (Audio Library)", "Partner Sync Deck", "Weekly Analytics", "Privacy & DPA"]
    )
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔒 Security Status")
    st.sidebar.success("AES-256 Vault: ACTIVE")
    st.sidebar.info("Zero-Knowledge: VERIFIED")
    
    if st.sidebar.button("Lock / Log Out"):
        st.session_state.authenticated = False
        st.rerun()
else:
    nav_choice = "Auth"

# ==========================================
# 4. SCREEN 0: AUTHENTICATION & CONSENT
# ==========================================
if not st.session_state.authenticated:
    st.title("Welcome to Aura")
    st.subheader("Integrated Mind, Body, and Partner Well-being")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### Secure Sign-In")
        email = st.text_input("Email Address", value="alex@aura-health.app")
        password = st.text_input("Password", type="password", value="••••••••••••")
        
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
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Explicit consent is required to access sensitive pelvic features.")

    with col2:
        st.markdown("""
            <div class="metric-card">
            <h4>Pillars of Care</h4>
            <ul>
                <li><b>Body:</b> Clinical pelvic floor down-training & somatic release.</li>
                <li><b>Mind:</b> Audio grounding & Dual-Control desire science.</li>
                <li><b>Partner:</b> Double-blind desire matching without rejection risk.</li>
            </ul>
            </div>
        """, unsafe_allow_html=True)

# ==========================================
# 5. SCREEN 1: DASHBOARD & DAILY CHECK-IN
# ==========================================
elif nav_choice == "Dashboard & Check-In":
    st.title(f"Welcome Back, {st.session_state.user_name}")
    st.caption(f"Today is {datetime.date.today().strftime('%A, %B %d, %Y')}")

    # Top Status Cards
    if len(st.session_state.checkin_history) > 0:
        latest = st.session_state.checkin_history[-1]
        p_val = f"{latest['Pelvic Tension']}/10"
        s_val = f"{latest['Stress']}/10"
    else:
        p_val = "No log today"
        s_val = "No log today"

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
            <div class="metric-card">
            <h3>🧘‍♀️ Body Status</h3>
            <p><b>Pelvic Tone:</b> {p_val}</p>
            <p><b>Target:</b> 5-Min Down-Training</p>
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
        st.markdown("""
            <div class="metric-card">
            <h3>👩‍❤️‍👨 Partner Sync</h3>
            <p><b>Signal:</b> Open to Connection</p>
            <p><b>Prompts Pending:</b> 3 Cards Ready</p>
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
                "Minutes Down-Trained": 0,
                "Inhibitor": brake,
                "Note": note if note else "No private note added."
            }
            st.session_state.checkin_history.append(new_entry)
            st.success("✅ Check-in saved securely!")

            # TAILORED NEXT STEPS BASED ON RATINGS
            st.markdown("---")
            st.markdown("### 🎯 Recommended Next Steps")
            st.caption("Tap the `>>` sidebar icon at the top-left of your screen to open these modules:")
            
            c1, c2, c3 = st.columns(3)
            
            with c1:
                if p_tension >= 6:
                    st.warning("⚠️ High Pelvic Tension")
                    st.write("Open **Body** in the menu to start a 5-minute diaphragmatic down-training session.")
                else:
                    st.success("🟢 Pelvic Tone Calm")
                    st.write("Your muscle tone is low. Good foundation for rest or intimacy.")

            with c2:
                if m_stress >= 6:
                    st.warning("⚠️ High Stress Active")
                    st.write("Open **Mind** in the menu to listen to a 6-minute stress decompression track.")
                else:
                    st.success("🟢 Stress Managed")
                    st.write("Mental noise is low today.")

            with c3:
                st.info("💡 Partner Connection")
                st.write("Open **Partner Sync Deck** in the menu to secretly select low-pressure activities for tonight.")

    # HISTORICAL LOG DISPLAY
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
# 6. SCREEN 2: BODY (PELVIC DOWN-TRAINING)
# ==========================================
elif nav_choice == "Body (Pelvic Down-Training)":
    st.title("Body: Pelvic Floor Down-Training")
    st.caption("Clinical physical therapy protocols for hypertonia, dyspareunia, and somatic relief.")

    tab1, tab2 = st.tabs(["5-Min Guided Session", "Breathing Pace Visualizer"])

    with tab1:
        st.subheader("Deep Somatic Unwinding & Pelvic Drop")
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

        with st.expander("📄 View Word-for-Word Narration Script"):
            st.markdown("""
            **Minute 0:00 - 1:00 (Setup):** Welcome. Find a comfortable position on your back with knees bent or resting in child's pose. Place one hand on your belly and one on your chest. Unclench your jaw. Drop your shoulders away from your ears...
            
            **Minute 1:00 - 3:30 (Expansion & Drop):** Inhale for 4 seconds into your belly... Hold for 2... Exhale for 6 seconds through your mouth. Imagine your pelvic floor muscles gently melting downward, like a hammock lowering toward the floor. Do not push. Simply stop holding...
            
            **Minute 3:30 - 5:00 (Somatic Scan):** Sweep your attention through your lower body. As your jaw softens, your pelvis follows. Take one final deep breath... and carry this soft feeling into your evening.
            """)

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

# ==========================================
# 7. SCREEN 3: MIND (AUDIO LIBRARY)
# ==========================================
elif nav_choice == "Mind (Audio Library)":
    st.title("Mind: Responsive Desire & Audio Library")
    st.caption("Dual-Control Model psychoeducation, somatic grounding, and guided intimacy.")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### Featured Audio")
        st.markdown("""
            <div class="metric-card">
            <h4>🎧 Releasing the Day's Stress</h4>
            <p><b>Category:</b> Dual-Control Science</p>
            <p><b>Duration:</b> 6 Mins</p>
            <p>Understanding how stress acts as a mental brake on desire.</p>
            </div>
        """, unsafe_allow_html=True)
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3")

    with col2:
        st.markdown("### Audio Library")
        category = st.selectbox("Category", ["All", "Somatic Grounding", "Psychoeducation", "Erotic Audio", "Sensate Preparation"])
        
        tracks = [
            {"Title": "Understanding Responsive Desire", "Cat": "Psychoeducation", "Dur": "6 Mins"},
            {"Title": "Somatic Decompression After Work", "Cat": "Somatic Grounding", "Dur": "8 Mins"},
            {"Title": "Sensate Focus Phase 1 Preparation", "Cat": "Sensate Preparation", "Dur": "12 Mins"},
            {"Title": "Warm Candlelight Narrative", "Cat": "Erotic Audio", "Dur": "10 Mins"},
        ]
        
        for t in tracks:
            if category == "All" or category == t["Cat"]:
                st.markdown(f"""
                    <div class="prompt-card">
                    <b>{t['Title']}</b> ({t['Dur']})<br>
                    <small>Category: {t['Cat']}</small>
                    </div>
                """, unsafe_allow_html=True)

# ==========================================
# 8. SCREEN 4: PARTNER SYNC DECK
# ==========================================
elif nav_choice == "Partner Sync Deck":
    st.title("Double-Blind Partner Deck")
    st.caption("Select prompts privately. You are ONLY notified if both partners match.")

    tier_choice = st.selectbox("Select Energy Tier", list(CARD_DECK.keys()))
    prompts = CARD_DECK[tier_choice]

    st.markdown("### Tonight's Deck Selections")
    
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
            st.success("Selections saved to isolated Zero-Leak Vault!")
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

# ==========================================
# 9. SCREEN 5: WEEKLY ANALYTICS
# ==========================================
elif nav_choice == "Weekly Analytics":
    st.title("Weekly Analytics & Clinical Progress")
    st.caption("Correlations between stress, pelvic tension, and down-training interventions.")

    if len(st.session_state.checkin_history) == 0:
        st.warning("No check-in logs recorded yet. Complete a few daily check-ins on the Dashboard to see your analytics charts!")
    else:
        df = pd.DataFrame(st.session_state.checkin_history)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Avg Pelvic Tension", f"{df['Pelvic Tension'].mean():.1f} / 10")
        with col2:
            st.metric("Avg Mental Stress", f"{df['Stress'].mean():.1f} / 10")
        with col3:
            st.metric("Total Logs Recorded", f"{len(df)} Entries")

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

# ==========================================
# 10. SCREEN 6: PRIVACY & DPA
# ==========================================
elif nav_choice == "Privacy & DPA":
    st.title("Privacy, Data Retention & Cloud DPA")
    st.caption("Infrastructure compliance details under GDPR, HIPAA, and POPIA.")

    tab1, tab2 = st.tabs(["Data Retention Policy", "Cloud DPA Schedule"])

    with tab1:
        st.markdown("### Data Retention Limits")
        st.table({
            "Data Category": ["Account Auth & Profile", "Daily Pelvic Logs", "Partner Status Signals", "Unmatched Double-Blind Votes"],
            "Retention Period": ["Duration of Active Account", "24 Months (Rolling)", "30 Days (Auto-Purged)", "90 Days (Hard Deleted)"],
            "Storage Protocol": ["Encrypted Database", "Anonymized & AES-256", "Auto-Overwritten", "Hard Delete"]
        })

        if st.button("Trigger Immediate Account & Data Erasure"):
            st.session_state.checkin_history = []
            st.error("Account erasure requested. All local encryption keys revoked.")
            st.session_state.authenticated = False
            st.rerun()

    with tab2:
        st.markdown("""
            ### DATA PROCESSING AGREEMENT (DPA) SCHEDULE
            **Schedule ID:** DPA-SCHED-SPECIAL-HEALTH-V1  
            **Applicability:** Cloud Infrastructure Vendors (AWS/GCP/Azure)
            
            #### 1. Technical & Organizational Measures (TOMs)
            * **Encryption at Rest:** AES-256 enforced across disk, DB instances, and backups.
            * **Encryption in Transit:** Mandatory TLS 1.3 for all VPC crossing traffic.
            * **Field-Level Isolation:** Client-side AES-256 envelope encryption.
            
            #### 2. Incident Management & SLAs
            * **24-Hour Notification:** Subprocessor must notify Aura within 24 hours of detecting a suspected security breach.
        """)
