import sys
from datetime import datetime, date, timedelta
import os


class Op:
    def __init__(self, op_name, bookId, personId):
        self.op_name = op_name
        self.bookId = bookId
        self.personId = personId

    def getOpName(self):
        return self.op_name

    def getBookId(self):
        return self.bookId

    def getPersonId(self):
        return self.personId


class Bs:
    def __init__(self):
        self.books = {}

    def addBook(self, bookId):
        if self.books.get(bookId) == None:
            self.books[bookId] = 1
        else:
            self.books[bookId] += 1

    def addBooks(self, bookId, num):
        if self.books.get(bookId) == None:
            self.books[bookId] = num
        else:
            self.books[bookId] += num

    def subBook(self, bookId):
        self.books[bookId] -= 1
        if self.books[bookId] == 0:
            self.books.pop(bookId)

    def getNum(self, bookId):
        return self.books[bookId]

    def contain(self, bookId):
        return self.books.__contains__(bookId)


class Bro:
    def __init__(self):
        self.books = {}
        pass

    def addBook(self, bookId):
        if self.books.get(bookId) == None:
            self.books[bookId] = 1
        else:
            self.books[bookId] += 1

    def addBooks(self, bookId, num):
        if self.books.get(bookId) == None:
            self.books[bookId] = num
        else:
            self.books[bookId] += num

    def subBook(self, bookId):
        self.books[bookId] -= 1
        if self.books[bookId] == 0:
            self.books.pop(bookId)

    def getNum(self, bookId):
        return self.books[bookId]


class Appointment:
    def __init__(self, bookId, personId, date_begin):
        self.bookId = bookId
        self.personId = personId
        self.date_begin = date_begin

    def getBookId(self):
        return self.bookId

    def getPersonId(self):
        return self.personId

    def getDateBegin(self):
        return self.date_begin


class Ao:
    def __init__(self):
        self.books = {}
        self.appointments = {}
        pass

    def addBook(self, bookId):
        if self.books.get(bookId) == None:
            self.books[bookId] = 1
        else:
            self.books[bookId] += 1

    def addBooks(self, bookId, num):
        if self.books.get(bookId) == None:
            self.books[bookId] = num
        else:
            self.books[bookId] += num

    def subBook(self, bookId):
        self.books[bookId] -= 1
        if self.books[bookId] == 0:
            self.books.pop(bookId)

    def getNum(self, bookId):
        return self.books[bookId]

    def addAppointment(self, appointment):
        if self.appointments.get(appointment.getPersonId()) == None:
            p2a = []
            p2a.append(appointment)
            self.appointments[appointment.getPersonId()] = p2a
        else:
            self.appointments[appointment.getPersonId()].append(appointment)

    def subAppointment(self, appointment):
        self.appointments[appointment.getPersonId()].remove(appointment)
        if len(self.appointments[appointment.getPersonId()]) == 0:
            self.appointments.pop(appointment.getPersonId())

    def canPick(self, personId, bookId, my_date):
        flag = -1
        if self.appointments.get(personId) == None:
            return False
        for appointment in self.appointments[personId]:
            if appointment.getBookId() == bookId:
                flag = self.appointments[personId].index(appointment)
        if flag == -1:
            return False
        appointment = self.appointments[personId][flag]
        if appointment.getDateBegin() + timedelta(days=4) < my_date:
            return False
        self.appointments[personId].remove(appointment)
        if len(self.appointments[personId]) == 0:
            self.appointments.pop(personId)
        return True

    def contain(self, bookId):
        return self.books.__contains__(bookId)


