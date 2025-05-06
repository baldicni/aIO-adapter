################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (13.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
/home/mat/STM32Cube/Repository/Packs/ARM/CMSIS/6.1.0/CMSIS/Core/Source/irq_ctrl_gic.c 

C_DEPS += \
./Source/irq_ctrl_gic.d 

OBJS += \
./Source/irq_ctrl_gic.o 


# Each subdirectory must supply rules for building sources it contributes
Source/irq_ctrl_gic.o: /home/mat/STM32Cube/Repository/Packs/ARM/CMSIS/6.1.0/CMSIS/Core/Source/irq_ctrl_gic.c Source/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m7 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F767xx -c -I../Core/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F7xx/Include -I../Drivers/CMSIS/Include -I/home/mat/STM32Cube/Repository/Packs/ARM/CMSIS/6.1.0/CMSIS/Core/Include -I/home/mat/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Source

clean-Source:
	-$(RM) ./Source/irq_ctrl_gic.cyclo ./Source/irq_ctrl_gic.d ./Source/irq_ctrl_gic.o ./Source/irq_ctrl_gic.su

.PHONY: clean-Source

