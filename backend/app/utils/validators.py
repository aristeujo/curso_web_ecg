import re
from datetime import date, datetime

SYS_MIN, SYS_MAX = 60, 300
DIA_MIN, DIA_MAX = 30, 200

def parse_birth_date(birth_date):
    if birth_date in (None,""):
        return None
    if isinstance(birth_date, date):
        return birth_date
    return datetime.strptime(birth_date, "%d/%m/%Y").date()

def normalize_phone_br(v: str) -> str:
    # v = "+55 (92) 98424-4668"
    s = re.sub(r"\D", "", str(v or ""))
    # s = 559298424668
    if not s: 
        raise ValueError("telefone vazio")
    #  Para remover o código do país, se presente
    if s.startswith("0055"):
        local = s[4:] 
        # local = "9298424668"
    elif s.startswith("55"):
        local = s[2:]
    else:
        local = s
    
    # Para remover o zero da operadora
    if local.startswith("0"):
        cand = local[1:]
        if len(cand) in (10, 11):
            local = cand
    if len(local) not in (10, 11):
        raise ValueError("telefone inválido")
    return "+55" + local

def validate_pressure(pressure_value: str) -> str: 
    if not isinstance(pressure_value, str):
        raise ValueError("Pressão deve estar no formato: 'sistólica/diastólica' ou seja '120/80'")
    raw = pressure_value.strip()
    parts = raw.split("/")

    if len(parts) != 2:
        raise ValueError("A pressão deve estar no formato: '120/80'")

    try: 
        syst_pressure = int(parts[0])
        diast_pressure = int(parts[1])
    except Exception:
        raise ValueError("Pressão deve conter apenas números inteiros")
    
    if not (SYS_MIN <= syst_pressure <= SYS_MAX) or not (DIA_MIN <= diast_pressure <= DIA_MAX):
        raise ValueError("Valores estão fora do intervalo permitido.")

    return f"{syst_pressure}/{diast_pressure}"

def _make_pressure(syst: int | str, diast: int | str) -> str:
    try: 
        syst_value = int(syst)
        diast_value = int(diast)
    except Exception:
        raise ValueError("os valores devem ser inteiros!")
    
    if not (SYS_MIN <= syst_value <= SYS_MAX) or not (DIA_MIN <= diast_value <= DIA_MAX):
        raise ValueError("Valores estão fora do intervalo permitido.")
    
    return f"{syst_value}/{diast_value}"

def unify_pressure_payload(data):
    if not isinstance(data, dict): 
        return data
    
    p = data.get("pressure")
    s = data.get("systolic_mmHg")
    d = data.get("diastolic_mmHg")

    if p and (s is None and d is None):
        data["pressure"] = validate_pressure(p)
        return data

    if not p and (s is not None and d is not None):
        data["pressure"] = _make_pressure(s, d)
        return data

    if p and (s is not None and d is not None):
        p_norm = validate_pressure(p)
        expected = _make_pressure(s, d)
        if p_norm != expected:
            raise ValueError("pressure e (systolic_mmHg, diastolic_mmHg) não conferem")
        data["pressure"] = p_norm
        return data

    raise ValueError("Informe 'pressure' ou ambos 'systolic_mmHg' e 'diastolic_mmHg'.")

    