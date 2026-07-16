from ddgs import DDGS
import requests

from PIL import Image
from io import BytesIO
from urllib.parse import urlparse


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def is_transparent_png(url):
    """
    실제 투명 PNG인지 검사

    조건:
    1. 이미지 파일이어야 함
    2. PNG 형식이어야 함
    3. Alpha 채널이 존재해야 함
    4. 실제 투명 픽셀이 있어야 함
    """

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=8
        )

        img = Image.open(
            BytesIO(response.content)
        )


        # 실제 PNG 검사
        if img.format != "PNG":
            return False


        # RGBA가 아니면 투명 없음
        if "A" not in img.getbands():
            return False


        alpha = img.getchannel("A")


        # alpha 최소값
        min_alpha, max_alpha = alpha.getextrema()


        # 완전 불투명 이미지 제외
        if min_alpha == 255:
            return False


        return True


    except Exception:

        return False



def make_queries(keyword):
    """
    여러 언어/표현으로 검색 강화
    """

    return [

        f"{keyword} png",

        f"{keyword} transparent png",

        f"{keyword} transparent background png",

        f"{keyword} no background png",

        f"{keyword} cutout png",

        f"{keyword} alpha png"

    ]



def search_png(keyword, max_results=30):

    results = []

    checked = set()


    queries = make_queries(keyword)


    try:

        with DDGS() as ddgs:


            for query in queries:


                try:

                    images = ddgs.images(
                        query,
                        max_results=50
                    )


                except Exception:

                    continue



                for img in images:


                    image_url = img.get(
                        "image"
                    )


                    if not image_url:
                        continue


                    # 중복 제거
                    if image_url in checked:
                        continue


                    checked.add(
                        image_url
                    )


                    # 투명 PNG 검사
                    if is_transparent_png(
                        image_url
                    ):


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
                                    "thumbnail",
                                    image_url
                                ),

                            "source":
                                img.get(
                                    "source",
                                    ""
                                ),

                            "page":
                                img.get(
                                    "url",
                                    ""
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
