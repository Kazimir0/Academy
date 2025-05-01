from dash import html, dcc

navbar = html.Nav(
    className="navbar navbar-expand-lg navbar-light bg-light",
    children=[
        html.Div(
            className="container",
            children=[
                dcc.Link(
                    html.Span("ElectroShop", className="navbar-brand"),
                    href="/",
                ),
                html.Div(
                    className="collapse navbar-collapse",
                    id="navbarNav",
                    children=[
                        html.Ul(
                            className="navbar-nav",
                            children=[
                                html.Li(
                                    className="nav-item",
                                    children=dcc.Link(
                                        "Home",
                                        href="/",
                                        className="nav-link"
                                    )
                                ),
                                html.Li(
                                    className="nav-item",
                                    children=dcc.Link(
                                        "Adaugă Produs",
                                        href="/add-product",
                                        className="nav-link"
                                    )
                                ),
                                html.Li(
                                    className="nav-item",
                                    children=dcc.Link(
                                        "Vezi Produsele",
                                        href="/products",
                                        className="nav-link"
                                    )
                                ),
                                html.Li(
                                    className="nav-item position-relative",
                                    children=[
                                        dcc.Link(
                                            "Coșul Meu",
                                            href="/cart",
                                            className="nav-link"
                                        ),
                                        html.Span(
                                            id="cart-badge",
                                            className="badge bg-success position-absolute top-0 start-100 translate-middle",
                                            style={"display": "none"}
                                        )
                                    ]
                                ),
                                html.Li(
                                    className="nav-item",
                                    children=dcc.Link(
                                        "Comenzile Mele",
                                        href="/orders",
                                        className="nav-link"
                                    )
                                ),
                            ]
                        )
                    ]
                ),
            ]
        )
    ]
)