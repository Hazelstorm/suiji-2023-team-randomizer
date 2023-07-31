import json


google_sheet_data = """Eriha	19199.5
sheplet	18907.1
goheegy	18023.7
5henry	16700.4
My Angel Eru	16538.4
AuroraPhasmata	16308
MEGAMELA	16270
Zed0x	16207.5
R J	16131.9
-yukineko-	15841.5
CloggyBobby	15753.2
SilverTyrant	15701.9
D3kuu	15513.5
YaniFR	15423.9
Polemo03	15374.6
ImChro	14909.4
_knots	14894.5
Kyoumo	14838.7
Raphalge	14804.3
Xok	14744.7
dragonmaxx	14688.6
Roxy-	14675.2
uone	14661.7
MantequillAlex	14548.8
Dioramos	14426.3
Yuemiao	14332.7
Daniels	14223.9
Miniature Lamp	14222
Ranshi	14205.9
r1chyy	14057.2
-Ryuji-	14014
HiroK	13711.1
Joltzzz	13548.9
Esconyan	13491.9
Dusk-	13361.6
janitore	13300.2
_Illustrious_	13187.6
furry feet	13174.5
GoZaRaNi	13151.8
-Akitai-	13074.4
chibamasu	13073.1
Klarion	12950.1
Vasko2o	12777.5
Touche	12690.5
Noko_BSF	12637.6
nevqr	12573.5
Tsukani	12559.2
Cookie_Tree	12545.1
Hivan111	12502.8
_somet	12463.2
akumufangirl	12344.7
JarHed	12240.9
Akamileusz	12227.4
BabySnakes	12070.7
Dayzeek	12036
Inigo	12023.3
CrabCow	12013.1
_mtk	11926.5
duski	11898.1
krokodil_koban	11803.1
Boaz	11796.2
Ponamis	11720.4
Dynutka	11695
Ookura Risona	11620.9
knibblet	11588.4
alemagno333	11565.8
Chernobog	11499.5
Shyguy	11470.1
faheen	11465.9
Glaceon-	11456.1
Mazzuli500	11430.5
Huntey	11353.9
Mikalodo	11340.4
Friggy-chan	11340.4
MrrMiller	11317.3
Fenrir029	11299
_TheXFactory_	11297.9
Nethen	11291.3
Ak1o	11245.2
nuku0315	11208.1
BWithey	11181.3
Hotman	11176.1
Acii_	11135.6
Krekker	11124.1
Skey	11117.7
Heipharambe	11083.1
skolodojko	11051.4
davidminh0111	11041.5
MuraToy	11007.3
Lightning Wyvern	10961.3
Reu70	10810.9
HHVanilla Ice	10772.1
Iojioji	10751.6
megalovania lol	10726.9
Ratchet0203	10678.8
Ku_Ren	10556.3
ParraCharlie	10541.3
Twin2	10540.3
OldFriend	10488.7
dots_	10463
Vendelicious	10434.3
Kioshinxs	10406.8
Briesmas	10366.6
KITEMMUORT322	10364.5
-Nervi	10343.3
NaNaHiDa	10305.2
vun	10288.3
Gamelan4	10284.8
_Alice	10266.6
Jintsuu	10149.8
Sleepti	10080.6
Zippywin	9970.12
_Christmas	9932.49
WLYMinato	9876.19
Invisible O	9745.83
Chupalika	9713.53
Gomen Yuuka	9701.43
ZupOSU	9644.84
49Leo	9643.65
L1ght	9442.7
Agresywny Arbuz	9434.58
Kiara	9414.82
Haypzeh	9399.29
Sammu	9363.26
wen294	9309.2
Brown918	9287.59
Ping7731	9187.14
mikuhatsunegirl10	9071.11
lowelo random	9031.55
JunkyTrack	9015.95
ThomasZQY	8984.06
FabriGamer84	8902.59
Zest2822	8888.18
Mist31	8772.08
H1Pur	8765.6
Sandile	8698.37
Taikore	8687.69
Chrono_L	8630
DoKito	8627.83
fafik99	8611.57
Alwaysyukaz	8581.54
theangelov	8571.35
-Schwarts	8531.36
verosikachan	8526.02
bexs	8475.98
EHEPGODAP	8444.19
v5k	8420.74
DXA FonG	8356.56
njshift1	8355.44
aerarii	8349.84
Creeperbrine303	8316.61
LordTimeWaste	8241.2
SeaWeedAssassin	8193.46
AlloRus	8120.91
lemonduck	8093.96
Batu	8071.36
Lumenite-	8023.13
mekkimous	8007.57
South Korea	7918.54
Loutestoland	7766.45
Rocma	7765.2
AnZaaayy	7762.11
Dau	7689.15
Kappu	7617.85
MashedPotato	7492.65
Relae	7358.23
AutisticWeebBoy	7317.69
Ryukishi	7268.86
kururuminoah	7182.19
Potato9756	7134.93
DimplesRMe	7130.66
groggiy	7066.73
afe	7003.83
Minami-Kotori	7000.66
Maloacoa	6957.28
willowww	6858.45
-flakeur-	6786.27
YonGin	6769.58
Luna Yuuki	6650.52
Minion24	6610.24
KEK0	6562.3
404usernotfound	6188.74
T3mie	6168.59
_gt	6090.92
saderen	6031.48
Atra_	5973.58
Defectum	5956.58
Nyahnny	5953.9
UnagiDon	5892.23
Jason X	5849.8
Haryume	5727.65
alion02	5676.91"""

players = []
for player in google_sheet_data.split("\n"):
    username, pp = player.split("\t")
    players.append({"username": username, "pp": float(pp)})

with open("players.json", "w+") as file:
    json.dump(players, file)

print("finished generating player json!")
