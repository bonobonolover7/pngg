import streamlit as st

from search import search_png
from download import fetch_image, download_name


# -------------------------
# 기본 설정
# -------------------------

st.set_page_config(
    page_title="PNG Search",
    page_icon="🖼️",
    layout="wide"
)


# -------------------------
# CSS
# -------------------------

st.markdown(
    """
<style>

.main-title {
    text-align:center;
    font-size:45px;
    font-weight:700;
    margin-top:50px;
}

.search-box {
    max-width:700px;
    margin:auto;
}

.card {

    border-radius:15px;
    padding:15px;
    background:#ffffff;
    box-shadow:
        0 4px 15px rgba(0,0,0,0.1);

    margin-bottom:25px;

}


.card img {

    border-radius:10px;

}


.small-text {

    color:#777;
    font-size:13px;

}


</style>
""",
    unsafe_allow_html=True
)



# -------------------------
# 제목
# -------------------------

st.markdown(
    """
<div class="main-title">
🖼️ PNG Search
</div>
""",
    unsafe_allow_html=True
)


st.write("")


# -------------------------
# 검색창
# -------------------------

keyword = st.text_input(
    "",
    placeholder="검색할 PNG 키워드를 입력하세요",
    key="search"
)



search_button = st.button(
    "🔍 검색",
    use_container_width=True
)



# -------------------------
# 검색 실행
# -------------------------

if search_button and keyword:


    with st.spinner(
        "PNG 이미지를 검색중..."
    ):


        results = search_png(
            keyword,
            max_results=20
        )


        st.session_state["results"] = results



# -------------------------
# 결과 표시
# -------------------------

if "results" in st.session_state:


    results = st.session_state["results"]


    if len(results) == 0:

        st.warning(
            "PNG 이미지를 찾지 못했습니다."
        )


    else:


        st.success(
            f"{len(results)}개의 PNG 이미지를 찾았습니다."
        )


        cols = st.columns(4)


        for index, img in enumerate(results):


            with cols[index % 4]:


                st.image(
                    img["thumbnail"]
                    or img["image"],
                    use_container_width=True
                )


                st.write(
                    img["title"]
                )


                if img.get("source"):

                    st.caption(
                        img["source"]
                    )


                # 원본 페이지
                if img.get("page"):

                    st.link_button(
                        "🔗 원본 보기",
                        img["page"]
                    )



                # 다운로드
                data = fetch_image(
                    img["image"]
                )


                if data:


                    st.download_button(

                        label="⬇ 다운로드",

                        data=data,

                        file_name=
                        download_name(
                            img["title"]
                        ),

                        mime="image/png",

                        key=f"download_{index}"

                    )
