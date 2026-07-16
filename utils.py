import re
from urllib.parse import urlparse


def clean_filename(name):
    """
    파일명으로 사용할 수 없는 문자 제거
    """

    if not name:
        return "image"

    name = re.sub(
        r'[\\/*?:"<>|]',
        "",
        name
    )

    name = name.strip()

    if len(name) > 80:
        name = name[:80]

    return name



def get_extension(url):
    """
    URL에서 이미지 확장자 추출
    """

    try:

        path = urlparse(url).path

        ext = path.split(".")[-1].lower()

        if ext in [
            "png",
            "jpg",
            "jpeg",
            "webp",
            "gif"
        ]:
            return ext

    except Exception:
        pass


    return "png"



def make_filename(title, url):
    """
    다운로드 파일명 생성
    """

    title = clean_filename(title)

    ext = get_extension(url)

    return f"{title}.{ext}"



def is_valid_url(url):
    """
    URL 유효성 검사
    """

    if not url:
        return False


    return (
        url.startswith("http://")
        or
        url.startswith("https://")
    )
