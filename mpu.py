from machine import I2C, Pin  # type: ignore # Raspberry Pi Pico 用の I2C モジュール
import time

# MPU6050 の I2C アドレス
MPU6050_ADDR = 0x68

# MPU6050 のレジスタアドレス
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

# I2C の初期化 (SDA: Pin 6, SCL: Pin 7)
i2c = I2C(1, sda=Pin(6), scl=Pin(7), freq=400000)

# LED の初期化 (LED1: Pin 15, LED2: Pin 14, LED3: Pin 13, LED4: Pin 12)
red_led = Pin(16, Pin.OUT)
blue_led = Pin(17, Pin.OUT)
yellow_led = Pin(15, Pin.OUT)
white_led = Pin(14, Pin.OUT)


# MPU6050 の初期化
def mpu6050_init():
    # MPU6050 をスリープモードから解除

    i2c.writeto_mem(MPU6050_ADDR, PWR_MGMT_1, b"\x00")


# 16ビットデータを取得するヘルパー関数
def read_raw_data(addr):
    high = i2c.readfrom_mem(MPU6050_ADDR, addr, 1)[0]
    low = i2c.readfrom_mem(MPU6050_ADDR, addr + 1, 1)[0]
    value = (high << 8) | low
    # 2の補数表現を考慮して値を変換
    if value > 32768:
        value -= 65536
    return value


# 初期化処理
mpu6050_init()

print("MPU6050 初期化完了")

# データ取得ループ
while True:
    # 加速度データの取得
    accel_x = read_raw_data(ACCEL_XOUT_H) / 16384.0
    accel_y = read_raw_data(ACCEL_XOUT_H + 2) / 16384.0
    accel_z = read_raw_data(ACCEL_XOUT_H + 4) / 16384.0

    # ジャイロスコープデータの取得
    gyro_x = read_raw_data(GYRO_XOUT_H) / 131.0
    gyro_y = read_raw_data(GYRO_XOUT_H + 2) / 131.0
    gyro_z = read_raw_data(GYRO_XOUT_H + 4) / 131.0

    # データの表示
    print("加速度: X=%.2f, Y=%.2f, Z=%.2f" % (accel_x, accel_y, accel_z))
    print("ジャイロ: X=%.2f, Y=%.2f, Z=%.2f" % (gyro_x, gyro_y, gyro_z))

    # LED の制御
    if accel_x > 0.1:
        red_led.value(1)
    else:
        red_led.value(0)

    if accel_y > 0.1:
        blue_led.value(1)
    else:
        blue_led.value(0)

    if accel_z > 0.1:
        yellow_led.value(1)
    else:
        yellow_led.value(0)

    if gyro_x > 0.1:
        white_led.value(1)
    else:
        white_led.value(0)

    # 1秒待機
    time.sleep(3)
