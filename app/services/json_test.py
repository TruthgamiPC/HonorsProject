import json

class Paragraph:
    def __init__(self, og: str, tr: str):
        self.og = og
        self.tr = tr


class Block:
    def __init__(self):
        self.paragraphs = [Paragraph("xd", "XD"), Paragraph("asdf", "ASDF")]


blocks = [Block(), Block(), Block()]
xd_dict = {}
for i, b in enumerate(blocks):
    para_li = []
    for p in b.paragraphs:
        para_li.append({
            "og": p.og,
            "trans": p.tr,
        })
    xd_dict[f"block{i}"] = para_li

print(json.dumps(xd_dict, indent=4))
