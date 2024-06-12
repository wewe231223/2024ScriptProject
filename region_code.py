def read_token(file):
    token = file.readline().rstrip('\n')
    s, loop = token.split()
    return s, int(loop)


def read_umd_token(file):
    token = file.readline().rstrip('\n')
    strs = list(token.split())
    s = strs[0]+' '+strs[1]
    loop = int(strs[-1])
    return s, int(loop)


def read_codes(file, n):
    codes = { }
    for _ in range(n):
        code, cont = file.readline().rstrip('\n').split()
        codes[cont] = code
    return codes


def read_umds(file, n):
    umd_names = []
    for _ in range(n):
        umd_names.append(file.readline().rstrip('\n'))
    return umd_names


def load_sgg_codes():
    global sgg_codes
    f = open('코드정보.txt')
    _, loop = read_token(f)
    for _ in range(loop):
        sido, loop = read_token(f)
        sgg_codes[sido] = read_codes(f, loop)


def load_umds():
    global umds
    f = open('읍면동정보.txt')
    _, loop = read_token(f)
    for _ in range(loop):
        sgg, loop = read_umd_token(f)
        umds[sgg] = read_umds(f, loop)


def get_sidos():
    return list(sgg_codes.keys())


def get_sggs(sido_nm):
    return list(sgg_codes[sido_nm].keys())

def get_umds():
    pass


sgg_codes = { }
umds = { }
load_sgg_codes()
print(sgg_codes)

load_umds()