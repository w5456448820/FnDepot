# -*- coding: utf-8 -*-
"""
证件号生成核心逻辑（无 GUI 依赖版）
抽取自 w5456448820/id-number-generator V2.3 的 id_generator.py，
仅保留纯算法部分，供 fnOS fpk 内的 HTTP 服务调用。

【用途声明】本程序生成的号码均为随机虚构，仅供软件开发测试、系统联调、
数据脱敏演示等合法场景使用。严禁用于伪造证件、冒用他人身份、绕过实名认证
或任何其他违法违规用途，使用者须自行承担全部法律责任。
"""
import os
import re
import json
import random
from datetime import date, timedelta

# ---------------- 统一社会信用代码 / 组织机构代码 ----------------
check_dict = {
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'J': 18, 'K': 19,
    'L': 20, 'M': 21, 'N': 22, 'P': 23, 'Q': 24, 'R': 25, 'T': 26, 'U': 27, 'W': 28,
    'X': 29, 'Y': 30}
dict_check = {value: key for key, value in check_dict.items()}
area_code = [
    110000, 120000, 130000, 140000, 150000, 210000, 220000, 230000, 310000,
    320000, 330000, 340000, 350000, 360000, 370000, 410000, 420000, 430000,
    440000, 450000, 460000, 500000, 510000, 520000, 530000, 540000, 610000,
    620000, 630000, 640000, 650000, 710000, 810000, 820000]
manage_code = [9]
type_code = [1, 2, 3, 9]

weight_code = [1, 3, 9, 27, 19, 26, 16, 17, 20, 29, 25, 13, 8, 24, 10, 30, 28]


def create_organization():
    """生成 9 位组织机构代码（8 位本体 + 1 位校验码）"""
    ww = [3, 7, 9, 10, 5, 8, 4, 2]
    cc = []
    dd = 0
    for i in range(8):
        cc.append(random.randint(1, 9))
        dd = dd + cc[i] * ww[i]
    for i in range(len(cc)):
        cc[i] = str(cc[i])
    C9 = 11 - dd % 11
    if C9 == 10:
        C9 = "X"
    elif C9 == 11:
        # 修正原版缺陷：GB11714 规定校验码为 11 时应取 "0"，原版返回空串导致后续越界
        C9 = "0"
    else:
        C9 = str(C9)
    cc.append(C9)
    return "".join(cc)


def create_social_credit():
    """生成 18 位统一社会信用代码"""
    org_code = create_organization().replace("-", "")
    total = 0
    code = (str(random.choice(manage_code)) + str(random.choice(type_code))
            + str(random.choice(area_code)) + org_code)
    for i in range(17):
        total = total + check_dict[code[i]] * weight_code[i]
    # 修正原版缺陷：total % 31 == 0 时 31-0=31 会触发 KeyError
    C18 = dict_check[(31 - total % 31) % 31]
    return code + C18


def Org_code():
    """生成 8 位-1 位格式的组织机构代码，如 12345678-X"""
    org_code = create_organization().replace("-", "")
    return org_code[:8] + "-" + org_code[-1]


# ---------------- 居民身份证号码（GB 11643-1999） ----------------
ID_WEIGHT = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
ID_CHECK = "10X98765432"


def id_check_code(body17):
    """按 GB 11643-1999 计算第 18 位校验码"""
    total = 0
    for i in range(17):
        total += int(body17[i]) * ID_WEIGHT[i]
    return ID_CHECK[total % 11]


def build_area6(prov, city, dist):
    """
    由三级选择的行政区划代码拼出 6 位地址码：
    prov/city/dist 分别为 2 / 4 / 6 位代码。
    选“随机”（空）时，从该层级下真实存在的区县码中随机抽取，不再拼凑随机数字，
    保证生成的地址码在 GB/T 2260 中有对应行政区划。
    """
    if dist:
        return dist
    if city:
        pool = CITY_CODES.get(city) or []
        if pool:
            return random.choice(pool)
        return city + "00"
    if prov:
        pool = PROV_CODES.get(prov) or []
        if pool:
            return random.choice(pool)
        return prov + "0000"
    if ALL_DISTRICT_CODES:
        return random.choice(ALL_DISTRICT_CODES)
    return "110101"


