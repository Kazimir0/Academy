from dash import html

home_layout = html.Div(
    className="container mt-5 text-center",
    children=[
        html.H1("ElectroShop", className="mb-4"),
        html.P(
            "Bine ați venit la ElectroShop, destinația dumneavoastră online pentru cele mai noi și inovatoare gadgeturi și tehnologie! "
            "Descoperiți o gamă variată de telefoane inteligente, ceasuri smart performante, căști audio de înaltă calitate și multe altele. "
            "Ne angajăm să vă oferim produse de top la prețuri competitive, alături de o experiență de cumpărare simplă și plăcută.",
            className="lead mb-4",
        ),
        html.P(
            "Explorați categoriile noastre de produse sau vedeți direct lista completă pentru a găsi exact ceea ce căutați.",
            className="mb-4",
        ),
    ]
)