import time

import streamlit as st


GAME_SECONDS = 60
st.set_page_config(page_title="Number Hunt Game", page_icon="🔢", layout="centered")

st.markdown("""
<style>
:root { --ink:#15233b; --muted:#64748b; --blue:#465df5; --mint:#dff8ef; }
.stApp { background: radial-gradient(ellipse at 8% 0%,#e5ebff 0,transparent 38%),#f5f7fc; color:var(--ink); }
.block-container { max-width:780px; padding:1.4rem 1.2rem 2rem; }
html, body, [class*="css"] { font-family:system-ui,-apple-system,'Segoe UI',sans-serif; }
h1,h2,h3 { font-family:system-ui,-apple-system,'Segoe UI',sans-serif !important; color:var(--ink); }
.brand { display:flex; align-items:center; gap:12px; margin:0 0 1.25rem; }
.brand-icon { display:grid; place-items:center; width:48px; height:48px; border-radius:15px; background:#465df5; color:white; font-size:25px; box-shadow:0 8px 20px #465df540; }
.brand-title { font:700 1.1rem system-ui,sans-serif; letter-spacing:-.03em; }
.brand-sub { color:var(--muted); font-size:.78rem; }
.hero,.panel { background:#fff; border:1px solid #e8ecf5; border-radius:24px; padding:clamp(1.15rem,4vw,2rem); box-shadow:0 14px 40px #263a6410; }
.eyebrow { color:#465df5; font-size:.76rem; font-weight:800; letter-spacing:.12em; text-transform:uppercase; }
.hero h1 { font-size:clamp(2rem,7vw,3.25rem); line-height:1.03; margin:.5rem 0 .8rem; letter-spacing:-.06em; }
.intro { color:#52627a; font-size:1.02rem; line-height:1.65; }
.developer { margin-top:1.2rem; color:#52627a; font-size:.88rem; }
.developer strong { color:#263654; }
.stats { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin:1rem 0; }
.stat { background:#f7f8ff; border:1px solid #e9ecfa; border-radius:17px; padding:14px 17px; }
.stat-label { color:#70809b; font-size:.76rem; font-weight:700; text-transform:uppercase; letter-spacing:.08em; }
.stat-value { color:#1a2944; font:700 clamp(1.25rem,4vw,1.75rem) system-ui,sans-serif; margin-top:2px; overflow-wrap:anywhere; }
.guess-card { text-align:center; border-radius:22px; padding:1.1rem 1rem .9rem; color:#fff; background:linear-gradient(135deg,#465df5,#7384ff); box-shadow:0 12px 28px #465df53a; margin:.8rem 0 1rem; }
.guess-label { font-size:.78rem; letter-spacing:.12em; font-weight:700; text-transform:uppercase; opacity:.85; }
.guess-number { font:700 clamp(4rem,17vw,6.3rem)/1 system-ui,sans-serif; letter-spacing:-.07em; }
.hint { border-radius:14px; padding:12px 15px; background:#eef2ff; color:#3d50cf; font-weight:600; margin:.6rem 0 1rem; }
.hint.good { background:#e6f8ef; color:#14734c; }
.hint.bad { background:#fff3e4; color:#985a06; }
div.stButton > button { min-height:3.5rem; border-radius:14px; font-weight:700; font-size:1rem; border:1px solid #e0e6f1; transition:transform .15s,box-shadow .15s; }
div.stButton > button:hover { transform:translateY(-2px); box-shadow:0 8px 18px #263a6418; border-color:#aab7ff; }
div.stButton > button[kind="primary"] { background:#465df5; border-color:#465df5; }
[data-testid="stProgressBar"] { margin-bottom:1rem; }
@media(max-width:600px) {
 .block-container { padding:.9rem .8rem 1.2rem; }
 .brand { margin-bottom:.8rem; }
 .brand-icon { width:42px;height:42px; }
 .hero,.panel { border-radius:19px; }
 .stats { gap:8px; }
 .stat { padding:11px 12px; }
 div[data-testid="stHorizontalBlock"] { gap:.45rem; }
 div[data-testid="stHorizontalBlock"] div.stButton > button { min-height:3.7rem; padding:0 .35rem; font-size:.88rem; }
}
</style>
""", unsafe_allow_html=True)


