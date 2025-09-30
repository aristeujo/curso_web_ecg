import re

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