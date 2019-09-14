import subprocess
import tempfile
from utils import get_logger   #, logging

# mod_name = os.path.split(__file__)[1]
# prefix_mod_name = os.path.splitext(mod_name)[0]
#
# logger = get_logger(prefix_mod_name)
logger = get_logger(__name__, 'agent.log')


# agent 执行器
class Executor:
    def __init__(self):
        logger.info('info test')
        logger.error('error test')

    def run(self, scripts:str, timeout=2):
        with tempfile.TemporaryFile() as f: # 自动生成临时文件
            # linux 中fork 一个子进程执行脚本内容
            proc = subprocess.Popen(scripts, shell=True, stderr=f, stdout=f)

            try:
                code = proc.wait(timeout) # 执行等待超时， 返回执行结果状态码

                f.seek(0) # 信息追加到文件中，需要把指针移动到开始，下面才可以看到结果
                if code == 0:
                    text = f.read()
                else:
                    text = f.read()
                logger.info('{}-{}'.format(code, text))
                return code, text
            except Exception as e:
                logger.error(e)
                return 1, '错误'

if __name__ == '__main__':
    ex = Executor()
    # ex.run('dir')
    print(ex.run('pause'))