def reset_game():
    st.session_state.phase = "home"
    st.session_state.low = 1
    st.session_state.high = 1000
    st.session_state.guesses = 0
    st.session_state.guess = None
    st.session_state.deadline = None
    st.session_state.result = None
    st.session_state.feedback = None


def finish(result):
    st.session_state.phase = "done"
    st.session_state.result = result


if "phase" not in st.session_state:
    reset_game()

st.markdown('''<div class="brand"><div class="brand-icon">✦</div><div><div class="brand-title">NUMBER HUNT</div><div class="brand-sub">A quick game of higher or lower</div></div></div>''', unsafe_allow_html=True)

if st.session_state.phase == "home":
    st.markdown(f'''<div class="hero"><div class="eyebrow">Think it. Keep it secret.</div><h1>Can the computer<br>find your number?</h1><div class="intro">Choose a whole number from <b>1 to 1000</b> in your head. Don't enter it anywhere. After each computer guess, tap <b>Too low</b>, <b>Too high</b>, or <b>Correct</b>.</div><div class="developer">Created by <strong>Afifah Ali</strong> &amp; <strong>ChatGPT</strong></div></div>''', unsafe_allow_html=True)
    st.write("")
    if st.button("Start Game  →", type="primary", use_container_width=True):
        st.session_state.phase = "playing"
        st.session_state.low = 1
        st.session_state.high = 1000
        st.session_state.guesses = 1
        st.session_state.guess = (1 + 1000) // 2
        st.session_state.deadline = time.monotonic() + GAME_SECONDS
        st.session_state.feedback = None
        st.rerun()

elif st.session_state.phase == "playing":
    @st.fragment(run_every="1s")
    def game_round():
        remaining = max(0, int(st.session_state.deadline - time.monotonic() + 0.999))
        if remaining == 0:
            finish("Time ran out. The secret number was not identified.")
            st.rerun()
            return
        st.progress(remaining / GAME_SECONDS, text=f"⏱  {remaining} seconds remaining")
        st.markdown(f'''<div class="guess-card"><div class="guess-label">Computer's guess</div><div class="guess-number">{st.session_state.guess}</div></div><div class="stats"><div class="stat"><div class="stat-label">Attempts</div><div class="stat-value">{st.session_state.guesses}</div></div><div class="stat"><div class="stat-label">Possible range</div><div class="stat-value">{st.session_state.low} – {st.session_state.high}</div></div></div>''', unsafe_allow_html=True)
        if st.session_state.feedback:
            kind, message = st.session_state.feedback
            st.markdown(f'<div class="hint {kind}">{message}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="hint">Your feedback tells the computer which direction to search.</div>', unsafe_allow_html=True)

        low_col, high_col, correct_col = st.columns(3)
        if low_col.button("⬆  Too low", use_container_width=True):
            st.session_state.feedback = ("good", f"Got it — {st.session_state.guess} is too low. Searching higher.")
            st.session_state.low = st.session_state.guess + 1
            if st.session_state.low > st.session_state.high:
                finish("Contradictory feedback: no number remains in the possible range.")
            else:
                st.session_state.guess = (st.session_state.low + st.session_state.high) // 2
                st.session_state.guesses += 1
            st.rerun()
        if high_col.button("⬇  Too high", use_container_width=True):
            st.session_state.feedback = ("bad", f"Understood — {st.session_state.guess} is too high. Searching lower.")
            st.session_state.high = st.session_state.guess - 1
            if st.session_state.low > st.session_state.high:
                finish("Contradictory feedback: no number remains in the possible range.")
            else:
                st.session_state.guess = (st.session_state.low + st.session_state.high) // 2
                st.session_state.guesses += 1
            st.rerun()
        if correct_col.button("✓  Correct", type="primary", use_container_width=True):
            st.session_state.feedback = ("good", "You confirmed the computer's guess!")
            finish("The computer found your secret number!")
            st.rerun()
    game_round()

else:
    st.markdown(f'''<div class="hero"><div class="eyebrow">Round complete</div><h1>Game over</h1><div class="intro">{st.session_state.result}</div><div class="developer">Total attempts: <strong>{st.session_state.guesses}</strong></div><div class="developer">Created by <strong>Afifah Ali</strong> &amp; <strong>ChatGPT</strong></div></div>''', unsafe_allow_html=True)
    st.write("")
    if st.button("Play Again  ↻", type="primary", use_container_width=True):
        reset_game()
        st.rerun()