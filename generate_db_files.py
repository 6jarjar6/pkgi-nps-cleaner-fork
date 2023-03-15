import requests
import pandas as pd

PS3_GAMES = "http://nopaystation.com/tsv/PS3_GAMES.tsv"
PS3_DLCS = "http://nopaystation.com/tsv/PS3_DLCS.tsv"
PS3_THEMES = "http://nopaystation.com/tsv/PS3_THEMES.tsv"
PS3_AVATARS = "http://nopaystation.com/tsv/PS3_AVATARS.tsv"
PS3_DEMOS = "http://nopaystation.com/tsv/PS3_DEMOS.tsv"
PSP_GAMES = "http://nopaystation.com/tsv/PSP_GAMES.tsv"
PSM_GAMES = "http://nopaystation.com/tsv/PSM_GAMES.tsv"
PSX_GAMES = "http://nopaystation.com/tsv/PSX_GAMES.tsv"

PS1_PREFIX = "[PS1]"
PS2_PREFIX = "[PS2]"
PS3_PREFIX = "[PS3]"

download = [
    (PS3_GAMES, 'pkgi_games.txt', PS3_PREFIX),
    (PS3_DLCS, 'pkgi_dlcs.txt', '[DLC]'),
    (PS3_THEMES, 'pkgi_themes.txt', '[THM]'),
    (PS3_AVATARS, 'pkgi_avatars.txt', '[AVT]'),
    (PS3_DEMOS, 'pkgi_demos.txt', '[DEMO]'),
]


def add_prefix(text):
    if "(PS2)" in text:
        return PS2_PREFIX + text.replace("(PS2)", "")
    if "(PS2 Classic)" in text:
        return PS2_PREFIX + text.replace("(PS2 Classic)", "")
    if "(PSX)" in text:
        return PS1_PREFIX + text.replace("(PSX)", "")
    if "(PS1 Classic)" in text:
        return PS1_PREFIX + text.replace("(PS1 Classic)", "")
    return nameprefix + text


nameprefix = "[???]"
for x in download:
    fileurl = x[0]
    filepath = x[1]
    nameprefix = x[2]

    file = requests.get(fileurl)
    open("raw_"+filepath, 'wb').write(file.content)

    df = pd.read_csv("raw_"+filepath, delimiter='\t', dtype=str, na_values="")
    df.dropna(subset=["Content ID"], inplace=True)
    df.dropna(subset=["Name"], inplace=True)

    if "games" in filepath:
        df = df[~df["Content ID"].str.contains("DEMO")]
        df = df[~df["Name"].str.contains("Beta")]
        df = df[~df["Name"].str.contains("BETA")]
        df = df[~df["Name"].str.contains("(DEMO)")]
        df = df[~df["Name"].str.endswith("Demo")]
        df = df[~df["Name"].str.startswith("Demo ")]

    df = df[~df["PKG direct link"].str.contains("MISSING")]

    df["Name"] = df["Name"].apply(add_prefix)

    df.to_csv(filepath, sep='\t', index=False)
