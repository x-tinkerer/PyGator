import streamline


if __name__ == "__main__":
    sl = streamline.Streamline()
    # 1. Prepare
    sl.prepare()
    # 2. Connect
    sl.connect()
    # 3. Config
    sl.config()
    # 4. Start
    print 'Start Capture'
    sl.start_record()

    ################################################
    #                 Main Loop
    ################################################
    sl.main_loop()

    # 5. Stop
    print 'Stop Capture'
    sl.start_record()

