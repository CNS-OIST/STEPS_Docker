"""Push README.md to the Docker Hub repository description.

The description is a separate copy that nothing keeps in sync, which is how it
drifted years behind the README. Run from the repository root:

    DOCKERHUB_USERNAME=... DOCKERHUB_TOKEN=... python3 .github/sync_hub_description.py cnsoist/steps

Relative image links are rewritten to raw.githubusercontent.com, since Docker Hub
has no repository to resolve them against.
"""

import json
import os
import re
import sys
import urllib.error
import urllib.request

RAW = "https://raw.githubusercontent.com/CNS-OIST/STEPS_Docker/master/"
# Docker Hub rejects anything longer.
MAX_DESCRIPTION = 25000

image = sys.argv[1] if len(sys.argv) > 1 else "cnsoist/steps"
user = os.environ["DOCKERHUB_USERNAME"]
token = os.environ["DOCKERHUB_TOKEN"]

readme = open("README.md", encoding="utf-8").read()
# ![alt](images/x.png) -> absolute, otherwise Docker Hub renders a broken image
readme = re.sub(r"(!\[[^\]]*\]\()(?!https?://)([^)]+)\)", rf"\1{RAW}\2)", readme)

if len(readme) > MAX_DESCRIPTION:
    sys.exit(f"README is {len(readme)} chars, over Docker Hub's {MAX_DESCRIPTION} limit")


def post(url, payload, method="POST", auth=None):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method=method,
    )
    if auth:
        req.add_header("Authorization", auth)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


jwt = post(
    "https://hub.docker.com/v2/users/login/",
    {"username": user, "password": token},
)["token"]

namespace, name = image.split("/", 1)
post(
    f"https://hub.docker.com/v2/repositories/{namespace}/{name}/",
    {"full_description": readme},
    method="PATCH",
    auth=f"JWT {jwt}",
)
print(f"Updated {image} description from README.md ({len(readme)} chars)")
