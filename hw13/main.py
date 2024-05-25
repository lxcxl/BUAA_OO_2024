import os

if __name__ == '__main__':
    jar1 = 'my.jar'
    jar2 = 'hw13.jar'
    check_name1 = 'output1.txt'
    check_name2 = 'output2.txt'
########################################################
    os.system('python data.py > data.txt')
    os.system(f'java -jar {jar1} < data.txt > output1.txt')
    os.system(f'java -jar {jar2} < data.txt > output2.txt')
    os.system(f'python checker.py {check_name1}')
    os.system(f'python checker.py {check_name2}')
