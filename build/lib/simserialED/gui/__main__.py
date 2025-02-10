from simserialED.gui import app

def main():
    import webbrowser
    if webbrowser.open("http://127.0.0.1:5000"):
        app.run(load_dotenv=False)

if __name__ == "__main__":
    main()