# ---------------- 出生日期 ----------------
MONTH_DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def days_in_month(y, m):
    """返回指定年月的天数（含闰年判断）"""
    if m == 2 and y % 4 == 0 and (y % 100 != 0 or y % 400 == 0):
        return 29
    return MONTH_DAYS[m - 1]


def valid_date(y, m, d):
    try:
        date(y, m, d)
        return True
    except ValueError:
        return False


# 出生年份允许范围：下限 1900，上限 = 系统当前年份 + 10 年
YEAR_MIN = 1900
YEAR_MAX = date.today().year + 10


def random_birthday():
    """随机生日（1960-01-01 ~ 2005-12-31），8 位 YYYYMMDD"""
    start = date(1960, 1, 1)
    span = (date(2005, 12, 31) - start).days
    return (start + timedelta(days=random.randint(0, span))).strftime("%Y%m%d")


def normalize_birth(raw):
    """
    把手输的多种日期写法规范为 8 位 YYYYMMDD：
      19900101 / 1990-1-1 / 1990.1.1 / 1990/01/01 / 1990年1月1日 / 900101 / 1990
    空串返回 ""（表示随机生成）；无法识别返回 None
    """
    t = (raw or "").strip()
    if not t or t == "随机":
        return ""
    for sep in ("年", "月", "/", ".", "。", "\\", "－", "—", "_"):
        t = t.replace(sep, "-")
    t = t.replace("日", "")
    groups = [g for g in re.split(r"[-\s,，、]+", t) if g]
    y = m = d = None
    if len(groups) >= 3 and all(g.isdigit() for g in groups[:3]):
        y, m, d = int(groups[0]), int(groups[1]), int(groups[2])
        if y < 100:
            y += 1900 if y > 40 else 2000
    elif len(groups) == 1 and groups[0].isdigit():
        dig = groups[0]
        if len(dig) == 8:
            y, m, d = int(dig[:4]), int(dig[4:6]), int(dig[6:8])
        elif len(dig) == 6:
            yy = int(dig[:2])
            y, m, d = (1900 if yy > 40 else 2000) + yy, int(dig[2:4]), int(dig[4:6])
        elif len(dig) == 4:
            y, m, d = int(dig), 1, 1
    if y is None:
        return None
    if not (YEAR_MIN <= y <= YEAR_MAX):
        return None
    if not valid_date(y, m, d):
        return None
    return "%04d%02d%02d" % (y, m, d)


def create_id_number(area="", birthday="", sex="随机"):
    """
    生成 18 位居民身份证号码（随机虚构，仅测试用）
    area     : 6 位地址码，留空则随机
    birthday : 8 位出生日期 YYYYMMDD，留空则随机 1960-01-01 ~ 2005-12-31
    sex      : "随机" / "男" / "女"，决定顺序码第 3 位的奇偶
    返回 (号码, 错误信息)
    """
    area = str(area).strip()
    if area == "":
        area = build_area6("", "", "")
    elif len(area) == 2 and area.isdigit():
        area = build_area6(area, "", "")
    elif len(area) == 4 and area.isdigit():
        area = build_area6("", area, "")
    elif not (len(area) == 6 and area.isdigit()):
        return "", "地区码需为 6 位数字"

    # 出生日期
    birthday = str(birthday).strip()
    if birthday == "":
        start = date(1960, 1, 1)
        span = (date(2005, 12, 31) - start).days
        d = start + timedelta(days=random.randint(0, span))
        birthday = d.strftime("%Y%m%d")
    else:
        if len(birthday) != 8 or not birthday.isdigit():
            return "", "出生日期需为 8 位数字，格式 YYYYMMDD"
        try:
            date(int(birthday[0:4]), int(birthday[4:6]), int(birthday[6:8]))
        except ValueError:
            return "", "出生日期不是有效日期"
        if not (YEAR_MIN <= int(birthday[0:4]) <= YEAR_MAX):
            return "", "出生年份超出合理范围"

    # 顺序码（第 17 位奇数为男、偶数为女）
    order = random.randint(1, 999)
    if sex == "男" and order % 2 == 0:
        order = order - 1 if order > 1 else order + 1
    elif sex == "女" and order % 2 == 1:
        order = order + 1 if order < 999 else order - 1
    body = area + birthday + "%03d" % order
    return body + id_check_code(body), ""


