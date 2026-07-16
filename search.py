from ddgs import DDGS


def search_png(keyword, max_results=30):

    results = []

    try:

        with DDGS() as ddgs:

            query = f"{keyword} png"

            images = ddgs.images(
                query,
                max_results=max_results
            )


            for img in images:

                image_url = img.get("image")

                if not image_url:
                    continue


                results.append(
                    {
                        "title": img.get(
                            "title",
                            "PNG Image"
                        ),

                        "image": image_url,

                        "thumbnail": img.get(
                            "thumbnail",
                            image_url
                        ),

                        "source": img.get(
                            "source",
                            ""
                        ),

                        "page": img.get(
                            "url",
                            ""
                        )
                    }
                )


    except Exception as e:

        print(
            "DuckDuckGo Error:",
            e
        )


    return results
