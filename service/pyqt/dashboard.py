import serial
import threading
import time
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import pyqtSignal, QTimer


class SerialThread(QtCore.QThread):
    received_data = pyqtSignal(str)

    def __init__(self, serial_port, baud_rate):
        super().__init__()
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.ser = None
        self.running = False

    def run(self):
        try:
            self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
            self.running = True
            while self.running:
                if self.ser.in_waiting > 0:
                    data = self.ser.readline().decode('utf-8').strip()
                    if data:
                        self.received_data.emit(data)
                time.sleep(0.01)  # Small delay to prevent busy-waiting
        except serial.SerialException as e:
            print(f"Serial Error: {e}")
        finally:
            if self.ser and self.ser.is_open:
                self.ser.close()

    def stop(self):
        self.running = False
        self.wait()

    def write(self, data):
        if self.ser and self.ser.is_open:
            self.ser.write(data.encode('utf-8'))


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1039, 582)
        self.groupBox_e = QtWidgets.QGroupBox(parent=Dialog)
        self.groupBox_e.setGeometry(QtCore.QRect(70, 20, 341, 141))
        self.groupBox_e.setObjectName("groupBox_e")
        self.le_e_id = QtWidgets.QLineEdit(parent=self.groupBox_e)
        self.le_e_id.setGeometry(QtCore.QRect(20, 50, 221, 41))
        self.le_e_id.setReadOnly(True)
        self.le_e_id.setObjectName("le_e_id")
        self.label_e_id = QtWidgets.QLabel(parent=self.groupBox_e)
        self.label_e_id.setGeometry(QtCore.QRect(20, 30, 66, 18))
        self.label_e_id.setObjectName("label_e_id")
        self.label_e_approv = QtWidgets.QLabel(parent=self.groupBox_e)
        self.label_e_approv.setGeometry(QtCore.QRect(250, 50, 61, 41))
        self.label_e_approv.setObjectName("label_e_approv")
        self.pushButton_e = QtWidgets.QPushButton(parent=self.groupBox_e)
        self.pushButton_e.setGeometry(QtCore.QRect(180, 100, 151, 30))
        self.pushButton_e.setObjectName("pushButton_e")
        self.groupBox_ele = QtWidgets.QGroupBox(parent=Dialog)
        self.groupBox_ele.setGeometry(QtCore.QRect(70, 190, 341, 291))
        self.groupBox_ele.setObjectName("groupBox_ele")
        self.lcdNumber_floor = QtWidgets.QLCDNumber(parent=self.groupBox_ele)
        self.lcdNumber_floor.setGeometry(QtCore.QRect(-110, 100, 181, 91))
        self.lcdNumber_floor.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.lcdNumber_floor.setLineWidth(-1)
        self.lcdNumber_floor.setObjectName("lcdNumber_floor")
        self.label = QtWidgets.QLabel(parent=self.groupBox_ele)
        self.label.setGeometry(QtCore.QRect(10, 90, 66, 18))
        self.label.setObjectName("label")
        self.pushButton_1f = QtWidgets.QPushButton(parent=self.groupBox_ele)
        self.pushButton_1f.setGeometry(QtCore.QRect(190, 190, 88, 26))
        self.pushButton_1f.setObjectName("pushButton_1f")
        self.pushButton_2f = QtWidgets.QPushButton(parent=self.groupBox_ele)
        self.pushButton_2f.setGeometry(QtCore.QRect(190, 130, 88, 26))
        self.pushButton_2f.setObjectName("pushButton_2f")
        self.pushButton_3f = QtWidgets.QPushButton(parent=self.groupBox_ele)
        self.pushButton_3f.setGeometry(QtCore.QRect(190, 70, 88, 26))
        self.pushButton_3f.setObjectName("pushButton_3f")
        self.label_ele_3f = QtWidgets.QLabel(parent=self.groupBox_ele)
        self.label_ele_3f.setGeometry(QtCore.QRect(170, 70, 16, 18))
        self.label_ele_3f.setObjectName("label_ele_3f")
        self.label_ele_2f = QtWidgets.QLabel(parent=self.groupBox_ele)
        self.label_ele_2f.setGeometry(QtCore.QRect(170, 130, 16, 18))
        self.label_ele_2f.setObjectName("label_ele_2f")
        self.label_ele_1f = QtWidgets.QLabel(parent=self.groupBox_ele)
        self.label_ele_1f.setGeometry(QtCore.QRect(170, 190, 16, 18))
        self.label_ele_1f.setObjectName("label_ele_1f")
        self.groupBox_home = QtWidgets.QGroupBox(parent=Dialog)
        self.groupBox_home.setGeometry(QtCore.QRect(440, 20, 571, 491))
        self.groupBox_home.setObjectName("groupBox_home")
        self.widget_graph = QtWidgets.QWidget(parent=self.groupBox_home)
        self.widget_graph.setGeometry(QtCore.QRect(129, 50, 371, 141))
        self.widget_graph.setObjectName("widget_graph")
        self.lcdNumber_temp = QtWidgets.QLCDNumber(parent=self.groupBox_home)
        self.lcdNumber_temp.setGeometry(QtCore.QRect(10, 50, 101, 51))
        self.lcdNumber_temp.setObjectName("lcdNumber_temp")
        self.lcdNumber_hu = QtWidgets.QLCDNumber(parent=self.groupBox_home)
        self.lcdNumber_hu.setGeometry(QtCore.QRect(10, 130, 101, 51))
        self.lcdNumber_hu.setObjectName("lcdNumber_hu")
        self.label_2 = QtWidgets.QLabel(parent=self.groupBox_home)
        self.label_2.setGeometry(QtCore.QRect(10, 30, 66, 18))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(parent=self.groupBox_home)
        self.label_3.setGeometry(QtCore.QRect(10, 110, 66, 18))
        self.label_3.setObjectName("label_3")
        self.lcdNumber_lux = QtWidgets.QLCDNumber(parent=self.groupBox_home)
        self.lcdNumber_lux.setGeometry(QtCore.QRect(20, 330, 101, 51))
        self.lcdNumber_lux.setObjectName("lcdNumber_lux")
        self.label_4 = QtWidgets.QLabel(parent=self.groupBox_home)
        self.label_4.setGeometry(QtCore.QRect(20, 300, 101, 18))
        self.label_4.setObjectName("label_4")
        self.pushButton_curOpen = QtWidgets.QPushButton(parent=self.groupBox_home)
        self.pushButton_curOpen.setGeometry(QtCore.QRect(20, 430, 121, 26))
        self.pushButton_curOpen.setObjectName("pushButton_curOpen")
        self.pushButton_curClose = QtWidgets.QPushButton(parent=self.groupBox_home)
        self.pushButton_curClose.setGeometry(QtCore.QRect(160, 430, 121, 26))
        self.pushButton_curClose.setObjectName("pushButton_curClose")
        self.pushButton_curStop = QtWidgets.QPushButton(parent=self.groupBox_home)
        self.pushButton_curStop.setGeometry(QtCore.QRect(290, 430, 121, 26))
        self.pushButton_curStop.setObjectName("pushButton_curStop")
        self.progressBar_cur = QtWidgets.QProgressBar(parent=self.groupBox_home)
        self.progressBar_cur.setGeometry(QtCore.QRect(150, 330, 241, 41))
        self.progressBar_cur.setProperty("value", 24)
        self.progressBar_cur.setObjectName("progressBar_cur")
        self.label_5 = QtWidgets.QLabel(parent=self.groupBox_home)
        self.label_5.setGeometry(QtCore.QRect(150, 300, 101, 18))
        self.label_5.setObjectName("label_5")
        self.label_airState = QtWidgets.QLabel(parent=self.groupBox_home)
        self.label_airState.setGeometry(QtCore.QRect(20, 200, 151, 18))
        self.label_airState.setObjectName("label_airState")
        self.label_heatState = QtWidgets.QLabel(parent=self.groupBox_home)
        self.label_heatState.setGeometry(QtCore.QRect(200, 200, 151, 18))
        self.label_heatState.setObjectName("label_heatState")
        self.label_humiState = QtWidgets.QLabel(parent=self.groupBox_home)
        self.label_humiState.setGeometry(QtCore.QRect(380, 200, 151, 18))
        self.label_humiState.setObjectName("label_humiState")
        self.pushButton_curAuto = QtWidgets.QPushButton(parent=self.groupBox_home)
        self.pushButton_curAuto.setGeometry(QtCore.QRect(430, 430, 121, 26))
        self.pushButton_curAuto.setObjectName("pushButton_curAuto")
        self.label_curState = QtWidgets.QLabel(parent=self.groupBox_home)
        # self.label_curState.setGeometry(QtCore.QRect(160, 400, 520, 18))
        self.label_curState.setObjectName("label_curState")
        self.pushButton_heat = QtWidgets.QPushButton(parent=self.groupBox_home)
        self.pushButton_heat.setGeometry(QtCore.QRect(200, 220, 151, 30))
        self.pushButton_heat.setObjectName("pushButton_heat")
        self.pushButton_air = QtWidgets.QPushButton(parent=self.groupBox_home)
        self.pushButton_air.setGeometry(QtCore.QRect(20, 220, 151, 30))
        self.pushButton_air.setObjectName("pushButton_air")
        self.pushButton_humi = QtWidgets.QPushButton(parent=self.groupBox_home)
        self.pushButton_humi.setGeometry(QtCore.QRect(380, 220, 151, 30))
        self.pushButton_humi.setObjectName("pushButton_humi")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        # Initialize serial communication
        self.serial_thread = SerialThread(serial_port='/dev/ttyACM0', baud_rate=9600)  # Adjust port and baud rate as needed
        self.serial_thread.received_data.connect(self.handle_serial_data)
        self.serial_thread.start()

        # Connect buttons to slots
        self.pushButton_1f.clicked.connect(self.elevator_1f_call)
        self.pushButton_2f.clicked.connect(self.elevator_2f_call)
        self.pushButton_3f.clicked.connect(self.elevator_3f_call)
        
        self.pushButton_e.clicked.connect(self.entrance_open)

        self.pushButton_curOpen.clicked.connect(self.curtain_open)
        self.pushButton_curClose.clicked.connect(self.curtain_close)
        self.pushButton_curStop.clicked.connect(self.curtain_stop)
        self.pushButton_curAuto.clicked.connect(self.curtain_enable_auto)
        self.progressBar_cur.setRange(0, 100)

        self.curtain_max_steps = int(1.3 * 2048)
        self.curtain_auto_mode = True
        self.curtain_motion_state = "정지"
        self.curtain_status_message = ""
        self.progressBar_cur.setRange(0, 100)
        self._refresh_curtain_controls()

        # Initially hide all check icons
        self.label_ele_1f.setText("")
        self.label_ele_2f.setText("")
        self.label_ele_3f.setText("")

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox_e.setTitle(_translate("Dialog", "공동현관"))
        self.label_e_id.setText(_translate("Dialog", "ID"))
        self.label_e_approv.setText(_translate("Dialog", ""))
        self.pushButton_e.setText(_translate("Dialog", "공동현관 열기"))
        self.groupBox_ele.setTitle(_translate("Dialog", "엘리베이터"))
        self.label.setText(_translate("Dialog", "층"))
        self.pushButton_1f.setText(_translate("Dialog", "1층"))
        self.pushButton_2f.setText(_translate("Dialog", "2층"))
        self.pushButton_3f.setText(_translate("Dialog", "3층"))
        # self.label_ele_3f.setText(_translate("Dialog", "✅"))
        # self.label_ele_2f.setText(_translate("Dialog", "✅"))
        # self.label_ele_1f.setText(_translate("Dialog", "✅"))
        self.groupBox_home.setTitle(_translate("Dialog", "Home"))
        self.label_2.setText(_translate("Dialog", "온도(C)"))
        self.label_3.setText(_translate("Dialog", "습도(%)"))
        self.label_4.setText(_translate("Dialog", "외부조도(LUX)"))
        self.pushButton_curOpen.setText(_translate("Dialog", "커튼 OPEN"))
        self.pushButton_curClose.setText(_translate("Dialog", "커튼 CLOSE"))
        self.pushButton_curStop.setText(_translate("Dialog", "커튼 STOP"))
        self.label_5.setText(_translate("Dialog", "커튼 열림 정도"))
        self.label_airState.setText(_translate("Dialog", "state"))
        self.label_heatState.setText(_translate("Dialog", "state"))
        self.label_humiState.setText(_translate("Dialog", "state"))
        self.pushButton_curAuto.setText(_translate("Dialog", "커튼 Auto 복귀"))
        self.label_curState.setText(_translate("Dialog", "state"))
        self.pushButton_heat.setText(_translate("Dialog", "히터 ON/OFF/Auto"))
        self.pushButton_air.setText(_translate("Dialog", "에어컨 ON/OFF/Auto"))
        self.pushButton_humi.setText(_translate("Dialog", "가습기 ON/OFF/Auto"))

    def entrance_open(self):
        command = "CMO,MOTOR,1\n"
        self.serial_thread.write(command)
        self.label_e_approv.setText("✅")

    def elevator_1f_call(self):
        command = "CMO,FLOOR,1\n"
        self.serial_thread.write(command)
        self.label_ele_1f.setText("✅")

    def elevator_2f_call(self):
        command = "CMO,FLOOR,2\n"
        self.serial_thread.write(command)
        self.label_ele_2f.setText("✅")

    def elevator_3f_call(self):
        command = "CMO,FLOOR,3\n"
        self.serial_thread.write(command)
        self.label_ele_3f.setText("✅")

    def handle_serial_data(self, data):
        data = data.strip()
        if not data:
            return

        parts = data.split(',')
        if len(parts) != 3:
            print(f"[ERROR] invalid frame: {data!r}")
            return

        data_type, metric_name, value = parts

        if data_type == "ACK":
            self._handle_ack(metric_name, value)
        elif data_type == "SEN":
            self._handle_sensor(metric_name, value)
        else:
            print(f"[WARN] unsupported frame type: {data_type!r}")

    def _handle_ack(self, metric_name, value):
        if metric_name == "FLOOR":
            if value == "1":
                self.label_ele_1f.setText("")
            elif value == "2":
                self.label_ele_2f.setText("")
            elif value == "3":
                self.label_ele_3f.setText("")
            return

        if metric_name == "MOTOR":
            if self.curtain_auto_mode:
                self.curtain_auto_mode = False
                self._refresh_curtain_controls()
            self._set_curtain_status_message(f"ACK:{value}")
        elif metric_name == "MODE":
            self.curtain_auto_mode = value.upper() == "AUTO"
            self._refresh_curtain_controls()
            self._set_curtain_status_message(f"MODE:{value}")
        elif metric_name == "ERROR":
            self._set_curtain_status_message(f"ERROR:{value}")
        else:
            print(f"[INFO] ACK ignored: {metric_name},{value}")

    def _handle_sensor(self, metric_name, value):
        if metric_name == "FLOOR":
            try:
                self.lcdNumber_floor.display(int(float(value)))
            except ValueError:
                print(f"[ERROR] invalid floor number: {value!r}")
            return

        if metric_name == "RFID_ACCESS":
            self.le_e_id.setText(str(value))
            self.label_e_approv.setText("✅")
            return
        if metric_name == "RFID_DENY":
            self.le_e_id.setText(str(value))
            self.label_e_approv.setText("❌")
            return
        if metric_name == "MOTOR" and value == "-1":
            self.le_e_id.clear()
            self.label_e_approv.setText("")
            return

        if metric_name == "LIGHT":
            try:
                self.lcdNumber_lux.display(float(value))
            except ValueError:
                print(f"[ERROR] invalid light value: {value!r}")
            return
        if metric_name == "CUR_STEP":
            self._update_curtain_progress(value)
            return
        if metric_name == "MOTOR_DIR":
            self._handle_curtain_direction(value)
            return

        print(f"[INFO] sensor metric ignored: {metric_name},{value}")

    def curtain_open(self):
        self.serial_thread.write("CMO,MOTOR,OPEN\n")
        self._mark_manual_mode_requested()
        self._set_curtain_status_message("요청:OPEN")

    def curtain_close(self):
        self.serial_thread.write("CMO,MOTOR,CLOSE\n")
        self._mark_manual_mode_requested()
        self._set_curtain_status_message("요청:CLOSE")

    def curtain_stop(self):
        self.serial_thread.write("CMO,MOTOR,STOP\n")
        self._mark_manual_mode_requested()
        self._set_curtain_status_message("요청:STOP")

    def curtain_enable_auto(self):
        self.serial_thread.write("CMO,MODE,AUTO\n")
        self._set_curtain_status_message("요청:AUTO")

    def _handle_curtain_direction(self, value):
        try:
            direction = int(float(value))
        except ValueError:
            print(f"[ERROR] invalid motor direction: {value!r}")
            return

        if direction > 0:
            motion_text = "열림 중"
        elif direction < 0:
            motion_text = "닫힘 중"
        else:
            motion_text = "정지"

        self._set_curtain_motion_state(motion_text)

    def _update_curtain_progress(self, step_value):
        try:
            steps = float(step_value)
        except ValueError:
            print(f"[ERROR] invalid curtain step value: {step_value!r}")
            return

        if self.curtain_max_steps <= 0:
            return

        percentage = max(0, min(100, int((steps / self.curtain_max_steps) * 100)))
        self.progressBar_cur.setValue(percentage)

    def _refresh_curtain_controls(self):
        self.pushButton_curAuto.setText("커튼 Auto 복귀")
        self._refresh_curtain_status_label()

    def _set_curtain_motion_state(self, text):
        self.curtain_motion_state = text
        self.curtain_status_message = ""
        self._refresh_curtain_status_label()

    def _set_curtain_status_message(self, text):
        self.curtain_status_message = text
        self._refresh_curtain_status_label()

    def _refresh_curtain_status_label(self):
        mode_text = "AUTO" if self.curtain_auto_mode else "MANUAL"
        parts = [f"모드: {mode_text}", f"상태: {self.curtain_motion_state}"]
        if self.curtain_status_message:
            parts.append(self.curtain_status_message)
        self.label_curState.setText('  |  '.join(filter(None, parts)))

    def _mark_manual_mode_requested(self):
        if self.curtain_auto_mode:
            self.curtain_auto_mode = False
            self._refresh_curtain_controls()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())
