import os

from tqdm import tqdm

if __name__ == '__main__':
    jar1 = 'my.jar'
    jar2 = 'hw13.jar'
    check_name1 = 'output1.txt'
    check_name2 = 'output2.txt'
########################################################
    my_list = list(range(100))
    # 创建一个tqdm对象，传入迭代次数
    pbar = tqdm(total=len(my_list))
    # 在循环中迭代列表，并更新进度条
    for item in my_list:
        # 模拟一些耗时的操作
        dir_path = str(item)
        os.makedirs(dir_path, exist_ok=True)
        data_path = os.path.join(dir_path, 'data.txt')
        output1_path = os.path.join(dir_path, 'output1.txt')
        output2_path = os.path.join(dir_path, 'output2.txt')
        os.system(f'python data.py > {data_path}')
        os.system(f'java -jar {jar1} < {data_path} > {output1_path}')
        os.system(f'java -jar {jar2} < {data_path} > {output2_path}')
        os.system(f'python checker.py {data_path} {output1_path}')
        os.system(f'python checker.py {data_path} {output2_path}')
        # 更新进度条
        pbar.update(1)
    # 循环结束后，关闭进度条
    pbar.close()


