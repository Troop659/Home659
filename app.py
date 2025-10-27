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
    print(target)
    async with httpx.AsyncClient() as client:
        resp = await client.get(target)

    headers = dict(resp.headers)
    headers.pop("content-encoding", None)
    headers.pop("transfer-encoding", None)
    headers.pop("content-length", None)

    return Response(
        resp.text, resp.status_code, headers=headers  # type: ignore
    )


if __name__ == '__main__':
    app.run()
