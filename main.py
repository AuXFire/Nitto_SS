import random
import xml.etree.ElementTree as ET

from flask import request, jsonify, Flask, Response, render_template, send_from_directory

app = Flask(__name__, static_folder='static')

KEY = "516284"
FACTOR = 986
FACTOR2 = 38
SEED_LENGTH = 2


class LoginXml:
    # create lists to add only necessary xml nodes
    def __init__(self):
        self.logins = []
        self.locations = []
        self.garages = []
        self.badges = []
        self.sclevels = []
        self.getdealer = []
        self.dealercars = []
        self.startercars = []

    # dealer categories node
    def get_dealer(self, n):
        self.getdealer.append({
            "n": n
        })

    # dealer cars node
    # TODO: create proper XML format - location? -> categories-> cars?
    def add_dealer_cars(self, cd):
        self.dealercars.append({
            "cd": cd
        })

    def starter_showroom(self, wid, id, ws):
        self.startercars.append({
            "wid": wid,
            "id": id,
            "ws": ws
        })

    # SC node
    def add_sc(self, i, sc, c):
        self.sclevels.append({
            "id": i,
            "sc": sc,
            "c": c
        })

    # badges awarded node
    def add_badges(self, i, n, v):
        self.badges.append({
            "i": i,
            "n": n,
            "v": v
        })

    # user data node
    def add_login(self, bg, dc, i, im, m, p, sc, ti, tr, u, vip, fbc, alr, bpr, sr, lid, aid, mb):
        self.logins.append(({
            "bg": bg,
            "dc": dc,
            "i": i,
            "im": im,
            "m": m,
            "p": p,
            "sc": sc,
            "ti": ti,
            "tr": tr,
            "u": u,
            "vip": vip,
            "fbc": fbc,
            "alr": alr,
            "bpr": bpr,
            "sr": sr,
            "lid": lid,
            "aid": aid,
            "mb": mb
        }))

    # global locations node
    def add_location(self, lid, f, r, ps, pf, ln):
        self.locations.append({
            "lid": lid,
            "f": f,
            "r": r,
            "ps": ps,
            "pf": pf,
            "ln": ln
        })

    # user owned cars node
    def add_garage(self, acid, i, ci, n, cc, pi, pn, ii, i_f, sel, children=[]):
        # Find the parent element by its 'i' value
        parent = next((elem for elem in self.garages if elem["i"] == i), None)

        # If the parent doesn't exist, add it to the list of elements
        if parent is None:
            parent = {
                "acid": acid,
                "i": i,
                "ci": ci,
                "n": n,
                "cc": cc,
                "pi": pi,
                "pn": pn,
                "ii": ii,
                "if": i_f,
                "sel": sel,
                "children": []
            }
            self.garages.append(parent)

        # Add the child elements to the parent's 'children' list
        for child in children:
            parent["children"].append(child)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route('/cache/<path:filename>', methods=['GET'])
def serve_file_cache(filename):
    cache_folder = 'cache'
    print(f"Static Cache: {filename}")
    return send_from_directory(app.static_folder, cache_folder + '/' + filename)


@app.route('/cache/car/packages/<directory>/<filename>', methods=['GET'])
def serve_static_car(directory, filename):
    static_folder = 'static'
    filepath = f'cache/car/packages/{directory}/{filename}'
    return send_from_directory(static_folder, filepath)


@app.route('/car/wheel/<filename>', methods=['GET'])
def serve_static_wheel(filename):
    static_folder = 'static'
    directory = 'car/wheel'
    filepath = f'{directory}/{filename}'
    return send_from_directory(static_folder, filepath)


@app.route('/cache/sounds/<filename>', methods=['GET'])
def serve_static_sound(filename):
    static_folder = 'static'
    print(f"Static Sound: {filename}")
    return send_from_directory(static_folder, filename)


@app.route('/race', methods=['POST', 'GET'])
def race():
    print('Request Method:', request.method)
    print('Request Headers:', request.headers)
    print('Request Data:', request.data)
    print('Request Form:', request.form)
    print('Request Args:', request.args)
    print('Request Files:', request.files)
    print('Request JSON:', request.json)
    print('Request Remote Address:', request.remote_addr)
    throttlePercent = request.form['throttlePercent']
    print(throttlePercent)
    # Use throttlePercent in some calculation to get the values
    rpm = random.randint(1000, 9000)
    mph = random.randint(0, 100)
    d = random.randint(1, 6)
    boostPSI = random.uniform(5.0, 25.0)
    # Construct the response XML
    response = f"<response rpm='{rpm}' mph='{mph}' d='{d}' boostPSI='{boostPSI}' />"
    return response, 200, {'Content-Type': 'application/xml'}


@app.route('/start', methods=['GET', 'POST'])
def start_id():
    start = LoginXml()

    id_element = ET.Element("c", id="12345")

    # serialize the XML element to a string for proper parsing in nitto
    xml_str = ET.tostring(id_element, encoding="unicode", method="xml")
    return Response(xml_str, mimetype='text/xml'), 200


