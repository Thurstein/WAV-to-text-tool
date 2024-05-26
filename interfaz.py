import os, warnings, threading
from convertidor import AudioThread
from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QMainWindow,QVBoxLayout, QHBoxLayout,QPushButton, QFileDialog, QLabel, QTextEdit, QWidget

warnings.filterwarnings("ignore")
(MyWindowWidth,MyWindowHeight) = (800,600)
(BUTTON_WIDTH,BUTTON_HEIGHT) = (200,50)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.my_signal = QtCore.Signal(str)
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 300, 200)
        WINDOW_TITLE = "WAV to TXT converter"
        self.setWindowTitle(WINDOW_TITLE)
        self.resize(MyWindowWidth,MyWindowHeight)

        # Creamos un contenedor para el layout horizontal
        self.container = QWidget()
        self.setCentralWidget(self.container)

        # Establecemos el layout horizontal para el contenedor
        self.main_layout = QHBoxLayout()
        self.container.setLayout(self.main_layout)

        # Creamos dos layouts verticales para cada sección
        self.layout1 = QVBoxLayout()
        self.layout2 = QVBoxLayout()
        self.layout3 = QVBoxLayout()

        # Widgets
        ## Botones
        self.btn_select_file = QPushButton('Seleccionar archivo')
        self.btn_select_file.clicked.connect(self.abrirArchivo)
        self.convert_button = QPushButton("Convertir audio", self)
        self.convert_button.clicked.connect(self.convertir_audio)
        self.delete_text = QPushButton("Borrar texto", self)
        self.delete_text.clicked.connect(self.borrarTexto)
        ## Caja de texto
        self.transcription_box = QTextEdit(self)
        self.transcription_box.setReadOnly(True)
        
        ## Labels
        self.seleccionado = QLabel("Por favor seleccione un archivo para comenzar", self)
        self.proceso = QLabel("-", self)
        
        # Añadir los widgets al layout
        self.layout1.addWidget(self.btn_select_file)
        self.layout1.addWidget(self.convert_button)
        self.layout1.addWidget(self.delete_text)
        self.layout2.addWidget(self.transcription_box)
        self.layout3.addWidget(self.seleccionado)
        self.layout3.addWidget(self.proceso)

        # Creamos los Qwidgets
        self.widget1= QWidget()
        self.widget2= QWidget()
        self.widget3= QWidget()
        self.widget1.setLayout(self.layout1)
        self.widget2.setLayout(self.layout2)
        self.widget3.setLayout(self.layout3)
        self.widget1.setStyleSheet("background-color: #1596B6")
        self.widget2.setStyleSheet("background-color: lightblue; border-radius: 10px;")
        self.widget3.setStyleSheet("background-color: #1596B6")

        # Añadir los layouts a un layout horizontal principal
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.widget1)
        self.main_layout.addWidget(self.widget2)
        self.main_layout.addWidget(self.widget3)

        # Asignar el layout principal a la ventana principal
        self.container = QWidget()
        self.setCentralWidget(self.container)
        self.container.setLayout(self.main_layout)

        #Listas
        buttonList = [self.btn_select_file,self.convert_button,self.delete_text]
        #Características de los botones
        for buttons in buttonList:
            buttons.setFixedSize(BUTTON_WIDTH,BUTTON_HEIGHT)

        # Iniciar hilo para procesar audio
        self.thread = AudioThread()
        self.thread.signal.connect(self.update_transcription_box)
        self.thread.start()

    def update_transcription_box(self, text):
        self.transcription_box.append(text)
        
    def abrirArchivo(self):
        FILE_FILTER = "Todos los archivos (*.*)"
        fileName, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo", "", FILE_FILTER)
        self.nombreArchivo = os.path.basename(fileName)
        self.seleccionado.setText(f'Archivo seleccionado: {self.nombreArchivo}')
        self.proceso.setText('Archivo listo para convertir')
        print(f'Se seleccionó el archivo: {self.nombreArchivo}')

    def convertir_audio(self):
        self.proceso.setText('Convirtiendo audio')
        threading.Thread(target=self.thread.process_audio, args=[self.nombreArchivo]).start()

    def borrarTexto(self):
        self.transcription_box.clear()
        try:
            if os.path.exists("the_audio.txt"):
                os.remove("the_audio.txt")
            else:
                print("El archivo 'the_audio.txt' no existe.")
        except Exception as e:
            print(f'Error al eliminar el archivo: {e}')

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()