import requests


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def fetch_image(url):
    """
    이미지 URL에서 데이터 가져오기

    return:
        bytes 데이터
    """

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15
        )

        if response.status_code == 200:

            return response.content


    except Exception as e:

        print(
            "Download Error:",
            e
        )


    return None



def download_name(title):
    """
    다운로드 파일명 생성
    """

    if not title:
        title = "download"


    # 파일명에 사용할 수 없는 문자 제거
    invalid_chars = [
        "\\",
        "/",
        ":",
        "*",
        "?",
        "\"",
        "<",
        ">",
        "|"
    ]


    for char in invalid_chars:
        title = title.replace(
            char,
            ""
        )


    return title[:50] + ".png"
