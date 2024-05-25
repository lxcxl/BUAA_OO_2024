import random
from datetime import date, timedelta


def initialBS():
    bookList = []
    bs = {}
    class_num = random.randint(1, 100)
    print(class_num)
    for i in range(class_num):
        list = ['A', 'B', 'C']
        book_class = list[random.randint(0, 2)]
        book_uid = random.randint(0, 9999)
        bookList.append(f'{book_class}-{book_uid:04d}')
        num = random.randint(1, 10)
        bs[f'{book_class}-{book_uid:04d}'] = num
        print(f'{book_class}-{book_uid:04d} {num}')
    return bookList, bs


def generatePerson():
    personList = []
    person_num = random.randint(1, 100)
    for i in range(person_num):
        personList.append(f'{2237}{random.randint(0, 9999):04d}')
    return personList


def generateOp(bookList, personList, bs):
    op_num = random.randint(1, 200)
    opList = ['borrowed', 'returned', 'queried', 'ordered', 'picked','CLOSE']
    beginDate = date.today()
    canReturn = {}
    canPick = {}
    haveBorrowed = {}
    my_date = beginDate
    flag = 0
    for i in range(op_num):
        if i == op_num - 1:
            print(f'[{my_date}] CLOSE')
            continue
        if flag == 0:
            dateaddList = [1,2,5,6,7]
            date_add = random.randint(0, 4)
            my_date = my_date + timedelta(days=dateaddList[date_add])
            print(f'[{my_date}] OPEN')
            flag = 1
            continue
        opIndex = random.randint(0, len(opList) - 1)
        bookIndex = random.randint(0, len(bookList) - 1)
        personIndex = random.randint(0, len(personList) - 1)
        if opList[opIndex] == 'CLOSE' and flag == 1 and i != op_num - 2:
            print(f'[{my_date}] CLOSE')
            flag = 0
            continue

        if opList[opIndex] == 'queried':
            print(f'[{my_date}] {personList[personIndex]} queried {bookList[bookIndex]}')
            continue
        if opList[opIndex] == 'borrowed':
            print(f'[{my_date}] {personList[personIndex]} borrowed {bookList[bookIndex]}')
            if bs[bookList[bookIndex]] > 0 and haveBorrowed.get(personList[personIndex]) == None and bookList[bookIndex][0] != 'A':
                bs[bookList[bookIndex]] -= 1
                haveBorrowed[personList[personIndex]] = bookList[bookIndex]
            continue
        if opList[opIndex] == 'returned':
            if haveBorrowed.get(personList[personIndex]) != None:
                print(f'[{my_date}] {personList[personIndex]} returned {haveBorrowed[personList[personIndex]]}')
                haveBorrowed.pop(personList[personIndex])
            continue
        if opList[opIndex] == 'ordered':
            print(f'[{my_date}] {personList[personIndex]} ordered {bookList[bookIndex]}')
            if bookList[bookIndex][0] == 'A':
                continue
            if haveBorrowed.get(personList[personIndex]) != None and haveBorrowed.get(personList[personIndex])[0] != bookList[bookIndex]:
                if haveBorrowed.get(personList[personIndex])[0] == 'B' and bookList[bookIndex][0] == 'B':
                    continue
                canPick[personList[personIndex]] = bookList[bookIndex]
            continue
        if opList[opIndex] == 'picked':
            if canPick.get(personList[personIndex]) != None:
                print(f'[{my_date}] {personList[personIndex]} picked {canPick[personList[personIndex]]}')
                canPick.pop(personList[personIndex])

def getBookList():
    return bookList

if __name__ == '__main__':
    bookList, bs = initialBS()
    personList = generatePerson()
    personNum = len(personList)
    generateOp(bookList, personList, bs)
