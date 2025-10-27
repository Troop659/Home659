import logging

import httpx
from quart import Quart, Response, render_template

app = Quart(__name__)
logger = app.logger
logger.setLevel(logging.INFO)

TARGETS: dict[str, str] = {
    "evaluator": "https://scoutevaluator.onrender.com/{}"
}


@app.route("/")
async def index():
    return await render_template("index.html")


@app.route("/scoutevaluator", defaults={'subpath': ''})
@app.route("/scoutevaluator/<path:subpath>")
async def proxy_evaluator(subpath):
    target = TARGETS["evaluator"].format(subpath)
    return await reroute_to(target)


@app.route("/scoutevaluator/static/<path:subpath>")
async def proxy_evaluator_static(subpath):
    target = f"https://scoutevaluator.onrender.com/static/{subpath}"
    return await reroute_to(target)


async def reroute_to(url: str) -> Response:
    logger.info(f"Attempting re-route to {url}")
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)

    headers = dict(resp.headers)
    headers.pop("content-encoding", None)
    headers.pop("transfer-encoding", None)
    headers.pop("content-length", None)

    logger.debug(
        f"Re-route returned code {resp.status_code} with {resp.text}"
    )

    return Response(resp.content, resp.status_code, headers=headers)


if __name__ == '__main__':
    app.run()
