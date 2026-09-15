import re
import requests
from bs4 import BeautifulSoup

MAIN_URL = "https://apnetv.xyz/Hindi-Serial/episodes/Bigg-Boss-Season-20"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15"
}


def get_episodes():
    response = requests.get(MAIN_URL, headers=HEADERS, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    episodes = []

    dropdown = soup.find("select", id="oneclick-episode")

    if dropdown:
        for option in dropdown.find_all("option"):
            val = option.get("value", "")

            if "#@#" in val:
                url = val.split("#@#")[-1]
                title = option.text.strip()
                episodes.append((title, url))

    return episodes


def extract_mp4(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)

        match = re.search(
            r'https?://[^"\']+\.mp4',
            res.text,
            re.IGNORECASE
        )

        return match.group(0) if match else None

    except Exception as e:
        print(f"Error extracting MP4 from {url}: {e}")
        return None


def main():
    print("Scraping episodes...")

    episodes = get_episodes()
    episode_data = []

    for title, url in episodes:
        mp4 = extract_mp4(url)

        if mp4:
            print(f"Found stream for: {title}")
            episode_data.append(
                {
                    "title": title,
                    "mp4": mp4,
                }
            )

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bigg Boss Season 20</title>

<style>
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #121212;
    color: #fff;
    margin: 0;
    padding: 20px;
}

.container {
    max-width: 900px;
    margin: 0 auto;
}

h1 {
    text-align: center;
    color: #e50914;
}

video {
    width: 100%;
    border-radius: 8px;
    background: #000;
    margin-bottom: 20px;
}

.playlist {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.item {
    padding: 15px;
    background: #1e1e1e;
    border-radius: 6px;
    cursor: pointer;
    transition: background 0.2s;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.item:hover {
    background: #2a2a2a;
}

.item.active {
    border-left: 4px solid #e50914;
    background: #252525;
}

a.direct-link {
    color: #888;
    text-decoration: none;
    font-size: 0.9em;
    border: 1px solid #444;
    padding: 4px 8px;
    border-radius: 4px;
}

a.direct-link:hover {
    color: #fff;
    border-color: #666;
}
</style>
</head>

<body>
<div class="container">
<h1>Bigg Boss Season 20</h1>

<video id="player" controls autoplay></video>

<div class="playlist" id="playlist">
"""

    for ep in episode_data:
        html_content += f"""
<div class="item" onclick="playVideo('{ep['mp4']}', this)">
    <span>{ep['title']}</span>
    <a class="direct-link"
       href="{ep['mp4']}"
       target="_blank"
       onclick="event.stopPropagation()">
       Direct MP4
    </a>
onst player = document.getElementById('player');
    player.src = url;
    player.play();

    document.querySelectorAll('.item').forEach(el => {
        el.classList.remove('active');
    });

    if (element) {
        element.classList.add('active');
    }
}

const firstItem = document.querySelector('.item');

if (firstItem) {
    firstItem.click();
}
</script>

</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("Saved index.html successfully!")


if __name__ == "__main__":
    main()
