from calendar_module import fetch_events

def test_fetch():
    events = fetch_events()
    print("Fetched events:", events)

if __name__ == "__main__":
    test_fetch()