import json


class Candidat():
    def __init__(self, path_to_json):
        dico = json.load(open(path_to_json, "rb"), encoding="utf-8")
        self.name = dico["name"]
        self.nickname = dico["nickname"].lower()
        self.parti = dico["parti"]
        self.site = dico["site"]
        self.propositions = dico["propositions"]
        self.num_propositions = len(dico["propositions"])
        return