@app.route('/startershowroom', methods=['GET', 'POST'])
def get_starter_cars():
    starter = LoginXml()

    root = ET.Element('n2')

    child_elements = [
        ET.Element('c', i="2", rh="6", ts="19"),
        ET.Element('c', i="4", rh="6", ts="19"),
        ET.Element('c', i="6", rh="6", ts="19")
    ]

    starter.starter_showroom(64, 64, 17)
    starter.add_dealer_cars("FFFFF")
    starter.add_dealer_cars("FF0FF")
    starter.add_dealer_cars("00F0F")

    i = 0
    while i < len(child_elements):
        for attr_name, attr_value in starter.__dict__.items():
            if attr_name == "startercars":
                # create a location node for each location in the list
                for starter_car in attr_value:
                    wheel_element = ET.Element('w')
                    wheel_sub = ET.Element('p')
                    for key, value in starter_car.items():
                        wheel_sub.set(key, str(value))
                    wheel_element.append(wheel_sub)
                    child_elements[i].append(wheel_element)
        i += 1

    i = 0
    while i < len(child_elements):
        for attr_name, attr_value in starter.__dict__.items():
            if attr_name == "dealercars":
                # create a location node for each location in the list
                color_element = ET.Element('c')
                for dealer in attr_value:
                    color_sub = ET.Element('l')
                    for key, value in dealer.items():
                        color_sub.set(key, str(value))
                    color_element.append(color_sub)
                child_elements[i].append(color_element)
        i += 1

    for child in child_elements:
        root.append(child)

    # serialize the XML element to a string for proper parsing in nitto
    xml_str = ET.tostring(root, encoding="unicode", method="xml")
    return Response(xml_str, mimetype='text/xml'), 200


@app.route('/getdealer', methods=['GET', 'POST'])
def get_dealer():
    dealer = LoginXml()

    root = ET.Element("dealer")

    child_elements = [
        ET.Element('l', pi="0", c="0", i="1", p="1000", n="Honda", cl="", g="grade"),
        ET.Element('l', pi="0", c="0", i="2", p="1000", n="Mazda", cl="", g="grade"),
        ET.Element('l', pi="0", c="0", i="3", p="1000", n="Nissan", cl="", g="grade"),
        ET.Element('l', pi="0", c="0", i="4", p="1000", n="Chevrolet", cl="", g="grade"),
        ET.Element('l', pi="0", c="0", i="5", p="1000", n="Ford", cl="", g="grade"),
        ET.Element('l', pi="0", c="0", i="6", p="1000", n="McLaren", cl="", g="grade"),
        ET.Element('l', pi="0", c="0", i="7", p="1000", n="Porsche", cl="", g="grade"),
        ET.Element('l', pi="0", c="0", i="8", p="1000", n="Dodge", cl="", g="grade"),
        ET.Element('l', pi="0", c="0", i="9", p="1000", n="Scion", cl="", g="grade"),
        ET.Element('l', pi="0", c="0", i="10", p="1000", n="Special", cl="FFFFF", g="grade")
    ]

    dealer.get_dealer("Honda")
    dealer.get_dealer("Mazda")

    for attr_name, attr_value in dealer.__dict__.items():
        if attr_name == "getdealer":
            # create a location node for each location in the list
            for dealercar in attr_value:
                dealer_element = ET.Element('l')
                for key, value in dealercar.items():
                    dealer_element.set(key, str(value))
                child_elements[0].append(dealer_element)
    for child in child_elements:
        root.append(child)

    # serialize the XML element to a string for proper parsing in nitto
    xml_str = ET.tostring(root, encoding="unicode", method="xml")
    return Response(xml_str, mimetype='text/xml'), 200


