import requests
from telethon.sync import TelegramClient
from telethon.tl.functions.account import ReportPeerRequest
from telethon.tl.types import InputReportReasonViolence
from random import uniform, choice
from tqdm import tqdm
from time import sleep


try:
    chat_id_to_report_list = requests.get("https://fuckrussianbots.xyz/static/latest_list.csv").text.split("\n")
except:
    chat_id_to_report_list = []
chat_id_to_report_list = set(chat_id_to_report_list + ['boris_rozhin', 'grey_zone', 'go338', 'omonmoscow', 'wingsofwar', 'chvkmedia', 'hackberegini', 'mig41', 'pezdicide', 'SergeyKolyasnikov', 'MedvedevVesti', 'SIL0VIKI', 'balkanossiper', 'pl_syrenka', 'brussinf', 'lady_north', 'sex_drugs_kahlo', 'usaperiodical', 'russ_orientalist', 'vladlentatarsky', 'neoficialniybezsonov', 'rybar', 'milinfolive', 'grey_zone', 'rlz_the_kraken', 'warjournaltg', 'bbbreaking', 'milinfolive', 'Ugolok_Sitha', 'informator_life', 'chesnokmedia', 'ghost_of_novorossia', 'notes_veterans', 'diplomatia', 'bulbe_de_trones', 'olegtsarov', 'akimapache', 'zola_of_renovation', 'Hard_Blog_Line', 'ice_inii', 'swodki', 'infantmilitario', 'rt_russian', 'gazetaru', 'rbc_news', 'vedomosti', 'tass_agency', 'kremlinprachka', 'RVvoenkor ', 'rusvesnasu ', 'wargonzo', 'oldminerkomi', 'julia_chicherina', 'nezhurka', 'Sladkov_plus', 'Doninside', 'news_forfree', 'mikayelbad', 'donbassr', 'voenkorKotenok', 'marochkolive', 'rlz_the_kraken', 'miroshnik_r', 'sev_polit_takt', 'cmiye', 'holmogortalks', 'JokerDNR', 'svarschiki', 'donbass_segodnya', 'epoddubny', 'RtrDonetsk', 'medvedev_note', 'infantmilitario', 'RVvoenkor', 'conqueror95', 'rusyerevantoday', 'vysokygovorit', 'notes_veterans', 'neoficialniybezsonov', 'SergeyKolyasnikov', 'ontnews', 'Za_Derjavy', 'delyagin', 'military_corner', 'intelslava', 'vorposte', 'RIA82rf', 'adirect', 'ghost_of_novorossia', 'MaterikMedia', 'BeregTime', 'bbbreaking', 'intuition2036', 'karaulny', 'glavpolit', 'parbut', 'boris_rozhin', 'chvkmedia', 'mig41', 'mardanaka', 'tikandelaki', 'kbrvdvkr', 'skfo_telegraph', 'ia_steklomoy', 'BorodaV', 'akitilop', 'gossluga', 'glavmedia', 'operdrain', 'minzdravny', 'MayorFSB', 'orfosvinstvo', 'Baronova', 'pridybaylo', 'ChasovojPogody', 'robabayan', 'MedvedevVesti', 'skabeeva', 'nailyaaskerzade', 'MedvedevVesti', 'prbezposhady', 'vladivostok1978', 'milinfolive', 'vrogov', 'dplatonova', 'warjournaltg', 'SolovievLive', 'nailyaaskerzade', 'sashakots', 'epoddubny', 'Sladkov_plus', 'evgenyprimakov', 'akashevarova', 'superdolgov', 'romagolovanov', 'ASGasparyan', 'annashafran', 'ntnzn', 'NeSocSeti', 'radlekukh', 'egorgalenko', 'yudenich', 'Marinaslovo', 'vladlentatarsky', 'SonOfMonarchy', 'MaximYusin',])   # ids or names

# 2 ways to get api_id and api_hash (see "The Legacy way"): https://telegra.ph/How-to-get-Telegram-APP-ID--API-HASH-05-27
short_name = ''  # Short name from https://my.telegram.org/apps
api_id = 00000  # App api_id from https://my.telegram.org/apps
api_hash = ''  # App api_hash from https://my.telegram.org/apps
reasons = ['Support for the Russian invasion of Ukraine, support for violence', 'Пропаганда вбивства мирного українського населення та українських війських.', 'Пропаганда убийства мирного населения Украины и украинских военных', 'Propaganda for the killing of the civilian population of Ukraine and the Ukrainian military', "Ukraine", "Russian invasion", "War in Ukraine", "Russia started war", "Terrorism", "Російське вторгнення","Російське вторгнення в Україну"]
end_symbols = ["!", ".", "!!", "!!!"]

with TelegramClient(short_name, api_id, api_hash) as client:
    for reason in tqdm(reasons, desc='Reasons'):
        for channel in tqdm(chat_id_to_report_list, desc='Chat ids'):
            try:
                response = client(ReportPeerRequest(
                    peer=channel,
                    reason=InputReportReasonViolence(),
                    message=f"{reason}{choice(end_symbols)}"
                ))
            except:
                pass
            finally:
                sleep(uniform(2, 5))
        sleep(uniform(30, 60))
    