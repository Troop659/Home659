import logging

import httpx
from quart import Quart, Response, render_template

app = Quart(__name__)
logger = app.logger
logger.setLevel(logging.INFO)

TARGETS: dict[str, str] = {
    "scoutevaluator": "https://scoutevaluator.onrender.com/"
}


@app.route("/")
async def index():
    return await render_template("index.html")


@app.route("/<path:subpath>")
async def proxy(subpath: str):
    target = TARGETS[subpath]
    return await reroute_to(target, subpath)


async def reroute_to(url: str, sub: str) -> Response:
    logger.info(f"Attempting re-route to {url}")
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)

    headers = dict(resp.headers)
    headers.pop("content-encoding", None)
    headers.pop("transfer-encoding", None)
    headers.pop("content-length", None)

    content = resp.content
    if "text/html" in resp.headers.get("content-type", ""):
        content = content.decode("utf-8")
        content = content.replace(
            "<head>",
            f'<head><base href="{sub}">'
        )
        content = content.encode("utf-8")

    logger.debug(
        f"Re-route returned code {resp.status_code} with {content}"
    )

    return Response(content, resp.status_code, headers=headers)


if __name__ == '__main__':
    app.run()
