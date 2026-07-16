import requests
from urllib.parse import urlparse

from duckduckgo_search import DDGS


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def is_png(url):
    """
    PNG 여부 확인
    """

    if not url:
        return False


    # 1차: URL 확장자 확인
    path = urlparse(url).path.lower()

    if path.endswith(".png"):
        return True


    # 2차: 실제 파일 타입 확인
    try:

        r = requests.get(
            url,
            headers=HEADERS,
            timeout=8,
            stream=True
        )


        content_type = r.headers.get(
            "Content-Type",
            ""
        ).lower()


        r.close()


        if "image/png" in content_type:
            return True


    except Exception:
        pass


    return False



def search_png(keyword, max_results=30):

    results = []

    used = set()


    # 언어 상관없이 PNG 검색 강화
    search_words = [
        f"{keyword} png",
        f"{keyword} transparent png",
        f"{keyword} filetype png"
    ]


    try:

        with DDGS() as ddgs:


            for query in search_words:


                images = ddgs.images(
                    keywords=query,
                    max_results=max_results * 3
                )


                for img in images:


                    image_url = img.get(
                        "image"
                    )


                    if not image_url:
                        continue


                    if image_url in used:
                        continue


                    used.add(image_url)


                    if is_png(image_url):


                        results.append({

                            "title":
                                img.get(
                                    "title",
                                    "PNG Image"
                                ),

                            "image":
                                image_url,

                            "thumbnail":
                                img.get(
                                    "thumbnail"
                                ),

                            "source":
                                img.get(
                                    "source"
                                ),

                            "page":
                                img.get(
                                    "url"
                                )

                        })


                    if len(results) >= max_results:
                        return results


    except Exception as e:

        print(
            "Search Error:",
            e
        )


    return results
