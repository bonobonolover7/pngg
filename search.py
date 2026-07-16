from ddgs import DDGS
import requests
from PIL import Image
from io import BytesIO


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def is_real_png(url):
    """
    실제 파일이 PNG인지 검사
    """

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10,
            stream=True
        )

        data = response.content

        response.close()


        image = Image.open(
            BytesIO(data)
        )


        # Pillow가 판별한 실제 포맷
        return image.format == "PNG"


    except Exception:

        return False



def search_png(keyword, max_results=30):

    results = []

    checked = set()


    try:

        with DDGS() as ddgs:

            images = ddgs.images(
                f"{keyword} png",
                max_results=max_results * 5
            )


            for img in images:


                image_url = img.get(
                    "image"
                )


                if not image_url:
                    continue


                if image_url in checked:
                    continue


                checked.add(
                    image_url
                )


                # 진짜 PNG 검사
                if is_real_png(image_url):

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
                    break


    except Exception as e:

        print(
            "Search Error:",
            e
        )


    return results
