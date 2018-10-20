import requests
import re
import datetime

def get_last_release():
    with open("CHANGELOG.md") as file:
        data = file.read()
        m = re.search(r"## \[.*\]", data)
        return ("".join(m.group(0).rsplit(" ", 1)[1:]))[1:-1]

def get_new_release(old_version):
    while True:
        new_release = input("Last release version was {}, \nEnter the new version number: ".format(old_version))
        if new_release == old_version:
            print("New release cannot be same as the last release")
            continue
        return new_release

def get_changes():
    changes = []
    link = "https://api.github.com/repos/sendgrid/open-source-library-data-collector/"
    releases = requests.get(link + "releases").json()
    pulls = requests.get(link + "pulls?state=closed&per_page=100").json()
    for pr in pulls:
        if(pr["merged_at"] and pr["merged_at"] > releases[0]["created_at"]):
            message = "".join(pr["body"].rsplit("-->", 1)[1:])
            m = re.search(r"[Resolves|Closes|Fixes|resolves|closes|fixes]+ #(\d+)", message)
            if m is not None:
                issue = "".join(m.group(0).rsplit(" ", 1)[1:])
                changes.append("Issue {} {}, fixed by Pull #{}".format(issue, pr["title"], pr["number"]))
            else:
                changes.append("{}, #{}".format(pr["title"], pr["number"]))
            changes.append("Big thanks to @{} for the PR!".format(pr["user"]["login"]))
    changes = "\n- ".join(changes)
    changes = "- " + changes
    return changes

def generate_changelog():
    old_version = get_last_release()
    version = get_new_release(old_version)
    changelog = "## [{}] - {}\n".format(version, str(datetime.datetime.today()).split()[0])
    release_notes = "### Fixed\n"
    release_notes += get_changes()
    changelog += release_notes
    changelog += "\n\n"
    tmp = ""
    with open("CHANGELOG.md", 'r') as file:
        data = file.read()
        tmp = data[:data.find("## [{}]".format(old_version))]
        tmp += changelog
        tmp += data[data.find("## [{}]".format(old_version)):]
        tmp = "".join(tmp)
    with open("CHANGELOG.md", 'w') as file:
        file.write(tmp)
    print("Here are the release notes\n---------------\n{}\n---------------".format(release_notes))

generate_changelog()
