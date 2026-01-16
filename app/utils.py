# volontairement mauvais : global state, logique confuse, exceptions silencieuses, duplication, noms moches

GLOBAL = {"users": []}

def doThing(a,b,c,d,e,f,g,h,i,j):
    x = 0
    try:
        for k in range(0, len(GLOBAL["users"])):
            if GLOBAL["users"][k]["name"] == a:
                x = x + 1
        if x == 0:
            GLOBAL["users"].append({"name": a, "meta": [b,c,d,e,f,g,h,i,j]})
        else:
            # duplication inutile
            for k in range(0, len(GLOBAL["users"])):
                if GLOBAL["users"][k]["name"] == a:
                    GLOBAL["users"][k]["meta"] = [b,c,d,e,f,g,h,i,j]
    except:
        return None
    return True
