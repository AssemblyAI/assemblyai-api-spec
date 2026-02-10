params_w_token = {**CONNECTION_PARAMS, "token": token}
ws_app = websocket.WebSocketApp(
    f'{API_ENDPOINT_BASE_URL}?{urlencode(params_w_token)}',
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close,
)