# ---------------- 行政区划数据（GB/T 2260） ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def resource_path(rel):
    """资源查找：优先脚本同级目录，其次上级目录（兼容打包前后两种布局）。"""
    for base in (BASE_DIR, os.path.dirname(BASE_DIR)):
        p = os.path.join(base, rel)
        if os.path.exists(p):
            return p
    return os.path.join(BASE_DIR, rel)


def load_districts():
    path = resource_path("pca-code.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def normalize_districts(raw):
    """
    规整行政数据：只保留合法的 6 位区县码作为身份证地址码。
    东莞、中山等不设区的地级市，原始数据下挂的是 9 位街道码（如 441900003），
    这类不能作为身份证地址码，统一替换为“市本级”选项（市码 + 00，即 441900）。
    """
    out = []
    for p in raw:
        pcode = str(p.get("code", ""))
        if len(pcode) != 2 or not pcode.isdigit():
            continue
        cities = []
        for c in p.get("children") or []:
            ccode = str(c.get("code", ""))
            if len(ccode) != 4 or not ccode.isdigit():
                continue
            raw_children = c.get("children") or []
            valid = [d for d in raw_children
                     if len(str(d.get("code", ""))) == 6 and str(d.get("code")).isdigit()]
            dists = []
            if len(valid) != len(raw_children):
                dists.append({"code": ccode + "00", "name": "（市本级）" + c.get("name", "")})
            dists.extend({"code": d["code"], "name": d["name"]} for d in valid)
            cities.append({"code": ccode, "name": c.get("name", ""), "children": dists})
        out.append({"code": pcode, "name": p.get("name", ""), "children": cities})
    return out


DISTRICTS = load_districts()
PROVINCES = [(p["code"], p["name"], p["children"]) for p in normalize_districts(DISTRICTS)]

# 真实区县地址码索引：随机选择时只在真实存在的层级代码中抽取
ALL_DISTRICT_CODES = [d["code"]
                      for _pc, _pn, _cs in PROVINCES
                      for _c in _cs
                      for d in (_c.get("children") or [])
                      if len(str(d.get("code", ""))) == 6 and str(d.get("code")).isdigit()]
PROV_CODES = {}
CITY_CODES = {}
for _pc, _pn, _cs in PROVINCES:
    _prov_pool = []
    for _c in _cs:
        _dpool = [d["code"] for d in (_c.get("children") or [])
                  if len(str(d.get("code", ""))) == 6 and str(d.get("code")).isdigit()]
        if _dpool:
            CITY_CODES[_c["code"]] = _dpool
            _prov_pool.extend(_dpool)
    if _prov_pool:
        PROV_CODES[_pc] = _prov_pool


def districts_payload():
    """给前端的三级联动数据结构。"""
    return [{"code": pc, "name": pn,
             "cities": [{"code": c["code"], "name": c["name"],
                         "districts": [{"code": d["code"], "name": d["name"]} for d in (c.get("children") or [])]}
                        for c in cs]}
            for pc, pn, cs in PROVINCES]


def generate(kind, count=1, area="", birthday="", sex="随机"):
    """
    统一入口。kind: scc(统一社会信用代码) / org(组织机构代码) / id(身份证)
    返回 (列表, 错误信息)
    """
    try:
        count = int(count)
    except Exception:
        count = 1
    count = max(1, min(count, 200))

    out = []
    if kind == "scc":
        for _ in range(count):
            out.append(create_social_credit())
        return out, ""

    if kind == "org":
        for _ in range(count):
            out.append(Org_code())
        return out, ""

    if kind == "id":
        b = normalize_birth(birthday)
        if b is None:
            return [], "出生日期无法识别，支持 19900101 / 1990-1-1 / 1990年1月1日 等写法"
        a = str(area or "").strip()
        if a and not (a.isdigit() and len(a) in (2, 4, 6)):
            return [], "地区码需为 2 / 4 / 6 位数字"
        for _ in range(count):
            code, err = create_id_number(area=a, birthday=b, sex=sex or "随机")
            if err:
                return [], err
            out.append(code)
        return out, ""

    return [], "未知的生成类型"
