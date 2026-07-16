from serpapi import GoogleSearch
import requests

SERP_API_KEY = "여기에_본인_SERPAPI_KEY"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def is_png(url):
    """
    URL이 실제 PNG인지 확인
    """
    try:
        r = requests.head(
            url,
            allow_redirects=True,
            headers=HEADERS,
            timeout=5
        )

        content = r.headers.get("Content-Type", "").lower()

        return "image/png" in content

    except Exception:
        return False


def download_image(url):
    """
    이미지 다운로드
    """
    try:
        r = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        if r.status_code == 200:
            return r.content

    except Exception:
        pass

    return None


def search_png(keyword, count=20):
    """
    구글 이미지 검색 후
    PNG만 반환
    """

    params = {
        "engine": "google_images",
        "q": keyword,
        "ijn": "0",
        "api_key": SERP_API_KEY,
        "safe": "active"
    }

    search = GoogleSearch(params)

    results = search.get_dict()

    images = []

    if "images_results" not in results:
        return images

    for img in results["images_results"]:

        url = img.get("original")

        if not url:
            continue

        if is_png(url):

            images.append({

                "title": img.get("title"),

                "thumbnail": img.get("thumbnail"),

                "url": url,

                "source": img.get("source"),

                "link": img.get("link")

            })

        if len(images) >= count:
            break

    return images
