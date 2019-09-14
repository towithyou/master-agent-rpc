from agent import Agent


if __name__ == '__main__':
    agent = Agent()
    try:
        agent.start()
    except KeyboardInterrupt as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        agent.shutdown()