# TODO: Create XML structure for dealer cars
@app.route('/getdealercars', methods=['GET', 'POST'])
def dealer():
    dealer = LoginXml()

    root = ET.Element("n2")
    child_elements = [
        # NO CAR IDS: 27, 103, 108, 130, 132, 151, 152, 154, 157. Max 160
        # TODO: why so many paint swatches
        ET.Element('l', id="McLaren F1", i="123", l="100", pi="6", p="100000", n="McLaren F1", wid="13", ws="18",
                   ts="20", eo="Yes", dt="RWD", np="5?", ct="Sum", et="Massive boom pow", tt="6-Speed Manual",
                   sw="2500", st="3.4", cb1="0", cb="0", po="0", poc="0", pp="10000", y="2023", led="led", cd=""),
        ET.Element('l', id="Honda", i="37", l="100", pi="1", p="24000", n="Honda Civic Si", wid="88", ws="15", ts="17",
                   eo="4-Banger", dt="FWD", np="5?", ct="Sum", et="Massive boom pow", tt="6-Speed Manual", sw="2800",
                   st="8.6", cb1="0", cb="0", po="0", poc="", pp="1000", y="1996", led="led", cd="FFFFF"),
        ET.Element('l', id="Honda", i="1", l="100", pi="1", p="0"),
        ET.Element('l', id="Honda", i="2", l="100", pi="1", p="0"),
        ET.Element('l', id="Honda", i="3", l="100", pi="1", p="0"),
        ET.Element('l', id="Honda", i="4", l="100", pi="1", p="0"),
        ET.Element('l', id="Honda", i="5", l="100", pi="1", p="0"),
        ET.Element('l', id="Honda", i="6", l="100", pi="1", p="0"),
        ET.Element('l', id="Honda", i="7", l="100", pi="1", p="0"),
        ET.Element('l', id="Honda", i="8", l="100", pi="1", p="0"),
        ET.Element('l', id="Honda", i="9", l="100", pi="1", p="0"),
        ET.Element('l', id="Honda", i="10", l="100", pi="2", p="0"),
        ET.Element('l', id="Honda", i="12", l="100", pi="2", p="0"),
        ET.Element('l', id="Honda", i="13", l="100", pi="2", p="0"),
        ET.Element('l', id="Honda", i="14", l="100", pi="2", p="0"),
        ET.Element('l', id="Honda", i="15", l="100", pi="2", p="0"),
        ET.Element('l', id="Honda", i="16", l="100", pi="2", p="0"),
        ET.Element('l', id="Honda", i="17", l="100", pi="2", p="0"),
        ET.Element('l', id="Honda", i="18", l="100", pi="3", p="0"),
        ET.Element('l', id="Honda", i="19", l="100", pi="3", p="0"),
        ET.Element('l', id="Honda", i="20", l="100", pi="3", p="0"),
        ET.Element('l', id="Honda", i="21", l="100", pi="3", p="0"),
        ET.Element('l', id="Honda", i="22", l="100", pi="3", p="0"),
        ET.Element('l', id="Honda", i="23", l="100", pi="3", p="0"),
        ET.Element('l', id="Honda", i="24", l="100", pi="3", p="0"),
        ET.Element('l', id="Honda", i="25", l="100", pi="4", p="0"),
        ET.Element('l', id="Honda", i="26", l="100", pi="4", p="0"),
        ET.Element('l', id="Honda", i="28", l="100", pi="4", p="0"),
        ET.Element('l', id="Honda", i="29", l="100", pi="4", p="0"),
        ET.Element('l', id="Honda", i="30", l="100", pi="4", p="0"),
        ET.Element('l', id="Honda", i="31", l="200", pi="5", p="0"),
        ET.Element('l', id="Honda", i="32", l="200", pi="5", p="0"),
        ET.Element('l', id="Honda", i="33", l="200", pi="5", p="0"),
        ET.Element('l', id="Honda", i="34", l="200", pi="5", p="0"),
        ET.Element('l', id="Honda", i="35", l="200", pi="5", p="0"),
        ET.Element('l', id="Honda", i="36", l="200", pi="5", p="0"),
        ET.Element('l', id="Honda", i="37", l="200", pi="3", p="0"),
        ET.Element('l', id="Honda", i="38", l="200", pi="3", p="0"),
        ET.Element('l', id="Honda", i="39", l="200", pi="3", p="0"),
        ET.Element('l', id="Honda", i="40", l="200", pi="3", p="0"),
        ET.Element('l', id="Honda", i="41", l="200", pi="3", p="0"),
        ET.Element('l', id="Honda", i="42", l="200", pi="3", p="0"),
        ET.Element('l', id="Honda", i="43", l="200", pi="3", p="0"),
        ET.Element('l', id="Honda", i="44", l="200", pi="4", p="0"),
        ET.Element('l', id="Honda", i="45", l="300", pi="4", p="0"),
        ET.Element('l', id="Honda", i="46", l="300", pi="4", p="0"),
        ET.Element('l', id="Honda", i="47", l="300", pi="4", p="0"),
        ET.Element('l', id="Honda", i="48", l="300", pi="4", p="0"),
        ET.Element('l', id="Honda", i="49", l="300", pi="4", p="0"),
        ET.Element('l', id="Honda", i="50", l="300", pi="5", p="0"),
        ET.Element('l', id="Honda", i="51", l="300", pi="5", p="0"),
        ET.Element('l', id="Honda", i="52", l="300", pi="5", p="0"),
        ET.Element('l', id="Honda", i="53", l="300", pi="5", p="0"),
        ET.Element('l', id="Honda", i="54", l="300", pi="5", p="0"),
        ET.Element('l', id="Honda", i="55", l="400", pi="5", p="0"),
        ET.Element('l', id="Honda", i="56", l="400", pi="3", p="0"),
        ET.Element('l', id="Honda", i="57", l="400", pi="3", p="0"),
        ET.Element('l', id="Honda", i="58", l="400", pi="3", p="0"),
        ET.Element('l', id="Honda", i="59", l="400", pi="3", p="0"),
        ET.Element('l', id="Honda", i="60", l="400", pi="3", p="0"),
        ET.Element('l', id="Honda", i="61", l="400", pi="3", p="0"),
        ET.Element('l', id="Honda", i="62", l="400", pi="3", p="0"),
        ET.Element('l', id="Honda", i="63", l="400", pi="4", p="0"),
        ET.Element('l', id="Honda", i="64", l="400", pi="4", p="0"),
        ET.Element('l', id="Honda", i="65", l="400", pi="4", p="0"),
        ET.Element('l', id="Honda", i="66", l="500", pi="4", p="0"),
        ET.Element('l', id="Honda", i="67", l="500", pi="4", p="0"),
        ET.Element('l', id="Honda", i="68", l="500", pi="4", p="0"),
        ET.Element('l', id="Honda", i="69", l="500", pi="5", p="0"),
        ET.Element('l', id="Honda", i="70", l="500", pi="5", p="0"),
        ET.Element('l', id="Honda", i="71", l="500", pi="5", p="0"),
        ET.Element('l', id="Honda", i="72", l="500", pi="5", p="0"),
        ET.Element('l', id="Honda", i="73", l="500", pi="5", p="0"),
        ET.Element('l', id="Honda", i="74", l="500", pi="5", p="0"),
        ET.Element('l', id="Honda", i="75", l="500", pi="3", p="0"),
        ET.Element('l', id="Honda", i="76", l="500", pi="3", p="0"),
        ET.Element('l', id="Honda", i="77", l="500", pi="3", p="0"),
        ET.Element('l', id="Honda", i="78", l="500", pi="3", p="0"),
        ET.Element('l', id="Honda", i="79", l="300", pi="3", p="0"),
        ET.Element('l', id="Honda", i="80", l="300", pi="3", p="0"),
        ET.Element('l', id="Honda", i="81", l="300", pi="3", p="0"),
        ET.Element('l', id="Honda", i="82", l="300", pi="4", p="0"),
        ET.Element('l', id="Honda", i="83", l="300", pi="4", p="0"),
        ET.Element('l', id="Honda", i="84", l="400", pi="4", p="0"),
        ET.Element('l', id="Honda", i="85", l="400", pi="4", p="0"),
        ET.Element('l', id="Honda", i="86", l="400", pi="4", p="0"),
        ET.Element('l', id="Honda", i="87", l="400", pi="4", p="0"),
        ET.Element('l', id="Honda", i="88", l="400", pi="5", p="0"),
        ET.Element('l', id="Honda", i="89", l="400", pi="5", p="0"),
        ET.Element('l', id="Honda", i="90", l="400", pi="5", p="0"),
        ET.Element('l', id="Honda", i="91", l="100", pi="5", p="0"),
        ET.Element('l', id="Honda", i="92", l="500", pi="5", p="0"),
        ET.Element('l', id="Honda", i="93", l="500", pi="5", p="0")
    ]

    dealer.add_dealer_cars(cd="FF0000")
    dealer.add_dealer_cars(cd="00FF00")
    dealer.add_dealer_cars(cd="FFFF00")
    dealer.add_dealer_cars(cd="FF00FF")
    dealer.add_dealer_cars(cd="00FFFF")
    dealer.add_dealer_cars(cd="800080")
    dealer.add_dealer_cars(cd="FFA500")

    i = 0
    while i < len(child_elements):
        for attr_name, attr_value in dealer.__dict__.items():
            if attr_name == "dealercars":
                # create a location node for each location in the list
                for dealercar in attr_value:
                    car_element = ET.Element('l')
                    for key, value in dealercar.items():
                        car_element.set(key, str(value))
                    child_elements[i].append(car_element)
        i += 1

    # append all parent and child nodes to root xml
    for child in child_elements:
        root.append(child)

    # serialize the XML element to a string for proper parsing in nitto
    xml_str = ET.tostring(root, encoding="unicode", method="xml")
    return Response(xml_str, mimetype='text/xml'), 200


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('u')
    password = request.form.get('p')
    print(username, password)
    # Your login logic here
    if username == 'q' and password == 'q':
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False}), 200