class Person:
    def __init__(self, personId):
        self.personId = personId
        self.Bbooks = {}
        self.Cbooks = {}

    def addBook(self, bookId):
        if bookId[0] == 'B':
            if self.Bbooks.get(bookId) == None:
                self.Bbooks[bookId] = 1
            else:
                self.Bbooks[bookId] += 1
        else:
            if self.Cbooks.get(bookId) == None:
                self.Cbooks[bookId] = 1
            else:
                self.Cbooks[bookId] += 1

    def getPersonId(self):
        return self.personId

    def subBook(self, bookId):
        if bookId[0] == 'B':
            self.Bbooks[bookId] -= 1
            if self.Bbooks[bookId] == 0:
                self.Bbooks.pop(bookId)
        else:
            self.Cbooks[bookId] -= 1
            if self.Cbooks[bookId] == 0:
                self.Cbooks.pop(bookId)

    def isContainB(self):
        return len(self.Bbooks) > 0

    def containC(self, bookId):
        return self.Cbooks.__contains__(bookId)


def processOpen(outList, j, bs, bro, ao):
    assert outList[j].split()[0].isdigit()
    n = int(outList[j])
    for k in range(n):
        j += 1
        line = outList[j]
        line_blocks = line.split()
        bookId = line_blocks[2]
        from_place = line_blocks[4]
        to_place = line_blocks[6]
        my_date = datetime.strptime(line_blocks[0], '[%Y-%m-%d]').date()
        assert not bookId.__contains__('A')
        if from_place == 'bs':
            assert bs.contain(bookId)
            bs.subBook(bookId)
        elif from_place == 'bro':
            assert bro.contain(bookId)
            bro.subBook(bookId)
        else:
            assert ao.contain(bookId)
            ao.subBook(bookId)

        if to_place == 'bs':
            bs.addBook(bookId)
        elif to_place == 'bro':
            bro.addBook(bookId)
        else:
            ao.addBook(bookId)
            assert len(line_blocks) == 9
            ao.addAppointment(Appointment(bookId, line_blocks[8], my_date))
    return j + 1


def processClose(outList, j, bs, bro, ao):
    assert outList[j].split()[0].isdigit()
    n = int(outList[j])
    for k in range(n):
        j += 1
        line = outList[j]
        line_blocks = line.split()
        bookId = line_blocks[2]
        from_place = line_blocks[4]
        to_place = line_blocks[6]
        my_date = datetime.strptime(line_blocks[0], '[%Y-%m-%d]').date()
        assert not bookId.__contains__('A')
        if from_place == 'bs':
            assert bs.contain(bookId)
            bs.subBook(bookId)
        elif from_place == 'bro':
            assert bro.contain(bookId)
            bro.subBook(bookId)
        else:
            assert ao.contain(bookId)
            ao.subBook(bookId)

        if to_place == 'bs':
            bs.addBook(bookId)
        elif to_place == 'bro':
            bro.addBook(bookId)
        else:
            ao.addBook(bookId)
            assert len(line_blocks) == 9
            ao.addAppointment(Appointment(bookId, line_blocks[8], my_date + timedelta(days=1)))
    return j + 1


def processQueried(outList, j, bs, bro, ao):
    assert len(outList[j].split()) == 3
    line_blocks = outList[j].split()
    assert bs.getNum(line_blocks[1]) == int(line_blocks[2])


def processBorrowed(outList, j, bs, bro, ao, persons):
    line_blocks = outList[j].split()
    result = ['[accept]', '[reject]']
    assert len(line_blocks) == 5
    bookId = line_blocks[4]
    personId = line_blocks[2]
    if persons.get(personId) == None:
        persons[personId] = Person(personId)
    if bs.getNum(bookId) == 0:
        assert result[1] == line_blocks[1]
        return
    if bookId[0] == 'A':
        assert result[1] == line_blocks[1]
        return
    person = persons[personId]
    if person.isContainB() and bookId[0] == 'B':
        assert result[1] == line_blocks[1]
        return
    if bookId[0] == 'C' and person.containC(bookId):
        assert result[1] == line_blocks[1]
        return
    person.addBook(bookId)
    bs.subBook(bookId)
    assert result[0] == line_blocks[1]


def processReturned(outList, j, bs, bro, ao, persons):
    line_blocks = outList[j].split()
    result = ['[accept]', '[reject]']
    assert len(line_blocks) == 5
    bookId = line_blocks[4]
    personId = line_blocks[2]
    if persons.get(personId) == None:
        persons[personId] = Person(personId)
    if bookId[0] == 'A':
        assert result[1] == line_blocks[1]
        return
    person = persons[personId]
    person.subBook(bookId)
    bro.addBook(bookId)
    assert result[0] == line_blocks[1]


