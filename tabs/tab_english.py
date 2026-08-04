"""🇬🇧 英语学习 — 番茄钟 + 素材学习 / 录屏练习"""

import streamlit as st
from streamlit.components.v1 import html as st_html
from datetime import datetime
from tabs.english import daily_materials, screen_recording


def render():
    _render_pomodoro()
    st.markdown("---")
    daily_materials.render_content()
    st.markdown("---")
    with st.expander("🎙️ 录屏练习", expanded=False):
        screen_recording.render_content()


def _render_pomodoro():
    """番茄钟 — 点击番茄开始 25 分钟倒计时"""
    pomodoro_html = """
    <style>
      body { margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }
      .pomo-wrap {
        display: flex; align-items: center; gap: 16px;
        padding: 12px 20px; border-radius: 12px;
        background: linear-gradient(135deg, #fff5f5 0%, #ffe8e8 100%);
        box-shadow: 0 2px 8px rgba(231,76,60,0.1);
      }
      .pomo-btn {
        width: 48px; height: 48px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.6em; cursor: pointer; user-select: none;
        background: #fff; border: 2px solid #e74c3c;
        box-shadow: 0 2px 6px rgba(231,76,60,0.2);
        transition: all 0.2s;
      }
      .pomo-btn:hover { transform: scale(1.1); box-shadow: 0 4px 12px rgba(231,76,60,0.3); }
      .pomo-btn:active { transform: scale(0.95); }
      .pomo-btn.running { background: #e74c3c; border-color: #c0392b; }
      .pomo-timer {
        font-size: 1.6em; font-weight: 700; font-variant-numeric: tabular-nums;
        color: #e74c3c; min-width: 80px; letter-spacing: 1px;
      }
      .pomo-timer.done { color: #27ae60; }
      .pomo-status { font-size: 0.85em; color: #999; }
    </style>
    <div class="pomo-wrap">
      <button class="pomo-btn" id="pomoBtn" onclick="togglePomo()" title="点击开始/暂停">🍅</button>
      <span class="pomo-timer" id="pomoTimer">25:00</span>
      <span class="pomo-status" id="pomoStatus">点击开始专注</span>
    </div>
    <script>
      let pomoInterval = null;
      let pomoSeconds = 25 * 60;
      let pomoRunning = false;

      function togglePomo() {
        if (pomoRunning) {
          clearInterval(pomoInterval);
          pomoRunning = false;
          document.getElementById('pomoStatus').textContent = '已暂停 · 再次点击继续';
          document.getElementById('pomoBtn').textContent = '🍅';
          document.getElementById('pomoBtn').classList.remove('running');
        } else {
          if (pomoSeconds <= 0) pomoSeconds = 25 * 60;
          pomoRunning = true;
          document.getElementById('pomoStatus').textContent = '专注中...';
          document.getElementById('pomoBtn').textContent = '⏸';
          document.getElementById('pomoBtn').classList.add('running');
          pomoInterval = setInterval(() => {
            pomoSeconds--;
            if (pomoSeconds <= 0) {
              clearInterval(pomoInterval);
              pomoRunning = false;
              document.getElementById('pomoTimer').textContent = '00:00';
              document.getElementById('pomoTimer').classList.add('done');
              document.getElementById('pomoStatus').textContent = '完成！休息一下吧';
              document.getElementById('pomoBtn').textContent = '🍅';
              document.getElementById('pomoBtn').classList.remove('running');
              return;
            }
            updateDisplay();
          }, 1000);
        }
      }

      function updateDisplay() {
        let m = Math.floor(pomoSeconds / 60);
        let s = pomoSeconds % 60;
        document.getElementById('pomoTimer').textContent =
          String(m).padStart(2,'0') + ':' + String(s).padStart(2,'0');
        document.getElementById('pomoTimer').classList.remove('done');
      }
    </script>
    """
    st_html(pomodoro_html, height=80)
