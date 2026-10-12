import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='agent.log',
    encoding='utf-8')
logger = logging.getLogger(__name__)
logger.info("程序启动")
from agent.core import run_agent


if __name__ == "__main__":
    run_agent()
