from master import Master


if __name__ == '__main__':
    master = Master()
    try:
        master.start()
    except KeyboardInterrupt as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        master.shutdown()