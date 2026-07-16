from duckduckgo_search import DDGS


def search_png(keyword, max_results=20):

    results = []

    try:
        with DDGS() as ddgs:

            images = ddgs.images(
                keywords=f"{keyword} png",
                max_results=max_results
            )

            for img in images:

                results.append({

                    "title": img.get("title", "image"),

                    "image": img.get("image"),

                    "thumbnail": img.get("thumbnail"),

                    "source": img.get("source"),

                    "page": img.get("url")

                })


    except Exception as e:

        print("ERROR:", e)


    return results
