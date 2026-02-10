def run():
    # ... initialization code ...

    ws_thread = threading.Thread(target=ws_app.run_forever)
    ws_thread.daemon = True
    ws_thread.start()

    try:
        while ws_thread.is_alive():
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nCtrl+C received. Stopping...")
        stop_event.set()

        # Send termination message
        if ws_app and ws_app.sock and ws_app.sock.connected:
            try:
                terminate_message = {"type": "Terminate"}
                ws_app.send(json.dumps(terminate_message))
                time.sleep(5)  # Allow message processing
            except Exception as e:
                print(f"Error sending termination message: {e}")

        ws_app.close()
        ws_thread.join(timeout=2.0)
    finally:
        # Final cleanup
        # ... resource cleanup code ...
