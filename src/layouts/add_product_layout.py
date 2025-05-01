from dash import html, dcc

product_add_layout = html.Div(
    className="container mt-5",
    children=[
        html.H1("Adaugă un Produs", className="text-center mb-4"),
        html.Div(id="error-message", className="alert alert-danger mb-3", style={"display": "none"}),
        html.Div(className="mb-3", children=[
            html.Label("Nume Produs", className="form-label"),
            dcc.Input(id="product-name", type="text", className="form-control", placeholder="Introduceți numele produsului"),
            html.Div(id="error-name", className="invalid-feedback"),
        ]),
        html.Div(className="mb-3", children=[
            html.Label("Preț Produs", className="form-label"),
            dcc.Input(id="product-price", type="number", className="form-control", placeholder="Introduceți prețul produsului"),
            html.Div(id="error-price", className="invalid-feedback"),
        ]),
        html.Div(className="mb-3", children=[
            html.Label("Descriere", className="form-label"),
            dcc.Textarea(id="product-description", className="form-control", placeholder="Introduceți descrierea produsului"),
            html.Div(id="error-description", className="invalid-feedback"),
        ]),
        html.Div(className="mb-3", children=[
            html.Label("Încarcă Imagine", className="form-label"),
            dcc.Upload(
                id="upload-image",
                children=html.Div(["Trageți și fixați sau selectați un fișier"]),
                className="upload-box",
                multiple=False,
            ),
            html.Div(id="error-image", className="invalid-feedback"),
            html.Div(id="output-image-upload"),
        ]),
        html.Div(className="d-grid gap-2 d-md-flex justify-content-md-end", children=[
            html.Button("Adaugă Produs", id="add-product-button", className="btn btn-success btn-lg"),
            html.A("Vezi Lista de Produse", href="/products", className="btn btn-secondary btn-lg ms-2"),
        ]),
        html.Div(id="add-product-message", className="mt-3"),
    ]
)