import requests
import re
t = {}
link = "https://api.github.com/repos/sendgrid/open-source-library-data-collector/"
releases = requests.get(link + "releases").json()
pulls = requests.get(link + "pulls?state=closed&per_page=100").json()
for pr in pulls:
    if(pr["merged_at"] and pr["merged_at"] > releases[0]["created_at"]):
        s = pr["body"]
        t = "".join(s.rsplit("-->", 1)[1:])
        m = re.search(r"[Resolves|Closes|Fixes]+ #(\d+)", t)
        if m is not None:
            issue = "".join(m.group(0).rsplit(" ", 1)[1:])
            print("Issue {} {}, fixed by Pull #{}".format(issue, pr["title"], pr["number"]))
        else:
            print("{}, #{}".format(pr["title"], pr["number"]))
        print("Big thanks to @{} for the PR!".format(pr["user"]["login"]))
