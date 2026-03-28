# DJI Mini 2 RC to Xbox Controller

Преобразование пульта управления дрона DJI Mini 2 (RC‑N1, RCS231, WM161b‑RC‑N1) в игровой контроллер Xbox 360 для ПК.  
Программа предназначена для использования в FPV‑симуляторах (Liftoff, VelociDrone, DRL и др.) и любых играх, поддерживающих геймпад.

Turn the DJI Mini 2 remote controller (RC‑N1, RCS231, WM161b‑RC‑N1) into a virtual Xbox 360 gamepad. It is intended for use in FPV simulators (Liftoff, VelociDrone, DRL, etc.) and any game that supports a gamepad.

## Использование / How to use

**Основные элементы интерфейса / Main interface elements**

* **COM Port** – выбор последовательного порта, к которому подключён пульт.  
  Select the serial port connected to the remote controller.

* **Connect / Disconnect** – подключение/отключение от пульта.  
  Connect to or disconnect from the controller.

* **Calibrate** – запуск калибровки стиков и колёсика. Следуйте инструкциям на экране: двигайте каждый стик во все крайние положения и оставляйте в центре.  
  Launch stick and wheel calibration. Follow the on‑screen instructions: move each stick to all extremes and release to the center.

* **Start Emulation / Stop Emulation** – начало/остановка эмуляции Xbox‑контроллера.  
  Start or stop Xbox controller emulation.

* **Current Stick Values** – числовые значения всех осей и кнопок в реальном времени.  
  Real‑time numeric values of all axes and buttons.

* **Графики / Graphs** – визуальное отображение положения левого и правого стиков.  
  Visual representation of left and right stick positions.

**Соответствие кнопок пульта кнопкам Xbox / Button mapping**

| Элемент пульта               | Кнопка Xbox       |
|------------------------------|-------------------|
| Левый стик (X, Y)            | Левый стик        |
| Правый стик (X, Y)           | Правый стик       |
| Левое колёсико               | Правый триггер RT |
| Переключатель скоростей      | Левый триггер LT  |
| FN                           | A                 |
| Camera Mode                  | B                 |
| Shutter                      | X                 |
| Home                         | Y                 |

| RC element                   | Xbox button       |
|------------------------------|-------------------|
| Left stick (X, Y)            | Left stick        |
| Right stick (X, Y)           | Right stick       |
| Left wheel                   | Right trigger RT  |
| Speed switch                 | Left trigger LT   |
| FN                           | A                 |
| Camera Mode                  | B                 |
| Shutter                      | X                 |
| Home                         | Y                 |

*После запуска эмуляции проверьте работу контроллера в стандартной утилите Windows: `joy.cpl`.*  
*After starting emulation, test the virtual controller using the Windows built‑in tool: `joy.cpl`.*

## Системные требования и установка / System requirements & installation

**Требования / Requirements**
- Windows 7 / 8 / 10 / 11
- Python 3.7 или выше / Python 3.7 or higher
- Драйвер vJoy (виртуальный джойстик) – [скачать](https://sourceforge.net/projects/vjoystick/)  
  vJoy driver – [download](https://sourceforge.net/projects/vjoystick/)
- Драйвер ScpVBus (vXboxInterface) – [релиз](https://github.com/shauleiz/vXboxInterface/releases) (необходим для работы `pyxinput`)  
  ScpVBus driver – [release](https://github.com/shauleiz/vXboxInterface/releases) (required for `pyxinput`)
- Пульт DJI Mini 2, подключённый к ПК через USB (определяется как COM-порт)  
  DJI Mini 2 remote controller connected via USB (appears as a COM port)

**Установка / Installation**

1. Установите vJoy и ScpVBus, следуя инструкциям на их страницах (запуск от имени администратора, перезагрузка).  
   Install vJoy and ScpVBus following the instructions on their pages (run as administrator, reboot).

2. Убедитесь, что в Диспетчере устройств появились `vJoy Device` и `Scp Virtual Bus Driver`.  
   Verify that `vJoy Device` and `Scp Virtual Bus Driver` appear in Device Manager.

3. Скачайте или скопируйте файлы программы в отдельную папку:  
   Download or copy the program files into a separate folder:
   - `rc_to_xbox.py`
   - `requirements.txt`
   - `install_and_run.bat` (опционально / optional)

4. Установите необходимые библиотеки Python:  
   Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

5. Запустите программу:  
   Run the program:
   ```bash
   python rc_to_xbox.py
   ```
   Или дважды кликните `install_and_run.bat` (запустит установку и сразу откроет программу).  
   Or double‑click `install_and_run.bat` (it will install dependencies and launch the program).

## Автор / Author

Created by Nill|981
