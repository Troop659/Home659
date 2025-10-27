import httpx
from quart import Quart, render_template, Response

app = Quart(__name__)

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
    async with httpx.AsyncClient() as client:
        resp = await client.get(target)

    return Response(
        resp.content, resp.status_code, headers=resp.headers  # type: ignore
    )


if __name__ == '__main__':
    app.run()
