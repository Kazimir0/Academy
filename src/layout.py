from dash import html, dcc
from layouts.navbar import navbar

app_layout = html.Div(
    children=[
        dcc.Location(id="url", refresh=False),
        navbar,
        html.Div(id="page-content", className="container mt-4"),
        html.Div(id="edit-product-page-container", style={'display': 'none'}),

        html.Div(id="hidden-components", style={"display": "none"}, children=[
            # Stores
            dcc.Store(id="edit-product-data"),
            dcc.Store(id="current-product-data"),
            dcc.Store(id="delete-list-message-store"),
            dcc.Store(id="selected-product-id"),
            dcc.Store(id="current-page", data=1),
            dcc.Store(id="cart-items-store", storage_type="local"),
            html.Div(id="cart-feedback"),

            # INPUTURI - Add product
            dcc.Input(id="search-input"),
            dcc.Input(id="product-name"),
            dcc.Input(id="product-price"),
            dcc.Textarea(id="product-description"),
            dcc.Upload(id="upload-image"),
            html.Button(id="add-product-button"),

            # OUTPUTURI - Add product
            html.Div(id="add-product-message"),
            html.Div(id="error-message"),
            html.Div(id="error-name"),
            html.Div(id="error-price"),
            html.Div(id="error-description"),
            html.Div(id="error-image"),
            html.Div(id="output-image-upload"),

            # INPUTURI - Edit product
            dcc.Input(id="edit-product-name"),
            dcc.Input(id="edit-product-price"),
            dcc.Textarea(id="edit-product-description"),
            dcc.Upload(id="edit-upload-image"),
            html.Button(id="save-edit-button"),
            html.Button(id="cancel-edit-button"),

            # OUTPUTURI - Edit product
            html.Div(id="edit-error-message"),
            html.Div(id="edit-error-name"),
            html.Div(id="edit-error-price"),
            html.Div(id="edit-error-description"),
            html.Div(id="edit-error-image"),
            html.Div(id="edit-output-image-upload"),
            html.Div(id="edit-success-message"),

            # Global buttons
            html.Button(id="delete-product-button"),
            html.Button(id="add-to-cart-button"),
            html.Button(id="finalize-order-button", style={"display": "none"}),

            dcc.ConfirmDialog(id="confirm-delete", message="", displayed=False),
            html.Div(id="product-details"),
            html.Div(id="product-details-container"),
            html.Div(id="edit-delete-buttons"),
            html.Div(id="delete-product-message"),
            html.Div(id="product-list"),
            html.Div(id="page-number"),
            html.Div(id="delete-list-message"),

            # Pagination buttons
            html.Button(id="prev-button"),
            html.Button(id="next-button"),
            html.Button(id="edit-product-button", style={"display": "none"}),
        ]),
        dcc.ConfirmDialog(id="delete-confirm-dialog"),
    ]
)