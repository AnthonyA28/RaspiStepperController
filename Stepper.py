import RPi.GPIO as GPIO
import time

motor_pin_1 = 13
motor_pin_2 = 11
motor_pin_3 = 15
motor_pin_4 = 12





class Stepper:
    def __init__(self, number_of_steps, motor_pin_1, motor_pin_2, motor_pin_3, motor_pin_4, mm_per_turn=1, full_step = True):
        
        self.step_number = 0
        self.direction = 0
        self.last_step_time = 0
        self.number_of_steps = number_of_steps
        self.mm_per_turn = mm_per_turn
        self.full_step = full_step
        
        
        self.motor_pin_1 = motor_pin_1
        self.motor_pin_2 = motor_pin_2
        self.motor_pin_3 = motor_pin_3
        self.motor_pin_4 = motor_pin_4
        
        # Setup the pins for controller connection
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(motor_pin_1, GPIO.OUT)
        GPIO.setup(motor_pin_2, GPIO.OUT)
        GPIO.setup(motor_pin_3, GPIO.OUT)
        GPIO.setup(motor_pin_4, GPIO.OUT)
        
    def setRPM(self, whatSpeed):
        print("Setting RPM to ", whatSpeed)
        self.step_delay = 60 * 1000  / self.number_of_steps / whatSpeed
        
    def setMMPerSec(self, mm_per_sec):
        print("Setting velocity to ", mm_per_sec, " mm/sec")
        rots_per_min = mm_per_sec/self.mm_per_turn*60
        print("    rots_per_min: ", rots_per_min)
        self.setRPM(rots_per_min)
    
    def step_motor_full(self, thisStep):
        print("stepping ", thisStep)
        i = thisStep

        if i ==0:
          GPIO.output(motor_pin_1,GPIO.HIGH)
          GPIO.output(motor_pin_2,GPIO.LOW)
          GPIO.output(motor_pin_3,GPIO.HIGH)
          GPIO.output(motor_pin_4,GPIO.LOW)
        elif i==1:
          GPIO.output(motor_pin_1,GPIO.LOW)
          GPIO.output(motor_pin_2,GPIO.HIGH)
          GPIO.output(motor_pin_3,GPIO.HIGH)
          GPIO.output(motor_pin_4,GPIO.LOW)
        elif i==2:
          GPIO.output(motor_pin_1,GPIO.LOW)
          GPIO.output(motor_pin_2,GPIO.HIGH)
          GPIO.output(motor_pin_3,GPIO.LOW)
          GPIO.output(motor_pin_4,GPIO.HIGH)
        elif i==3:
          GPIO.output(motor_pin_1,GPIO.HIGH)
          GPIO.output(motor_pin_2,GPIO.LOW)
          GPIO.output(motor_pin_3,GPIO.LOW)
          GPIO.output(motor_pin_4,GPIO.HIGH)
        
        
    def step_motor_half(self, thisStep):
        #print("stepping ", thisStep)
        i = thisStep

        if i ==0:
          GPIO.output(motor_pin_1,GPIO.HIGH)
          GPIO.output(motor_pin_2,GPIO.LOW)
          GPIO.output(motor_pin_3,GPIO.LOW)
          GPIO.output(motor_pin_4,GPIO.LOW)
        elif i==1:
          GPIO.output(motor_pin_1,GPIO.HIGH)
          GPIO.output(motor_pin_2,GPIO.HIGH)
          GPIO.output(motor_pin_3,GPIO.LOW)
          GPIO.output(motor_pin_4,GPIO.LOW)
        elif i==2:
          GPIO.output(motor_pin_1,GPIO.LOW)
          GPIO.output(motor_pin_2,GPIO.HIGH)
          GPIO.output(motor_pin_3,GPIO.LOW)
          GPIO.output(motor_pin_4,GPIO.LOW)
        elif i==3:
          GPIO.output(motor_pin_1,GPIO.LOW)
          GPIO.output(motor_pin_2,GPIO.HIGH)
          GPIO.output(motor_pin_3,GPIO.HIGH)
          GPIO.output(motor_pin_4,GPIO.LOW)
        elif i==4:
          GPIO.output(motor_pin_1,GPIO.LOW)
          GPIO.output(motor_pin_2,GPIO.LOW)
          GPIO.output(motor_pin_3,GPIO.HIGH)
          GPIO.output(motor_pin_4,GPIO.LOW)
        elif i==5:
          GPIO.output(motor_pin_1,GPIO.LOW)
          GPIO.output(motor_pin_2,GPIO.LOW)
          GPIO.output(motor_pin_3,GPIO.HIGH)
          GPIO.output(motor_pin_4,GPIO.HIGH)
        elif i==6:
          GPIO.output(motor_pin_1,GPIO.LOW)
          GPIO.output(motor_pin_2,GPIO.LOW)
          GPIO.output(motor_pin_3,GPIO.LOW)
          GPIO.output(motor_pin_4,GPIO.HIGH)
        elif i==7:
          GPIO.output(motor_pin_1,GPIO.HIGH)
          GPIO.output(motor_pin_2,GPIO.LOW)
          GPIO.output(motor_pin_3,GPIO.LOW)
          GPIO.output(motor_pin_4,GPIO.HIGH)
                
        
    def step(self, steps_to_move):
        steps_left = abs(steps_to_move)
        
        # determine direction based on whether steps_to_move is + or -
        if steps_to_move > 0 : self.direction = 1
        if steps_to_move < 0 : self.direction = 0
        
        while (steps_left > 0):
            now = time.time()*1000
            if (now - self.last_step_time >= self.step_delay):
                self.last_step_time = now
                if (self.direction == 1):
                    self.step_number += 1
                    if( self.step_number == self.number_of_steps ):
                        self.step_number = 0
                else:
                    if (self.step_number == 0):
                        self.step_number = self.number_of_steps
                    self.step_number -= 1
                steps_left -= 1
                if self.full_step:
                    self.step_motor_full(self.step_number % 4 )
                else:
                    self.step_motor_half(self.step_number % 8 )

        
    def slide_mm(self, length):
        steps = length/self.mm_per_turn*self.number_of_steps
        print("sliding ", length, "mm (", steps , " steps) ")
        self.step(steps)
        
            

if __name__ == "__main__":
    start = time.time()
    try:
        motor_pin_1 = 13
        motor_pin_2 = 11
        motor_pin_3 = 15
        motor_pin_4 = 12
        s = Stepper(400, motor_pin_1,motor_pin_2,motor_pin_3,motor_pin_4, mm_per_turn = 5, full_step=False)
        s.setMMPerSec(5)
        s.slide_mm(-100)
        done = time.time()
        print("this took ", str(done-start))
                  
    except KeyboardInterrupt:
        GPIO.cleanup()
    GPIO.cleanup()