def processOrdered(outList, j, bs, bro, ao, persons):
    line_blocks = outList[j].split()
    result = ['[accept]', '[reject]']
    assert len(line_blocks) == 5
    bookId = line_blocks[4]
    personId = line_blocks[2]
    if persons.get(personId) == None:
        persons[personId] = Person(personId)
    if bookId[0] == 'A':
        assert result[1] == line_blocks[1]
        return
    person = persons[personId]
    if person.isContainB() and bookId[0] == 'B':
        assert result[1] == line_blocks[1]
        return
    if bookId[0] == 'C' and person.containC(bookId):
        assert result[1] == line_blocks[1]
        return
    assert result[0] == line_blocks[1]


def processPicked(outList, j, bs, bro, ao, persons):
    line_blocks = outList[j].split()
    result = ['[accept]', '[reject]']
    assert len(line_blocks) == 5
    bookId = line_blocks[4]
    personId = line_blocks[2]
    if persons.get(personId) == None:
        persons[personId] = Person(personId)
    assert ao.getNum(bookId) > 0
    if bookId[0] == 'A':
        assert result[1] == line_blocks[1]
        return
    person = persons[personId]
    if person.isContainB() and bookId[0] == 'B':
        assert result[1] == line_blocks[1]
        return
    if bookId[0] == 'C' and person.containC(bookId):
        assert result[1] == line_blocks[1]
        return
    my_date = datetime.strptime(line_blocks[0], '[%Y-%m-%d]').date()
    if ao.canPick(personId, bookId, my_date) == True:
        assert result[0] == line_blocks[1]
        person.addBook(bookId)
        ao.subBook(bookId)
        return
    assert result[1] == line_blocks[1]


def check(outList, bs, bro, ao, opList):
    j = 0
    persons = {}
    for i in range(len(opList)):
        person = persons.get('22377982')
        op = opList[i]
        if op.getOpName() == 'OPEN':
            j = processOpen(outList, j, bs, bro, ao)
        elif op.getOpName() == 'CLOSE':
            j = processClose(outList, j, bs, bro, ao)
        elif op.getOpName() == 'queried':
            processQueried(outList, j, bs, bro, ao)
            j += 1
        elif op.getOpName() == 'borrowed':
            processBorrowed(outList, j, bs, bro, ao, persons)
            j += 1
        elif op.getOpName() == 'returned':
            processReturned(outList, j, bs, bro, ao, persons)
            j += 1
        elif op.getOpName() == 'ordered':
            processOrdered(outList, j, bs, bro, ao, persons)
            j += 1
        elif op.getOpName() == 'picked':
            processPicked(outList, j, bs, bro, ao, persons)
            j += 1


def getSome(data_list):
    bs = Bs()
    opList = []
    flag = 0
    n = 0
    for i in range(len(data_list)):
        line = data_list[i]
        if i == 0:
            n = int(line)
            continue
        if flag == 0:
            bs.addBooks(line.split()[0], int(line.split()[1]))
            n -= 1
            if n == 0:
                flag = 1
            continue
        if flag == 1:
            if line.split()[1] == 'CLOSE' or line.split()[1] == 'OPEN':
                op = Op(line.split()[1], '', '')
                opList.append(op)
            else:
                op = Op(line.split()[2], line.split()[3], line.split()[1])
                opList.append(op)
    return bs, opList


if __name__ == '__main__':
    data_name = 'data.txt'
    file_name = sys.argv[1]
    #################################################################

    data_list = open(data_name, 'r').readlines()
    bs, opList = getSome(data_list)
    # orderList = {}
    # personOwned = {}
    file = open(file_name, 'r')
    outList = file.readlines()
    bro = Bro()
    ao = Ao()
    check(outList, bs, bro, ao, opList)
