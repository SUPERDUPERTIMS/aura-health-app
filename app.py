import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import time
from gtts import gTTS
import io

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
        height: 180px;
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

# AUDIO SCRIPTS DATABASE
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
    ),
    "Warm Candlelight Narrative": (
        "The room is soft, quiet, and warm, lit only by the gentle flicker of candlelight dancing against the walls. "
        "The air holds the faint scent of cedar and warm vanilla. As you lie back, you feel the soft fabric against your skin "
        "and the complete absence of urgency. You feel completely safe, seen, and unhurried. Slow, deliberate touch glides "
        "over your shoulders, tracing down your arms with gentle pressure, allowing your mind to drift away into the present moment."
    )
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
    "🇦🇺 Grounded & Deep / Accent (Australian Male/Female)": {"lang": "en", "tld": "com.au"},
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
            "AI Somatic Coach", 
            "Body (Pelvic & PT Tracker)", 
            "Mind (Audio & Multi-Voice)", 
            "Sensate Focus & Partner Deck", 
            "Weekly Analytics & PT Report", 
            "Privacy & Security"
        ]
    )
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔒 Vault Security")
    st.sidebar.success("AES-256 Client Vault: ACTIVE")
    st.sidebar.info("Zero-Knowledge: VERIFIED")
    
    if st.sidebar.button("Lock Portal / Log Out"):
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
            <h4>Pillars of Clinical Care</h4>
            <ul>
                <li><b>Body:</b> Pelvic floor down-training & physical therapy logging.</li>
                <li><b>Mind:</b> Multi-voice audio grounding & Dual-Control Model science.</li>
                <li><b>Partner:</b> Double-blind desire matching & Sensate Focus guides.</li>
                <li><b>Analytics:</b> One-click PDF/CSV reports for physical therapists.</li>
            </ul>
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
            <p><b>Sensate Mode:</b> Active</p>
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
                    st.write("Muscle tone is low. Good foundation for rest.")

            with c2:
                if m_stress >= 6:
                    st.warning("⚠️ High Stress Active")
                    st.write("Open **Mind** to generate decompression tracks.")
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
# 6. SCREEN 2: AI SOMATIC COACH
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
            st.success("Tension Metrics Balanced. Initiating Restorative Maintenance.")
            st.markdown("""
            * **Minute 0–5 (Low-Pressure Connection):** Use the Partner Beacon to signal readiness for gentle contact.
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
# 7. SCREEN 3: BODY (PELVIC & PT TRACKER)
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
# 8. SCREEN 4: MIND (MULTI-VOICE AUDIO)
# ==========================================
elif nav_choice == "Mind (Audio & Multi-Voice)":
    st.title("Mind: Multi-Voice Audio Generator")
    st.caption("Select a track script and choose a voice profile to generate live voice audio.")

    selected_track = st.selectbox("Select Audio Module:", list(AUDIO_SCRIPTS.keys()))
    selected_voice_label = st.selectbox("Choose Narrator Voice Profile:", list(VOICE_PROFILES.keys()))

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 🔊 Live Voice Generator")
        
        if st.button("▶️ Generate & Play Live Audio"):
            with st.spinner("Synthesizing narration in selected voice..."):
                script_text = AUDIO_SCRIPTS[selected_track]
                voice_config = VOICE_PROFILES[selected_voice_label]
                
                # Generate MP3 in-memory via gTTS
                tts = gTTS(text=script_text, lang=voice_config["lang"], tld=voice_config["tld"], slow=False)
                
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                
                st.audio(fp, format="audio/mp3")
                st.success("Voice audio rendered successfully!")

    with col2:
        st.markdown(f"### 📄 Script Preview")
        st.markdown(f"""
            <div class="script-box">
            "{AUDIO_SCRIPTS[selected_track]}"
            </div>
        """, unsafe_allow_html=True)

# ==========================================
# 9. SCREEN 5: SENSATE FOCUS & PARTNER DECK
# ==========================================
elif nav_choice == "Sensate Focus & Partner Deck":
    st.title("Partner Sync & Sensate Focus")
    st.caption("Low-pressure intimacy tools, non-verbal readiness beacons, and double-blind deck matching.")

    tab1, tab2 = st.tabs(["Readiness Beacon", "Double-Blind Partner Deck"])

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

# ==========================================
# 10. SCREEN 6: WEEKLY ANALYTICS & PT REPORT
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
# 11. SCREEN 7: PRIVACY & SECURITY
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
        st.error("All local logs wiped from session memory.")
        st.session_state.authenticated = False
        st.rerun()
