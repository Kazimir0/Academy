from dash import html, dcc

edit_product_layout = html.Div(
    id="edit-product-page",
    className="container mt-5",
    children=[
        html.H1("Editează Produs", className="text-center mb-4"),
        dcc.Store(id="edit-product-id"),  # Store to hold the product ID
        html.Div(id="edit-error-message", className="alert alert-danger mb-3", style={"display": "none"}),
        html.Div(className="mb-3", children=[
            html.Label("Nume Produs", className="form-label"),
            dcc.Input(id="edit-product-name", type="text", className="form-control", placeholder="Introduceți numele produsului"),
            html.Div(id="edit-error-name", className="invalid-feedback"),
        ]),
        html.Div(className="mb-3", children=[
            html.Label("Preț Produs", className="form-label"),
            dcc.Input(id="edit-product-price", type="number", className="form-control", placeholder="Introduceți prețul produsului"),
            html.Div(id="edit-error-price", className="invalid-feedback"),
        ]),
        html.Div(className="mb-3", children=[
            html.Label("Descriere", className="form-label"),
            dcc.Textarea(id="edit-product-description", className="form-control", placeholder="Introduceți descrierea produsului"),
            html.Div(id="edit-error-description", className="invalid-feedback"),
        ]),
        html.Div(className="mb-3", children=[
            html.Label("Încarcă Imagine", className="form-label"),
            dcc.Upload(
                id="edit-upload-image",
                children=html.Div(["Trageți și fixați sau selectați un fișier"]),
                className="upload-box",
                multiple=False,
            ),
            html.Div(id="edit-error-image", className="invalid-feedback"),
            html.Div(id="edit-output-image-upload"),
        ]),
        html.Div(className="d-grid gap-2 d-md-flex justify-content-md-end", children=[
            html.Button("Salvează Modificările", id="save-edit-button", className="btn btn-success btn-lg"),
            html.Button("Anulează", id="cancel-edit-button", className="btn btn-secondary btn-lg ms-2"),
        ]),
        html.Div(id="edit-success-message", className="mt-3", style={"display": "none"}),
    ]
)