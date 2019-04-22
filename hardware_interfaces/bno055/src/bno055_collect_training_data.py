import math
import time
import BNO055
import numpy as np
import pandas as pd

#time series
time_series = np.zeros((200, 10)) #data type of floats with shape 200, 10

#builds the timeseries and writes it to a csv file
#each input is a tuple of lengths 3, 3, 4 respectively
def updateArray(angular_velocity, linear_acceleration, orientation):
	#collects a finte n-dimensional time series to store IMU data for immediate analysis by nerual network
	#once collected the time series will be stored in a csv file with any action labels that can be usde for training

	#The finite time series is 2 seconds long given that the sensor is collecting data at 100Hz (timseries is 200 slots)
	global time_series
	np.roll(time_series, 0)
	#x, y, z, X, Y, Z, x`, y`, z`, w`
	time_series[0] = [angular_velocity[0], angular_velocity[1], angular_velocity[2],
		linear_acceleration[0], linear_acceleration[1], linear_acceleration[2],
		orientation[0], orientation[1], orientation[2], orientation[3]]

	#write the time series into a csv file




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
		print('Failed to read BNO055 system status! %s', e)

	print('System status: %s', status)
	print('Self test result (0x0F is normal): %s', hex(self_test))
	# Print out an error if system status is in error mode.
	if(status == 0x01):
		print('System error: %s', error)
   		print('See datasheet section 4.3.59 for the meaning.')

	# Print BNO055 software revision and other diagnostic data.
	try:
		sw, bl, accel, mag, gyro = sensor.get_revision()
	except Exception as e:
		rospy.logerr('Failed to read BNO055 meta-inforamtion! %s', e)

	print('Software version:   %d', sw)
	print('Bootloader version: %d', bl)
	print('Accelerometer ID:   %s', hex(accel))
	print('Magnetometer ID:    %s', hex(mag))
	print('Gyroscope ID:       %s', hex(gyro))

	print('Reading BNO055 data...')

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
				print('Failed to read BNO055 calibration stat and temp! %s', e)
				attempts += 1
				time.sleep(0.01)

		if(attempts != 4):
			info.sysCalibration = sys
			info.accelCalibration = accel
			info.gyroCalibration = gyro
			info.magnoCalibration = mag
			info.tempC = temp_c


		attempts = 0
		while(attempts < 4):
			try:
    				# Orientation as a quaternion:
				orientation.x, orientation.y, orientation.z, orientation.w  = sensor.read_quaternion()

				# Gyroscope data (in degrees per second converted to radians per second):
				gry_x, gry_y, gry_z = sensor.read_gyroscope()
				angular_vel.x = math.radians(gry_x)
				angular_vel.y = math.radians(gry_y)
				angular_vel.z = math.radians(gry_z)

				# Linear acceleration data (i.e. acceleration from movement, not gravity--
    				# returned in meters per second squared):
				linear_accel.x, linear_accel.y, linear_accel.z = sensor.read_linear_acceleration()
				break
			except Exception as e:
				rospy.logdebug('Failed to read BNO055 data! %s', e)
				attempts += 1
				rospy.sleep(0.01)

		if(attempts != 4):
			msg.orientation = orientation
			msg.angular_velocity = angular_vel
			msg.linear_acceleration = linear_accel


		time.sleep(0.05)

if __name__ == '__main__':
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
