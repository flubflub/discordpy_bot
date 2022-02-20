# steamID64: 76561198073025954
# steamdID3: [U:1:112760226]
# steamID: STEAM_0:0:56380113
# source: https://gist.github.com/bcahue/4eae86ae1d10364bb66d

steamid64_base = 76561197960265728


def steamid64_to_steamid(steamid64):
    steamid = ['STEAM_0:']
    steamidacc = int(steamid64) - steamid64_base
    if steamidacc % 2 == 0:
        steamid.append('0:')
    else:
        steamid.append('1:')
    steamid.append(str(steamidacc // 2))
    return ''.join(steamid)


def steamid_to_steamid64(steamid):
    sid_split = steamid.split(':')
    steamid64 = int(sid_split[2]) * 2
    if sid_split[1] == '1':
        steamid64 += 1
    steamid64 += steamid64_base
    return steamid64


def steamid64_to_steamid3(steamid64):
    steamid3 = ['[U:1:']
    steamidacc = int(steamid64) - steamid64_base
    steamid3.append(str(steamidacc) + ']')
    return ''.join(steamid3)


def steamid3_to_steamid64(steamid3):
    for ch in ['[', ']']:
        if ch in steamid3:
            steamid3 = steamid3.replace(ch, '')
    steamid3_split = steamid3.split(':')
    steamid64 = int(steamid3_split[2]) + steamid64_base
    return steamid64


def steamid_to_steamid3(steamid):
    steamid_split = steamid.split(':')
    steamid3 = ['[U:1:']
    y = int(steamid_split[1])
    z = int(steamid_split[2])
    steamacc = z * 2 + y
    steamid3.append(str(steamacc) + ']')
    return ''.join(steamid3)


def steamid3_to_steamid(steamid3):
    for ch in ['[', ']']:
        if ch in steamid3:
            steamid3 = steamid3.replace(ch, '')
    steamid3_split = steamid3.split(':')
    steamid = ['STEAM_0:']
    z = int(steamid3_split[2])
    if z % 2 == 0:
        steamid.append('0:')
    else:
        steamid.append('1:')
    steamacc = z // 2
    steamid.append(str(steamacc))
    return ''.join(steamid)