# TODO: Add database request to own class and automate generation of XML data
# TODO: Figure out optimized database structure for each user.
@app.route('/nitto', methods=['GET', 'POST'])
def nitto():
    login = LoginXml()
    # create the XML element for the LoginXml object
    root = ET.Element("n2", s="1")
    child_elements = [
        ET.Element('l', id="login"),
        ET.Element('l', id="locations"),
        ET.Element('l', id="sclevels"),
        ET.Element('l', id="getlicenseplates"),
        ET.Element('l', id="getpaintcats"),
        ET.Element('l', id="getpaints"),
        ET.Element('l', id="banners"),
        ET.Element('l', id="getallcars"),
        ET.Element('l', id="dyno"),
        ET.Element('l', id="badges"),
        ET.Element('l', id="gears"),
        ET.Element('l', id="broadcast"),
        ET.Element('l', id="cars"),
        ET.Element('l', id="impound"),
        ET.Element('l', id="usedcars"),
        ET.Element('l', id="specialEvent"),
        ET.Element('l', id="testdrivecar"),
        ET.Element('l', id="intro"),
        ET.Element('l', id="userDecalBans")
    ]

    # user login data
    login.add_login(bg="FFFFFF", dc=15, i=1, im=1, m=10000.0, p=10000, sc=5000, ti=0, tr=0, u="AuX", vip=1,
                    fbc=0,
                    alr=0, bpr=1, sr=0, lid=500, aid=1, mb=1)
    # locationXML
    login.add_location(lid=100, f=0, r=0, ps=5, pf=0, ln="Toreno")
    login.add_location(lid=200, f=1000, r=500, ps=10, pf=1, ln="Newburg")
    login.add_location(lid=300, f=10000, r=5000, ps=25, pf=1, ln="Creek Side")
    login.add_location(lid=400, f=50000, r=25000, ps=50, pf=1, ln="Vista Heights")
    login.add_location(lid=500, f=100000, r=750000, ps=100, pf=1, ln="Diamond Point")

    # # add sc levels, not working
    # login.add_sc("Noob", 1000, "00FF00")
    # login.add_sc("Novice", 2000, "ADD8E6")
    # login.add_sc("Rookie", 3000, "FF0000")
    # login.add_sc("Pro", 3000, "FF0000")
    # login.add_sc("Champion", 3000, "FF0000")
    # login.add_sc("Legend", 3000, "FF0000")
    #
    # # add badges, not working
    # login.add_badges(1, 505, 1)
    # login.add_badges(161, 1, 1)
    # login.add_badges(6, 1, 1)

    # parts nodes for car
    children = [
        {'i': '48301', 'ci': '128', 'n': 'OEM Front Bumper', 'in': '1', 'di': '1', 'cc': 'FF0000', 'pt': 'c'},
        {'i': '48302', 'ci': '129', 'n': 'OEM Side Skirt', 'in': '1', 'di': '1', 'cc': 'FF0000', 'pt': 'c'},
        {'i': '48303', 'ci': '130', 'n': 'OEM Rear Bumper', 'in': '1', 'di': '1', 'cc': 'FF0000', 'pt': 'c'},
        {'i': '48304', 'ci': '13', 'n': 'Nitto 1320 Drag Slicks', 'in': '1', 'di': '5', 'cc': 'undefi',
         'pt': 'c',
         'ps': '25'},
        {'i': '48306', 'ci': '71', 'n': 'OEM Hood', 'in': '1', 'di': '1', 'cc': 'FF0000', 'pt': 'c'},
        {'i': '48307', 'ci': '77', 'n': 'OEM Taillights', 'in': '1', 'di': '1', 'cc': 'undefi', 'pt': 'c'},
        {'i': '48308', 'ci': '120', 'n': 'OEM Anti-sway bars', 'in': '1', 'di': '1', 'cc': 'undefi', 'pt': 'c'},
        {'i': '48309', 'ci': '114', 'n': 'OEM Spring &amp; Shock Absorber Set', 'in': '1', 'di': '1',
         'cc': 'undefi',
         'pt': 'c', 'ps': '8'},
        {'i': '48310', 'ci': '110', 'n': 'OEM Front Seat Set', 'in': '1', 'di': '1', 'cc': 'undefi', 'pt': 'c'},
        {'i': '48311', 'ci': '117', 'n': 'OEM Engine Mounts', 'in': '1', 'di': '1', 'cc': 'undefi', 'pt': 'c'},
        {'i': '48313', 'ci': '115', 'n': 'OEM Control Arms', 'in': '1', 'di': '0', 'cc': 'undefi', 'pt': 'c'},
        {'i': '48314', 'ci': '76', 'n': 'OEM Headlights', 'in': '1', 'di': '0', 'cc': 'undefi', 'pt': 'c'},
        {'i': '48315', 'ci': '121', 'n': 'OEM Torsion Bar', 'in': '1', 'di': '0', 'cc': 'undefi', 'pt': 'c'},
        {'i': '48316', 'ci': '144', 'n': 'OEM Trunk and Rear Panel', 'in': '1', 'di': '1', 'cc': 'FF0000',
         'pt': 'c'},
        {'i': '48305', 'ci': '14', 'n': 'Volk Racing RE30 F-Zero Blue 20&quot;', 'in': '1', 'di': '120',
         'cc': '0',
         'pt': 'c', 'ps': '20'},
        {'i': '42721', 'ci': '31', 'n': 'McLaren Battery', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42725', 'ci': '18', 'n': 'McLaren Clutch Kit', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42726', 'ci': '135', 'n': 'McLaren Connecting Rod Set', 'in': '1', 'di': '0', 'cc': '',
         'pt': 'e'},
        {'i': '42726', 'ci': '135', 'n': 'McLaren Connecting Rod Set', 'in': '1', 'di': '0', 'cc': '',
         'pt': 'e'},
        {'i': '42727', 'ci': '36', 'n': 'McLaren Crankshaft', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42728', 'ci': '39', 'n': 'McLaren Engine Block', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42729', 'ci': '37', 'n': 'McLaren Cylinder Head Assembly', 'in': '1', 'di': '0', 'cc': '',
         'pt': 'e'},
        {'i': '42730', 'ci': '25', 'n': 'McLaren ECU', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42731', 'ci': '19', 'n': 'McLaren Flywheel', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42732', 'ci': '54', 'n': 'McLaren Fuel Pressure Regulator', 'in': '1', 'di': '0', 'cc': '',
         'pt': 'e'},
        {'i': '42733', 'ci': '49', 'n': 'McLaren Fuel Pump', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42734', 'ci': '51', 'n': 'McLaren Fuel Rail', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42737', 'ci': '41', 'n': 'McLaren Oil pump', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42738', 'ci': '56', 'n': 'McLaren Exhaust Piping', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42739', 'ci': '44', 'n': 'McLaren Piston Kit', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42740', 'ci': '45', 'n': 'McLaren Valve Set', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42741', 'ci': '46', 'n': 'McLaren Valve Spring Kit', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42742', 'ci': '48', 'n': 'McLaren Throttle Body', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42743', 'ci': '29', 'n': 'McLaren Spark Plug Set', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42744', 'ci': '30', 'n': 'McLaren Spark Plug Cables', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42745', 'ci': '136', 'n': 'McLaren Head Gasket', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42746', 'ci': '59', 'n': 'McLaren Exhaust Manifolds', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42747', 'ci': '52', 'n': 'McLaren Fuel Injectors', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42880', 'ci': '102', 'n': 'Formuline 2 Bottle Kit 40lb Carbon Fiber Bottles', 'in': '1',
         'di': '0',
         'cc': '', 'pt': 'e'},
        {'i': '42881', 'ci': '139', 'n': 'Gasman 350 Shot Fogger', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42884', 'ci': '81', 'n': 'Autorock Elite Series Supercharger 12 psi', 'in': '1', 'di': '0',
         'cc': '',
         'pt': 'e'},
        {'i': '42798', 'ci': '167', 'n': 'Mishimoto Performance Aluminum Radiator', 'in': '1', 'di': '1',
         'cc': '',
         'pt': 'e'},
        {'i': '42799', 'ci': '170', 'n': 'Mishimoto Performance Low Temperature Thermostat', 'in': '1',
         'di': '1',
         'cc': '', 'pt': 'e'},
        {'i': '42790', 'ci': '165', 'n': 'Royal Purple Synthetic Lubricant Package', 'in': '1', 'di': '1',
         'cc': '',
         'pt': 'e'},
        {'i': '42776', 'ci': '169', 'n': 'Mishimoto Liquid Chill Coolant Additive', 'in': '1', 'di': '1',
         'cc': '',
         'pt': 'e'},
        {'i': '42797', 'ci': '168', 'n': 'Royal Purple Oil Filter', 'in': '1', 'di': '1', 'cc': '', 'pt': 'e'},
        {'i': '42787', 'ci': '97', 'n': 'Dynasty Supreme Flo XR 2.5&quot;', 'in': '1', 'di': '0', 'cc': '',
         'pt': 'e'},
        {'i': '42759', 'ci': '33', 'n': 'Autorock Sport Cam Gears', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42768', 'ci': '34', 'n': 'Formuline Speed IV Cams', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42791', 'ci': '55', 'n': 'Monarch Drag Muffler 3.50&quot;', 'in': '1', 'di': '0', 'cc': '',
         'pt': 'e'},
        {'i': '42883', 'ci': '82', 'n': 'Blowfish Lightweight Supercharger Pulley', 'in': '1', 'di': '0',
         'cc': '',
         'pt': 'e'},
        {'i': '42773', 'ci': '57', 'n': 'FastFlow Race Pipe 2.5', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42750', 'ci': '96', 'n': 'FastFlow Air Filter', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42756', 'ci': '17', 'n': 'X Motorsports Super Lightweight Axle Set', 'in': '1', 'di': '0',
         'cc': '',
         'pt': 'e'},
        {'i': '130', 'ci': '133', 'n': 'BMW S70/3 (Engine)', 'in': '1', 'di': '0', 'cc': '', 'pt': 'm'}
    ]

    i = 15
    while i <= 25:
        # car node itself with parts nodes as child nodes
        login.add_garage(i, i, i, "F1 GTR Longtail", "FF0000", 1, "F1_____", 0, 0, 0, children=children)
        i += 1

    # sort child nodes properly
    for attr_name, attr_value in login.__dict__.items():
        if attr_name == "locations":
            # create a location node for each location in the list
            for location in attr_value:
                location_element = ET.Element('location')
                for key, value in location.items():
                    location_element.set(key, str(value))
                child_elements[1].append(location_element)
        elif attr_name == "badges":
            for badge in attr_value:
                badge_element = ET.Element("b")
                for key, value in badge.items():
                    badge_element.set(key, str(value))
                child_elements[9].append(badge_element)
        elif attr_name == "sclevels":
            for sc in attr_value:
                sc_element = ET.Element("u")
                for key, value in sc.items():
                    sc_element.set(key, str(value))
                child_elements[2].append(sc_element)
        elif attr_name == "logins":
            login_element = ET.Element("l")
            for login in attr_value:
                for key, value in login.items():
                    login_element.set(key, str(value))  # set the attributes on the existing login element
                child_elements[0].append(login_element)
        elif attr_name == "garages":
            for garage in attr_value:
                car_element = ET.Element("c")
                for key, value in garage.items():
                    if key != "children":
                        car_element.set(key, str(value))
                    elif key == "children":
                        for child_dict in value:
                            part_element = ET.Element("p")
                            for k, v in child_dict.items():
                                part_element.set(k, str(v))
                            car_element.append(part_element)
                child_elements[7].append(car_element)  # append the car_element to id=getallcars
        elif attr_value is not None:
            child_elements[0].set(attr_name, str(attr_value))

    # append all parent and child nodes to root xml
    for child in child_elements:
        root.append(child)

    # serialize the XML element to a string for proper parsing in nitto
    xml_str = ET.tostring(root, encoding="unicode", method="xml")
    return Response(xml_str, mimetype='text/xml')


