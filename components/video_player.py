"""YouTube iframe 嵌入 + youzack 嵌入组件"""


def youtube_player_html(video_id: str, speed: float = 1.0, loop: bool = False) -> str:
    loop_param = "&loop=1&playlist=" + video_id if loop else ""
    return f"""
    <style>
      .yt-wrap {{ position: relative; width: 100%; padding-bottom: 56.25%; border-radius: 8px; overflow: hidden; }}
      .yt-wrap iframe {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; }}
      .speed-tip {{ font-size: 12px; color: #888; margin-top: 6px; text-align: center; }}
    </style>
    <div class="yt-wrap">
      <iframe src="https://www.youtube.com/embed/{video_id}?rel=0&modestbranding=1&autoplay=1{loop_param}"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
              allowfullscreen>
      </iframe>
    </div>
    <p class="speed-tip">💡 倍速：点击视频右下角 ⚙️ 设置 → 播放速度 （当前建议: {speed}x）</p>
    """


def youzack_player_html(url: str) -> str:
    return f"""
    <style>
      .yz-wrap {{ width: 100%; border-radius: 8px; overflow: hidden; }}
      .yz-wrap iframe {{ width: 100%; height: 500px; border: none; }}
    </style>
    <div class="yz-wrap">
      <iframe src="{url}" allow="autoplay; fullscreen" allowfullscreen></iframe>
    </div>
    """
