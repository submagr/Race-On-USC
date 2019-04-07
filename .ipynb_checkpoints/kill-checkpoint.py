from pwm import PWM
pwm0 = PWM(0)
pwm0.export()
pwm0.period = 20000000
pwm0.duty_cycle = 1000000
pwm0.enable = True
pwm0.duty_cycle = 1000000