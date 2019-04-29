import math
import time
import BNO055
import numpy as np
import pandas as pd
import datetime
import signal
from threading import Timer,Thread,Event
import sys

#convenience class to run a timer on an interupt
class perpetualTimer():

   def __init__(self,t,hFunction):
      self.t=t
      self.hFunction = hFunction
      self.thread = Timer(self.t,self.handle_function)

   def handle_function(self):
      self.hFunction()
      self.thread = Timer(self.t,self.handle_function)
      self.thread.start()

   def start(self):
      self.thread.start()

   def cancel(self):
      self.thread.cancel()

#time series
time_series = np.zeros((200, 10)) #data type of floats with shape 200, 10
label = 0
df = pd.DataFrame(columns=['time series', 'label'])

#builds the timeseries and writes it to a csv file
#each input is a tuple of lengths 3, 3, 4 respectively
def updateTimeSeries(angular_velocity, linear_acceleration, orientation):
	#collects a finte n-dimensional time series to store IMU data for immediate analysis by nerual network
	#once collected the time series will be stored in a csv file with any action labels that can be usde for training

	#The finite time series is 2 seconds long given that the sensor is collecting data at 100Hz (timseries is 200 slots)
	global time_series
	time_series = np.roll(time_series, 2)
	#x, y, z, X, Y, Z, x`, y`, z`, w`
	time_series[0] = [angular_velocity[0], angular_velocity[1], angular_velocity[2],
		linear_acceleration[0], linear_acceleration[1], linear_acceleration[2],
		orientation[0], orientation[1], orientation[2], orientation[3]]

def addMemory():
	global time_series
	global label
	global df
	if not np.dot([time_series[199]], [1,1,1,1,1,1,1,1,1,1]) == 0: #make sure that the time_series has data
		newDf = pd.DataFrame({"time series":[time_series], "label":[label]})
		df = df.append(newDf, ignore_index=True, sort=False) #update dataframe


def signal_handler(signal, frame):
    global t
    file_name =  "data/" + str(datetime.datetime.now()) + ".csv"
    print('Saving file to ' + file_name)
    df.to_csv(file_name, index=None, header=True)
    print("File saved!")
    t.cancel()
    sys.exit(0)

def main():

	# Setup BNO055
	# Create and configure the BNO sensor connection.
	# Raspberry Pi configuration with I2C and RST connected to GPIO 27:
	sensor = BNO055.BNO055(rst=27)

	attempts = 0
	# Initialize the BNO055 and stop if something went wrong.
	while(attempts < 10):
		try:
			sensor.begin()
			break
		except Exception as e:
			attempts += 1
			time.sleep(0.25)

	if(attempts == 10):
		print('Failed to initialize BNO055! Program end')
		exit(1)

	# Print system status and self test result.
	try:
		status, self_test, error = sensor.get_system_status()
	except Exception as e:
		print('Failed to read BNO055 system status! ', e)

	print('\nSystem status: ', status)
	print('Self test result (0x0F is normal): ', hex(self_test))
	# Print out an error if system status is in error mode.
	if(status == 0x01):
		print('System error: ', error)
		print('See datasheet section 4.3.59 for the meaning.')

	# Print BNO055 software revision and other diagnostic data.
	try:
		sw, bl, accel, mag, gyro = sensor.get_revision()
	except Exception as e:
		rospy.logerr('Failed to read BNO055 meta-inforamtion!', e)

	print('Software version:   ', sw)
	print('Bootloader version: ', bl)
	print('Accelerometer ID:   ', hex(accel))
	print('Magnetometer ID:    ', hex(mag))
	print('Gyroscope ID:       ', hex(gyro))

	print('Reading BNO055 data...\n\n')

	while True:
		# Update data
		attempts = 0
		while(attempts < 4):
			try:
				# Read the calibration status, 0=uncalibrated and 3=fully calibrated.
				sys, gyro, accel, mag = sensor.get_calibration_status()
				temp_c = sensor.read_temp()
				break
			except Exception as e:
				print('Failed to read BNO055 calibration stat and temp! ', e)
				attempts += 1
				time.sleep(0.01)

		attempts = 0
		while(attempts < 4):
			try:
    			# Orientation as a quaternion:
				orientation = sensor.read_quaternion()

				# Gyroscope data (in degrees per second converted to radians per second):
				angular_vel = sensor.read_gyroscope()

				# Linear acceleration data (i.e. acceleration from movement, not gravity--
    			# returned in meters per second squared):
				linear_accel = sensor.read_linear_acceleration()
				break
			except Exception as e:
				print('Failed to read BNO055 data!', e)
				attempts += 1
				time.sleep(0.01)

		if(attempts != 4):
			if sys > 1: #if system calibrartion is 2 or 3
				updateTimeSeries(angular_vel, linear_accel, orientation)

		time.sleep(0.01) #~100Hz

t = perpetualTimer(0.1,addMemory)
if __name__ == '__main__':
	signal.signal(signal.SIGINT, signal_handler)
	#add memory to datafram every 0.1 seconds
	t.start()
	main()

# Unused functions
# Read the Euler angles for heading, roll, pitch (all in degrees).
# heading, roll, pitch = sensor.read_euler()
# Magnetometer data (in micro-Teslas):
# x,y,z = sensor.read_magnetometer()
# Accelerometer data (in meters per second squared):
# x,y,z = sensor.read_accelerometer()
# Gravity acceleration data (i.e. acceleration just from gravity--returned
# in meters per second squared):
# x,y,z = sensor.read_gravity()
