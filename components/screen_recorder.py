"""摄像头录制组件 — 录像 + 麦克风，输出 MP4"""


def recorder_html() -> str:
    return """
    <style>
      #rec-ui { font-family: -apple-system, BlinkMacSystemFont, sans-serif; text-align: center; padding: 10px; }
      #preview { width: 100%; max-width: 480px; border-radius: 10px; background: #000; margin: 0 auto 10px; display: block; }
      #timer { font-size: 2em; font-weight: bold; margin: 8px 0; font-variant-numeric: tabular-nums; }
      .rec-btn { padding: 10px 20px; margin: 6px; font-size: 0.95em; border: none; border-radius: 8px; cursor: pointer; transition: all 0.2s; }
      .rec-btn:hover { transform: scale(1.05); }
      #startBtn { background: #ff4b4b; color: white; }
      #stopBtn { background: #555; color: white; }
      #stopBtn:disabled { opacity: 0.4; cursor: not-allowed; }
      #status { margin-top: 8px; color: #666; font-size: 0.9em; }
    </style>
    <div id="rec-ui">
      <video id="preview" autoplay muted playsinline></video>
      <div id="timer">00:00</div>
      <button class="rec-btn" id="startBtn" onclick="startRec()">🔴 开始录制</button>
      <button class="rec-btn" id="stopBtn" onclick="stopRec()" disabled>⏹ 停止并下载</button>
      <p id="status">点击开始录制（摄像头 + 麦克风）</p>
    </div>
    <script>
      let mr, chunks = [], interval, seconds = 0, stream;

      (async function initPreview() {
        try {
          stream = await navigator.mediaDevices.getUserMedia({video: true, audio: true});
          document.getElementById('preview').srcObject = stream;
        } catch(e) {
          document.getElementById('status').textContent = '⚠️ 无法访问摄像头: ' + e.message;
        }
      })();

      async function startRec() {
        try {
          if (!stream) {
            stream = await navigator.mediaDevices.getUserMedia({
              video: {width: 1280, height: 720},
              audio: {echoCancellation: true, noiseSuppression: true}
            });
            document.getElementById('preview').srcObject = stream;
          }
          const candidates = [
            'video/mp4;codecs=avc1.42E01E,mp4a.40.2',
            'video/mp4;codecs=avc1,mp4a.40.2',
            'video/mp4',
            'video/webm;codecs=vp9,opus',
            'video/webm;codecs=vp8,opus',
            'video/webm'
          ];
          let mimeType = '';
          for (const c of candidates) {
            if (MediaRecorder.isTypeSupported(c)) { mimeType = c; break; }
          }
          if (!mimeType) mimeType = '';
          const ext = mimeType.includes('mp4') ? 'mp4' : 'webm';
          const opts = mimeType ? {mimeType: mimeType, audioBitsPerSecond: 128000, videoBitsPerSecond: 2500000} : {};
          mr = new MediaRecorder(stream, opts);
          mr.ondataavailable = e => { if (e.data.size > 0) chunks.push(e.data); };
          mr.onstop = () => {
            const blobType = mimeType || 'video/webm';
            const blob = new Blob(chunks, {type: blobType});
            const finalExt = blobType.includes('mp4') ? 'mp4' : 'webm';
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'english_practice_' + new Date().toISOString().slice(0, 10) + '.' + finalExt;
            a.click();
            URL.revokeObjectURL(url);
            document.getElementById('status').textContent = '✅ 录制完成 (' + formatTime(seconds) + ')，已下载 ' + finalExt.toUpperCase();
            document.getElementById('status').textContent += ' | 音轨: ' + stream.getAudioTracks().length;
          };
          chunks = [];
          seconds = 0;
          mr.start(1000);
          document.getElementById('startBtn').disabled = true;
          document.getElementById('stopBtn').disabled = false;
          document.getElementById('status').textContent = '🔴 录制中...';
          interval = setInterval(() => {
            seconds++;
            document.getElementById('timer').textContent = formatTime(seconds);
          }, 1000);
        } catch (e) {
          document.getElementById('status').textContent = '❌ ' + e.message;
        }
      }

      function stopRec() {
        if (mr && mr.state !== 'inactive') {
          mr.stop();
        }
        clearInterval(interval);
        document.getElementById('startBtn').disabled = false;
        document.getElementById('stopBtn').disabled = true;
      }

      function formatTime(s) {
        return String(Math.floor(s / 60)).padStart(2, '0') + ':' + String(s % 60).padStart(2, '0');
      }
    </script>
    """
