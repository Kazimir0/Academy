from dash import html, dcc

product_details_layout = html.Div(
    className="container mt-5",
    id="product-details-container",
    style={"display": "none"},  # Initially hidden
    children=[
        html.Div(
            id="product-details",
            children=[
                html.H3(id="product-name", className="text-primary"),
                html.Img(id="product-image", className="img-fluid"),
                html.P(id="product-description", className="mt-3"),
                html.P(id="product-price", className="text-success fw-bold"),
            ]
        ),
        html.Div(
            id="edit-delete-buttons",
            className="d-flex gap-2 mt-3",
            style={"display": "none"},
            children=[
                html.Button(
                    "Editează Produs",
                    id="edit-product-button",
                    className="btn btn-warning"
                ),
                html.Button(
                    "Șterge Produs",
                    id="delete-product-button",
                    className="btn btn-danger"
                ),
                html.Button(
                    "Adaugă în Coș",
                    id="add-to-cart-button",
                    className="btn btn-primary"
                ),
            ]
        ),
        html.H3("Comentarii", className="mt-5 text-primary"),
        html.Div(id="comments-section", className="mt-3"),
        html.Div(
            className="mt-4",
            children=[
                html.H4("Adaugă un comentariu", className="text-secondary"),
                dcc.Textarea(
                    id="comment-input",
                    className="form-control",
                    placeholder="Scrie un comentariu...",
                    style={"height": "100px"}
                ),
                dcc.Dropdown(
                    id="stars-rating",
                    options=[{"label": f"{i} stele", "value": i} for i in range(1, 6)],
                    placeholder="Alege numărul de stele",
                    className="mt-2"
                ),
                html.Button(
                    "Trimite",
                    id="submit-comment-button",
                    className="btn btn-primary mt-2"
                ),
                html.Div(id="comment-feedback", className="mt-2"),
            ]
        ),
    ]
)