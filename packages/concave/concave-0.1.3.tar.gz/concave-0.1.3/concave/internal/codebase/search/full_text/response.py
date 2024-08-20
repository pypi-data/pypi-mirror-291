# default yellow color
def colorize(text, color=33):
    return f"\033[{color}m{text}\033[0m"


class ZoektResponse:
    def __init__(self, raw):
        self.raw = raw["result"]

    def total_matches(self):
        return self.raw["Stats"]["MatchCount"]

    def parse_match(self, match):
        return {
            "filename": match["FileName"],
            "line_num": match["LineNum"],
            "fragments": match["Fragments"],
            "line": self.fragments2line(match["Fragments"])
        }

    @staticmethod
    def fragments2line(fragments):
        return "".join([f["Pre"] + f["Match"] + f["Post"] for f in fragments]).strip()

    def file_matches(self):
        results = []
        if not self.raw["FileMatches"]:
            return results

        print(self.raw)
        for f in self.raw["FileMatches"]:
            results.append({
                "filename": f["FileName"],
                "matches": [self.parse_match(m) for m in f["Matches"]]
            })
        return results

    def dict(self):
        files = []
        for f in self.file_matches():
            file = {
                "name": f["filename"],
                "lines": []
            }
            lines = set()
            for match in f["matches"]:
                line_num = match["line_num"]
                if line_num not in lines:
                    file["lines"].append([line_num, match["line"]])
            files.append(file)
        return files

    def print(self):
        print("=" * 30)
        print("| FULL TEXT SEARCH RESULTS")
        print("| Full text symbol results:", colorize(self.raw["QueryStr"]))
        print(f"| Total matches: {colorize(self.total_matches())}")
        print("=" * 30)
        for f in self.file_matches():
            print()
            print(f"{colorize(f['filename'], 32)}")
            print("-" * 20)
            for m in f["matches"]:
                line = ""
                for fragment in m["fragments"]:
                    line += fragment["Pre"] + colorize(fragment["Match"], 33) + fragment["Post"]
                num = colorize(f'{m["line_num"]}'.ljust(6, " "), 36)
                print(f"{num}|{line.rstrip()}")
