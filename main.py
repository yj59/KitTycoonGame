
# from _typeshed import NoneType
import sys
import csv
import platform
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import (QByteArray, QCoreApplication, QPropertyAnimation, QDate, QDateTime,
                          QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent, pyqtSignal, pyqtSlot, QThread)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase,
                         QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient, QMovie)
from PyQt5.QtWidgets import *
from queue import Queue
from PyQt5.QtCore import QTimer
# GUI FILE

from ui_main import Ui_MainWindow
import random
import threading


# class Thread1(threading.Thread):
#     def run(self) -> None

class Worker(QThread):
    timer = pyqtSignal()
    guestIn = pyqtSignal()
    guestOut = pyqtSignal()
    eventType = pyqtSignal()

    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)
        self.working = True
        self.count = 0
        self.t0 = 0
        self.guestIn.emit()

    def run(self):
        while self.working:
            self.sleep(1)
            self.count += 1
            self.timer.emit()
            if self.count % 20 == 0:
                if (self.count % 60 == 0) and (self.t0 == 1):
                    None
                else:
                    if(self.t0 == 0):
                        self.guestIn.emit()
                        self.t0 = 1
            if self.count % 30 == 0:
                if(self.count % 60 == 0) and (self.t0 == 1):
                    self.guestOut.emit()
                    self.t0 = 0
                else:
                    if(self.t0 == 1):
                        self.guestOut.emit()
                        self.t0 = 0
            if self.count % 10 == 0:
                self.eventType.emit()
                self.event = 0


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SLG : 붕어빵 장사 타이쿤")
        self.setupUi()

    def setupUi(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # QMainWindow.__init__(self)

        self.gameStart = int(time.time())
        self.red_count = 0
        self.chou_count = 0
        self.hour_count = 0
        self.min_count = 0
        self.sec_count = 0
        self.index = 0
        self.ranRedbean = 0
        self.ranChou = 0
        self.init = 0
        self.bun_cal = 0
        self.Tsell = 0
        self.picture = 0
        # 시간 관련
        # self.t0 = 0
        # 손님 대기 관련 변수
        self.guestQueue = [-1]
        self.guestTimeLine = [-1]
        self.guestNum = 1

        # 기타 설정값
        self.reputation = 50

        # 가게 확장
        self.levelCount = 1
        self.storeLoad = 'image:url(./img/level1.png); border:0px;'
        # 화면 설정
        self.ui.stackedWidget.setCurrentWidget(self.ui.startWindow)

        self.ui.start.setStyleSheet(
            'image:url(./img/gamebtn_start.png); border:0px;')
        self.ui.continue_2.setStyleSheet(
            'image:url(./img/gamebtn_con.png); border:0px;')
        self.ui.how.setStyleSheet(
            'image:url(./img/gamebtn_how.png); border:0px;')
        self.ui.next1.setStyleSheet(
            'image:url(./img/gamebtn_next.png); border:0px;')
        self.ui.returnbtn3.setStyleSheet(
            'image:url(./img/gamebtn_start.png); border:0px;')

        self.ui.progressBar.setValue(self.reputation)

        self.ui.action_open.triggered.connect(self.openFunction)
        self.ui.action_save.triggered.connect(self.saveFunction)
        self.ui.continue_2.clicked.connect(self.openFunction)
        self.ui.continue_2.clicked.connect(self.thread_start)

        self.ui.start.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.mainWindow))
        self.ui.start.clicked.connect(self.thread_start)
        # 게임 시작 버튼 클릭과 동시에 스레드

        self.ui.pushButton_2.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.upgrade))
        self.ui.pushButton_2.clicked.connect(lambda: self.ui.lack.setText(" "))
        self.ui.returnbtn1.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.mainWindow))
        self.ui.how.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.howTo))

        self.ui.next1.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.howTo2))

        self.ui.returnbtn3.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.mainWindow))
        self.ui.returnbtn3.clicked.connect(self.thread_start)

        self.ui.seestore.setStyleSheet(self.storeLoad)

        self.ui.flour.setStyleSheet(
            'image:url(./img/flour.png); border:0px;')
        self.ui.redbean.setStyleSheet(
            'image:url(./img/redbean.png); border:0px;')
        self.ui.chou.setStyleSheet(
            'image:url(./img/chou.png); border:0px;')
        self.ui.S_redbeanCount.valueChanged.connect(self.spinBoxChanged)
        self.ui.S_chouCount.valueChanged.connect(self.spinBoxChanged)
        self.ui.flour.setDisabled(True)
        self.ui.redbean.setDisabled(True)
        self.ui.chou.setDisabled(True)

        self.click = [-1, 0, 0, 0, 0, 0, 0]
        self.x = [-1, 0, 0, 0, 0, 0, 0]
        self.bunSort = [-1, self.ui.bunLevel, self.ui.bunLevel_2, self.ui.bunLevel_3,
                        self.ui.bunLevel_4, self.ui.bunLevel_5, self.ui.bunLevel_6]
        for i in range(1, 7):
            self.bunSort[i].setStyleSheet(
                'image:url(./img/bun0.png); border:0px;')

        self.bunSort[1].clicked.connect(lambda: self.bun_finished(1))
        self.bunSort[2].clicked.connect(lambda: self.bun_finished(2))
        self.bunSort[3].clicked.connect(lambda: self.bun_finished(3))
        self.bunSort[4].clicked.connect(lambda: self.bun_finished(4))
        self.bunSort[5].clicked.connect(lambda: self.bun_finished(5))
        self.bunSort[6].clicked.connect(lambda: self.bun_finished(6))

        self.ui.redbean.clicked.connect(lambda: self.redbean(self.index))
        self.ui.chou.clicked.connect(lambda: self.chou(self.index))
        self.ui.flour.clicked.connect(lambda: self.flour(self.index))
        self.ui.sellbtn.clicked.connect(self.guestPop_sale)

        self.th = Worker()
        self.th.timer.connect(self.totaltime)
        self.th.guestIn.connect(self.guestIn)
        self.th.guestOut.connect(self.guestOut)
        self.th.eventType.connect(self.eventType)
        self.ui.upbtn1.clicked.connect(lambda: self.storeUpgrade(1))
        self.ui.upbtn2.clicked.connect(lambda: self.storeUpgrade(2))
        self.ui.upbtn3.clicked.connect(lambda: self.storeUpgrade(3))

        self.snowEffect()
        self.show()

    # pyuic5 -x 변환할 파일(.ui) -o 변환되었을때 파일명(.py)

    @pyqtSlot()
    def thread_start(self):
        self.th.start()
        self.th.working = True

    @pyqtSlot()
    def thread_stop(self):
        self.th.working = False

    @pyqtSlot()
    def totaltime(self):
        self.sec_count += 1
        self.ui.second.setText(str(self.sec_count) + "초")

        if self.sec_count == 59:
            self.sec_count = 0
            self.min_count += 1
            self.ui.minute.setText(str(self.min_count) + "분")

            if self.min_count == 59:
                self.min_count = 0
                self.hour_count += 1
                self.ui.hour.setText(str(self.hour_count) + "시간")

    @pyqtSlot()
    def guestOut(self):
        if(len(self.guestTimeLine) >= 2):
            self.guestQueue.pop(1)
            self.guestTimeLine.pop(1)
            self.GuestNum()
            self.reputation -= 2
            self.ui.waitLine.setStyleSheet(
                'image:none; border:0px;')
            self.picture = 0
            self.ui.G_redBeanCount.setText(str(self.init) + "개")
            self.ui.G_chouCount.setText(str(self.init) + "개")
            self.ui.S_redbeanCount.setValue(int(self.init))
            self.ui.S_chouCount.setValue(int(self.init))
            self.ui.progressBar.setValue(int(self.reputation))

        self.EndGame2()

    @pyqtSlot()
    def guestIn(self):
        self.guestQueue.append(self.guestNum)
        self.guestTimeLine.append(self.gameStart)
        self.guestOrder()
        self.guestNum += 1
        self.GuestNum()
        self.GuestPicture()
        # 이벤트 함수 구현

    @pyqtSlot()
    def eventType(self):
        noc = [0, 1, 2, 3]
        self.event = random.choices(noc, weights=(8, 2, 2, 1), k=4)[0]

        if(self.red_count > 0 and self.chou_count > 0 and self.Tsell > 0 and self.levelCount > 1):
            if self.event == 0:
                None

            elif self.event == 1:
                event_1 = QMessageBox()
                event_1.setText("자리를 비운 사이 붕어빵이 사라졌습니다.\n( 이전 붕어빵 개수 )\n팥 붕어빵 : "
                                + str(self.red_count) + " 개\n슈크림 붕어빵 : " + str(self.chou_count) + " 개")
                event_1.setWindowTitle("Event")

                self.red_count = 0
                self.chou_count = 0

                event_1.addButton('확인', QMessageBox.YesRole)
                event_1.exec_()

            elif self.event == 2:
                event_2 = QMessageBox()
                event_2.setText("한 눈을 판 사이 현찰을 모두 도둑맞았습니다.\n" +
                                "(이전 매출 현황 : " + str(self.Tsell) + " )")
                event_2.setWindowTitle("Event")
                event_2.addButton('확인', QMessageBox.YesRole)

                self.Tsell = 0

                event_2.exec_()

            elif self.event == 3:
                event_3 = QMessageBox()
                event_3.setText("바람이 심하게 불어 건물이 무너졌습니다.\n가게가 레벨이 초기화됩니다.\n(이전 가게 레벨 : "
                                + str(self.levelCount) + "Lv )")
                event_3.setWindowTitle("Event")
                event_3.addButton('확인', QMessageBox.YesRole)

                self.levelCount = 1
                self.storeLoad = 'image:url(./img/level1.png); border:0px;'

                event_3.exec_()

            self.uiLoad()

    def guestPop_sale(self):
        if(len(self.guestTimeLine) >= 2):
            redSale = self.ranRedbean
            chouSale = self.ranChou
            if(self.ui.S_redbeanCount.value() == redSale) and (self.ui.S_chouCount.value() == chouSale):
                if (self.red_count < redSale) or (self.chou_count < chouSale):
                    self.guestQueue.pop(1)
                    self.guestTimeLine.pop(1)
                    self.GuestNum()
                    self.reputation -= 2
                    self.ui.waitLine.setStyleSheet('image:none; border:0px;')
                    self.picture = 0
                    self.th.t0 = 0

                    self.ui.G_redBeanCount.setText(str(self.init) + "개")
                    self.ui.G_chouCount.setText(str(self.init) + "개")
                    self.ui.progressBar.setValue(int(self.reputation))
                    self.ui.S_redbeanCount.setValue(int(self.init))
                    self.ui.S_chouCount.setValue(int(self.init))

                    self.EndGame2()
                else:  # <붕어빵 판매완료>
                    self.ui.waitLine.setStyleSheet('image:none; border:0px;')
                    self.picture = 0
                    self.guestQueue.pop(1)
                    self.guestTimeLine.pop(1)
                    self.GuestNum()
                    self.th.t0 = 0

                    # 각 gui 초기화
                    self.red_count = self.red_count - self.ranRedbean
                    self.chou_count = self.chou_count - self.ranChou

                    self.ui.G_redBeanCount.setText(str(self.init) + "개")
                    self.ui.G_chouCount.setText(str(self.init) + "개")
                    self.ui.redbeanCount.setText(str(self.red_count)+"개")
                    self.ui.chouCount.setText(str(self.chou_count)+"개")

                    # 총 매출
                    self.Tsell += self.bun_cal
                    self.ui.profit2.setText(str(self.Tsell) + " GOLD")
                    self.ui.upgoldNum.setText(str(self.Tsell))
                    self.ui.S_redbeanCount.setValue(int(self.init))
                    self.ui.S_chouCount.setValue(int(self.init))
                    self.reputation += 1

                    # 메시지 출력
                    self.EndGame2()
                    self.ui.progressBar.setValue(int(self.reputation))

            elif(self.ui.S_redbeanCount.value() != redSale) or (self.ui.S_chouCount.value() != chouSale):

                self.GuestPicture()
                self.guestQueue.pop(1)
                self.guestTimeLine.pop(1)
                self.GuestNum()
                # 붕어빵 개수는 입력한 만큼 차감하되, 판매수익은 상승x
                self.reputation -= 2
                self.ui.G_redBeanCount.setText(str(self.init) + "개")
                self.ui.G_chouCount.setText(str(self.init) + "개")
                self.ui.progressBar.setValue(int(self.reputation))
                self.ui.S_redbeanCount.setValue(int(self.init))
                self.ui.S_chouCount.setValue(int(self.init))
                self.th.t0 = 0

                self.EndGame2()

            self.ui.profit.setText("0 GOLD")

    def guestOrder(self):
        order_num = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.ranRedbean = random.choices(
            order_num, weights=(5, 6, 5, 3, 2, 1, 1, 1, 1, 1, 1), k=11)[0]
        self.ranChou = random.choices(order_num, weights=(
            5, 6, 5, 3, 2, 1, 1, 1, 1, 1, 1), k=11)[0]

        if self.ranRedbean == 0 and self.ranChou == 0:
            self.guestOrder
        elif self.ranRedbean == 0:
            self.ui.G_redBeanCount.setText(str(self.ranRedbean) + "개")
            self.ui.G_chouCount.setText(str(self.ranChou) + "개")

        elif self.ranChou == 0:
            self.ui.G_redBeanCount.setText(str(self.ranRedbean) + "개")
            self.ui.G_chouCount.setText(str(self.ranChou) + "개")

        else:
            self.ui.G_redBeanCount.setText(str(self.ranRedbean) + "개")
            self.ui.G_chouCount.setText(str(self.ranChou) + "개")

    def GuestNum(self):
        self.T_guest = self.guestNum - 1
        self.ui.T_guestCount.setText(str(self.T_guest)+"명")
        self.N_guest = len(self.guestQueue) - 1
        self.ui.N_guestCount.setText(str(self.N_guest)+"명")

    def GuestPicture(self):
        if(self.picture == 0):
            i = random.randrange(1, 5)
            if i == 1:
                self.ui.waitLine.setStyleSheet(
                    'image:url(./img/people1.png); border:0px;')
                self.picture = 1
            elif i == 2:
                self.ui.waitLine.setStyleSheet(
                    'image:url(./img/people2.png); border:0px;')
                self.picture = 1
            elif i == 3:
                self.ui.waitLine.setStyleSheet(
                    'image:url(./img/people3.png); border:0px;')
                self.picture = 1
            else:
                self.ui.waitLine.setStyleSheet(
                    'image:url(./img/people4.png); border:0px;')
                self.picture = 1
        else:
            self.ui.waitLine.setStyleSheet(
                'image:none; border:0px;')
            self.picture = 0

    # 붕어빵 제작

    def bun_finished(self, index_):
        self.index = index_

        self.ui.flour.setDisabled(True)
        self.ui.redbean.setDisabled(True)
        self.ui.chou.setDisabled(True)
        self.bunSort[self.index].setEnabled(True)
        if self.x[index_] == 0:
            self.bunSort[self.index].setStyleSheet(
                'image:url(./img/bun0.png); border:0px;')
            if self.click[index_] == 0:
                self.ui.flour.setEnabled(True)
                # self.bunSort[self.index].setDisabled(True)

            elif self.click[index_] == 1:
                self.red_count += 1
                self.ui.redbeanCount.setText(str(self.red_count) + "개")
                self.click[index_] = 0

            elif self.click[index_] == 2:
                self.chou_count += 1
                self.ui.chouCount.setText(str(self.chou_count) + "개")
                self.click[index_] = 0
        if self.x[index_] == 1:
            self.ui.flour.setDisabled(True)
            self.ui.redbean.setEnabled(True)
            self.ui.chou.setEnabled(True)
        if self.x[index_] == 2:
            self.ui.flour.setEnabled(True)
            self.ui.redbean.setDisabled(True)
            self.ui.chou.setDisabled(True)
        if self.x[index_] == 3:
            self.ui.flour.setEnabled(True)
            self.ui.redbean.setDisabled(True)
            self.ui.chou.setDisabled(True)

    def flour(self, index_):
        self.index = index_
        if self.click[index_] == 0:

            self.bunSort[self.index].setStyleSheet(
                'image:url(./img/bun1.png); border:0px;')

            self.ui.flour.setDisabled(True)
            self.ui.redbean.setEnabled(True)
            self.ui.chou.setEnabled(True)
            self.x[index_] = 1
        elif self.click[index_] != 0:
            self.bunSort[self.index].setStyleSheet(
                'image:url(./img/bun3.png); border:0px;')
            self.ui.flour.setDisabled(True)
            self.ui.redbean.setDisabled(True)
            self.ui.chou.setDisabled(True)
            self.bunSort[self.index].setEnabled(True)
            self.x[index_] = 0

    def redbean(self, index_):
        self.index = index_
        self.click[index_] = 1

        self.ui.redbean.setDisabled(True)
        self.ui.chou.setDisabled(True)
        self.bunSort[self.index].setStyleSheet(
            'image:url(./img/bun2_redbean.png); border:0px;')
        self.ui.flour.setEnabled(True)
        self.x[index_] = 2


    def chou(self, index_):
        self.index = index_
        self.click[index_] = 2
        self.ui.redbean.setDisabled(True)
        self.ui.chou.setDisabled(True)
        self.bunSort[self.index].setStyleSheet(
            'image:url(./img/bun2_chou.png); border:0px;')
        self.ui.flour.setEnabled(True)
        self.x[index_] = 3

    def spinBoxChanged(self):
        self.bun_cal = 300 * \
            (int(self.ui.S_chouCount.value()) +
             int(self.ui.S_redbeanCount.value()))
        self.ui.profit.setText(str(self.bun_cal)+" GOLD")

    def storeUpgrade(self, upgradeNum):
        if self.levelCount > upgradeNum:
            self.ui.lack.setText("이미 확장시킨 \n건물입니다.")

        if self.Tsell < 5000:
            self.ui.lack.setText("잔액이 부족합니다.")

        elif(self.Tsell > 5000):
            if self.levelCount == upgradeNum:
                if upgradeNum == 1:
                    self.storeLoad = 'image:url(./img/level2.png); border:0px;'
                    self.ui.seestore.setStyleSheet(self.storeLoad)
                    self.levelCount = 2
                elif upgradeNum == 2:
                    if self.levelCount == 2:
                        self.storeLoad = 'image:url(./img/level3.png); border:0px;'
                        self.ui.seestore.setStyleSheet(self.storeLoad)
                        self.levelCount = 3
                elif upgradeNum == 3:
                    if self.levelCount == 3:
                        self.storeLoad = 'image:url(./img/level4.png); border:0px;'
                        self.ui.seestore.setStyleSheet(self.storeLoad)
                        self.levelCount = 4
                        self.EndGame()

                self.ui.lack.setText("확장 완료 !")
                self.Tsell -= 5000
                self.ui.upgoldNum.setText(str(self.Tsell))
                self.ui.profit2.setText(str(self.Tsell) + " GOLD")

            if self.levelCount < upgradeNum:
                self.ui.lack.setText("이전 단계를 \n먼저 확장시켜주세요.")

    def EndGame(self):
        msgBox = QMessageBox()
        msgBox.setText("게임을 성공적으로 클리어했습니다. 데이터 저장 및 종료를 해주세요.")
        msgBox.setWindowTitle("게임 엔딩")
        msgBox.addButton('저장', QMessageBox.YesRole)
        msgBox.addButton('계속하기', QMessageBox.NoRole)
        msgBox.addButton("통계보기", QMessageBox.RejectRole)
        ret = msgBox.exec_()

        if ret == 0:
            self.saveFunction()
        elif ret == 2:
            msgBox = QMessageBox()
            msgBox.setText("평판: " + str(self.reputation) +
                           "\n시간: " + str(self.hour_count)+"시간" + str(self.min_count)+"분" + str(self.sec_count)+"초" +
                           "\n총 손님 수:"+str(self.T_guest)+"명" +
                           "\n보유금액:"+str(self.Tsell)+"GOLD" +
                           "\n보유 붕어빵 수:"+str(self.chou_count)+str(self.red_count))
            msgBox.setWindowTitle("통계")
            msgBox.addButton('저장', QMessageBox.YesRole)
            msgBox.addButton('계속하기', QMessageBox.NoRole)
            rets = msgBox.exec_()

            if rets == 0:
                self.saveFunction()

    def EndGame2(self):
        if self.reputation < 20:
            msgBox = QMessageBox()
            msgBox.setText("평판이 낮아 진행이 불가합니다.")
            msgBox.setWindowTitle("게임 엔딩")
            msgBox.addButton('종료하기', QMessageBox.NoRole)
            msgBox.addButton("통계보기", QMessageBox.RejectRole)
            ret = msgBox.exec_()
            if ret == 0:
                exit()
            elif ret == 1:
                msgBox = QMessageBox()
                msgBox.setText("평판: " + str(self.reputation) +
                               "\n시간: " + str(self.hour_count)+"시간" + str(self.min_count)+"분" + str(self.sec_count)+"초" +
                               "\n총 손님 수:"+str(self.T_guest)+"명" +
                               "\n보유금액:"+str(self.Tsell)+"GOLD" +
                               "\n보유 붕어빵 수:"+str(self.chou_count)+str(self.red_count))
                msgBox.setWindowTitle("통계")
                msgBox.addButton('종료하기', QMessageBox.NoRole)

                rets = msgBox.exec_()

                if rets == 0:
                    exit()

        elif self.reputation == 100:
            msgBox = QMessageBox()
            msgBox.setText("축하합니다. 히든게임 엔딩에 도달하셨습니다.")
            msgBox.setWindowTitle("(히든) 게임 엔딩")
            msgBox.addButton('종료하기', QMessageBox.NoRole)
            msgBox.addButton("통계보기", QMessageBox.RejectRole)
            ret = msgBox.exec_()
            if ret == 0:
                exit()
            elif ret == 1:
                msgBox = QMessageBox()
                msgBox.setText("평판: " + str(self.reputation) +
                               "\n시간: " + str(self.hour_count)+"시간" + str(self.min_count)+"분" + str(self.sec_count)+"초" +
                               "\n총 손님 수:"+str(self.T_guest)+"명" +
                               "\n보유금액:"+str(self.Tsell)+"GOLD" +
                               "\n보유 붕어빵 수:"+str(self.chou_count)+str(self.red_count))
                msgBox.setWindowTitle("통계")
                msgBox.addButton('종료하기', QMessageBox.NoRole)
                rets = msgBox.exec_()

                if rets == 0:
                    exit()

    def snowEffect(self):
        self.movie = QMovie("./img/snow_.gif")
        self.ui.snow.setMovie(self.movie)
        self.ui.snow2.setMovie(self.movie)
        self.movie.start()

    def openFunction(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Open File', './save', 'CSV File (*.csv)')

        if fname[0]:
            with open(fname[0], 'r', encoding='UTF8') as f:
                read = csv.reader(f)
                linecnt = 0

                for info in read:
                    if linecnt == 0:
                        self.Tsell = int(info[0])
                        self.guestNum = int(info[1])
                        self.reputation = int(info[2])
                        self.red_count = int(info[3])
                        self.chou_count = int(info[4])
                        self.storeLoad = info[5]
                        self.levelCount = int(info[6])
                        self.sec_count = int(info[7])
                        self.min_count = int(info[8])
                        self.hour_count = int(info[9])
                        self.th.count = int(info[10])
        self.uiLoad()

    def uiLoad(self):
        self.th = Worker()
        self.th.timer.connect(self.totaltime)
        self.th.guestIn.connect(self.guestIn)
        self.th.guestOut.connect(self.guestOut)
        self.th.eventType.connect(self.eventType)

        self.ui.second.setText(str(self.sec_count) + "초")
        self.ui.minute.setText(str(self.min_count) + "분")
        self.ui.hour.setText(str(self.hour_count) + "시간")

        self.T_guest = self.guestNum - 1
        self.ui.T_guestCount.setText(str(self.T_guest) + "명")

        self.ui.N_guestCount.setText(str(len(self.guestQueue) - 1) + "명")

        self.ui.redbeanCount.setText(str(self.red_count) + "개")
        self.ui.chouCount.setText(str(self.chou_count) + "개")

        self.ui.profit2.setText(str(self.Tsell) + " GOLD")
        self.ui.upgoldNum.setText(str(self.Tsell))

        self.ui.seestore.setStyleSheet(self.storeLoad)

        self.ui.stackedWidget.setCurrentWidget(self.ui.mainWindow)
        self.ui.progressBar.setValue(int(self.reputation))

    def saveFunction(self):
        guestTotal = self.guestNum - (len(self.guestQueue) - 1)
        fname = QFileDialog.getSaveFileName(
            self, 'Save File', './save', 'CSV File (*.csv)')
        if fname[0]:
            with open(fname[0], 'w', newline="", encoding='UTF8') as f:
                write = csv.writer(f)
                #write.writerow(["매출량", "손님 수", "평판", "팥 붕어빵 개수", "슈크림 붕어빵 개수", "가게 이미지", "가게 확장 레벨"])
                write.writerow([str(self.Tsell), str(guestTotal), str(self.reputation),
                                str(self.red_count), str(self.chou_count),
                                self.storeLoad, str(self.levelCount),
                                str(self.sec_count), str(self.min_count), str(self.hour_count), str(self.th.count)])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
