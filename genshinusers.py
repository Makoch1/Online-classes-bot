import genshinstats as gs
import pickle

PICKLE_FILE = 'G_OBJECT.p'

Cookies = {
    # 'discordID': {'ltuid':LTUID, 'ltoken':LTOKEN}
}

def set_cookies():
    cks = []
    for i in Cookies:
        cks.append(Cookies[i])
    gs.set_cookies(*cks, clear=False)

def redeem_code_for_all(code:str):
    for i in Users.users:
        if i.lt_uid != None and i.code_cookie != None and i.uid != None:
            gs.redeem_code(code, uid=i.uid, cookie={'account_id':i.lt_uid, 'cookie_token':i.code_cookie})

def load_G_users():
    try:
      with open(PICKLE_FILE, "rb") as f:
          data = pickle.load(f)
      for i in data:
          Users(*i)
    except:
      print('no users to load')

def save_to_pickle():
    data = []
    for i in Users.users:
        data.append([
            i.discord_ID,
            i.lt_uid,
            i.l_token,
            i.uid,
            i.code_cookie
        ])
    with open(PICKLE_FILE, 'wb') as f:
        pickle.dump(data, f)

class Users:
    users = []

    def __init__(
        self, 
        discord_ID:int, 
        lt_uid:int = None,
        l_token:str = None, 
        uid:int = None,
        code_cookie:str = None
        ):
        
        self.discord_ID = discord_ID
        self.lt_uid = lt_uid
        self.l_token = l_token
        self.uid = uid
        self.code_cookie = code_cookie

        self.resin_alert = 140

        if self != None and self.discord_ID not in __class__.get_all_discordIDs():
            __class__.users.append(self)

        if self.lt_uid != None and self.l_token != None:
            __class__.add_to_Cookies()

        save_to_pickle()

    @staticmethod
    def add_to_Cookies():
        for i in Users.users:
            if i.lt_uid != None and i.l_token != None:
                Cookies[i.discord_ID] = {'ltuid':i.lt_uid, 'ltoken':i.l_token}
                print('amougus')
        set_cookies()

    @staticmethod
    def get_resin_all():
        data = {}
        for i in __class__.users:
            resin = i.get_resin_count()
            id = i.discord_ID
            data[id] = resin
        return data

    @staticmethod
    def get_object_by_discordID(disc_ID):
        data = []
        for i in Users.users:
            if i.discord_ID == disc_ID:
                data.append(i)
        try:        
            return data[0]
        except:
            return None

    @staticmethod
    def get_all_discordIDs():
      data = []
      for i in Users.users:
        data.append(i.discord_ID)
      return data

    def get_resin_count(self):
        notes = gs.get_notes(self.uid)
        resin = notes['resin']
        return int(resin)