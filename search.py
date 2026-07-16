import requests
from duckduckgo_search import DDGS


def check_png(url):
    """
    이미지 URL이 실제 PNG인지 확인
    """
    try:
        response = requests.head(
            url,
            timeout=5,
            allow_redirects=True,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        content_type = response.headers.get(
            "Content-Type",
            ""
        ).lower()

        return "image/png" in content_type

    except Exception:
        return False


def search_png(keyword, max_results=30):
    """
    DuckDuckGo 이미지 검색 후 PNG만 반환
    """

    results = []

    checked_urls = set()


    try:

        with DDGS() as ddgs:

            images = ddgs.images(
                keywords=keyword,
                max_results=max_results * 3
            )


            for img in images:

                image_url = img.get("image")

                if not image_url:
                    continue


                # 중복 제거
                if image_url in checked_urls:
                    continue

                checked_urls.add(image_url)


                # PNG 검사
                if check_png(image_url):

                    results.append({

                        "title": img.get(
                            "title",
                            "No title"
                        ),

                        "image": image_url,

                        "thumbnail": img.get(
                            "thumbnail"
                        ),

                        "source": img.get(
                            "source"
                        ),

                        "page": img.get(
                            "url"
                        )

                    })


                # 원하는 개수 도달
                if len(results) >= max_results:
                    break


    except Exception as e:

        print(
            "Search Error:",
            e
        )


    return results
