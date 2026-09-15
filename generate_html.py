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
            episode_data.append({
                "title": title,
                "mp4": mp4
            })

    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bigg Boss Season 20</title>

<style>
body {
    font-family: Arial, sans-serif;
    background: #121212;
    color: #ffffff;
    margin: 0;
    padding: 20px;
}

.container {
    max-width: 900px;
    margin: auto;
}

h1 {
    text-align: center;
    color: #e50914;
}

video {
    width: 100%;
    background: black;
    margin-bottom: 20px;
}

.playlist {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.item {
    background: #1e1e1e;
    padding: 15px;
    border-radius: 8px;
    cursor: pointer;
}

.item:hover {
    background: #2a2a2a;
}

.item.active {
    border-left: 4px solid #e50914;
}

.direct-link {
    display: inline-block;
    margin-top: 5px;
    color: #4da6ff;
}
</style>
</head>

<body>

<div class="container">
    <h1>Bigg Boss Season 20</h1>

    <video id="player" controls autoplay></video>

    <div class="playlist">
"""

    for ep in episode_data:
        html_content += f"""
        <div class="item" onclick="playVideo('{ep['mp4']}', this)">
            <div>{ep['title']}</div>
            <a class="direct-link"
               href="{ep['mp4']}"
               target="_blank"
               onclickv>
</div>

<script>
function playVideo(url, element) {
    const player = document.getElementById('player');
    player.src = url;
    player.play();

    document.querySelectorAll('.item').forEach(function(el) {
        el.classList.remove('active');
    });

    element.classList.add('active');
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
