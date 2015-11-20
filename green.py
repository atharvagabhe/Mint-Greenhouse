import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import sys
import os
import serial
import time
def greenhouse_startup():
	try:
		actuator_arduino=serial.Serial('/dev/ttyACM1',9600)
	except:
		print "Vorsicht:Actuator arduino not connected or ready"
	try:
		sensor_arduino=serial.Serial('/dev/ttyACM0',9600)
	except:
		print "Vorsicht:Sensor arduino not connected or ready"
def on_connect(mqttc, obj, flags,rc):#2 and 
    print("rc: "+str(rc)) 
def on_message(mqttc, obj, msg):#2 and
    payload = (str(msg.payload))
    if(payload[-1:]=="]"):
	mqtt_file=open("mqtt_data.txt","w")
	mqtt_file.write(payload)
	mqttc.disconnect()
    return payload	
def on_publish(mqttc, obj, mid):
    print("mid: "+str(mid)) 
def on_subscribe(mqttc, obj, mid,granted_qos):#2
    print("Subscribed: "+str(mid)+" "+str(granted_qos)) 
def on_log(mqttc, obj, level, string):
    print(string)
def get_exp_values(measure_type):#2
    mqttc.connect("m2m.eclipse.org", 1883, 60)
    mqttc.subscribe("greenhouse/sense/"+measure_type, 0)
    mqttc.loop_forever()	
    temp_array=[]
    #file=open("expect_"+measure_type+".txt","w")
    mqtt_file=open("mqtt_data.txt","r+")
    temp_array=mqtt_file.readline()
    temporary_array=temp_array[1:-1]
    temp_array=[int(x) for x in temporary_array.split(',')]
    return temp_array

def mqtt_startup():#1 and 3.mqtt	
    mqttc = mqtt.Client() 
    mqttc.on_message = on_message 
    mqttc.on_connect = on_connect 
    mqttc.on_publish = on_publish 
    mqttc.on_subscribe = on_subscribe
    mqttc.connect("m2m.eclipse.org", 1883, 60) 
def threshold_fuzzy(measure_type,read_value):#should run without problems
	read_value=int(read_value)
	if(measure_type==temperature):
		if(read_value<10):
			publish.single("greenhouse/fuzzy","Temperature:Cold",hostname="m2m.eclipse.org")
		elif(read_value>=10 and read_value<20):
			publish.single("greenhouse/fuzzy","Temperature:Pleasent",hostname="m2m.eclipse.org")
		elif(read_value>=20 and read_value<=30):
			publish.single("greenhouse/fuzzy","Temperature:Warm",hostname="m2m.eclipse.org")
		elif(read_value>30):
			publish.single("greenhouse/fuzzy","Temperature:Hot",hostname="m2m.eclipse.org")
	elif(measure_type==humidity):
		 if(read_value<50):
                        publish.single("greenhouse/fuzzy","Humidity:Dry",hostname="m2m.eclipse.org")
                 elif(read_value>=50 and read_value<70):
                        publish.single("greenhouse/fuzzy","Humidity:Moist",hostname="m2m.eclipse.org")
                 elif(read_value>=70 and read_value<=90):
                        publish.single("greenhouse/fuzzy","Humidity:Wet",hostname="m2m.eclipse.org")
                 elif(read_value>90):
                        publish.single("greenhouse/fuzzy","Humidity:Watered",hostname="m2m.eclipse.org")
	elif(measure_type==luminosity):
		 if(read_value<30):
                        publish.single("greenhouse/fuzzy","Luminosity:Pitch dark",hostname="m2m.eclipse.org")
                 elif(read_value>=30 and read_value<300):
                        publish.single("greenhouse/fuzzy","Luminosity:Dark",hostname="m2m.eclipse.org")
                 elif(read_value>=300 and read_value<=900):
                        publish.single("greenhouse/fuzzy","Luminosity:Bright",hostname="m2m.eclipse.org")
                 elif(read_value>900):
                        publish.single("greenhouse/fuzzy","Luminosity:Lucifer bright",hostname="m2m.eclipse.org")
	
def instant_deviation_check(measure_type,read_count):#should work
	#compare with value same value file from expected array and call inst deviation and mean deviation 
	if(measure_type==temperature):
		deviation=temperature_exp_array[read_count]-temperature_act_array[read_count]
		print "Deviation form expected value:"+str(deviation)
	elif(measure_type==humidity):
		deviation=humidity_exp_array[read_count]-humidity_act_array[read_count]
		print "Deviation form expected value:"+str(deviation)
	elif(measure_type==luminosity):
		deviation=luminosity_exp_array[read_count]-luminosity_act_array[read_count]
		print "Deviation form expected value:"+str(deviation)
	return deviation