@app.route('/beta', methods=['GET', 'POST'])
def beta():
    login = LoginXml()
    # create the XML element for the LoginXml object
    root = ET.Element("n2", s="1")
    child_elements = [
        ET.Element('l', id="login"),
        ET.Element('l', id="locations"),
        ET.Element('l', id="sclevels"),
        ET.Element('l', id="getlicenseplates"),
        ET.Element('l', id="getpaintcats"),
        ET.Element('l', id="getpaints"),
        ET.Element('l', id="banners"),
        ET.Element('l', id="getallcars"),
        ET.Element('l', id="dyno"),
        ET.Element('l', id="badges"),
        ET.Element('l', id="gears"),
        ET.Element('l', id="broadcast"),
        ET.Element('l', id="cars"),
        ET.Element('l', id="impound"),
        ET.Element('l', id="usedcars"),
        ET.Element('l', id="specialEvent"),
        ET.Element('l', id="testdrivecar"),
        ET.Element('l', id="intro"),
        ET.Element('l', id="userDecalBans")
    ]

    # user login data
    login.add_login(bg="FFFFFF", dc=15, i=1, im=1, m=10000.0, p=10000, sc=5000, ti=0, tr=0, u="AuX", vip=1,
                    fbc=0,
                    alr=0, bpr=1, sr=0, lid=400, aid=1, mb=1)
    # locationXML
    login.add_location(lid=100, f=0, r=0, ps=5, pf=0, ln="Toreno")
    login.add_location(lid=200, f=1000, r=500, ps=10, pf=1, ln="Newburg")
    login.add_location(lid=300, f=10000, r=5000, ps=25, pf=1, ln="Creek Side")
    login.add_location(lid=400, f=50000, r=25000, ps=50, pf=1, ln="Vista Heights")
    login.add_location(lid=500, f=100000, r=750000, ps=100, pf=1, ln="Diamond Point")

    # add sc levels, not working
    login.add_sc("Noob", 1000, "00FF00")
    login.add_sc("Novice", 2000, "ADD8E6")
    login.add_sc("Rookie", 3000, "FF0000")
    login.add_sc("Pro", 3000, "FF0000")
    login.add_sc("Champion", 3000, "FF0000")
    login.add_sc("Legend", 3000, "FF0000")

    # add badges, not working
    login.add_badges(1, 505, 1)
    login.add_badges(161, 1, 1)
    login.add_badges(6, 1, 1)

    # parts nodes for car
    children = [
        {'i': '48997', 'ci': '172', 'n': 'OEM Front Bumper', 'in': '1', 'di': '96', 'cc': '', 'pt': 'c'},
        {'i': '48301', 'ci': '128', 'n': 'OEM Front Bumper', 'in': '1', 'di': '1', 'cc': 'FF0000', 'pt': 'c'},
        {'i': '48302', 'ci': '129', 'n': 'OEM Side Skirt', 'in': '1', 'di': '1', 'cc': 'FF0000', 'pt': 'c'},
        {'i': '48303', 'ci': '130', 'n': 'OEM Rear Bumper', 'in': '1', 'di': '1', 'cc': 'FF0000', 'pt': 'c'},
        {'i': '48304', 'ci': '13', 'n': 'Nitto 1320 Drag Slicks', 'in': '1', 'di': '5', 'cc': 'undefi',
         'pt': 'c',
         'ps': '25'},
        {'i': '48306', 'ci': '71', 'n': 'OEM Hood', 'in': '1', 'di': '1', 'cc': 'FF0000', 'pt': 'c'},
        {'i': '48307', 'ci': '77', 'n': 'OEM Taillights', 'in': '1', 'di': '1', 'cc': 'undefi', 'pt': 'c'},
        {'i': '48308', 'ci': '120', 'n': 'OEM Anti-sway bars', 'in': '1', 'di': '1', 'cc': 'undefi', 'pt': 'c'},
        {'i': '48309', 'ci': '114', 'n': 'OEM Spring &amp; Shock Absorber Set', 'in': '1', 'di': '1',
         'cc': 'undefi',
         'pt': 'c', 'ps': '8'},
        {'i': '48310', 'ci': '110', 'n': 'OEM Front Seat Set', 'in': '1', 'di': '1', 'cc': 'undefi', 'pt': 'c'},
        {'i': '48311', 'ci': '117', 'n': 'OEM Engine Mounts', 'in': '1', 'di': '1', 'cc': 'undefi', 'pt': 'c'},
        {'i': '48313', 'ci': '115', 'n': 'OEM Control Arms', 'in': '1', 'di': '0', 'cc': 'undefi', 'pt': 'c'},
        {'i': '48314', 'ci': '76', 'n': 'OEM Headlights', 'in': '1', 'di': '0', 'cc': 'undefi', 'pt': 'c'},
        {'i': '48315', 'ci': '121', 'n': 'OEM Torsion Bar', 'in': '1', 'di': '0', 'cc': 'undefi', 'pt': 'c'},
        {'i': '48316', 'ci': '144', 'n': 'OEM Trunk and Rear Panel', 'in': '1', 'di': '1', 'cc': 'FF0000',
         'pt': 'c'},
        {'i': '48305', 'ci': '14', 'n': 'Volk Racing RE30 F-Zero Blue 20&quot;', 'in': '1', 'di': '120',
         'cc': '0',
         'pt': 'c', 'ps': '20'},
        {'i': '42721', 'ci': '31', 'n': 'McLaren Battery', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42725', 'ci': '18', 'n': 'McLaren Clutch Kit', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42726', 'ci': '135', 'n': 'McLaren Connecting Rod Set', 'in': '1', 'di': '0', 'cc': '',
         'pt': 'e'},
        {'i': '42726', 'ci': '135', 'n': 'McLaren Connecting Rod Set', 'in': '1', 'di': '0', 'cc': '',
         'pt': 'e'},
        {'i': '42727', 'ci': '36', 'n': 'McLaren Crankshaft', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42728', 'ci': '39', 'n': 'McLaren Engine Block', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42729', 'ci': '37', 'n': 'McLaren Cylinder Head Assembly', 'in': '1', 'di': '0', 'cc': '',
         'pt': 'e'},
        {'i': '42730', 'ci': '25', 'n': 'McLaren ECU', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42731', 'ci': '19', 'n': 'McLaren Flywheel', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42732', 'ci': '54', 'n': 'McLaren Fuel Pressure Regulator', 'in': '1', 'di': '0', 'cc': '',
         'pt': 'e'},
        {'i': '42733', 'ci': '49', 'n': 'McLaren Fuel Pump', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42734', 'ci': '51', 'n': 'McLaren Fuel Rail', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42737', 'ci': '41', 'n': 'McLaren Oil pump', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42738', 'ci': '56', 'n': 'McLaren Exhaust Piping', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42739', 'ci': '44', 'n': 'McLaren Piston Kit', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42740', 'ci': '45', 'n': 'McLaren Valve Set', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42741', 'ci': '46', 'n': 'McLaren Valve Spring Kit', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42742', 'ci': '48', 'n': 'McLaren Throttle Body', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42743', 'ci': '29', 'n': 'McLaren Spark Plug Set', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42744', 'ci': '30', 'n': 'McLaren Spark Plug Cables', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42745', 'ci': '136', 'n': 'McLaren Head Gasket', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42746', 'ci': '59', 'n': 'McLaren Exhaust Manifolds', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42747', 'ci': '52', 'n': 'McLaren Fuel Injectors', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42880', 'ci': '102', 'n': 'Formuline 2 Bottle Kit 40lb Carbon Fiber Bottles', 'in': '1',
         'di': '0',
         'cc': '', 'pt': 'e'},
        {'i': '42881', 'ci': '139', 'n': 'Gasman 350 Shot Fogger', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42884', 'ci': '81', 'n': 'Autorock Elite Series Supercharger 12 psi', 'in': '1', 'di': '0',
         'cc': '',
         'pt': 'e'},
        {'i': '42798', 'ci': '167', 'n': 'Mishimoto Performance Aluminum Radiator', 'in': '1', 'di': '1',
         'cc': '',
         'pt': 'e'},
        {'i': '42799', 'ci': '170', 'n': 'Mishimoto Performance Low Temperature Thermostat', 'in': '1',
         'di': '1',
         'cc': '', 'pt': 'e'},
        {'i': '42790', 'ci': '165', 'n': 'Royal Purple Synthetic Lubricant Package', 'in': '1', 'di': '1',
         'cc': '',
         'pt': 'e'},
        {'i': '42776', 'ci': '169', 'n': 'Mishimoto Liquid Chill Coolant Additive', 'in': '1', 'di': '1',
         'cc': '',
         'pt': 'e'},
        {'i': '42797', 'ci': '168', 'n': 'Royal Purple Oil Filter', 'in': '1', 'di': '1', 'cc': '', 'pt': 'e'},
        {'i': '42800', 'ci': '166', 'n': 'X Motorsports Traction Control', 'in': '1', 'di': '0', 'cc': '',
         'pt': 'e'},
        {'i': '42787', 'ci': '97', 'n': 'Dynasty Supreme Flo XR 2.5&quot;', 'in': '1', 'di': '0', 'cc': '',
         'pt': 'e'},
        {'i': '42759', 'ci': '33', 'n': 'Autorock Sport Cam Gears', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42768', 'ci': '34', 'n': 'Formuline Speed IV Cams', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42791', 'ci': '55', 'n': 'Monarch Drag Muffler 3.50&quot;', 'in': '1', 'di': '0', 'cc': '',
         'pt': 'e'},
        {'i': '42883', 'ci': '82', 'n': 'Blowfish Lightweight Supercharger Pulley', 'in': '1', 'di': '0',
         'cc': '',
         'pt': 'e'},
        {'i': '42773', 'ci': '57', 'n': 'FastFlow Race Pipe 2.5', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42750', 'ci': '96', 'n': 'FastFlow Air Filter', 'in': '1', 'di': '0', 'cc': '', 'pt': 'e'},
        {'i': '42756', 'ci': '17', 'n': 'X Motorsports Super Lightweight Axle Set', 'in': '1', 'di': '0',
         'cc': '',
         'pt': 'e'},
        {'i': '130', 'ci': '133', 'n': 'BMW S70/3 (Engine)', 'in': '1', 'di': '0', 'cc': '', 'pt': 'm'}
    ]

    login.add_garage(76543, 123, 123, "F1 GTR Longtail", "FF0000", 12, "F1_____", 0, 0, 1, children=children)

    i = 15
    while i <= 25:
        # car node itself with parts nodes as child nodes
        login.add_garage(i, i, i, "F1 GTR Longtail", "FF0000", 12, "F1_____", 0, 0, 0, children=children)
        i += 1

    # sort child nodes properly
    for attr_name, attr_value in login.__dict__.items():
        if attr_name == "locations":
            # create a location node for each location in the list
            for location in attr_value:
                location_element = ET.Element('location')
                for key, value in location.items():
                    location_element.set(key, str(value))
                child_elements[1].append(location_element)
        elif attr_name == "badges":
            for badge in attr_value:
                badge_element = ET.Element("b")
                for key, value in badge.items():
                    badge_element.set(key, str(value))
                child_elements[9].append(badge_element)
        elif attr_name == "sclevels":
            for sc in attr_value:
                sc_element = ET.Element("u")
                for key, value in sc.items():
                    sc_element.set(key, str(value))
                child_elements[2].append(sc_element)
        elif attr_name == "logins":
            login_element = ET.Element("l")
            for login in attr_value:
                for key, value in login.items():
                    login_element.set(key, str(value))  # set the attributes on the existing login element
                child_elements[0].append(login_element)
        elif attr_name == "garages":
            for garage in attr_value:
                car_element = ET.Element("c")
                for key, value in garage.items():
                    if key != "children":
                        car_element.set(key, str(value))
                    elif key == "children":
                        for child_dict in value:
                            part_element = ET.Element("p")
                            for k, v in child_dict.items():
                                part_element.set(k, str(v))
                            car_element.append(part_element)
                child_elements[7].append(car_element)  # append the car_element to id=getallcars
        elif attr_value is not None:
            child_elements[0].set(attr_name, str(attr_value))

    # append all parent and child nodes to root xml
    for child in child_elements:
        root.append(child)

    # serialize the XML element to a string for proper parsing in nitto
    xml_str = ET.tostring(root, encoding="unicode", method="xml")
    return Response(xml_str, mimetype='text/xml')


if __name__ == "__main__":
    app.run(debug=True)
