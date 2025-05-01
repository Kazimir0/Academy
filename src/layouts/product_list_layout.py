from dash import html, dcc
from products import fetch_products


product_list_layout = html.Div(
    className="container mt-4",
    children=[
        html.H2("Lista de Produse", className="mb-3"),
        html.Div(id="delete-list-message", className="alert mt-3", style={'display': 'none'}),
        html.Div(className="mb-3", children=[
            dcc.Input(id="search-input", type="text", className="form-control", placeholder="Căutați produse..."),
        ]),
        html.Div(
            id="product-list",
            className="row g-4",
            children=[
                html.Div(
                    className="col-12 col-sm-6 col-md-4 col-lg-3",  # Adjust column width for different screen sizes
                    children=[
                        html.Div(
                            className="card h-100 product-card",
                            children=[
                                html.Div(className="product-card-image-container",
                                         children=[
                                             html.Img(src=f"/static/uploads/{product['image_url']}", className="card-img-top", style={"maxHeight": "150px", "objectFit": "contain"})
                                         ]),
                                html.Div(
                                    className="card-body product-card-body",
                                    children=[
                                        html.H5(product['name'], className="card-title product-card-title"),
                                        html.P(f"Price: {product['price']} RON", className="card-text product-card-price"),
                                        dcc.Link(
                                            "Vezi detalii",
                                            href=f"/product/{product['id']}",
                                            className="btn btn-sm btn-outline-primary view-details-button"
                                        ),
                                    ]
                                )
                            ]
                        )
                    ]
                )
                for product in fetch_products()  # Dynamically generate product cards
            ]
        ),
        html.Div(className="d-flex justify-content-center mt-3", children=[
            html.Button("Prev", id="prev-button", className="btn btn-outline-primary me-2"),
            html.Div(id="page-number", className="align-self-center me-2"),
            html.Button("Next", id="next-button", className="btn btn-outline-primary"),
        ]),
    ]
)