def actual_sequence(measure_type,read_count):
		temp_hard=25
		humi_hard=51
		lumi_hard=900
		#--------get values from serial
		if(measure_type==temperature):
			#sensor_arduino.write("T")
			#read_value=sensor_arduino.readline()
			#print read_value
			#read_value=read_value[1:]
			#print("Actual Temperature "+str(read_value))
			#temperature_act_array.append(int(read_value))
			temperature_act_array.append(temp_hard)
			threshold_fuzzy(temperature,read_value)
			dev=instant_deviation_check(temperature,read_count)
			add_delay_from_instant_dev(temperature,dev)
		elif(measure_type==humidity):
			#sensor_arduino.write("H")
			#read_value=sensor_arduino.readline()
			#read_value=read_value[1:]
			#print ("Actual Humidity "+str(read_value))
			#humidity_act_array.append(int(read_value))
			humidity_act_array.append(humi_hard)			
			threshold_fuzzy(humidity,read_value)
			dev=instant_deviation_check(humidity,read_count)
			add_delay_from_instant_dev(humidity,dev)
		elif(measure_type==luminosity):
			#sensor_arduino.write("L")
			#read_value=sensor_arduino.readline()					 
			#read_value=int(read_value[1:])
			#print ("Actual Luminosity "+str(read_value))
			#luminosity_act_array.append(int(read_value))
			luminosity_act_array.append(lumi_hard)
			threshold_fuzzy(luminosity,read_value)
			dev=instant_deviation_check(luminosity,read_count)
			add_delay_from_instant_dev(luminosity,dev)	 		 
		return temperature_act_array,humidity_act_array,luminosity_act_array
def add_delay_from_instant_dev(measure_type,dev):#should work
        if(dev<-10):
                dev=-10
        elif(dev>10):
                dev=10
	temp_act_delay=1
        humi_act_delay=1
        lumi_act_delay=1
        if(measure_type==temperature):
        #Only maintainance between 12 and 22,cool if positive delay(steady led) and Heizung in negative(blink led)
		temp_act_delay=dev#for every cycle
		try:
			actuator_arduino.write("T"+str(temp_act_delay))
		except:
			print "errorT"
		print ("Delay in ms:T"+str(temp_act_delay))
        elif(measure_type==humidity):
        #Pump in positive(steady led) and Heizung in negative(blink led)
                humi_act_delay=dev
		try:
                        actuator_arduino.write("H"+str(temp_act_delay))
                except:
			print "errorH"
		print ("Delay in ms:H"+str(humi_act_delay))

        elif(measure_type==luminosity):
        #Flap in positive(steady led) and Lamp in negative(blink led)
                lumi_act_delay=dev
        	try:
			actuator_arduino.write("L"+str(lumi_act_delay))
		except:
			print "errorL"
		print ("Delay in ms:L"+str(lumi_act_delay))

def mean_deviation(measure_type):
	print "to do"
#-#-#-#-#-#-STARTUP VARIABLE DECLARATION--#-#-#-#-#-#-#
try:
      actuator_arduino=serial.Serial('/dev/ttyACM1',9600)
except:
      print "Vorsicht:Actuator Arduino not connected or ready"
try:
      sensor_arduino=serial.Serial('/dev/ttyACM0',9600)
except:
      print "Vorsicht:Sensor Arduino not connected or ready"
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
mqttc.connect("m2m.eclipse.org", 1883, 60)
crange=4#changed for demo
read_count=0
#hostname="m2m.eclipse.org"
temperature="temperature"
temperature_exp_array=[]
temperature_act_array=[]
humidity="humidity"
humidity_exp_array=[]
humidity_act_array=[]
luminosity="luminosity"	
luminosity_exp_array=[]
luminosity_act_array=[]
measure_type_counter=0
measure_type_array=[temperature,humidity,luminosity]
#1.Get expected values for the day:0800 hours
#from mqtt to file.on startup-----------------------------------------------expected values
#greenhouse_startup()#0.powerup pi and arduinos
while True:
	mqtt_startup()#1.mqtt
	print "Send expected temperature values via MQTT"
	temperature_exp_array=get_exp_values(temperature)#2.
	print "Send expected humidity values via MQTT"
	humidity_exp_array=get_exp_values(humidity)#2.removed for testing
	print "Send expected luminosity values via MQTT"
	luminosity_exp_array=get_exp_values(luminosity)#2.
	#2.Run during the day in parallel#
	mqtt_startup()#1.mqtt
	#-#-#-#-start measuring-#-#-#-#
	try:
		for read_count in range(0,crange):
			for read_count_free in range(0,3):
				measure_type=measure_type_array[read_count_free]
				temperature_act_array,humidity_act_array,luminosity_act_array=actual_sequence(measure_type,read_count)#3 no clear return path and read_count also unfunctional
				print ("#-#end of one reading#-#")
				time.sleep(5)
			read_count_free=read_count_free+1 
		read_count=read_count+1 
		time.sleep(30)	
	except:
		print "System malfunction:check range and input data. Shutting Down"
